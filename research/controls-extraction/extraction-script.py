#!/usr/bin/env python3
"""
Extract controls from markdown documents in a GitHub repository.

This script parses markdown files containing compliance controls in the format:
- Control blocks wrapped in {% step %} ... {% endstep %}
- Headers with anchor IDs like: ### Control Name <a href="#ca-01-id" id="ca-01-id"></a>
- Structured fields: WHY, SYSTEM BEHAVIOR, TRIGGERS, INPUTS, OUTPUTS, etc.

Usage:
    python extract_controls.py <repo_path_or_url> [--output controls.json]
    
Examples:
    # Local directory
    python extract_controls.py ./policies --output controls.json
    
    # GitHub URL (clones repo first)
    python extract_controls.py https://github.com/org/repo --output controls.json
"""

import argparse
import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


@dataclass
class Control:
    """Represents a single control extracted from a markdown document."""
    id: str
    name: str
    source_file: str
    anchor: str = ""
    why_reg_cite: str = ""
    system_behavior: str = ""
    triggers: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    timers_slas: str = ""
    edge_cases: str = ""
    audit_logs: list[str] = field(default_factory=list)
    access_control: str = ""
    alerts_metrics: str = ""
    primary_rules: list[str] = field(default_factory=list)
    purpose: str = ""


def clone_repo(url: str, target_dir: str) -> str:
    """Clone a GitHub repository to a target directory."""
    print(f"Cloning {url}...")
    subprocess.run(
        ["git", "clone", "--depth", "1", url, target_dir],
        check=True,
        capture_output=True
    )
    return target_dir


def find_markdown_files(repo_path: str) -> list[Path]:
    """Find all markdown files in the repository."""
    path = Path(repo_path)
    return list(path.rglob("*.md"))


def extract_control_index(content: str) -> dict[str, dict]:
    """
    Extract the Control Index table to get IDs, names, purposes, and primary rules.
    Returns a dict mapping control IDs to their metadata.
    """
    index = {}
    
    # Find the Control Index table
    table_pattern = r'\|\s*ID\s*\|.*?\n\|[-\s|]+\n((?:\|.*?\n)+)'
    match = re.search(table_pattern, content, re.IGNORECASE)
    
    if not match:
        return index
    
    rows = match.group(1).strip().split('\n')
    
    for row in rows:
        # Parse table row: | [ID](link) | Name | Purpose | Rules |
        cells = [c.strip() for c in row.split('|')[1:-1]]
        if len(cells) >= 4:
            # Extract ID from link like [CA-01](file.md#anchor)
            id_match = re.search(r'\[([A-Z]+-\d+)\]', cells[0])
            if id_match:
                control_id = id_match.group(1)
                index[control_id] = {
                    'name': cells[1],
                    'purpose': cells[2],
                    'primary_rules': [r.strip() for r in cells[3].split(';')]
                }
    
    return index


def parse_field_value(text: str, field_name: str) -> str:
    """Extract a field value from the control text."""
    patterns = {
        'why': r'\*\*WHY\s*\(Reg cite\):\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
        'system_behavior': r'\*\*SYSTEM BEHAVIOR:\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
        'triggers': r'\*\*TRIGGERS.*?:\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
        'inputs': r'\*\*INPUTS.*?:\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
        'outputs': r'\*\*OUTPUTS:\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
        'timers_slas': r'\*\*TIMERS/SLAs:\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
        'edge_cases': r'\*\*EDGE CASES:\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
        'audit_logs': r'\*\*AUDIT LOGS:\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
        'access_control': r'\*\*ACCESS CONTROL:\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
        'alerts_metrics': r'\*\*ALERTS/METRICS:\*\*\s*(.+?)(?=\n\*\s*\*\*|\Z)',
    }
    
    pattern = patterns.get(field_name)
    if not pattern:
        return ""
    
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def parse_list_field(value: str) -> list[str]:
    """Parse a field that contains multiple items (events, inputs, etc.)."""
    if not value:
        return []
    
    # Split on semicolons or find backtick-wrapped items
    items = []
    
    # Extract backtick-wrapped items like `event.name`
    backtick_items = re.findall(r'`([^`]+)`', value)
    if backtick_items:
        items.extend(backtick_items)
    
    # If no backtick items, try semicolon split
    if not items:
        items = [i.strip() for i in value.split(';') if i.strip()]
    
    return items


def extract_control_from_step(step_content: str, source_file: str, control_index: dict) -> Optional[Control]:
    """Extract a control from a {% step %} block."""
    
    # Extract the header with ID
    # Pattern: ### Name <a href="#id" id="id"></a>
    header_pattern = r'###\s+(.+?)\s*<a\s+href="#([^"]+)"\s+id="[^"]+"></a>'
    header_match = re.search(header_pattern, step_content)
    
    if not header_match:
        # Try alternative pattern without anchor
        alt_pattern = r'###\s+(.+?)(?:\n|$)'
        alt_match = re.search(alt_pattern, step_content)
        if alt_match:
            name = alt_match.group(1).strip()
            anchor = ""
        else:
            return None
    else:
        name = header_match.group(1).strip()
        anchor = header_match.group(2)
    
    # Extract control ID from anchor (e.g., "ca-01-governance--delegation" -> "CA-01")
    id_match = re.search(r'([a-z]+-\d+)', anchor, re.IGNORECASE)
    control_id = id_match.group(1).upper() if id_match else ""
    
    # Get additional metadata from control index
    index_data = control_index.get(control_id, {})
    
    # Parse all fields
    control = Control(
        id=control_id,
        name=index_data.get('name', name),
        source_file=source_file,
        anchor=anchor,
        why_reg_cite=parse_field_value(step_content, 'why'),
        system_behavior=parse_field_value(step_content, 'system_behavior'),
        triggers=parse_list_field(parse_field_value(step_content, 'triggers')),
        inputs=parse_list_field(parse_field_value(step_content, 'inputs')),
        outputs=parse_list_field(parse_field_value(step_content, 'outputs')),
        timers_slas=parse_field_value(step_content, 'timers_slas'),
        edge_cases=parse_field_value(step_content, 'edge_cases'),
        audit_logs=parse_list_field(parse_field_value(step_content, 'audit_logs')),
        access_control=parse_field_value(step_content, 'access_control'),
        alerts_metrics=parse_field_value(step_content, 'alerts_metrics'),
        primary_rules=index_data.get('primary_rules', []),
        purpose=index_data.get('purpose', ''),
    )
    
    return control


def extract_controls_from_file(file_path: Path) -> list[Control]:
    """Extract all controls from a markdown file."""
    content = file_path.read_text(encoding='utf-8')
    controls = []
    
    # Get the control index for metadata enrichment
    control_index = extract_control_index(content)
    
    # Find all {% step %} blocks
    step_pattern = r'\{%\s*step\s*%\}(.*?)\{%\s*endstep\s*%\}'
    steps = re.findall(step_pattern, content, re.DOTALL)
    
    source_file = str(file_path.name)
    
    for step_content in steps:
        control = extract_control_from_step(step_content, source_file, control_index)
        if control and control.id:
            controls.append(control)
    
    return controls


def extract_timing_matrix(content: str) -> list[dict]:
    """Extract the timing matrix table for additional trigger/deadline info."""
    entries = []
    
    # Find timing matrix section and its table
    section_pattern = r'## Timing Matrix.*?(?=\n## |\Z)'
    section_match = re.search(section_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not section_match:
        return entries
    
    section = section_match.group(0)
    
    # Find table rows (skip header and separator)
    lines = section.split('\n')
    in_table = False
    header_found = False
    
    for line in lines:
        if '|' not in line:
            continue
        
        # Skip header row
        if 'Scenario' in line or 'Trigger' in line:
            header_found = True
            continue
        
        # Skip separator row
        if re.match(r'\s*\|[\s\-:|]+\|', line):
            in_table = True
            continue
        
        if header_found and in_table:
            cells = [c.strip() for c in line.split('|')]
            # Remove empty first/last from split
            cells = [c for c in cells if c]
            
            if len(cells) >= 5:
                # Extract control ID from link in last cell
                control_match = re.search(r'\[([A-Z]+-\d+)\]', cells[4])
                if control_match:
                    entries.append({
                        'scenario': cells[0],
                        'trigger': cells[1],
                        'deadline': cells[2],
                        'content_reference': cells[3],
                        'control_id': control_match.group(1)
                    })
    
    return entries


def main():
    parser = argparse.ArgumentParser(
        description='Extract controls from markdown documents in a GitHub repo'
    )
    parser.add_argument(
        'repo_path',
        help='Path to local directory or GitHub URL'
    )
    parser.add_argument(
        '--output', '-o',
        default='controls.json',
        help='Output JSON file path (default: controls.json)'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'jsonl'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--include-timing',
        action='store_true',
        help='Include timing matrix entries in output'
    )
    
    args = parser.parse_args()
    
    # Determine if we need to clone
    repo_path = args.repo_path
    temp_dir = None
    
    if repo_path.startswith(('http://', 'https://', 'git@')):
        temp_dir = tempfile.mkdtemp()
        repo_path = clone_repo(repo_path, temp_dir)
    
    try:
        # Find all markdown files
        md_files = find_markdown_files(repo_path)
        print(f"Found {len(md_files)} markdown files")
        
        # Extract controls from all files
        all_controls = []
        all_timing = []
        
        for md_file in md_files:
            print(f"Processing {md_file.name}...")
            controls = extract_controls_from_file(md_file)
            all_controls.extend(controls)
            
            if args.include_timing:
                content = md_file.read_text(encoding='utf-8')
                timing = extract_timing_matrix(content)
                all_timing.extend(timing)
        
        print(f"Extracted {len(all_controls)} controls")
        
        # Prepare output
        output_data = {
            'controls': [asdict(c) for c in all_controls],
            'summary': {
                'total_controls': len(all_controls),
                'source_files': list(set(c.source_file for c in all_controls)),
                'control_ids': [c.id for c in all_controls]
            }
        }
        
        if args.include_timing:
            output_data['timing_matrix'] = all_timing
        
        # Write output
        output_path = Path(args.output)
        
        if args.format == 'jsonl':
            with open(output_path, 'w', encoding='utf-8') as f:
                for control in all_controls:
                    f.write(json.dumps(asdict(control)) + '\n')
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
        
        print(f"Output written to {output_path}")
        
    finally:
        # Clean up temp directory if we cloned
        if temp_dir:
            import shutil
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    main()