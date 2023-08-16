#!/bin/sh

for file in segment_*.csv; do
    echo $file;

    output=output_${file};

    if [ -f "$output" ]; then
        echo "$output exists, skipping..."
        continue  # Skip to the next iteration if the file exists
    fi

    python3 generate_locode_to_osmid.py $file $output;
done