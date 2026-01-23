Usage
# From a local directory
python extract_controls.py ./policies --output controls.json

# From a GitHub repo (clones automatically)
python extract_controls.py https://github.com/your-org/policies --output controls.json

# Include timing matrix data
python extract_controls.py ./policies --output controls.json --include-timing

# Output as JSON Lines (one control per line)
python extract_controls.py ./policies --output controls.jsonl --format jsonl