import typer
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from utils import download_video, extract_audio, transcribe_audio

# Configure Typer to show help if no args are passed
app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()

def run_fabric_pattern(text: str, pattern: str) -> Optional[str]:
    """
    Pipes the text to the fabric CLI and returns the output.
    """
    console.print(Panel(f"Running fabric with pattern: [bold]{pattern}[/bold]", border_style="blue"))
    
    try:
        process = subprocess.Popen(
            ["fabric", "--pattern", pattern],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=text)
        
        if process.returncode != 0:
            console.print(f"[bold red]Fabric error:[/bold red] {stderr}")
            return None

        return stdout

    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] 'fabric' command not found. Is it installed and in your PATH?")
        return None
    except Exception as e:
        console.print(f"[bold red]An error occurred running fabric:[/bold red] {e}")
        return None

def copy_to_clipboard(text: str):
    """Copies text to macOS clipboard using pbcopy."""
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
        console.print("[bold green]✓ Output copied to clipboard![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error copying to clipboard:[/bold red] {e}")

def save_to_file(text: str, path: Path):
    """Saves text to a file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        console.print(f"[bold green]✓ Output saved to: {path}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error saving to file:[/bold red] {e}")

@app.command()
def process(
    url: str = typer.Argument(..., help="The URL of the reel/video to process"),
    keep_files: bool = typer.Option(False, "--keep", "-k", help="Keep downloaded video and audio files"),
    model: str = typer.Option("base", "--model", "-m", help="Whisper model size (tiny, base, small, medium, large)"),
    pattern: str = typer.Option("extract_learning_points", "--pattern", "-p", help="Fabric pattern to use"),
    clipboard: bool = typer.Option(False, "--clipboard", "-c", help="Copy the result to the system clipboard"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Save the result to a specific file path")
):
    """
    Download a video, extract audio, transcribe it, and apply a Fabric pattern.
    """
    video_path = None
    audio_path = None
    
    try:
        # 1. Download
        video_path = download_video(url)
        
        # 2. Extract Audio
        audio_path = extract_audio(video_path)
        
        # 3. Transcribe
        text = transcribe_audio(audio_path, model_size=model)
        
        # 4. Pass to Fabric
        result = run_fabric_pattern(text, pattern)
        
        if result:
            # Display Output
            console.print(Panel(Markdown(result), title=f"Fabric Output ({pattern})", border_style="green"))
            
            # Handle Flags
            if clipboard:
                copy_to_clipboard(result)
            
            if output_file:
                save_to_file(result, output_file)

        # Cleanup
        if not keep_files:
            console.print("[dim]Cleaning up temporary files...[/dim]")
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            console.print("[dim]Cleanup done.[/dim]")
        else:
            console.print(f"[dim]Files kept at:\n- {video_path}\n- {audio_path}[/dim]")

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")
        # Attempt cleanup on error
        if not keep_files:
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)

if __name__ == "__main__":
    app()
