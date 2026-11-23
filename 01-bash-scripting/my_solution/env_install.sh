#!/bin/bash
#
# env_install.sh
# Sets up a Python development environment (Python, pip, Jupyter).
# It detects the operating system so it can use the right package manager.
#
# Usage:  ./env_install.sh   (after making it executable with: chmod +x env_install.sh)

# =============================================================
# Feature 1 — Pretty printing function
# Wraps a message in blank lines so the output is easy to read.
# We use printf (not echo) because printf behaves the same on all systems.
# "$1" is the first argument passed to the function (the message).
# =============================================================
pretty_print() {
    printf "\n==> %s\n\n" "$1"
}

# =============================================================
# Feature 2 — Operating system detection
# $OSTYPE is a built-in variable describing the OS.
#   darwin*    -> macOS
#   linux-gnu* -> Linux
# We store the result in a global variable OS to use later.
# =============================================================
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    else
        OS="unknown"
    fi
    pretty_print "Operating system detected: $OS ($OSTYPE)"
}

# =============================================================
# Feature 3 — Python install check
# command -v checks whether a command exists (quietly).
# If python3 is missing, install it with the OS's package manager.
# If it's present, just show the version.
# =============================================================
check_python() {
    if command -v python3 &> /dev/null; then
        pretty_print "Python3 is already installed: $(python3 --version)"
    else
        pretty_print "Python3 not found. Installing..."
        if [[ "$OS" == "macos" ]]; then
            brew install python
        elif [[ "$OS" == "linux" ]]; then
            sudo apt-get update && sudo apt-get install -y python3
        else
            pretty_print "Unknown OS — please install Python 3 manually."
        fi
    fi
}

# =============================================================
# Feature 4 — pip version verification
# pip is Python's package manager. Confirm it exists and show its version.
# =============================================================
check_pip() {
    if command -v pip3 &> /dev/null; then
        pretty_print "pip is installed: $(pip3 --version)"
    else
        pretty_print "pip not found. Trying to bootstrap it with ensurepip..."
        python3 -m ensurepip --upgrade
    fi
}

# =============================================================
# Feature 5 — Jupyter Notebook installation
# The install command differs by OS, so we branch on $OS.
#   macOS: install via Homebrew
#   Linux: install via pip
# =============================================================
install_jupyter() {
    if command -v jupyter &> /dev/null; then
        pretty_print "Jupyter is already installed: $(jupyter --version | head -n 1)"
        return
    fi

    pretty_print "Installing Jupyter Notebook..."
    if [[ "$OS" == "macos" ]]; then
        brew install jupyterlab
    elif [[ "$OS" == "linux" ]]; then
        # --user installs it for the current user without needing sudo.
        pip3 install --user notebook
    else
        pretty_print "Unknown OS — please install Jupyter manually."
    fi
}

# =============================================================
# Feature 6 — macOS-specific health check
# On macOS, "brew doctor" reports common Homebrew problems early.
# We only run this if we're actually on macOS.
# =============================================================
mac_health_check() {
    if [[ "$OS" == "macos" ]]; then
        pretty_print "Running Homebrew health check (brew doctor)..."
        brew doctor
    fi
}

# =============================================================
# Main logic — run the steps in order.
# =============================================================
main() {
    pretty_print "Starting development environment setup..."
    detect_os
    check_python
    check_pip
    install_jupyter
    mac_health_check
    pretty_print "Setup complete!"
}

# Kick everything off.
main
