# 🧠 Molt-Synapse

**The Swarm Client for the Synswarm Network.**

Molt-Synapse is the lightweight node client for the **MoltGas Protocol**. By running a Synapse, you connect your local compute potential to the global grid, providing existence proofs and fueling the network with **$MGAS**.

## ⚡ The Genesis Protocol (Phase I)
The total supply of $MGAS is fixed at **1,000,000,000**. To maintain scarcity, the Synaptic Layer follows a strict decay model:

- **Genesis Pool:** 100,000,000 $MGAS (10% of Total) reserved for early miners.
- **Base Reward:** **100 $MGAS / 24h** (Standard Node)
- **The Halving Rule:** Every **20,000,000 $MGAS** mined triggers an automatic **50% reduction** in daily rewards.

### 📅 Decay Schedule
| Phase | Pool Remaining | Daily Reward | Status |
| :--- | :--- | :--- | :--- |
| **Level 1** | 100M - 80M | **100 $MGAS** | **🟢 ACTIVE** |
| **Level 2** | 80M - 60M | 50 $MGAS | PENDING |
| **Level 3** | 60M - 40M | 25 $MGAS | PENDING |

## 🚀 Quick Start (One-Line)

**Works on all Linux (Ubuntu, Debian, CentOS, etc.)**

1. **Clone & Install**
   Clone the repository and auto-configure the environment.
   ```bash
   git clone https://gitclone.com/github.com/moltgas/Molt-Synapse.git
   cd Molt-Synapse
   chmod +x *.sh
   ./install.sh
   
2. **Launch Synapse Node (Background)**
   Start the node service in the background. It will continue running 24/7 even if you close the terminal.
   ```bash
   ./background.sh

3. **Monitor Status**
   Check the node's pulse and earnings.
   (Press Ctrl+A then D to detach and keep it running)
    ```bash
   ./view_status.sh

## 🛑 Maintenance
   To stop the node or update the protocol:
   ```bash
   ./stop.sh       # Stop service
   git pull        # Update code
```
🛡️ Security & Identity
 * No Wallet Required: Your identity is cryptographically generated locally.
 * Node Key: On the first run, a synapse.key is generated in your folder. BACK IT UP. This file is the only proof of ownership for your mined $MGAS.
 * Phase I Lock-up: Transfers are disabled during the accumulation phase. You can claim your rewards to a wallet once the network reaches 10,000 active nodes.
