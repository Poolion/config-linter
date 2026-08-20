# Text Summarizer

Extract key sentences from text using frequency-based ranking and sentence boundary detection. Ideal for creating quick summaries of meeting notes, documentation, or long articles.

## What It Does

- **Sentence splitting**: Handles abbreviations (Dr., Mr., Jr., etc.) correctly without false breaks
- **Key sentence extraction**: Uses word frequency to identify the most important sentences
- **Configurable output**: Set word count limits and sentence count for summaries
- **Simple CLI interface**: Pure Python, no dependencies needed

Perfect for processing long documents into concise overviews in minutes.

## Installation

```bash
# Download and run directly
git clone https://github.com/Poolion/text-summarizer.git
cd text-summarizer
python3 text-summarizer.py document.txt --words 50
```

Or add to PATH:
```bash
cp text-summarizer.py /usr/local/bin/
```

## Usage Examples

### Basic Summary

```bash
python text-summarizer.py article.md --words 100 --top-sentences 3
# Extract first 3 sentences with up to 100 words total
```

### Limit Word Count

```bash
python text-summarizer.py meeting-notes.txt --words 50
# Keep summary under 50 words
```

### Get Top Sentences Only

```bash
echo "Long article content here..." | python text-summarizer.py --top-sentences 5
```

## Features

- Handles common abbreviations (Dr., Jr., etc.) correctly
- Works with stdin or file input
- Configurable word count and sentence count limits
- Pure Python, no external libraries required

If you find this useful, you can support development: https://www.buymeacoffee.com/poolion