#!/bin/bash

# ZSH 配置文件备份脚本
# 备份 ~/.zshrc 和 ~/.zprofile 到 ~/.config/backups/zsh/

BACKUP_DIR="$HOME/.config/backups/zsh"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
MAX_BACKUPS=30

# 确保备份目录存在
mkdir -p "$BACKUP_DIR"

# 备份函数
backup_file() {
    local src="$1"
    local filename=$(basename "$src")
    local backup_name="${filename}.${TIMESTAMP}"
    local latest_link="${BACKUP_DIR}/${filename}.latest"
    
    if [[ -f "$src" ]]; then
        cp "$src" "$BACKUP_DIR/$backup_name"
        echo "✓ 已备份: $src -> $backup_name"
        
        # 更新 latest 软链接
        rm -f "$latest_link"
        ln -s "$backup_name" "$latest_link"
    else
        echo "✗ 文件不存在: $src"
    fi
}

# 执行备份
backup_file "$HOME/.zshrc"
backup_file "$HOME/.zprofile"

# 清理旧备份（保留最新的 MAX_BACKUPS 个）
cleanup_old_backups() {
    local filename="$1"
    local count=$(ls -1t "$BACKUP_DIR/${filename}".*[0-9] 2>/dev/null | wc -l)
    
    if [[ $count -gt $MAX_BACKUPS ]]; then
        ls -1t "$BACKUP_DIR/${filename}".*[0-9] | tail -n +$((MAX_BACKUPS + 1)) | while read oldfile; do
            rm "$BACKUP_DIR/$oldfile"
            echo "  已清理旧备份: $(basename "$oldfile")"
        done
    fi
}

cleanup_old_backups ".zshrc"
cleanup_old_backups ".zprofile"

echo "备份完成: $(date)"
