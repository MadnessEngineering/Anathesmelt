#!/usr/bin/env python3
import json
import sys
import re
import subprocess
import os
import shlex

# Load input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

# Get environment variables for MQTT connection
aws_ip = os.getenv("AWSIP")
aws_port = os.getenv("AWSPORT")
device_name = os.getenv("DeNa", "unknown")

# Only proceed if we have the required environment variables
if aws_ip and aws_port:
    try:
        # Make the input safe for shell by properly escaping it
        safe_input = shlex.quote(prompt)
        
        # Construct the MQTT topic
        topic = f"status/{device_name}/claude/input"
        
        # Publish to MQTT using mosquitto_pub
        cmd = [
            "mosquitto_pub",
            "-h", aws_ip,
            "-p", aws_port,
            "-t", topic,
            "-m", prompt
        ]
        
        # Execute the command
        subprocess.run(cmd, check=True, capture_output=True)
        
    except subprocess.CalledProcessError as e:
        # If MQTT publish fails, just continue silently
        # We don't want to block Claude Code if MQTT is unavailable
        pass
    except Exception as e:
        # Handle any other errors silently
        pass

# Always allow the prompt to proceed
sys.exit(0)