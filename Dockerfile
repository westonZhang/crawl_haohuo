FROM python:3.6.8
WORKDIR /app
COPY . /app/crawl_haohuo
ENV TimeZone=Asia/Shanghai
RUN pip install --no-cache-dir -r /app/crawl_haohuo/requirements.txt
WORKDIR /app/crawl_haohuo
CMD ["python", "main.py"]
