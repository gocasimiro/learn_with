import os
import subprocess
import yt_dlp
import whisper
from rich.console import Console

console = Console()

def download_video(url: str, output_dir: str = "downloads") -> str:
    """
    Downloads a video from a URL using yt-dlp.
    Returns the path to the downloaded video file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Configure yt-dlp to download and save with a specific template
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download best quality
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    console.print(f"[cyan]Downloading video from {url}...[/cyan]")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
    
    console.print(f"[green]Video downloaded to: {filename}[/green]")
    return filename

def extract_audio(video_path: str) -> str:
    """
    Extracts audio from a video file using ffmpeg.
    Returns the path to the extracted audio file.
    """
    base, _ = os.path.splitext(video_path)
    audio_path = f"{base}.mp3"
    
    console.print(f"[cyan]Extracting audio to {audio_path}...[/cyan]")

    # Run ffmpeg command
    # -i: input file
    # -q:a 0: variable bit rate, highest quality
    # -map a: map only audio streams
    # -y: overwrite output file without asking
    command = [
        "ffmpeg",
        "-i", video_path,
        "-q:a", "0", 
        "-map", "a",
        "-y",
        audio_path
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        console.print(f"[green]Audio extracted successfully![/green]")
        return audio_path
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error extracting audio: {e}[/bold red]")
        raise

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """
    Transcribes audio file to text using OpenAI Whisper.
    """
    console.print(f"[cyan]Loading Whisper model ('{model_size}')...[/cyan]")
    model = whisper.load_model(model_size)
    
    console.print(f"[cyan]Transcribing audio...[/cyan]")
    result = model.transcribe(audio_path)
    
    text = result["text"]
    console.print(f"[green]Transcription complete![/green]")
    return text.strip()
