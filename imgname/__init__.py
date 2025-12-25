#!/usr/bin/env python3
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import typer
from ollama import chat
from rich.console import Console

app = typer.Typer(
    help="Rename image files based on their content using Ollama vision models"
)
console = Console()


def sanitize_content(content: str) -> str:
    """
    Sanitize and format content description for filename.

    Args:
        content: The content description from the model

    Returns:
        A sanitized content string (lowercase, underscores, max 3 words)
    """
    # Remove any quotes or extra formatting
    content = content.strip("\"'`")
    # Convert to lowercase
    content = content.lower()
    # Replace spaces and special characters with underscores
    content = re.sub(r"[^\w\s-]", "", content)
    content = re.sub(r"[\s-]+", "_", content)
    # Remove leading/trailing underscores
    content = content.strip("_")

    # Limit to 3 words
    words = [w for w in content.split("_") if w]
    if len(words) > 3:
        words = words[:3]

    content = "_".join(words)

    # Ensure we have something
    if not content:
        content = "image"

    return content


def analyze_image(image_path: Path, model: str) -> str:
    """
    Analyze an image using Ollama vision model and get a content description.

    Args:
        image_path: Path to the image file
        model: Name of the Ollama model to use

    Returns:
        A content description for the image (up to 3 words)

    Raises:
        Exception: If the Ollama API call fails
    """
    prompt = (
        "Describe what this image is about in 1-3 words. "
        "Focus on the main subject, action, or theme. "
        "Use simple English words separated by spaces. "
        "Examples: 'sunset beach', 'cat sleeping', 'mountain landscape'. "
        "Only respond with the description, nothing else."
    )

    try:
        response = chat(
            model=model,
            messages=[{"role": "user", "content": prompt, "images": [str(image_path)]}],
        )

        # Extract and sanitize the content description
        content = response.message.content.strip()
        return sanitize_content(content)

    except Exception as e:
        raise Exception(f"Failed to analyze image with Ollama: {str(e)}")


def get_utc_timestamp(file_path: Path) -> str:
    """
    Get the file's modification time as a UTC timestamp string.

    Args:
        file_path: Path to the file

    Returns:
        Timestamp string in format YYYYMMDDHHMMSS
    """
    # Get modification time
    mtime = file_path.stat().st_mtime
    # Convert to UTC datetime
    dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
    # Format as YYYYMMDDHHMMSS
    return dt.strftime("%Y%m%d%H%M%S")


@app.command()
def rename(
    image_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Path to the image file to rename",
    ),
    model: str = typer.Option(
        "gemma3:4b", "--model", "-m", help="Ollama model to use for image analysis"
    ),
    in_place: bool = typer.Option(
        False, "--in-place", help="Rename the file in place instead of creating a copy"
    ),
):
    """
    Rename an image file based on its content using Ollama vision models.

    By default, creates a copy with the new name. Use --in-place to rename instead.
    """
    # Validate image file
    if not image_path.is_file():
        console.print(f"[red]Error:[/red] {image_path} is not a file", style="bold")
        raise typer.Exit(1)

    # Get file extension
    file_ext = image_path.suffix
    if not file_ext:
        console.print("[yellow]Warning:[/yellow] File has no extension")
        file_ext = ".jpg"  # Default to .jpg

    console.print(f"[cyan]Analyzing image:[/cyan] {image_path}")
    console.print(f"[cyan]Using model:[/cyan] {model}")
    console.print(
        f"[cyan]Mode:[/cyan] {'Rename in place' if in_place else 'Copy with new name'}"
    )

    # Get timestamp from file's modification time
    timestamp = get_utc_timestamp(image_path)

    # Analyze the image
    try:
        with console.status(
            "[bold cyan]Analyzing image with Ollama...", spinner="dots"
        ):
            content = analyze_image(image_path, model)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)

    # Construct new filename: YYYYMMDDHHMMSS_<Content>.ext
    new_filename = f"{timestamp}_{content}{file_ext}"
    new_path = image_path.parent / new_filename

    # Check if the new name already exists
    if new_path.exists() and new_path != image_path:
        console.print(f"[yellow]Warning:[/yellow] {new_filename} already exists!")
        # Add a counter to make it unique
        counter = 1
        while new_path.exists():
            new_filename = f"{timestamp}_{content}_{counter}{file_ext}"
            new_path = image_path.parent / new_filename
            counter += 1
        console.print(f"[cyan]Using:[/cyan] {new_filename} instead")

    # Display the result
    console.print(f"\n[green]New filename:[/green] {new_filename}")

    # Perform the operation
    try:
        if in_place:
            # Rename the file in place
            image_path.rename(new_path)
            console.print(
                f"[green]✓ Renamed:[/green] {image_path.name} → {new_filename}",
                style="bold",
            )
        else:
            # Copy the file with the new name
            shutil.copy2(image_path, new_path)
            console.print(
                f"[green]✓ Copied:[/green] {image_path.name} → {new_filename}",
                style="bold",
            )
            console.print(f"[dim]Original file unchanged: {image_path}[/dim]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
