#!/bin/bash

download_page() {
    local i=$1
    local response=$(curl -s "https://online-go.com/api/v1/puzzles?page=$i")
    if [[ $response == *"results"* ]]; then
        while IFS= read -r entry; do
            date=$(echo "$entry" | jq -r '.created' | cut -d'-' -f1)
            if [ "$date" == "2023" ]; then
                id=$(echo "$entry" | jq -r '.id')
                echo "$id"
            fi
        done < <(echo "$response" | jq -c '.results[]')
    fi
}

export -f download_page

max_pages=4872
parallel -j 32 download_page ::: $(seq 1 $max_pages) | jq -c '.' > go_ids.txt
