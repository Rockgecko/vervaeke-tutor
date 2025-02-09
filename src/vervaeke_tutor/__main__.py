"""Command-line interface for the Vervaeke Tutor."""

from .tutor import Tutor

def main():
    tutor = Tutor()
    
    # Get transcript directory
    while True:
        transcript_dir = input("Enter path to transcript directory: ").strip()
        if tutor.load_transcripts(transcript_dir):
            break
            
    tutor.start_dialogue()

if __name__ == "__main__":
    main()