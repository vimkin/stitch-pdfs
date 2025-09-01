#!/usr/bin/env python3
"""
Simple Docker utilities for PDF stitching tests.
Pure Docker operations without file system logic.
"""

import subprocess
from pathlib import Path


class DockerRunner:
    """Simple utility class for Docker operations in tests."""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def build_image(self, image_name="pdf-tools-test"):
        """Build the Docker image for testing."""
        print(f"Building Docker image {image_name}...")
        result = subprocess.run(
            ["docker", "build", "-t", image_name, "."],
            cwd=self.project_root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"Docker build stdout: {result.stdout}")
            print(f"Docker build stderr: {result.stderr}")
            raise RuntimeError(f"Failed to build Docker image: {result.stderr}")

    def run_command(
        self, command, workspace_dir, image_name="pdf-tools-test", timeout=120
    ):
        """Run a command in the Docker container with mounted workspace directory."""
        docker_cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{workspace_dir}:/workspace",
            "-w",
            "/workspace",
            image_name,
            "sh",
            "-c",
            command,
        ]

        result = subprocess.run(
            docker_cmd, capture_output=True, text=True, timeout=timeout
        )

        return result
