# 📊 Server Monitor (Python + Docker)

一个轻量级、可视化的 Linux 服务器监控面板。支持 **Web 仪表盘** 查看实时状态，支持 **SMTP 邮件报警** 和 **Healthchecks** 心跳检测。

## ✨ 功能特点

- **🔥 实时 Web 面板**：基于 Flask 开发，黑客风 UI，秒级刷新。
- **🐳 Docker 部署**：提供 Dockerfile 和 Compose，一行命令即可启动。
- **🚀 轻量高效**：基于 psutil 采集，资源占用极低 (<50MB)。
- **📧 智能报警**：CPU 负载 > 2.0 自动发送邮件。
- **🛡️ 安全设计**：配置与代码分离，敏感信息不泄露。

## 🛠️ 快速开始 (Docker Compose - 推荐)

### 1. 下载代码
```bash
git clone https://github.com/exploreni/server-monitor.git
cd server-monitor
```

### 2. 准备配置
在当前目录创建 `config.json`：
```json
{
    "email_sender": "...",
    "email_password": "...",
    "hc_url": "..."
}
```

### 3. 一键启动
```bash
docker compose up -d
```
访问 `http://你的IP:5000` 即可。

## 📦 其他方式
- **Docker Run**: `docker build -t monitor . && docker run -d -p 5000:5000 monitor`
- **Python**: `pip install flask psutil && python3 web_monitor.py`

## 📄 License
MIT License
