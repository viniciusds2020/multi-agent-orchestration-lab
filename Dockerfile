FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir ".[all]"
RUN mkdir -p /app/data
EXPOSE 8000
CMD ["multi-agent-lab"]

