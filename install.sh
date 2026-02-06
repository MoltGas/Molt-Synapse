#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "============================================================"
echo "   SYNSWARM NODE INSTALLER | MOLT-SYNAPSE v1.1"
echo "============================================================"
echo -e "${NC}"

# 1. 检测 Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[Error] Python3 not found. Please install it first.${NC}"
    exit 1
fi

echo -e "${CYAN}[*] Setting up isolated neural environment...${NC}"

# 2. 创建虚拟环境 (隔离舱)
# 这样可以绕过 'externally-managed-environment' 错误，且不污染用户系统
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[!] Failed to create venv. Trying fallback installation...${NC}"
        # 如果虚拟环境创建失败（极少见），尝试暴力安装
        pip install -r requirements.txt --break-system-packages
    else
        echo -e "${GREEN}[+] Virtual environment created.${NC}"
    fi
fi

# 3. 安装依赖
if [ -d ".venv" ]; then
    echo -e "${CYAN}[*] Installing dependencies into .venv...${NC}"
    # 使用虚拟环境内的 pip
    ./.venv/bin/pip install -r requirements.txt --upgrade
    
    # 4. 生成启动脚本 (Start Script)
    # 这是关键！让用户以后启动时不需要手动激活环境
    echo "#!/bin/bash" > start.sh
    echo "echo 'Starting Molt-Synapse...'" >> start.sh
    echo "./.venv/bin/python synapse_client.py" >> start.sh
    chmod +x start.sh
    
    echo -e "${GREEN}[+] Dependencies installed successfully.${NC}"
else
    # Fallback: 如果没有 venv，直接安装
    pip install -r requirements.txt
    echo "python3 synapse_client.py" > start.sh
    chmod +x start.sh
fi

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}   INSTALLATION COMPLETE!   ${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "To awaken your node, run:"
echo -e "${CYAN}    ./start.sh${NC}"
echo ""
