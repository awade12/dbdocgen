#!/usr/bin/env python3
"""
Version updater script for dbdocgen.

This script updates version numbers in:
- pyproject.toml
- dbdocgen/__init__.py

Usage:
    python scripts/updatever.py --major
    python scripts/updatever.py --minor
    python scripts/updatever.py --patch
    python scripts/updatever.py --beta
    python scripts/updatever.py --release
    python scripts/updatever.py --set X.Y.Z[bN]
"""

import argparse
import os
import re
import sys
from pathlib import Path


def get_current_version():
    """Get the current version from pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if version_match:
        return version_match.group(1)
    else:
        raise ValueError("Could not find version in pyproject.toml")


def parse_version(version_str):
    """Parse version string into components."""
    # Check if it's a beta version
    beta_match = re.match(r'^(\d+)\.(\d+)\.(\d+)b(\d+)$', version_str)
    if beta_match:
        major, minor, patch, beta = map(int, beta_match.groups())
        return major, minor, patch, beta
    
    # Regular version
    regular_match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_str)
    if regular_match:
        major, minor, patch = map(int, regular_match.groups())
        return major, minor, patch, None
    
    raise ValueError(f"Invalid version format: {version_str}")


def bump_version(current_version, bump_type):
    """Bump the version according to the specified type."""
    version_parts = parse_version(current_version)
    
    if len(version_parts) == 4:
        major, minor, patch, beta = version_parts
    else:
        major, minor, patch = version_parts[:3]
        beta = None
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    elif bump_type == 'beta':
        # If it's already a beta, increment the beta number
        if beta is not None:
            return f"{major}.{minor}.{patch}b{beta + 1}"
        # If it's not a beta yet, make it beta 1
        return f"{major}.{minor}.{patch}b1"
    elif bump_type == 'release':
        # If it's a beta, remove the beta part
        if beta is not None:
            return f"{major}.{minor}.{patch}"
        # If it's already a release, do nothing
        return current_version
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_pyproject_toml(new_version):
    """Update the version in pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    updated_content = re.sub(
        r'(version\s*=\s*)"([^"]+)"',
        f'\\1"{new_version}"',
        content
    )
    
    with open(pyproject_path, 'w') as f:
        f.write(updated_content)
    
    return pyproject_path


def update_init_py(new_version):
    """Update the version in __init__.py."""
    init_path = Path(__file__).parent.parent / "dbdocgen" / "__init__.py"
    
    with open(init_path, 'r') as f:
        content = f.read()
    
    updated_content = re.sub(
        r'(__version__\s*=\s*)"([^"]+)"',
        f'\\1"{new_version}"',
        content
    )
    
    with open(init_path, 'w') as f:
        f.write(updated_content)
    
    return init_path


def main():
    parser = argparse.ArgumentParser(description="Update version numbers in project files")
    
    # Create a mutually exclusive group for version actions
    version_group = parser.add_mutually_exclusive_group(required=True)
    version_group.add_argument('--major', action='store_true', help='Bump major version')
    version_group.add_argument('--minor', action='store_true', help='Bump minor version')
    version_group.add_argument('--patch', action='store_true', help='Bump patch version')
    version_group.add_argument('--beta', action='store_true', help='Create or increment beta version')
    version_group.add_argument('--release', action='store_true', help='Convert beta to release version')
    version_group.add_argument('--set', metavar='VERSION', help='Set specific version (X.Y.Z or X.Y.ZbN format)')
    
    args = parser.parse_args()
    
    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")
        
        if args.set:
            # Validate the format of the provided version
            if not re.match(r'^\d+\.\d+\.\d+(?:b\d+)?$', args.set):
                print("Error: Version must be in X.Y.Z or X.Y.ZbN format")
                sys.exit(1)
            new_version = args.set
        else:
            # Determine which part to bump
            bump_type = 'major' if args.major else 'minor' if args.minor else 'patch' if args.patch else 'beta' if args.beta else 'release'
            new_version = bump_version(current_version, bump_type)
        
        print(f"Updating to version: {new_version}")
        
        # Update files
        pyproject_path = update_pyproject_toml(new_version)
        init_path = update_init_py(new_version)
        
        print(f"Updated {pyproject_path}")
        print(f"Updated {init_path}")
        print(f"Version successfully updated to {new_version}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Usage examples:
# python3 scripts/updatever.py --major     # 0.1.0 -> 1.0.0
# python3 scripts/updatever.py --minor     # 0.1.0 -> 0.2.0
# python3 scripts/updatever.py --patch     # 0.1.0 -> 0.1.1
# python3 scripts/updatever.py --beta      # 0.1.0 -> 0.1.0b1, 0.1.0b1 -> 0.1.0b2
# python3 scripts/updatever.py --release   # 0.1.0b1 -> 0.1.0
# python3 scripts/updatever.py --set 1.0.0b2
