# PDF Page Stitcher

CLI utility to stitch odd and reversed even pages of a PDF together. Available as both **Nushell** and **Bash** scripts, using QPDF for fast, lossless PDF manipulation.

## Table of Contents

- [PDF Page Stitcher](#pdf-page-stitcher)
   - [Table of Contents](#table-of-contents)
   - [Features](#features)
   - [Example: Scanner Workflow](#example-scanner-workflow)
      - [Scanning Process](#scanning-process)
      - [How it works](#how-it-works)

   - [Installation \& Requirements](#installation--requirements)
      - [Prerequisites](#prerequisites)

   - [Usage](#usage)
      - [Script Options](#script-options)

   - [Development \& Testing](#development--testing)
   - [Architecture](#architecture)

## Features

- **Two implementations**: Choose between Nushell (`.nu`) or Bash (`.sh`) scripts
- **QPDF-based**: Fast, lossless PDF manipulation
- **Cross-platform**: Works on macOS, Linux, and Windows (with appropriate shell)

## Example: Scanner Workflow

This tool is particularly useful when you have a scanner that doesn't support double-sided scanning. Here's how it works:

### Scanning Process

1. **Scan odd pages**: Place your document in the scanner and scan pages 1, 3, 5, etc. (front sides)
2. **Flip and scan even pages**: Flip the entire stack and scan the back sides, which will be in reverse order: 6, 4, 2

### How it works

The script takes the first page from the odd file (page 1), then the last page from the even file (page 2), then the second page from the odd file (page 3), then the second-to-last page from the even file (page 4), and so on.

```md
Odd pages:  [1] [3] [5]
Even pages: [6] [4] [2]
Result:     [1][2][3][4][5][6]
```

## Installation & Requirements

### Prerequisites

- **QPDF**: The core PDF manipulation tool
   - macOS: `brew install qpdf`
   - Ubuntu/Debian: `apt install qpdf`
   - Windows: Download from [QPDF website](http://qpdf.sourceforge.net/)

## Usage

```bash
# Example usage - both scripts:

# Nushell script
./scripts/stitch-pdfs.nu -o final.pdf --odd pages-odd.pdf --even pages-even.pdf

# Bash script
./scripts/stitch-pdfs.sh --output final.pdf --odd pages-odd.pdf --even pages-even.pdf
```

### Script Options

Both scripts support the same command-line interface:

```bash
Options:
  --output FILE    Output PDF file
  --odd FILE       PDF with odd pages (1, 3, 5, ...)
  --even FILE      PDF with even pages in reverse order (6, 4, 2, ...)
  --help           Show help message
```

## Development & Testing

Before running tests, ensure you have installed all necessary Python and Docker dependencies.

Depending on whether you're executing these tests locally or in docker, you need to install python dependencies if executing tests locally.

To execute tests locally:

```bash
# Run all tests
pytest tests/ -v
```

To execute tests in docker:

```bash
# Build the Docker image
docker build -t pdf-tools-test .

# Run all tests
docker run --rm -v $(pwd):/app pdf-tools-test pytest tests/ -v
```

## Architecture

The project separates concerns cleanly:

- **Scripts** (`scripts/`): Two implementations of the same functionality

   - `stitch-pdfs.nu` - Nushell implementation with modern syntax
   - `stitch-pdfs.sh` - Bash implementation with traditional shell scripting

- **Docker environment**: Consistent testing environment with all dependencies
- **Test utilities**: Separated Docker operations from file system operations
- **Comprehensive testing**: Coverage of both success and error scenarios
