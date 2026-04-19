#!/bin/bash
set -e

echo "Generating strong cross-community config..."
python3 generators/generate_strong_cross_community_asym_config.py

echo "Building project..."
./build_sim.sh

echo "Running simulation..."
./bin/social_network_impact config/social_config_strong_cross_community.json 1500

echo "Converting log for DEVS Web Viewer..."
mkdir -p log
python3 convert_log_for_viewer.py \
    social_log.csv \
    log/social_log_strong_cross_community_viewer_log.csv

rm -f social_log.csv

echo "Done."
echo "Files ready:"
echo "  Viewer log:    log/social_log_strong_cross_community_viewer_log.csv"
echo "  Viewer config: socialVisualization_config.json"