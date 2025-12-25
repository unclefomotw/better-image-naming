# Smart Image Renaming

Automatically rename image files based on their content using AI-powered visual analysis with Ollama.

## Features

- Analyzes images using **local** Ollama vision models to understand content
- Generates descriptive filenames in format: `YYYYMMDDHHMMSS_<Content>.ext`
- Timestamp from file's modification time (UTC)
- Content description limited to 3 words maximum
- Two modes: copy with new name (default) or rename in place
- Supports any image format (JPEG, PNG, etc.)

## Prerequisites

1. **Python 3.8 or higher**
2. **Ollama** - Install from [ollama.com](https://ollama.com)
3. **A vision-capable model** - After installing Ollama, pull a vision model:
   ```bash
   ollama pull gemma3:4b
   ```

## Installation

### Using uv (Recommended)

The easiest way to install is using `uv`, a fast Python package installer and resolver.

1. Install uv if you haven't already:

   See the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/) for your platform.

2. Clone and install the project:
   ```bash
   git clone <repository-url>
   cd imgname
   uv sync
   ```

3. The tool is now ready to use with `uv run`:
   ```bash
   uv run imgname --help
   ```

### Installation as a System Command (Optional)

To install globally and use `imgname` directly from anywhere without `uv run`:

```bash
uv tool install .
```

This installs `imgname` as a global command. After installation, you can use it in any directory:

```bash
imgname path/to/image.jpg
```

To uninstall:
```bash
uv tool uninstall imgname
```

## Usage

### Basic Usage (Copy Mode)

By default, the tool creates a copy of your image with the new name:

```bash
uv run imgname path/to/image.jpg
```

Example:
```bash
$ uv run imgname vacation.jpg

Analyzing image: vacation.jpg
Using model: gemma3:4b
Mode: Copy with new name

New filename: 20231215143022_sunset_beach.jpg
✓ Copied: vacation.jpg → 20231215143022_sunset_beach.jpg
Original file unchanged: vacation.jpg
```

### Rename In Place

Use `--in-place` to rename the original file instead of creating a copy:

```bash
uv run imgname --in-place path/to/image.jpg
```

Example:
```bash
$ uv run imgname --in-place IMG_1234.jpg

Analyzing image: IMG_1234.jpg
Using model: gemma3:4b
Mode: Rename in place

New filename: 20231215143022_mountain_landscape.jpg
✓ Renamed: IMG_1234.jpg → 20231215143022_mountain_landscape.jpg
```

### Using a Different Model

Specify a different Ollama vision model with the `--model` or `-m` flag:

```bash
uv run imgname --model llava:7b image.jpg
```

### All Options

```bash
uv run imgname --help
```

Options:
- `IMAGE_PATH` - Path to the image file (required)
- `--model`, `-m` - Ollama model to use (default: `gemma3:4b`)
- `--in-place` - Rename file in place instead of creating a copy
- `--help` - Show help message

### Rename many images

The command itself renames one image at a time.  But you can use `find` or a loop to rename many images.

Example:

```bash
find ~/Screenshots -name 'Screenshot*.png' -exec imgname {} \;
```

## Filename Format

Generated filenames follow this format:
```
YYYYMMDDHHMMSS_<Content>.<ext>
```

Where:
- `YYYYMMDDHHMMSS` - File's modification time in UTC (e.g., 20231215143022)
- `<Content>` - AI-generated description (1-3 words, lowercase, underscores)
- `<ext>` - Original file extension

Examples:
- `20231215143022_cat_sleeping.jpg`
- `20240103120000_sunset_ocean.png`
- `20231225180000_family_dinner.jpg`

## Supported Models

Any Ollama **vision** model should work.

List your available models:
```bash
ollama list
```

Pull a new model:
```bash
ollama pull <model-name>
```

## Development

### Install Dependencies

```bash
uv sync
```

### Add a New Dependency

```bash
uv add <package-name>
```

### Run the Script Directly

```bash
uv run imgname path/to/image.jpg
```

## Troubleshooting

**Error: "Failed to analyze image with Ollama"**
- Make sure Ollama is running: `ollama serve`
- Verify the model is installed: `ollama list`
- Pull the model if needed: `ollama pull gemma3:4b`

**Error: "Connection refused"**
- Ensure Ollama service is running
- Check if Ollama is listening on the default port (11434)

**Poor naming results**
- Try a larger model like `gemma3:7b` or `llava:13b`
- Some images may be difficult for the model to interpret

## License

MIT
