## Goal

Use a visual AI model served by Ollama to analyze an image, and rename it based on the content.

## Command

This is a command line tool, with input:
- The image file to be renamed.
- Optional model name to be used.  Default to `gemma3:4b`.
- Flag to indicate whether to rename in place.  Default to `false`.

## Expected Impact

1. When the user runs the command, it should copy the image file to the same directory, and rename it the content.
    - The file name should be in the format of `YYYYMMDDHHMMSS_<Content>.jpg`, where `YYYYMMDDHHMMSS` is the file's modified time in UTC, and `<Content>` is the content of the image.
    - The content is what the image is about, what it represents, or what it is, or its intent.
    - The content used in the file name should be English words, up to 3 words.
2. When the user runs the command with `--in-place`, it should rename the image file in place rather than copying it.

## Installation

The users can install this to use this command line tool.

The installation procedure need to be simple and easy using `uv`, and explained in the @README.md.