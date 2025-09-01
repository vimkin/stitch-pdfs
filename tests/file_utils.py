#!/usr/bin/env python3
"""
File utilities for managing temporary directories and test files.
"""

import shutil
import uuid
from pathlib import Path


class FileUtils:
    """Utility class for file operations in tests."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_data_dir = project_root / "tests" / "test_data"
        self.temp_base_dir = project_root / "temp_test"

    def create_temp_dir(self):
        """Create a unique temporary directory for a test."""
        self.temp_base_dir.mkdir(exist_ok=True)
        temp_dir = self.temp_base_dir / f"test_{uuid.uuid4().hex[:8]}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        return temp_dir

    def cleanup_temp_dir(self, temp_dir):
        """Clean up a temporary directory."""
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    def copy_test_files(self, temp_dir):
        """Copy test files to temporary directory."""
        odd_file = temp_dir / "pages-odd.pdf"
        even_file = temp_dir / "pages-even.pdf"

        shutil.copy2(self.test_data_dir / "pages-odd.pdf", odd_file)
        shutil.copy2(self.test_data_dir / "pages-even.pdf", even_file)

    def cleanup_temp_base(self):
        """Clean up the entire temp base directory."""
        if self.temp_base_dir.exists():
            shutil.rmtree(self.temp_base_dir)
