#!/bin/bash
# System monitor
echo "CPU: $(top -l 1 | grep CPU)"
echo "Memory: free -m"