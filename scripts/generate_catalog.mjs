import { createHash } from 'node:crypto';
import { readdirSync, readFileSync, statSync, writeFileSync, existsSync } from 'node:fs';
import { join, relative, dirname } from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT_DIR = dirname(__dirname);
const PLUGINS_DIR = join(ROOT_DIR, 'plugins');

function hashLength(hash, length) {
  const framedLength = Buffer.allocUnsafe(8);
  framedLength.writeBigUInt64BE(BigInt(length));
  hash.update(framedLength);
}

function hashPluginTree(root) {
  const files = [];
  function collect(dir) {
    const entries = readdirSync(dir, { withFileTypes: true });
    entries.sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0));
    for (const entry of entries) {
      if (entry.name === '.git' || entry.name === 'node_modules' || entry.name === '.orca') continue;
      const full = join(dir, entry.name);
      if (entry.isDirectory()) {
        collect(full);
      } else if (entry.isFile()) {
        const stat = statSync(full);
        files.push({ full, rel: relative(root, full).replace(/\\/g, '/'), size: stat.size });
      }
    }
  }
  collect(root);
  const hash = createHash('sha256');
  hash.update('orca-plugin-tree-v1\0');
  let totalBytes = 0;
  for (const file of files) {
    totalBytes += file.size;
    hashLength(hash, Buffer.byteLength(file.rel, 'utf8'));
    hash.update(file.rel, 'utf8');
    hashLength(hash, file.size);
    hash.update(readFileSync(file.full));
  }
  return { hash: hash.digest('hex'), files: files.length, totalBytes };
}

function getGitHeadCommit() {
  try {
    return execSync('git rev-parse HEAD', { cwd: ROOT_DIR, encoding: 'utf8' }).trim();
  } catch (error) {
    return '0'.repeat(40);
  }
}

function deriveCatalogTypes(manifest) {
  const types = new Set();
  const c = manifest.contributes || {};
  if (c.languagePacks?.length) types.add('interface-language');
  if (c.themes?.length) types.add('app-theme');
  if (c.terminalThemes?.length) types.add('terminal-theme');
  if (c.iconThemes?.length) types.add('icon-theme');
  if (c.syntaxes?.length) types.add('syntax');
  if (c.vmRecipes?.length) types.add('instructions');
  if (c.panels?.length) types.add('panel');
  if (c.customEditors?.length) types.add('editor');
  if (manifest.main) types.add('worker');
  return Array.from(types);
}

function deriveContributionSummary(manifest) {
  const items = [];
  const c = manifest.contributes || {};
  if (c.languagePacks) {
    for (const p of c.languagePacks) items.push({ kind: 'languagePacks', name: p.locale });
  }
  if (c.themes) {
    for (const t of c.themes) items.push({ kind: 'themes', name: t.title || t.id });
  }
  if (c.terminalThemes) {
    for (const t of c.terminalThemes) items.push({ kind: 'terminalThemes', name: t.title || t.id });
  }
  if (c.iconThemes) {
    for (const t of c.iconThemes) items.push({ kind: 'iconThemes', name: t.title || t.id });
  }
  if (c.syntaxes) {
    for (const s of c.syntaxes) items.push({ kind: 'syntaxes', name: s.title || s.id });
  }
  if (c.panels) {
    for (const p of c.panels) items.push({ kind: 'panels', name: p.title || p.id });
  }
  if (c.commands) {
    for (const cmd of c.commands) items.push({ kind: 'commands', name: cmd.title || cmd.id });
  }
  if (c.keybindings) {
    for (const k of c.keybindings) items.push({ kind: 'keybindings', name: k.key });
  }
  return items;
}

export function generateCatalog() {
  const commit = getGitHeadCommit();
  if (!existsSync(PLUGINS_DIR)) {
    console.error('Plugins directory not found:', PLUGINS_DIR);
    return;
  }

  const existingCatalogPath = join(ROOT_DIR, 'orca-catalog.json');
  let existingCatalog = null;
  if (existsSync(existingCatalogPath)) {
    try {
      existingCatalog = JSON.parse(readFileSync(existingCatalogPath, 'utf8'));
    } catch {}
  }

  const pluginEntries = [];
  const entries = readdirSync(PLUGINS_DIR, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const pluginFolder = join(PLUGINS_DIR, entry.name);
    const manifestPath = join(pluginFolder, 'orca-plugin.json');
    if (!existsSync(manifestPath)) continue;

    const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
    const treeHash = hashPluginTree(pluginFolder);
    const types = deriveCatalogTypes(manifest);
    const summary = deriveContributionSummary(manifest);
    const relPath = `plugins/${entry.name}`;

    // Look up previous release commit if contentHash didn't change
    let releaseCommit = commit;
    if (existingCatalog?.plugins) {
      const prev = existingCatalog.plugins.find((p) => p.id === `fuevaco.${manifest.id}`);
      if (prev?.releases?.[0] && prev.releases[0].contentHash === treeHash.hash) {
        releaseCommit = prev.releases[0].commit;
      }
    }

    pluginEntries.push({
      id: `fuevaco.${manifest.id}`,
      source: {
        kind: 'git',
        url: 'https://github.com/fuevaco/orca-tw.git',
        ref: 'main',
        path: relPath
      },
      description: manifest.description || '',
      categories: types.includes('interface-language') ? ['languages'] : ['tools'],
      releases: [
        {
          version: manifest.version,
          commit: releaseCommit,
          contentHash: treeHash.hash,
          execution: manifest.execution || 'data',
          minimumOrca: manifest.engines?.orca?.replace(/^>=/, '') || '1.4.0',
          types: types.length > 0 ? types : ['interface-language'],
          ...(summary.length > 0 ? { contributes: summary } : {})
        }
      ]
    });

    console.log(`✓ Processed ${entry.name}: ${manifest.id} (v${manifest.version}, hash: ${treeHash.hash.slice(0, 12)}...)`);
  }

  const catalog = {
    catalogVersion: 2,
    name: 'fuevaco Orca Plugins Catalog',
    owner: 'fuevaco',
    plugins: pluginEntries
  };

  writeFileSync(existingCatalogPath, JSON.stringify(catalog, null, 2) + '\n', 'utf8');
  console.log(`\nSuccessfully updated ${existingCatalogPath} with ${pluginEntries.length} plugin(s).`);
}

generateCatalog();
