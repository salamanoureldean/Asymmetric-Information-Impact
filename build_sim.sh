#!/bin/bash
set -e

if [ -d "build" ]; then rm -Rf build; fi
mkdir -p build
cd build
cmake ..
make
cd ..
echo "Compilation done. Executable in the bin folder"