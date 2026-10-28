FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV PYTHONUNBUFFERED=1 PORT=8765 STATE_DIRECTORY=/data
EXPOSE 8765
CMD ["python", "server.py", "--no-browser", "--host", "0.0.0.0"]
