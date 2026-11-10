import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT_DIR = dirname(__dirname);

const [,, id, name, type = 'data'] = process.argv;

if (!id) {
  console.log(`
使用方式:
  node scripts/create_plugin.mjs <套件ID> [套件名稱] [類型]

範例:
  node scripts/create_plugin.mjs dark-plus "Dark Plus 主題" theme
  node scripts/create_plugin.mjs custom-shortcuts "自訂快捷指令" declarative
`);
  process.exit(0);
}

const pluginDir = join(ROOT_DIR, 'plugins', id);
if (existsSync(pluginDir)) {
  console.error(`錯誤: 目錄 plugins/${id} 已存在！`);
  process.exit(1);
}

mkdirSync(pluginDir, { recursive: true });

const execution = type === 'theme' ? 'data' : type === 'declarative' ? 'declarative' : 'data';

const manifest = {
  manifestVersion: 2,
  execution: execution,
  id: id,
  publisher: "fuevaco",
  name: name || id,
  version: "1.0.0",
  description: `${name || id} by fuevaco for Orca.`,
  author: {
    name: "fuevaco",
    url: "https://github.com/fuevaco"
  },
  repository: "https://github.com/fuevaco/orca-tw",
  engines: {
    orca: ">=1.4.0"
  },
  contributes: {},
  capabilities: []
};

if (type === 'theme') {
  manifest.contributes.themes = [
    {
      id: id,
      title: name || id,
      path: `themes/${id}.json`
    }
  ];
  mkdirSync(join(pluginDir, 'themes'), { recursive: true });
  writeFileSync(join(pluginDir, 'themes', `${id}.json`), JSON.stringify({ name: name || id, colors: {} }, null, 2) + '\n');
}

writeFileSync(join(pluginDir, 'orca-plugin.json'), JSON.stringify(manifest, null, 2) + '\n', 'utf8');

const readmeContent = `# ${name || id}

由 **fuevaco** 維護的 Orca 外掛套件。

- **外掛 ID**：\`fuevaco.${id}\`
- **版本**：\`1.0.0\`
`;
writeFileSync(join(pluginDir, 'README.md'), readmeContent, 'utf8');

console.log(`✓ 成功建立新套件: plugins/${id}`);
console.log(`✓ 請編輯 plugins/${id}/orca-plugin.json`);
console.log(`✓ 編輯完成後執行 node scripts/generate_catalog.mjs 即可同步至 orca-catalog.json！`);
