FROM node:18-alpine AS frontend-builder

WORKDIR /app

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm@9 && pnpm install --frozen-lockfile

COPY frontend/ ./
RUN [ -f ".env" ] || cp .env.example .env
RUN pnpm run build

FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY backend/ ./
RUN uv sync --frozen --no-dev

COPY --from=frontend-builder /app/dist ./static

EXPOSE 45600

CMD ["uv", "run", "python", "-m", "home.main"]
