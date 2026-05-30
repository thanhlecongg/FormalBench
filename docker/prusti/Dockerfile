FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl build-essential pkg-config libssl-dev \
    wget unzip git openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install Prusti from GitHub release.
ARG PRUSTI_RELEASE_URL=https://github.com/viperproject/prusti-dev/releases/latest/download/prusti-release-ubuntu.zip
RUN wget ${PRUSTI_RELEASE_URL} -O /tmp/prusti.zip \
    && mkdir -p /opt/prusti \
    && unzip /tmp/prusti.zip -d /opt/prusti \
    && rm /tmp/prusti.zip \
    && find /opt/prusti -type f -exec chmod +x {} +

ENV PATH="/opt/prusti:/root/.cargo/bin:${PATH}"
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Install the exact Rust nightly that Prusti requires.
RUN PRUSTI_NIGHTLY=$(grep 'channel' /opt/prusti/rust-toolchain | sed 's/.*"\(.*\)"/\1/') \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
       sh -s -- -y --default-toolchain ${PRUSTI_NIGHTLY}

# Set up a template Cargo project with prusti-contracts pre-resolved.
RUN cargo init --lib /home/prusti-template
WORKDIR /home/prusti-template
RUN printf '[package]\nname = "prusti-verify"\nversion = "0.1.0"\nedition = "2021"\n\n[dependencies]\nprusti-contracts = "*"\n\n# Pin transitive deps that publish edition-2024 crates\n# incompatible with Prusti nightly toolchain\ngetrandom = ">=0.1, <0.4"\nuuid = ">=1, <1.11"\nproc-macro2 = ">=1, <1.0.87"\n' > Cargo.toml
RUN cargo build || true
RUN cargo build 2>&1 | tail -5

# Install cargo-mutants for mutation analysis.
RUN cargo install cargo-mutants

WORKDIR /
CMD ["/bin/bash"]
