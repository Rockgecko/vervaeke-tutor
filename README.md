# Vervaeke Tutor

This application creates an AI tutor to help me digest John Vervaeke's "Awakening from the Meaning Crisis" lecture series.

## Project Structure

    ```
    vervaeke_app/
    ├── src/
    │   └── vervaeke_tutor/
    │       ├── __init__.py
    │       ├── __main__.py
    │       └── tutor.py
    ├── pyproject.toml
    └── README.md
    ```

## Setup

    1. Make sure you have `uv` installed. If not, install it:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    2. Create a virtual environment and install dependencies:

    ```bash
    uv venv
    source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
    uv pip install -e .
    ```

    3. Create a `.env` file in the project root and add your Anthropic API key:

    ```bash
    ANTHROPIC_API_KEY=your_api_key_here
    ```

    4. Place your lecture transcripts in a directory (e.g., `transcripts/`) with each lecture as a separate .txt file.

## Transcript Requirements

Create a directory called `transcripts` and place your lecture files there. Files must be named:

    ```
    transcripts/
    ├── episode_01.txt
    ├── episode_02.txt
    └── episode_03.txt
    ...
    ```

Each file should contain the full transcript text for that episode. Episode numbers should be zero-padded (e.g. `episode_05.txt` not `episode_5.txt`).

## Usage

Run the application using the installed command:

    ```bash
    vervaeke-tutor
    ```

Or run it directly with Python:

    ```bash
    python -m vervaeke_tutor
    ```

The tutor will engage you in a dialogue about the concepts from Vervaeke's lectures. Ask questions, and the tutor will help guide you to deeper understanding through thoughtful questions and discussion.
Type 'quit' to exit the application.
