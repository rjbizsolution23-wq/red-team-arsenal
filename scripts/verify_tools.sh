#!/bin/bash
# 🔴 Arsenal Health Check & Tool Verification

echo "🔴 Verifying Red Team Arsenal Components..."

check_tool() {
    if command -v $1 &> /dev/null; then
        echo "[✓] $1 is ready."
    else
        echo "[✗] $1 - MISSING"
    fi
}

# Core Tools
check_tool nmap
check_tool msfconsole
check_tool sliver-server
check_tool nuclei
check_tool hashcat

# Check Binaries
if [ -d "/opt/arsenal/windows/mimikatz" ]; then
    echo "[✓] Windows Binaries: Mimikatz detected."
else
    echo "[✗] Windows Binaries: NOT FOUND."
fi

echo "🔴 Verification Completed."
