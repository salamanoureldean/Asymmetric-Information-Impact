#!/bin/bash
set -e

echo "Generating boundary seed config..."
python3 generators/generate_boundary_seed_asym_config.py

echo "Building project..."
./build_sim.sh

echo "Running simulation..."
./bin/social_network_impact config/social_config_boundary_seed.json 1500

echo "Converting log for DEVS Web Viewer..."
mkdir -p log
python3 convert_log_for_viewer.py \
    social_log.csv \
    log/social_log_boundary_seed_viewer_log.csv

rm -f social_log.csv

echo "Done."
echo "Files ready:"
echo "  Viewer log:    log/social_log_boundary_seed_viewer_log.csv"
echo "  Viewer config: socialVisualization_config.json"