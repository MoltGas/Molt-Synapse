#!/bin/bash
echo "Terminating Neural Uplink..."
# 发送 quit 信号给后台进程
screen -X -S synswarm quit
echo "Connection severed. Node offline."
