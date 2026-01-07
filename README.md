# learn_with

A powerful command-line tool that extracts wisdom from short-form video content (Instagram Reels, TikToks, YouTube Shorts). It downloads the video, extracts the audio, transcribes it locally using OpenAI's Whisper, and then processes the text through a specialized LLM agent (via Fabric) to generate structured learning notes.

## 🚀 Features

*   **Video Download**: Automatically handles video downloading via `yt-dlp`.
*   **Audio Extraction**: Converts video to high-quality audio using `ffmpeg`.
*   **Local Transcription**: Uses OpenAI's Whisper model (runs 100% locally, privacy-focused).
*   **AI Analysis**: Integrates with [Fabric](https://github.com/danielmiessler/fabric) to extract actionable insights, tips, and mental models using a custom specialized pattern.
*   **Clipboard Support**: Optionally copy the final output directly to your clipboard (`-c`).
*   **File Output**: Save the results to a Markdown file automatically (`-o`).

## 🛠️ Prerequisites

*   **Python 3.10+**
*   **ffmpeg**: Required for audio processing (`brew install ffmpeg` on macOS).
*   **Fabric**: The AI augmentation tool must be installed and configured.
    *   [Install Fabric](https://github.com/danielmiessler/fabric)
*   **pbcopy** (macOS) or equivalent for clipboard support.

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    mkdir -p ~/development/tools
    git clone https://github.com/gocasimiro/learn_with.git {YOUR_TOOLING_LOCATION}
    ```

2.  **Set up the Virtual Environment**:
    ```bash
    cd ~/development/tools/reel_to_text_cli
    python3 -m venv venv
    source venv/bin/activate
    pip install yt-dlp typer rich openai-whisper
    ```

3.  **Install the Custom Pattern (Crucial Step)**:
    This tool uses a custom Fabric pattern designed to extract learning points from videos. The pattern file is included in this repository. You need to copy it to your Fabric configuration folder so Fabric can "see" it.

    ```bash
    # Create the pattern directory in Fabric
    mkdir -p ~/.config/fabric/patterns/extract_learning_points
    
    # Copy the system.md file from this repo to Fabric's folder
    cp patterns/extract_learning_points/system.md ~/.config/fabric/patterns/extract_learning_points/system.md
    ```

4.  **Create the Global Alias (Optional)**:
    To run the tool from anywhere using the command `learn_with`, create a wrapper script:

    ```bash
    # Create the script in your local bin
    echo '#!/bin/bash
    PROJECT_DIR="${YOUR_TOOLING_DIRECTORY}/learn_with"
    "$PROJECT_DIR/venv/bin/python3" "$PROJECT_DIR/main.py" "$@"' > ~/.local/bin/learn_with
    
    # Make it executable
    chmod +x ~/.local/bin/learn_with
    ```
    *(Ensure `~/.local/bin` is in your `$PATH`)*

## 📖 Usage

Run the tool from anywhere in your terminal:

```bash
learn_with [OPTIONS] URL
```

### Examples

**Basic Usage (Process and Print to Screen):**
```bash
learn_with "https://www.instagram.com/reel/example_id/"
```

**Copy to Clipboard (`-c`):**
Perfect for pasting directly into Notion or Obsidian.
```bash
learn_with "https://www.instagram.com/reel/example_id/" -c
```

**Save to a File (`-o`):**
```bash
learn_with "https://www.instagram.com/reel/example_id/" -o notes.md
```

**Use a Different Whisper Model (`-m`):**
Options: `tiny`, `base`, `small`, `medium`, `large`. (Default is `base`)
```bash
learn_with "https://www.instagram.com/reel/example_id/" -m medium
```

## ⚙️ Configuration

The tool defaults to using the `extract_learning_points` Fabric pattern. You can override this with the `--pattern` flag if you want to use other patterns like `summarize` or `extract_wisdom`.

```bash
learn_with "URL" --pattern summarize
```

## 📂 Project Structure

```
reel_to_text_cli/
├── main.py          # Entry point and CLI logic (Typer)
├── utils.py         # Helper functions (Download, Transcribe)
├── patterns/        # Contains the custom Fabric patterns
│   └── extract_learning_points/
│       └── system.md
├── venv/            # Python Virtual Environment
└── README.md        # Documentation
```

## 🤝 Contributing

Feel free to open issues or submit PRs to improve the extraction prompts or add support for other LLM providers.