# .config

个人配置文件仓库，包含 shell、编辑器、终端等各种工具的配置。

```bash
git clone https://github.com/suprecreator/.config.git ~/.config
```

---

## 常用命令速查

选择你的系统查看对应命令：

<table>
<tr>
<td width="33%" align="center">

**🍎 macOS**

</td>
<td width="33%" align="center">

**🐧 Linux**

</td>
<td width="33%" align="center">

**🪟 Windows**

</td>
</tr>
<tr>
<td>

<details open>
<summary>展开 macOS 命令</summary>

#### 系统设置
```bash
# 显示隐藏文件
defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder

# 隐藏桌面图标
defaults write com.apple.finder CreateDesktop -bool false && killall Finder

# 截图保存到剪贴板
defaults write com.apple.screencapture target -string "clipboard"

# 查看系统完整性保护状态
csrutil status
```

#### Homebrew
```bash
# 安装
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 更新
brew update && brew upgrade

# 常用工具
brew install git vim tmux fzf ripgrep fd eza bat zoxide starship

# GUI 应用
brew install --cask alacritty raycast
```

#### Shell
```bash
# 切换默认 shell
chsh -s /bin/zsh

# 重新加载配置
source ~/.zshrc
source ~/.zprofile
```

#### 定时任务 (launchd)
```bash
# 加载/重载任务
launchctl load ~/Library/LaunchAgents/com.user.zsh-backup.plist

# 卸载任务
launchctl unload ~/Library/LaunchAgents/com.user.zsh-backup.plist

# 查看运行状态
launchctl list | grep com.user
```

#### 路径速查
| 项目 | 路径 |
|------|------|
| ZSH 配置 | `~/.zshrc`, `~/.zprofile` |
| SSH 密钥 | `~/.ssh/` |
| 启动项 | `~/Library/LaunchAgents/` |
| 备份目录 | `~/.config/backups/zsh/` |

</details>

</td>
<td>

<details>
<summary>展开 Linux 命令</summary>

*待补充...* 欢迎 PR！

</details>

</td>
<td>

<details>
<summary>展开 Windows 命令</summary>

*待补充...* 欢迎 PR！

</details>

</td>
</tr>
</table>

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
~/.config/backups/zsh/backup.sh
```

**查看最新备份：**
```bash
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
