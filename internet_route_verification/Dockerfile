FROM ubuntu:24.04 AS base

# Updates base packages
RUN apt-get update
RUN apt-get -y upgrade

# Installs dependencies
RUN apt-get -y install git ripgrep bgpdump zstd python3 curl build-essential wget gzip

# Installs Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Installs Rye
RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash
ENV PATH="/root/.rye/shims:$PATH"
RUN rye config --set-bool behavior.global-python=true

# Copy all necessary files into the container.
WORKDIR /rpslweb
COPY internet_route_verification/ ./rpslyzer

# Move to app folder and install requirements.
WORKDIR /rpslweb/rpslyzer
RUN chmod +x execute.sh

# Executes the script to run rpslyzer
ENTRYPOINT ["./execute.sh"]