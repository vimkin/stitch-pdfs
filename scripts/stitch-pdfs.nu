#!/usr/bin/env nu

# QPDF-based PDF page stitcher (Nushell version)
# Usage: ./stitch-pdfs.nu --output output.pdf --odd pages-odd.pdf --even pages-even.pdf

def main [
    --output (-o): string  # Output PDF file
    --odd: string          # PDF with odd pages (1, 3, 5, ...)
    --even: string         # PDF with even pages in reverse order (6, 4, 2, ...)
    --help (-h)            # Show this help message
] {
    if $help {
        print_usage
        return
    }

    # Validate required arguments
    if ($output | is-empty) or ($odd | is-empty) or ($even | is-empty) {
        print "❌ Missing required arguments"
        print_usage
        exit 1
    }

    # Check if QPDF is installed
    if not (which qpdf | is-not-empty) {
        print "❌ QPDF is not installed."
        print "Install QPDF and rerun this script."
        exit 1
    }

    # Check if input files exist
    if not ($odd | path exists) {
        print $"❌ Odd file does not exist: ($odd)"
        exit 1
    }

    if not ($even | path exists) {
        print $"❌ Even file does not exist: ($even)"
        exit 1
    }

    print "🔍 Analyzing PDF files..."

    # Get page counts using QPDF
    let odd_pages = (qpdf --show-npages $odd | into int)
    let even_pages = (qpdf --show-npages $even | into int)

    print $"📄 Odd file has ($odd_pages) pages"
    print $"📄 Even file has ($even_pages) pages"

    if $odd_pages != $even_pages {
        print $"❌ Page count mismatch: odd file has ($odd_pages) pages, even file has ($even_pages) pages"
        exit 1
    }

    print "🔄 Stitching pages with QPDF (lossless)..."

    # Build qpdf command with page ranges
    let qpdf_pages = (0..<$odd_pages | each {|i|
        let odd_page = $i + 1
        let even_page = $even_pages - $i
        [$odd, $odd_page, $even, $even_page]
    } | flatten)

    # Execute qpdf command
    print "🚀 Executing QPDF merge..."

    let qpdf_result = (do {
        ^qpdf --empty --pages ...$qpdf_pages -- $output
    } | complete)

    if $qpdf_result.exit_code == 0 {
        print $"✅ Success! Output saved to: ($output)"
        let file_size = (ls $output | get size | first | into string)
        print $"📏 File size: ($file_size)"
    } else {
        print "❌ Failed to create PDF"
        if ($qpdf_result.stderr | is-not-empty) {
            print $"Error: ($qpdf_result.stderr)"
        }
        exit 1
    }
}

def print_usage [] {
    print "Stitch odd and reversed even pages of a PDF together using QPDF"
    print ""
    print "Usage: ./stitch-pdfs.nu --output OUTPUT_FILE --odd ODD_FILE --even EVEN_FILE"
    print ""
    print "Options:"
    print "  --output, -o FILE    Output PDF file"
    print "  --odd FILE           PDF with odd pages (1, 3, 5, ...)"
    print "  --even FILE          PDF with even pages in reverse order (6, 4, 2, ...)"
    print "  --help, -h           Show this help message"
    print ""
    print "Example:"
    print "  ./stitch-pdfs.nu --output document.pdf --odd pages-odd.pdf --even pages-even.pdf"
    print ""
    print "Requirements:"
    print "  - QPDF (install with: brew install qpdf)"
}
