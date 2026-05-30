FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl build-essential pkg-config libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install stable Rust toolchain.
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --default-toolchain stable

ENV PATH="/root/.cargo/bin:${PATH}"

# Install cargo-mutants.
RUN cargo install cargo-mutants

WORKDIR /
CMD ["/bin/bash"]
