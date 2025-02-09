"""Command-line interface for the Vervaeke Tutor."""

import typer
from vervaeke_tutor.tutor import Tutor

app = typer.Typer()

@app.command()
def main(transcripts_dir: str = 'transcripts'):
    tutor = Tutor()
    
    if not tutor.load_transcripts(transcripts_dir):
        while True:
            transcript_dir = input("Enter path to transcript directory:").strip()
            if tutor.load_transcripts(transcript_dir):
                break

if __name__ == "__main__":
    app()