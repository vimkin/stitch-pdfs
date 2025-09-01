#!/bin/bash

# QPDF-based PDF page stitcher
# Usage: ./stitch-qpdf.sh --output output.pdf --odd pages-odd.pdf --even pages-even.pdf

usage() {
    echo "Stitch odd and reversed even pages of a PDF together using QPDF"
    echo ""
    echo "Usage: $0 --output OUTPUT_FILE --odd ODD_FILE --even EVEN_FILE"
    echo ""
    echo "Options:"
    echo "  --output FILE    Output PDF file"
    echo "  --odd FILE       PDF with odd pages (1, 3, 5, ...)"
    echo "  --even FILE      PDF with even pages in reverse order (6, 4, 2, ...)"
    echo "  --help           Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 --output document.pdf --odd pages-odd.pdf --even pages-even.pdf"
    echo ""
    echo "Requirements:"
    echo "  - QPDF (install with: brew install qpdf)"
}

# Check if QPDF is installed
if ! command -v qpdf &> /dev/null; then
    echo "❌ QPDF is not installed."
    echo "Install with: brew install qpdf (macOS) or apt install qpdf (Ubuntu)"
    exit 1
fi

# Parse command line arguments
OUTPUT_FILE=""
ODD_FILE=""
EVEN_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --odd)
            ODD_FILE="$2"
            shift 2
            ;;
        --even)
            EVEN_FILE="$2"
            shift 2
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate arguments
if [[ -z "$OUTPUT_FILE" || -z "$ODD_FILE" || -z "$EVEN_FILE" ]]; then
    echo "❌ Missing required arguments"
    usage
    exit 1
fi

# Check if input files exist
if [[ ! -f "$ODD_FILE" ]]; then
    echo "❌ Odd file does not exist: $ODD_FILE"
    exit 1
fi

if [[ ! -f "$EVEN_FILE" ]]; then
    echo "❌ Even file does not exist: $EVEN_FILE"
    exit 1
fi

echo "🔍 Analyzing PDF files..."

# Get page counts using QPDF
ODD_PAGES=$(qpdf --show-npages "$ODD_FILE")
EVEN_PAGES=$(qpdf --show-npages "$EVEN_FILE")

echo "📄 Odd file has $ODD_PAGES pages"
echo "📄 Even file has $EVEN_PAGES pages"

if [[ "$ODD_PAGES" != "$EVEN_PAGES" ]]; then
    echo "❌ Page count mismatch: odd file has $ODD_PAGES pages, even file has $EVEN_PAGES pages"
    exit 1
fi

echo "🔄 Stitching pages with QPDF (lossless)..."

# Build qpdf command with page ranges
QPDF_PAGES=""

for ((i=0; i<ODD_PAGES; i++)); do
    ODD_PAGE=$((i + 1))
    EVEN_PAGE=$((EVEN_PAGES - i))
    QPDF_PAGES="$QPDF_PAGES \"$ODD_FILE\" $ODD_PAGE \"$EVEN_FILE\" $EVEN_PAGE"
done

# Execute qpdf command
echo "🚀 Executing QPDF merge..."
eval "qpdf --empty --pages $QPDF_PAGES -- \"$OUTPUT_FILE\""

if [[ $? -eq 0 ]]; then
    echo "✅ Success! Output saved to: $OUTPUT_FILE"
    echo "📏 File size: $(du -h "$OUTPUT_FILE" | cut -f1)"
else
    echo "❌ Failed to create PDF"
    exit 1
fi
