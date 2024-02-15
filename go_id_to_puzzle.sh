#!/bin/bash

# Check if id.txt file exists
if [ ! -f "go_ids.txt" ]; then
  echo "Error: id.txt file not found."
  exit 1
fi

# Create a directory to store the output files
mkdir -p go_sgf

# Read each line from id.txt and run the Python script in parallel
while IFS= read -r id; do
  # Run the modified Python script in the background with the current id
  python download_go_puzzle.py "$id" &

done < "go_ids.txt"

# Wait for all background processes to finish
wait

python combine_go_sgf.py

wait