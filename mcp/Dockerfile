FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV CONTAINER_HOME=/app

WORKDIR $CONTAINER_HOME

COPY pyproject.toml  ./

RUN uv sync

COPY server.py . 

EXPOSE 8888

CMD ["uv", "run", "server.py"]
