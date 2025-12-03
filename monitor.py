#!/usr/bin/env python3
import json
import smtplib
import subprocess
import urllib.request
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# --- 1. 读取配置 ---
try:
    with open('/root/practice/config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("❌ 错误: 找不到 config.json 配置文件")
    exit(1)

# --- 2. 获取系统信息 (升级版) ---
def get_server_status():
    report = []
    is_danger = False  # 默认安全标志位
    
    report.append(f"=== 服务器每日体检报告 ===")
    report.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("-" * 30)

    # [新增] 获取 CPU 负载 (你刚才验证过的逻辑)
    try:
        report.append("[CPU 负载]")
        raw = subprocess.check_output("uptime", shell=True).decode('utf-8')
        # 清理逗号并切割
        parts = raw.replace(',', ' ').split()
        load_1min = float(parts[-3]) # 获取倒数第3个数字
        
        report.append(f"1分钟平均负载: {load_1min}")
        
        # 判断是否报警
        if load_1min > 2.0:
            report.append("⚠️ 警告: CPU 负载过高！")
            is_danger = True  # 举起红旗！
        else:
            report.append("✅ 状态正常")
            
    except Exception as e:
        report.append(f"[CPU 获取失败: {e}]")
    
    report.append("")
    
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
                available_mem = parts[6] if len(parts) > 6 else parts[-1]
                report.append(f"总内存: {parts[1]}, 已用: {parts[2]}")
                report.append(f"真实可用: {available_mem} (含缓存)")
    except:
        report.append("[内存获取失败]")
        
    # 返回两个值：报告内容，以及 是否危险
    return "\n".join(report), is_danger

# --- 3. 发送邮件 (接收报警信号) ---
def send_email(content, is_danger=False):
    sender = config['email_sender']
    password = config['email_password']
    receiver = config['email_receiver']
    
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = formataddr(("服务器管家", sender))
    message['To'] = formataddr(("主人", receiver))
    
    # [新增] 动态修改标题
    prefix = "【警告】" if is_danger else ""
    subject = f"{prefix}服务器日报 {datetime.now().strftime('%F')}"
    
    message['Subject'] = Header(subject, 'utf-8')

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender, password)
        server.sendmail(sender, [receiver], message.as_string())
        server.quit()
        print(f"✅ 邮件发送成功 (报警状态: {is_danger})")
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

# --- 主程序入口 ---
if __name__ == "__main__":
    # 1. 获取状态 (拿到两个返回值)
    report_content, danger_signal = get_server_status()
    
    # 2. 发送邮件 (把报警信号传进去)
    send_email(report_content, danger_signal)
    
    # 3. 打卡
    ping_healthchecks()
