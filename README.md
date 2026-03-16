# .config

个人配置文件仓库，包含 shell、编辑器、终端等各种工具的配置。

```bash
git clone https://github.com/suprecreator/.config.git ~/.config
```

---

## 常用命令速查

### 系统设置

| 🍎 macOS | 🐧 Linux | 🪟 Windows |
|:---------|:---------|:-----------|
| `defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder` | *待补充* | *待补充* |
| `defaults write com.apple.finder CreateDesktop -bool false && killall Finder` | | |
| `defaults write com.apple.screencapture target -string "clipboard"` | | |

### Homebrew / 包管理器

| 🍎 macOS | 🐧 Linux | 🪟 Windows |
|:---------|:---------|:-----------|
| **安装 Homebrew**<br>`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` | *apt/dnf/pacman* | *choco/scoop/winget* |
| **更新**<br>`brew update && brew upgrade` | `sudo apt update && sudo apt upgrade` | `choco upgrade all` |
| **常用工具**<br>`brew install git vim tmux fzf ripgrep fd eza bat zoxide starship` | `sudo apt install git vim tmux fzf ripgrep fd-find bat zoxide` | `choco install git vim tmux fzf ripgrep fd bat zoxide` |
| **GUI 应用**<br>`brew install --cask alacritty raycast` | *各发行版不同* | `choco install alacritty` |

### Shell 配置

| 🍎 macOS | 🐧 Linux | 🪟 Windows |
|:---------|:---------|:-----------|
| **切换默认 shell**<br>`chsh -s /bin/zsh` | `chsh -s /usr/bin/zsh` | *使用 Windows Terminal* |
| **重新加载配置**<br>`source ~/.zshrc` | `source ~/.zshrc` | `source $PROFILE` |
| **ZSH 配置路径**<br>`~/.zshrc`, `~/.zprofile` | `~/.zshrc` | *PowerShell 配置文件* |

### 定时任务

| 🍎 macOS (launchd) | 🐧 Linux (systemd) | 🪟 Windows |
|:-------------------|:-------------------|:-----------|
| **加载任务**<br>`launchctl load ~/Library/LaunchAgents/com.user.zsh-backup.plist` | `systemctl --user enable zsh-backup.timer` | *任务计划程序* |
| **卸载任务**<br>`launchctl unload ~/Library/LaunchAgents/com.user.zsh-backup.plist` | `systemctl --user disable zsh-backup.timer` | |
| **查看状态**<br>`launchctl list \| grep com.user` | `systemctl --user list-timers` | `Get-ScheduledTask` |

### SSH 密钥

| 🍎 macOS | 🐧 Linux | 🪟 Windows |
|:---------|:---------|:-----------|
| **生成密钥**<br>`ssh-keygen -t ed25519 -C "email@example.com"` | 同 macOS | 同 macOS |
| **添加密钥**<br>`ssh-add ~/.ssh/id_ed25519` | `ssh-add ~/.ssh/id_ed25519` | `ssh-add $env:USERPROFILE\.ssh\id_ed25519` |
| **SSH 目录**<br>`~/.ssh/` | `~/.ssh/` | `%USERPROFILE%\.ssh\` |

---

## 配置结构

```
~/.config/
├── alacritty/      # 终端配置
├── nvim/           # Neovim 配置
├── fish/           # Fish shell 配置
├── tmux/           # Tmux 配置
├── forge/          # AI agents 配置
├── backups/        # 自动备份
│   └── zsh/        # ZSH 配置备份 ⭐
└── agents/         # Agent skills
    └── skills/
        └── pua/    # PUA 万能激励引擎
```

---

## Features

### 💾 ZSH 自动备份

你的 `~/.zshrc` 和 `~/.zprofile` 会被自动备份到：

```
~/.config/backups/zsh/
├── .zshrc.latest              → 最新版本（软链接）
├── .zshrc.20260313_190402     # 带时间戳的历史版本
├── .zprofile.latest           → 最新版本（软链接）
└── .zprofile.20260313_190402  # 带时间戳的历史版本
```

**备份策略：**
- ⏰ 每天上午 10:00 自动执行
- 🔓 登录时也会备份一次
- 📦 保留最近 30 个版本，自动清理旧的

**手动备份：**
```bash
# macOS / Linux
~/.config/backups/zsh/backup.sh
```

**查看最新备份：**
```bash
# macOS / Linux
cat ~/.config/backups/zsh/.zshrc.latest
```

---

### 🤖 PUA Skill

位于 `agents/skills/pua/` - 一个强制系统化解题方法论的技能模块。

**三条铁律：**
1. **穷尽一切** - 禁止说"我无法解决"
2. **先做后问** - 先用工具自查
3. **主动闭环** - 端到端交付

---

## License

MIT
