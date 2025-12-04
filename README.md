# 📊 Server Monitor (Python + Docker)

一个轻量级、可视化的 Linux 服务器监控面板。支持 **Web 仪表盘** 查看实时状态，支持 **SMTP 邮件报警** 和 **Healthchecks** 心跳检测。

## ✨ 功能特点

- **🔥 实时 Web 面板**：基于 Flask 开发，黑客风 UI，秒级刷新。
- **🐳 Docker 部署**：提供 Dockerfile，一行命令即可启动，环境零依赖。
- **🚀 轻量高效**：基于 psutil 采集，资源占用极低 (<50MB)。
- **📧 智能报警**：CPU 负载 > 2.0 自动发送邮件，磁盘/内存可视化展示。
- **🛡️ 安全设计**：配置与代码分离，支持通过环境变量或挂载文件配置敏感信息。

## 🛠️ 快速开始 (Docker 方式 - 推荐)

### 1. 下载代码
```bash
git clone https://github.com/exploreni/server-monitor.git
cd server-monitor
```

### 2. 准备配置文件
请在当前目录创建一个 `config.json` 文件（参考代码中的格式）：
```json
{
    "email_sender": "...",
    "email_password": "...",
    "hc_url": "..."
}
```

### 3. 构建并启动
```bash
# 构建镜像
docker build -t my-monitor .

# 启动容器 (映射5000端口)
docker run -d -p 5000:5000 --name server-monitor --restart always my-monitor
```

访问浏览器 `http://你的IP:5000` 即可看到监控面板。

## 📦 传统方式运行 (Python)
如果你不想用 Docker，也可以直接运行：
```bash
pip install flask psutil
python3 web_monitor.py
```

## 📄 License
MIT License
