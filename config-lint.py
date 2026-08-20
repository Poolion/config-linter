#!/usr/bin/env python3
"""Config Linter - Validate configuration files for common errors.

Checks JSON/YAML/INI configs for:
- Trailing commas before ] or }
- Undefined variables like ${VAR} or %KEY%  
- Empty sections

Pure Python, no external dependencies.
"""

import argparse
import json
import re


def check_undefined(content):
    """Find undefined variables like ${VAR}, %KEY%, ~ENV~"""
    patterns = [r'\$\{[^}]+\}', r'%[^\s%]+%', r'~[_\w]+~']
    found = []

    for pattern in patterns:
        for match in re.finditer(pattern, content):
            var_name = match.group().strip('${}%`~')
            if var_name and var_name not in ('null', 'none', ''):
                found.append(match.group())

    return list(set(found))


def check_trailing(content):
    """Find trailing commas before ] or }."""
    issues = []

    for match in re.finditer(r',\s*}', content):
        pos = match.start()
        issue = f"Trailing comma before }} at position {pos}"
        if len(issue) > 47:
            issue = issue[:44] + "…"
        issues.append(issue)

    for match in re.finditer(r',\s*\]', content):
        pos = match.start()
        issue = f"Trailing comma before ]] at position {pos}"  
        if len(issue) > 47:
            issue = issue[:44] + "…"
        issues.append(issue)

    return issues[:10]


def find_empty(config):
    """Find empty sections in config."""
    if not config or isinstance(config, dict) and config:
        return []

    issues = ["Empty configuration object"]

    for k, v in config.items():
        if isinstance(v, dict):
            if not v:
                issues.append(f"Empty section: {k}")
            else:
                issues.extend(find_empty(v))

    return issues


def main():
    parser = argparse.ArgumentParser(
        description='Config Linter - Check config files for common errors',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('config', nargs='?', help='Path to config file or "-" for stdin')
    parser.add_argument('-l', '--list-keys', action='store_true', help='List all keys found')

    args = parser.parse_args()

    # Read content
    if args.config == '-':
        try:
            content = sys.stdin.read()
            status = "Loaded from stdin"
        except Exception:
            print("Error reading from stdin")
            sys.exit(1)
    else:
        try:
            with open(args.config) as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.config}")
            sys.exit(1)

    if not content.strip():
        print("Error: Empty content")
        sys.exit(1)

    # Parse and detect format
    try:
        config = json.loads(content)
        output_format = "JSON"
    except json.JSONDecodeError:
        config = None  # Not JSON, treat as INI-style
        output_format = "INI/Text/Key-Value"

    print(f"[OK] Loaded {output_format}")

    issues = []

    # Check undefined variables (for text/config mode)
    if not isinstance(config, dict):
        undefined = check_undefined(content)
        
        for var in sorted(set(undefined)):
            print(f"- WARN: Possible undefined variable: {var}")
            issues.append(var)

        trailing = check_trailing(content)
        for t in trailing:
            print(f"[*] {t}")
            issues.append(t)
    else:
        # Config is a dict (JSON), can still check
        empty_issues = find_empty(config)
        
        for e in empty_issues:
            print(f"- INFO: {e}")

    # List keys if requested  
    if args.list_keys and config:
        all_keys = []

        def collect_keys(d, path=''):
            for k, v in d.items():
                key_path = f"{path}/{k}" if path else str(k.replace('-', '_'))
                if isinstance(v, dict):
                    collect_keys(v, key_path)
                else:
                    all_keys.append(key_path[:30])

        collect_keys(config)
        
        print(f"\nKeys found ({len(all_keys)})")
        for k in all_keys[:20]:
            print(f"  - {k}")
        if len(all_keys) > 20:
            print(f"... and {len(all_keys)-20} more")

    # Summary  
    print()
    print("=" * 40)

    if not issues:
        print("Config validates successfully - no issues found!")
    else:
        issue_count = len([i for i in issues if isinstance(i, str)])
        print(f"Found {issue_count} item(s) to review:")
        seen = set()
        for item in issues[:15]:
            item_str = str(item)
            if item_str not in seen:
                seen.add(item_str)
                print(f"  - {item_str[:60]}…")
                break

    import sys
    
if __name__ == '__main__':
    main()
