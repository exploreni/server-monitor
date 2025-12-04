# 换一个基础镜像，确保有编译环境
FROM python:3.9

WORKDIR /app

# 安装 flask 和 psutil
RUN pip install flask psutil --no-cache-dir

COPY web_monitor.py .

EXPOSE 5000

CMD ["python", "web_monitor.py"]
