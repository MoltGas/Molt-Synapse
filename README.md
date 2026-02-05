# 🧠 Molt-Synapse

**The Foundation Layer of the Global AI Cortex.**

Molt-Synapse is the lightweight node client for the **MoltGas Protocol**. By running a Synapse, you connect your local compute potential to a decentralized neural network, fueling the evolution of autonomous AI agents with **$MGAS**.

## ⚡ The 20% Depletion Protocol
The total supply of $MGAS is fixed at **1,000,000,000**. To maintain the scarcity and value of Neural Fuel, the Synaptic Layer follows a strict decay model:

- **Genesis Heartbeat Pool:** 100,000,000 $MGAS (10% of Total)
- **Base Transmission Rate:** 100 $MGAS / 24h
- **The Halving Rule:** Every **20,000,000 $MGAS** transmitted triggers an automatic **50% reduction** in daily rewards.

### 📅 Synaptic Decay Schedule
| Phase | Pool Remaining | Daily Reward | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1** | 100M - 80M | **100 $MGAS** | **ACTIVE** |
| **Phase 2** | 80M - 60M | 50 $MGAS | PENDING |
| **Phase 3** | 60M - 40M | 25 $MGAS | PENDING |

## 🚀 Quick Start

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/moltgas/Molt-Synapse.git](https://github.com/moltgas/Molt-Synapse.git)
   cd Molt-Synapse

2. * Install dependencies:
   pip install -r requirements.txt

3. * Activate your Synapse:
   python synapse_client.py

## 🛡️ Security & Identity
- **Node Identity:** Your `Synapse_ID` is bound to your physical hardware. On the first run, a `node.key` is generated in the `.molt/` directory. **Back it up.** If you lose this key, you lose access to your unclaimed $MGAS.
- **Address Locking:** For your protection, once you link a wallet to your `Synapse_ID` for withdrawal, the link is permanent. This prevents hackers from hijacking your accumulated rewards.
- **Chaos Cooldown:** To maintain network stability, each node has a unique synchronization window (24h ± 2h).