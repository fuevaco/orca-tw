import { createHash } from 'node:crypto';
import { readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT_DIR = dirname(__dirname);

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

export function generateCatalog() {
  const commit = getGitHeadCommit();
  const pluginDir = join(ROOT_DIR, 'plugins', 'zh-tw');
  const manifest = JSON.parse(readFileSync(join(pluginDir, 'orca-plugin.json'), 'utf8'));
  const treeHash = hashPluginTree(pluginDir);

  const catalog = {
    catalogVersion: 2,
    name: 'Orca 繁體中文外掛目錄 (fuevaco)',
    owner: 'fuevaco',
    plugins: [
      {
        id: `fuevaco.${manifest.id}`,
        source: {
          kind: 'git',
          url: 'https://github.com/fuevaco/orca-tw.git',
          ref: 'main',
          path: 'plugins/zh-tw'
        },
        description: manifest.description,
        categories: ['languages'],
        releases: [
          {
            version: manifest.version,
            commit: commit,
            contentHash: treeHash.hash,
            execution: manifest.execution || 'data',
            minimumOrca: manifest.engines.orca.replace(/^>=/, ''),
            types: ['interface-language'],
            contributes: [
              {
                kind: 'languagePacks',
                name: 'zh-TW'
              }
            ]
          }
        ]
      }
    ]
  };

  const catalogPath = join(ROOT_DIR, 'orca-catalog.json');
  writeFileSync(catalogPath, JSON.stringify(catalog, null, 2) + '\n', 'utf8');
  console.log(`Updated ${catalogPath} (commit: ${commit}, contentHash: ${treeHash.hash})`);
}

generateCatalog();
