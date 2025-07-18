# Imagen base fijada por digest para seguridad y consistencia
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:5c8edeb8b5644b618882e06ddaa8ddf509dcd1aa7d08fedac7155106116a9a9e

# Capturar el commit SHA para fines de depuración y versionado
ARG GITHUB_SHA=unknown
ENV GITHUB_SHA=$GITHUB_SHA

# Configuración de entorno para Python y UV
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/mesh/.venv/bin:$PATH"

# Instalar dependencias de sistema necesarias
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    libpq-dev \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias primero para cachear correctamente las capas
COPY mesh/pyproject.toml mesh/uv.lock /app/mesh/

# Instalar dependencias de Python (sin instalar el código del proyecto aún)
RUN --mount=type=cache,target=/root/.cache/uv \
    cd mesh && uv sync --frozen --no-install-project --no-dev

# Copiar el script de entrypoint y hacerlo ejecutable
COPY .docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copiar todo el código del proyecto
COPY . /app

# Definir el entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
