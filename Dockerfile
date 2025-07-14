# Base image pinned by digest for security and consistency
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:5c8edeb8b5644b618882e06ddaa8ddf509dcd1aa7d08fedac7155106116a9a9e

# Build-time Git commit SHA capture for debugging/versioning
ARG GITHUB_SHA=unknown
ENV GITHUB_SHA=${GITHUB_SHA}

# Environment configurations for UV and Python paths
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/mesh/.venv/bin:$PATH"

# Install system-level dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -yqq --no-install-recommends \
        curl \
        git \
        libpq-dev \
        gcc \
        libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency management files early for caching
COPY mesh/pyproject.toml mesh/uv.lock ./mesh/

# Install Python dependencies without installing project code yet
RUN --mount=type=cache,target=/root/.cache/uv \
    cd mesh && \
    uv sync --frozen --no-install-project --no-dev

# Copy entrypoint script and make it executable
COPY .docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy full application source
COPY . .

# Set entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
