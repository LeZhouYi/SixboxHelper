FROM python:3.12-slim

WORKDIR /app

# 复制安装依赖
COPY poetry.lock ./
COPY pyproject.toml ./

# 安装Poetry并配置
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

# 安装项目依赖
RUN poetry install --no-root

# 复制运行文件
COPY .env ./
COPY core ./core/
COPY main.py ./

CMD ["python","main.py"]