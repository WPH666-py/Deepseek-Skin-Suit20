// DeepSkin Suit20 — DeepSeek 蓝色大肥鱼皮肤套件20 (VSCode / Trae / CodeX)
const vscode = require('vscode');
const { spawn, spawnSync } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');

const REPO_URL = 'https://github.com/WPH666-py/Deepseek-Skin-Suit20.git';

function expand(p) {
  if (!p) return p;
  if (p.startsWith('~')) p = path.join(os.homedir(), p.slice(1));
  return p;
}

function detectPython() {
  const cfg = vscode.workspace.getConfiguration('deepskin20').get('pythonPath', '');
  if (cfg && fileOk(cfg)) return cfg;
  for (const cand of ['python', 'python3']) {
    const r = spawnSync(cand, ['-c', 'print(1)'], { encoding: 'utf8', timeout: 8000, windowsHide: true });
    if (r.status === 0) return cand;
  }
  return null;
}

function fileOk(p) {
  try {
    return fs.existsSync(p);
  } catch (e) {
    return false;
  }
}

function pilOk(py) {
  const r = spawnSync(py, ['-c', 'import PIL'], { encoding: 'utf8', timeout: 15000, windowsHide: true });
  return r.status === 0;
}

function ensurePil(py) {
  if (pilOk(py)) return true;
  try {
    spawnSync(py, ['-m', 'pip', 'install', '--user', 'pillow'], {
      encoding: 'utf8',
      timeout: 180000,
      windowsHide: true
    });
  } catch (e) { /* ignore */ }
  return pilOk(py);
}

function findRepo() {
  const cfg = expand(vscode.workspace.getConfiguration('deepskin20').get('repoPath', ''));
  const cands = [
    cfg,
    path.join(os.homedir(), '.deepskin-suit20'),
    process.env.USERPROFILE ? path.join(process.env.USERPROFILE, 'DeepSkin-Suit20') : null,
    path.join(os.homedir(), 'DeepSkin-Suit20')
  ].filter(Boolean);
  for (const c of cands) {
    try {
      if (fs.existsSync(path.join(c, 'tools', 'wallpaper.py'))) return c;
    } catch (e) { /* ignore */ }
  }
  return null;
}

function envError(msg) {
  vscode.window.showWarningMessage(
    msg + ' 请先在终端执行: git clone ' + REPO_URL + ' ' +
    path.join(process.env.USERPROFILE || os.homedir(), 'DeepSkin-Suit20') + ' 并安装 Python3 + Pillow。'
  );
}

function runWallpaper(args) {
  const py = detectPython();
  const repo = findRepo();
  if (!repo) return envError('未找到皮肤套件20仓库。');
  if (!py) return envError('未找到 Python。');
  if (!ensurePil(py)) return envError('Pillow 安装失败。');
  const script = path.join(repo, 'tools', 'wallpaper.py');
  const child = spawn(py, [script].concat(args), { cwd: repo, windowsHide: true });
  let out = '';
  child.stdout.on('data', (d) => (out += d.toString()));
  child.stderr.on('data', (d) => (out += d.toString()));
  child.on('close', (code) => {
    if (code === 0) {
      vscode.window.setStatusBarMessage('🐳 大肥鱼20壁纸已应用!', 5000);
    } else {
      envError('换壁纸失败(' + code + '): ' + out.slice(-300));
    }
  });
}

function spawnGui(script) {
  const py = detectPython();
  const repo = findRepo();
  if (!repo) return envError('未找到皮肤套件20仓库。');
  if (!py) return envError('未找到 Python。');
  let exe = py;
  if (process.platform === 'win32') {
    const w = path.join(path.dirname(py), 'pythonw.exe');
    if (fileOk(w)) exe = w;
  }
  const child = spawn(exe, [path.join(repo, 'tools', script)], {
    cwd: repo,
    detached: true,
    stdio: 'ignore',
    windowsHide: true
  });
  child.unref();
}

class GalleryProvider {
  constructor() {
    this._view = null;
  }
  resolveWebviewView(view) {
    this._view = view;
    const ext = vscode.extensions.getExtension('wp666.deepskin-suit20');
    const media = path.join(ext.extensionPath, 'media');
    const thumb = (f) => view.webview.asWebviewUri(vscode.Uri.file(path.join(media, f)));
    const repo = findRepo();
    view.webview.html = html(thumb, repo);
    view.webview.onDidReceiveMessage((msg) => {
      if (msg && msg.cmd === 'apply') runWallpaper([msg.mode, '--set']);
    });
  }
}

function html(thumb, repo) {
  const cards = [
    { mode: 'grid', t: '全屏铺满(cover)', img: 'thumb-grid.png' },
    { mode: 'single1', t: '卡片单图', img: 'thumb-1.png' }
  ];
  const card = (c) =>
    '<div class="card"><img src="' + thumb(c.img) + '"/><div class="t">' + c.t + '</div>' +
    '<button data-mode="' + c.mode + '">设为壁纸</button></div>';
  const ready = repo ? '' : '未检测到皮肤套件20仓库, 请先克隆 ' + REPO_URL;
  return (
    '<!doctype html><html><head><style>' +
    'body{background:#0f141b;color:#e8eef7;font-family:system-ui;padding:10px}' +
    '.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}' +
    '.card{background:#182130;border-radius:12px;padding:10px;text-align:center}' +
    '.card img{width:100%;border-radius:8px;display:block}' +
    '.card .t{margin:6px 0 2px;font-weight:600}' +
    'button{margin-top:6px;width:100%;border:none;border-radius:8px;padding:7px 0;background:#2f6fe4;color:#fff;cursor:pointer}' +
    'button:hover{background:#4b85f0}.warn{color:#f4c15a;font-size:12px;padding:6px 0}' +
    '.cmds{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}' +
    '</style></head><body>' +
    (ready ? '<div class="warn">⚠ ' + ready + '</div>' : '') +
    '<div class="grid">' + cards.map(card).join('') + '</div>' +
    '<div class="cmds"><button data-mode="random">🎲 随机换一张</button></div>' +
    '<script>const vscode=acquireVsCodeApi();' +
    'document.querySelectorAll("button").forEach(b=>b.addEventListener("click",()=>' +
    'vscode.postMessage({cmd:"apply",mode:b.dataset.mode})));</script>' +
    '</body></html>'
  );
}

function activate(ctx) {
  const register = (cmd, fn) => ctx.subscriptions.push(vscode.commands.registerCommand(cmd, fn));
  register('deepskin20.setGrid', () => runWallpaper(['grid']));
  register('deepskin20.setSingle1', () => runWallpaper(['single1']));
  register('deepskin20.setRandom', () => runWallpaper(['random']));
  register('deepskin20.openSwitcher', () => spawnGui('switcher.py'));
  register('deepskin20.startPet', () => spawnGui('pet.py'));
  register('deepskin20.openGallery', () =>
    vscode.commands.executeCommand('workbench.view.extension.deepskin20')
  );
  ctx.subscriptions.push(
    vscode.window.registerWebviewViewProvider('deepskin20.gallery', new GalleryProvider(), {
      webviewOptions: { retainContextWhenHidden: true }
    })
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
