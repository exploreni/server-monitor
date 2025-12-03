#!/bin/bash

# --- 配置区域 ---
EMAIL="1665791070@qq.com"
REPORT_FILE="/root/practice/report.txt"
HC_URL="https://hc-ping.com/8ac036bc-690e-41b8-86bf-8d0f7593b0bb"

# 1. 生成体检报告
echo "=== 服务器每日体检报告 ===" > $REPORT_FILE
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')" >> $REPORT_FILE
echo "--------------------------" >> $REPORT_FILE

# 磁盘使用情况 (过滤出根目录)
echo "[磁盘空间]" >> $REPORT_FILE
df -h | grep '/$' | awk '{print "根分区: 总共"$2", 已用"$3", 剩余"$4", 使用率"$5}' >> $REPORT_FILE
echo "" >> $REPORT_FILE

# 内存使用情况
echo "[内存状态]" >> $REPORT_FILE
free -h | awk '/Mem:/ {print "总内存: "$2", 已用: "$3", 空闲: "$4}' >> $REPORT_FILE
echo "" >> $REPORT_FILE

# 2. 发送邮件 (带容错处理)
# 就算邮件发不出去，脚本也会继续往下跑，不会卡死
if echo "请查收今日服务器状态" | s-nail -s "服务器日报 $(date +%F)" -a $REPORT_FILE $EMAIL; then
    echo "✅ 邮件发送成功"
else
    echo "❌ 邮件发送失败，但继续执行心跳检测"
fi

# 3. 告诉 Healthchecks 我还活着 (Ping)
curl -fsS -m 10 --retry 5 $HC_URL > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Healthchecks 打卡成功"
else
    echo "❌ Healthchecks 打卡失败"
fi

# 4. 清理临时文件 (保留空文件以免报错)
> $REPORT_FILE
