#!/bin/bash

# 定义日志文件路径
LOG_FILE="./log/log.txt"

# 检查 crontab 是否已存在该任务
# 每天6:59分执行 run.sh 脚本，并将输出重定向到日志文件
CRON_JOB="59 6 * * * run.sh >> $LOG_FILE 2>&1"
(crontab -l 2>/dev/null | grep -F "$CRON_JOB") || {
  # 如果 crontab 中不存在该任务，则将其添加到 crontab 中
  (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
}

# 进入脚本所在目录
cd "$(dirname "$0")"

# 加载 conda 命令
# source ~/opt/anaconda3/etc/profile.d/conda.sh

# 激活 conda 虚拟环境
conda init
conda activate courtbooking

# 执行 Python 脚本，并将输出重定向到日志文件
python main.py >> $LOG_FILE 2>&1