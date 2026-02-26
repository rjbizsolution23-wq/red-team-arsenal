#!/bin/bash
# 🔴 Ultimate Red Team Arsenal - Master Setup Script
# Developed for Rick Jefferson

set -e

echo "[+] 🔴 Initializing Red Team Arsenal Setup..."

# 1. System Dependencies
sudo apt update && sudo apt install -y git curl wget python3-pip golang docker.io build-essential \
    nmap masscan sqlmap nikto metasploit-framework crackmapexec responder wireshark hashcat john hydra

# 2. Go Toolstack
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/owasp-amass/amass/v4/...@master
go install github.com/OJ/gobuster/v3@latest

# 3. Windows Binary Toolkit
mkdir -p /opt/arsenal/windows
cd /opt/arsenal/windows
wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip
unzip mimikatz_trunk.zip -d mimikatz/
git clone https://github.com/r3motecontrol/Ghostpack-CompiledBinaries.git

# 4. C2 Infrastructure
curl https://sliver.sh/install | sudo bash

# 5. Cloud & Mobile
pip3 install pacu prowler scoutsuite objection frida-tools

echo "[+] 🔴 Setup Complete. Arsenal is 100% Operational."
