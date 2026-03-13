# .config

个人配置文件仓库，包含 shell、编辑器、终端等各种工具的配置。

## 快速开始

```bash
git clone https://github.com/suprecreator/.config.git ~/.config
```

---

## 常用命令参考

<details open>
<summary><b>🍎 macOS</b></summary>

### 系统
```bash
# 显示隐藏文件
defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder

# 隐藏桌面图标
defaults write com.apple.finder CreateDesktop -bool false && killall Finder

# 截图保存到剪贴板
defaults write com.apple.screencapture target -string "clipboard"

# 禁用系统完整性保护检查（谨慎使用）
csrutil status
```

### Homebrew
```bash
# 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 更新
brew update && brew upgrade

# 安装常用工具
brew install git vim tmux fzf ripgrep fd eza bat zoxide starship

# 安装 GUI 应用
brew install --cask alacritty raycast
```

### Shell
```bash
# 切换到 zsh
chsh -s /bin/zsh

# 加载配置
source ~/.zshrc
source ~/.zprofile
```

### 定时任务 (launchd)
```bash
# 加载任务
launchctl load ~/Library/LaunchAgents/com.user.zsh-backup.plist

# 卸载任务
launchctl unload ~/Library/LaunchAgents/com.user.zsh-backup.plist

# 查看任务状态
launchctl list | grep com.user
```

### SSH
```bash
# 生成密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 添加密钥到 ssh-agent
ssh-add ~/.ssh/id_ed25519
```

</details>

<details>
<summary><b>🐧 Linux</b></summary>

*待补充...*

</details>

<details>
<summary><b>🪟 Windows</b></summary>

*待补充...*

</details>

---

## 配置结构

```
~/.config/
├── alacritty/      # 终端配置
├── nvim/           # Neovim 配置
├── fish/           # Fish shell 配置
├── tmux/           # Tmux 配置
├── forge/          # AI agents 配置
├── backups/zsh/    # ZSH 自动备份
└── agents/         # Agent skills
    └── skills/
        └── pua/    # PUA 万能激励引擎
```

---

## Features

### 🤖 PUA Skill

位于 `agents/skills/pua/`，一个强制系统化解题方法论的技能模块。

**核心原则：**
- **铁律一**：穷尽一切方案之前，禁止说"我无法解决"
- **铁律二**：先用工具自查，再问用户
- **铁律三**：端到端交付，主动闭环

### 💾 自动备份

ZSH 配置文件 (`~/.zshrc`, `~/.zprofile`) 每天自动备份到 `backups/zsh/`：
- 保留最近 30 个版本
- 每天上午 10:00 自动执行
- 登录时也会执行一次

```bash
# 手动备份
~/.config/backups/zsh/backup.sh
```

---

## License

MIT
