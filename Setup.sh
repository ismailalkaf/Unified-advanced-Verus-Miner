#!/bin/bash

# Unified Miner Setup Script
echo "Setting up the unified advanced Verus miner..."

# Install required dependencies
apt install -y git clang cmake make openssl

# Clone and build oink70 miner
if [ ! -d "oink70" ]; then
    echo "Cloning oink70 miner..."
    git clone https://github.com/oink70/veruscoin.git oink70
fi
echo "Building oink70 miner..."
cd oink70/src || exit
make -j$(nproc)
cd ../../

# Clone and build verus-solver miner
if [ ! -d "verus-solver" ]; then
    echo "Cloning verus-solver miner..."
    git clone https://github.com/VerusCoin/verus-solver.git
fi
echo "Building verus-solver miner..."
cd verus-solver || exit
cmake . -DCMAKE_BUILD_TYPE=Release
make
cd ..

echo "Setup complete! Use 'python3 unified_miner.py' to start mining."
