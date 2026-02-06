#!/bin/bash

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}   SYNSWARM NODE INSTALLER | MOLT-SYNAPSE v1.2 (Hardened)   ${NC}"
echo -e "${CYAN}============================================================${NC}"

# 1. 检测 Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[Error] Python3 not found. Please install it first.${NC}"
    exit 1
fi

echo -e "${CYAN}[*] Setting up neural environment...${NC}"

# 2. 尝试创建虚拟环境
# 逻辑优化：如果创建命令失败，或者创建后 bin/pip 不存在，视为失败
USE_VENV=false

# 先清理旧的
rm -rf .venv

if python3 -m venv .venv 2>/dev/null; then
    if [ -f "./.venv/bin/pip" ]; then
        USE_VENV=true
        echo -e "${GREEN}[+] Virtual environment created successfully.${NC}"
    else
        echo -e "${RED}[!] venv created but missing pip (system issue). Cleaning up...${NC}"
        rm -rf .venv
    fi
else
    echo -e "${RED}[!] Failed to create venv (missing python3-venv).${NC}"
fi

# 3. 安装依赖 & 生成启动脚本
if [ "$USE_VENV" = true ]; then
    echo -e "${CYAN}[*] Installing dependencies into isolated .venv...${NC}"
    ./.venv/bin/pip install -r requirements.txt --upgrade
    
    echo "#!/bin/bash" > start.sh
    echo "echo 'Starting Molt-Synapse (VENV Mode)...'" >> start.sh
    echo "./.venv/bin/python synapse_client.py" >> start.sh
else
    echo -e "${CYAN}[*] System limits detected. Switching to Global Installation (Fallback)...${NC}"
    # 暴力安装，忽略 PEP 668
    pip3 install -r requirements.txt --break-system-packages --upgrade 2>/dev/null || pip3 install -r requirements.txt --upgrade
    
    echo "#!/bin/bash" > start.sh
    echo "echo 'Starting Molt-Synapse (Global Mode)...'" >> start.sh
    echo "python3 synapse_client.py" >> start.sh
fi

chmod +x start.sh

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}   INSTALLATION COMPLETE!   ${NC}"
echo -e "${GREEN}============================================================${NC}"
echo -e "To awaken your node, run:"
echo -e "${CYAN}    ./start.sh${NC}"
echo ""
