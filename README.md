# learn_with 🧠

A CLI tool to extract actionable insights from Reels, TikToks, and YouTube Shorts. It automates the process of downloading, transcribing locally (Whisper), and analyzing content using AI (Fabric).

## 🚀 Features

*   **Local Transcription**: Uses OpenAI's Whisper model (runs 100% on your CPU/GPU).
*   **AI Intelligence**: Integrates with [Fabric](https://github.com/danielmiessler/fabric) for high-quality analysis.
*   **Workflow Ready**: Support for system clipboard (`-c`) and file output (`-o`).
*   **Clean**: Automatic cleanup of temporary video and audio files.

## 🛠️ Prerequisites

*   **Python 3.10+**
*   **ffmpeg**: `brew install ffmpeg`
*   **Fabric**: [Installation Guide](https://github.com/danielmiessler/fabric)
*   **pbcopy**: Standard on macOS (used for the `-c` flag).

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/gocasimiro/learn_with.git
    cd learn_with
    ```

2.  **Setup Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Install the Custom Pattern**:
    The tool requires the `extract_learning_points` pattern to be available in Fabric.
    ```bash
    mkdir -p ~/.config/fabric/patterns/extract_learning_points
    cp patterns/extract_learning_points/system.md ~/.config/fabric/patterns/extract_learning_points/system.md
    ```

4.  **Create a Global Alias**:
    To use the `learn_with` command from any directory:
    ```bash
    # Replace [PATH_TO_REPO] with the actual path where you cloned this
    echo '#!/bin/bash
    REPO_DIR="'"$(pwd)"'"
    "$REPO_DIR/venv/bin/python3" "$REPO_DIR/main.py" "$@"' > ~/.local/bin/learn_with
    
    chmod +x ~/.local/bin/learn_with
    ```

## 📖 Usage

```bash
# Show help
learn_with

# Process a Reel
learn_with "URL"

# Process and copy result to clipboard
learn_with "URL" -c

# Save result to a markdown file
learn_with "URL" -o my_notes.md
```

## ⚙️ Options

*   `-c, --clipboard`: Copy the AI output to your clipboard.
*   `-o, --output PATH`: Save the output to a specific file.
*   `-k, --keep`: Do not delete the downloaded video/audio files.
*   `-m, --model [tiny|base|small|medium|large]`: Choose Whisper model size (default: base).
*   `-p, --pattern NAME`: Use a different Fabric pattern.

## 📂 Structure

*   `main.py`: CLI logic.
*   `utils.py`: Download and transcription helpers.
*   `patterns/`: Custom prompt templates for Fabric.
