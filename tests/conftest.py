"""Pytest configuration for export-geoconfirmed tests."""

import sys
from pathlib import Path

# Add app directory to path so internal imports work
app_dir = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_dir))
