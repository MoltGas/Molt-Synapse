#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}==================================================${NC}"
echo -e "${CYAN}   MOLT-SYNAPSE | ALWAYS-ON UPLINK SERVICE        ${NC}"
echo -e "${CYAN}==================================================${NC}"

# 1. 检查 screen 工具
if ! command -v screen &> /dev/null; then
    echo "Installing background service tools..."
    if [ -f /etc/debian_version ]; then
        sudo apt-get update && sudo apt-get install screen -y
    elif [ -f /etc/redhat-release ]; then
        sudo yum install screen -y
    fi
fi

# 2. 检查是否已经在运行
if screen -list | grep -q "synswarm"; then
    echo -e "${GREEN}[!] Uplink is ALREADY active in background.${NC}"
    echo -e "To access interface, run: ./view_status.sh"
    exit 1
fi

# 3. 启动后台进程 (Detached Mode)
echo "Initializing Neural Uplink in background..."
screen -dmS synswarm ./start.sh

echo -e "${GREEN}[+] SUCCESS: Node is contributing compute 24/7.${NC}"
echo -e "${CYAN}[INFO] You can close this terminal window safely.${NC}"
echo ""
echo -e "To check status:       ${GREEN}./view_status.sh${NC}"
echo -e "To terminate link:     ${GREEN}./stop.sh${NC}"
echo ""
