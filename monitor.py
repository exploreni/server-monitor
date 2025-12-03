#!/usr/bin/env python3
import json
import smtplib
import subprocess
import urllib.request
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr  # 新增这个工具

# --- 1. 读取配置 ---
try:
    with open('/root/practice/config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("❌ 错误: 找不到 config.json 配置文件")
    exit(1)

# --- 2. 获取系统信息 ---
def get_server_status():
    report = []
    report.append(f"=== 服务器每日体检报告 ===")
    report.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("-" * 30)
    
    # 获取磁盘
    try:
        df = subprocess.check_output("df -h | grep '/$'", shell=True).decode('utf-8')
        report.append("[磁盘空间]")
        parts = df.split()
        if len(parts) >= 5:
            report.append(f"根分区: 总共{parts[1]}, 已用{parts[2]}, 剩余{parts[3]}, 使用率{parts[4]}")
    except:
        report.append("[磁盘获取失败]")

    report.append("")

    # 获取内存
    try:
        free = subprocess.check_output("free -h", shell=True).decode('utf-8')
        report.append("[内存状态]")
        for line in free.split('\n'):
            if "Mem:" in line:
                parts = line.split()
                report.append(f"总内存: {parts[1]}, 已用: {parts[2]}, 空闲: {parts[3]}")
    except:
        report.append("[内存获取失败]")
        
    return "\n".join(report)

# --- 3. 发送邮件 (修复版) ---
def send_email(content):
    sender = config['email_sender']
    password = config['email_password']
    receiver = config['email_receiver']
    
    message = MIMEText(content, 'plain', 'utf-8')
    
    # 【关键修复】使用标准格式： 昵称 <邮箱地址>
    message['From'] = formataddr(("服务器管家", sender))
    message['To'] = formataddr(("主人", receiver))
    message['Subject'] = Header(f"服务器日报 {datetime.now().strftime('%F')}", 'utf-8')

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender, password)
        server.sendmail(sender, [receiver], message.as_string())
        server.quit()
        print("✅ 邮件发送成功")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

# --- 4. 心跳打卡 ---
def ping_healthchecks():
    url = config['hc_url']
    try:
        urllib.request.urlopen(url, timeout=10)
        print("✅ Healthchecks 打卡成功")
    except Exception as e:
        print(f"❌ Healthchecks 打卡失败: {e}")

# --- 主程序 ---
if __name__ == "__main__":
    report_content = get_server_status()
    send_email(report_content)
    ping_healthchecks()
