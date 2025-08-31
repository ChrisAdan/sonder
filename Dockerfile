# Multi-stage build for Sonder simulation
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid 1000 sonder \
    && useradd --uid 1000 --gid sonder --shell /bin/bash --create-home sonder

# Set work directory
WORKDIR /app

# Copy project files
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/
COPY tests/ tests/

# Install package
RUN pip install --upgrade pip && \
    pip install -e .

# Create data directory for database
RUN mkdir -p /data && chown -R sonder:sonder /data /app

# Switch to non-root user
USER sonder

# Initialize database
RUN python -m sonder init-db --database-path /data/sonder.db

# Expose port for potential web interface
EXPOSE 8000

# Default command
CMD ["python", "-m", "sonder", "run", "--database-path", "/data/sonder.db"]

# Development stage with additional tools
FROM base as dev

USER root

# Install development dependencies
RUN pip install -e ".[dev,analytics]"

# Install additional development tools
RUN apt-get update && apt-get install -y \
    git \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

USER sonder

CMD ["/bin/bash"]
