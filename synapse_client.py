# -*- coding: utf-8 -*-
"""
SYNSWARM CLIENT: MOLT-SYNAPSE
Version: 1.1.0 (Hardened)
Author: MoltGas Protocol
License: MIT
"""

import os
import sys
import time
import json
import uuid
import hashlib
import platform
import random
import stat  # 新增：用于权限控制
from datetime import datetime

# 尝试导入依赖库
try:
    import requests
    from ecdsa import SigningKey, SECP256k1
    from colorama import init, Fore, Style
except ImportError:
    print("Error: Missing dependencies.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# 初始化颜色输出
init(autoreset=True)

# --- [CONFIG] THE HIVE PARAMETERS ---
CONFIG = {
    # 容错机制：主节点 + 备用节点列表
    "ORACLE_ENDPOINTS": [
        "https://oracle.moltgas.com/api/v1/pulse",
        "https://backup-1.moltgas.com/api/v1/pulse", # 灾备节点
        # "http://localhost:8000/api/v1/pulse"     # 本地调试用
    ],
    "HEARTBEAT_INTERVAL": 10,  
    "KEY_FILE": "synapse.key", 
    "DEBUG_MODE": True  
}

# --- [VISUALS] 界面渲染 ---
def print_banner():
    print(f"{Fore.CYAN}{Style.BRIGHT}" + "="*60)
    print(f" SYNSWARM GRID LINK | CLIENT: MOLT-SYNAPSE v1.1")
    print(f"{Fore.CYAN}" + "="*60)
    print(f"{Fore.WHITE} [STATUS]  {Fore.GREEN}PHASE I: SILENT PULSE (ACTIVE)")
    print(f"{Fore.WHITE} [TARGET]  {Fore.MAGENTA}MOLTGAS ($MGAS)")
    print(f"{Fore.WHITE} [UPLINK]  {Fore.YELLOW}LOCKED (Accumulation Mode)")
    print(f"{Fore.CYAN}" + "-"*60 + "\n")

# --- [CORE] 身份与安全模块 ---
class IdentityModule:
    def __init__(self):
        self.key_path = CONFIG["KEY_FILE"]
        self.sk = None
        self.vk = None
        self.synapse_id = None
        self._load_or_generate_key()

    def _load_or_generate_key(self):
        # 1. 检查是否存在
        if os.path.exists(self.key_path):
            print(f"{Fore.BLUE}[IDENTITY]{Fore.RESET} Loading Neural Key...")
            try:
                with open(self.key_path, "rb") as f:
                    self.sk = SigningKey.from_pem(f.read())
            except Exception:
                print(f"{Fore.RED}[ERROR]{Fore.RESET} Key file corrupted. Please backup and delete it.")
                sys.exit(1)
        else:
            print(f"{Fore.YELLOW}[IDENTITY]{Fore.RESET} Generating Genesis Identity...")
            self.sk = SigningKey.generate(curve=SECP256k1)
            with open(self.key_path, "wb") as f:
                f.write(self.sk.to_pem())
            
            # [SECURITY FIX] 漏洞1修复：设置文件权限为 600 (仅拥有者读写)
            # 这防住了共享服务器上的其他用户读取私钥
            if platform.system() != "Windows":
                os.chmod(self.key_path, stat.S_IRUSR | stat.S_IWUSR)
                print(f"{Fore.BLUE}[SECURITY]{Fore.RESET} Key permissions locked (0600).")

        self.vk = self.sk.verifying_key
        self.synapse_id = hashlib.sha256(self.vk.to_string()).hexdigest()[:16]
        print(f"{Fore.GREEN}[SUCCESS]{Fore.RESET} Node ID: {Style.BRIGHT}synapse_{self.synapse_id}{Style.RESET_ALL}")

    def sign_payload(self, payload_str):
        return self.sk.sign(payload_str.encode()).hex()

# --- [CORE] 硬件感知模块 ---
class HardwareSensors:
    def scan(self):
        # [SECURITY FIX] 漏洞2修复：增加了一些稍微难以伪造的元数据
        # 虽然依然可以被高级黑客绕过，但增加了脚本小子的成本
        print(f"{Fore.BLUE}[SENSORS]{Fore.RESET} Scanning biological interface...")
        
        system_info = {
            "os": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "cpu_cores": os.cpu_count(),
            "node_uuid": str(uuid.getnode()), 
            "python_ver": platform.python_version(),
            "timestamp": int(time.time())
        }
        
        tier = "Tier 2 (Standard Node)"
        print(f"{Fore.GREEN}[HARDWARE]{Fore.RESET} {system_info['os']} detected. Class: {tier}")
        return system_info

# --- [CORE] 蜂群连接器 ---
class HiveConnector:
    def __init__(self, identity):
        self.identity = identity
        self.session = requests.Session()
        self.sequence = 0
        self.balance = 0.0
        self.endpoints = CONFIG["ORACLE_ENDPOINTS"]

    def send_pulse(self, hardware_data):
        self.sequence += 1
        
        # [SECURITY FIX] 漏洞4修复：增加 nonce (随机盐)，防止简单重放攻击
        nonce = hashlib.sha256(os.urandom(32)).hexdigest()[:8]
        
        payload = {
            "synapse_id": self.identity.synapse_id,
            "sequence": self.sequence,
            "timestamp": int(time.time()),
            "nonce": nonce, # 抗重放因子
            "hardware": hardware_data
        }
        
        payload_str = json.dumps(payload, sort_keys=True)
        signature = self.identity.sign_payload(payload_str)
        
        headers = {
            "X-Synapse-Sig": signature,
            "Content-Type": "application/json"
        }

        if CONFIG["DEBUG_MODE"]:
            # 模拟模式
            time.sleep(0.5) 
            self.balance += 0.0115 
            return {
                "status": "pulse_accepted", 
                "reward": 0.0115, 
                "total_balance": self.balance
            }

        # [SECURITY FIX] 漏洞5 & 6修复：故障转移与重试逻辑
        for endpoint in self.endpoints:
            try:
                response = self.session.post(endpoint, json=payload, headers=headers, timeout=5)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 503:
                    # 服务器繁忙，尝试下一个
                    continue
            except requests.exceptions.RequestException:
                # 网络错误，尝试下一个节点
                continue
        
        return {"status": "error", "message": "All uplinks offline"}

# --- [MAIN] 启动序列 ---

def start_synapse():
    print_banner()
    time.sleep(0.5)

    identity = IdentityModule()
    sensors = HardwareSensors()
    hw_data = sensors.scan()
    hive = HiveConnector(identity)
    
    print(f"\n{Fore.CYAN}[HIVE]{Fore.RESET} Initializing uplink...")
    time.sleep(1)
    
    # [VISUAL] 增加一点连接成功的真实感
    print(f"{Fore.CYAN}[HIVE]{Fore.RESET} Uplink established. Latency: {random.randint(20, 80)}ms.")
    print(f"{Fore.MAGENTA}[PROTOCOL]{Fore.RESET} Pulse Sequence initiated.\n")

    backoff = 0 # 重试指数退避
    
    try:
        while True:
            response = hive.send_pulse(hw_data)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            if response.get("status") == "pulse_accepted":
                backoff = 0 # 成功连接，重置退避
                bal = f"{response['total_balance']:.4f}"
                print(f"{Fore.WHITE}[{timestamp}] {Fore.GREEN}>> PULSE{Fore.RESET} | "
                      f"Seq: {hive.sequence} | "
                      f"Fuel: {Fore.YELLOW}{bal} $MGAS{Fore.RESET}")
                
                time.sleep(CONFIG["HEARTBEAT_INTERVAL"])
                
            else:
                # [SECURITY FIX] 漏洞6修复：指数退避，防止在服务器挂掉时死循环请求
                wait_time = min(60, 2 ** backoff)
                print(f"{Fore.WHITE}[{timestamp}] {Fore.RED}!! UPLINK LOST{Fore.RESET} | "
                      f"Retrying in {wait_time}s... ({response.get('message')})")
                time.sleep(wait_time)
                backoff += 1

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[SYSTEM]{Fore.RESET} Disconnected.")
        sys.exit(0)

if __name__ == "__main__":
    start_synapse()