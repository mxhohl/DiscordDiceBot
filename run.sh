#! /bin/bash

# Ensure we're in the DiceBot directory
cd "$(dirname "$BASH_SOURCE")"

# Activate the virtual environment
source venv/bin/activate

# Run the bot
python3 run.py
