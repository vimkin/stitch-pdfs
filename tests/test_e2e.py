#!/usr/bin/env python3
"""
Refactored end-to-end tests for PDF stitching scripts.
Uses simple Docker utilities - same logic, just cleaner organization.
"""

import pytest
from pathlib import Path
import sys

# Add the tests directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from docker_utils import DockerRunner
from file_utils import FileUtils


class TestPDFStitchingE2E:
    """End-to-end tests for PDF stitching scripts."""

    @classmethod
    def setup_class(cls):
        """Setup test environment."""
        cls.project_root = Path(__file__).parent.parent
        cls.docker = DockerRunner(cls.project_root)
        cls.file_utils = FileUtils(cls.project_root)

        # Ensure test data exists
        test_data_dir = cls.project_root / "tests" / "test_data"
        assert (test_data_dir / "pages-odd.pdf").exists(), "pages-odd.pdf not found"
        assert (test_data_dir / "pages-even.pdf").exists(), "pages-even.pdf not found"

        # Build Docker image
        cls.docker.build_image()

    @classmethod
    def teardown_class(cls):
        """Cleanup test environment."""
        cls.file_utils.cleanup_temp_base()

    def _extract_page_numbers(self, pdf_path, temp_dir):
        """Extract page numbers from PDF using pdftotext in Docker."""
        command = f"pdftotext -raw {pdf_path} - | grep -o '[0-9]\\+' | paste -sd ','"
        result = self.docker.run_command(command, temp_dir, timeout=30)

        if result.returncode != 0:
            print(f"Error extracting page numbers: {result.stderr}")
            return ""

        return result.stdout.strip()

    def test_nushell_script_e2e(self):
        """Test the nushell PDF stitching script end-to-end."""
        temp_dir = self.file_utils.create_temp_dir()
        try:
            # Copy test files to temp directory
            self.file_utils.copy_test_files(temp_dir)

            output_pdf = "output-nu.pdf"

            # Command to run the nushell script
            command = f"""
                nu /pdf-tools/scripts/stitch-pdfs.nu \\
                    --output {output_pdf} \\
                    --odd pages-odd.pdf \\
                    --even pages-even.pdf
            """

            # Run the stitching script
            result = self.docker.run_command(command, temp_dir)

            print(f"Nushell script stdout: {result.stdout}")
            print(f"Nushell script stderr: {result.stderr}")

            # Check if the script succeeded
            assert result.returncode == 0, f"Nushell script failed: {result.stderr}"

            # Check if output file was created
            output_file = temp_dir / output_pdf
            assert output_file.exists(), f"Output PDF {output_pdf} was not created"
            assert output_file.stat().st_size > 0, "Output PDF is empty"

            # Extract page numbers and verify sequence
            page_numbers = self._extract_page_numbers(output_pdf, temp_dir)
            print(f"Extracted page numbers from nushell output: {page_numbers}")

            # Verify the page sequence is correct (should be 1,2,3,4,5,6)
            expected_sequence = "1,2,3,4,5,6"
            assert (
                page_numbers == expected_sequence
            ), f"Page sequence incorrect. Expected: {expected_sequence}, Got: {page_numbers}"
        finally:
            self.file_utils.cleanup_temp_dir(temp_dir)

    def test_bash_script_e2e(self):
        """Test the bash PDF stitching script end-to-end."""
        temp_dir = self.file_utils.create_temp_dir()
        try:
            # Copy test files to temp directory
            self.file_utils.copy_test_files(temp_dir)

            output_pdf = "output-sh.pdf"

            # Command to run the bash script
            command = f"""
                bash /pdf-tools/scripts/stitch-pdfs.sh \\
                    --output {output_pdf} \\
                    --odd pages-odd.pdf \\
                    --even pages-even.pdf
            """

            # Run the stitching script
            result = self.docker.run_command(command, temp_dir)

            print(f"Bash script stdout: {result.stdout}")
            print(f"Bash script stderr: {result.stderr}")

            # Check if the script succeeded
            assert result.returncode == 0, f"Bash script failed: {result.stderr}"

            # Check if output file was created
            output_file = temp_dir / output_pdf
            assert output_file.exists(), f"Output PDF {output_pdf} was not created"
            assert output_file.stat().st_size > 0, "Output PDF is empty"

            # Extract page numbers and verify sequence
            page_numbers = self._extract_page_numbers(output_pdf, temp_dir)
            print(f"Extracted page numbers from bash output: {page_numbers}")

            # Verify the page sequence is correct (should be 1,2,3,4,5,6)
            expected_sequence = "1,2,3,4,5,6"
            assert (
                page_numbers == expected_sequence
            ), f"Page sequence incorrect. Expected: {expected_sequence}, Got: {page_numbers}"
        finally:
            self.file_utils.cleanup_temp_dir(temp_dir)

    def test_error_handling_missing_files(self):
        """Test error handling when input files are missing."""
        temp_dir = self.file_utils.create_temp_dir()
        try:
            # Test nushell script with missing files (don't copy test files)
            nu_command = f"""
                nu /pdf-tools/scripts/stitch-pdfs.nu \\
                    --output output.pdf \\
                    --odd nonexistent-odd.pdf \\
                    --even nonexistent-even.pdf
            """

            nu_result = self.docker.run_command(nu_command, temp_dir)
            assert (
                nu_result.returncode != 0
            ), "Nushell script should fail with missing files"

            # Test bash script with missing files (don't copy test files)
            sh_command = f"""
                bash /pdf-tools/scripts/stitch-pdfs.sh \\
                    --output output.pdf \\
                    --odd nonexistent-odd.pdf \\
                    --even nonexistent-even.pdf
            """

            sh_result = self.docker.run_command(sh_command, temp_dir)
            assert (
                sh_result.returncode != 0
            ), "Bash script should fail with missing files"
        finally:
            self.file_utils.cleanup_temp_dir(temp_dir)

    def test_help_options(self, snapshot):
        """Test help options for both scripts using snapshot testing."""
        temp_dir = self.file_utils.create_temp_dir()
        try:
            # Test nushell script help
            nu_help_command = "nu /pdf-tools/scripts/stitch-pdfs.nu --help"
            nu_help_result = self.docker.run_command(nu_help_command, temp_dir)
            assert nu_help_result.returncode == 0, "Nushell help should succeed"
            assert "Usage:" in nu_help_result.stdout, "Help should contain usage info"

            # Snapshot test for nushell help output
            snapshot.assert_match(nu_help_result.stdout, "nushell_help_output.txt")

            # Test bash script help
            sh_help_command = "bash /pdf-tools/scripts/stitch-pdfs.sh --help"
            sh_help_result = self.docker.run_command(sh_help_command, temp_dir)
            assert sh_help_result.returncode == 0, "Bash help should succeed"
            assert "Usage:" in sh_help_result.stdout, "Help should contain usage info"

            # Snapshot test for bash help output
            snapshot.assert_match(sh_help_result.stdout, "bash_help_output.txt")
        finally:
            self.file_utils.cleanup_temp_dir(temp_dir)


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "-s"])
