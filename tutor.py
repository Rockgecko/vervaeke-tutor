import os
from pathlib import Path
import anthropic
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

class SocraticTutor:
    def __init__(self):
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.transcripts = {}
        self.current_episode = None
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        
    def load_transcripts(self, transcript_dir):
        """Load all transcript files from the specified directory."""
        print(transcript_dir)
        try:
            transcript_path = Path(transcript_dir)
            if not transcript_path.exists():
                raise FileNotFoundError(f"Directory not found: {transcript_dir}")
                
            episode_files = list(transcript_path.glob('episode_*.txt'))
            if not episode_files:
                raise ValueError("No episode files found (expected format: episode_nn.txt)")
                
            self.transcripts.clear()
            for file in episode_files:
                try:
                    episode_num = int(re.search(r'episode_(\d+)\.txt', file.name).group(1))
                    with open(file, 'r', encoding='utf-8') as f:
                        self.transcripts[episode_num] = f.read()
                except Exception as e:
                    print(f"Skipping invalid file {file.name}: {str(e)}")
            
            print(f"\nSuccessfully loaded {len(self.transcripts)} episode transcripts")
            return True
            
        except Exception as e:
            print(f"\nError loading transcripts: {str(e)}")
            return False
    
    def get_episode_content(self, episode_num):
        """Get the content of a specific episode."""
        return self.transcripts.get(episode_num, None)
    
    def list_available_episodes(self):
        """List all available episode numbers."""
        episodes = sorted(self.transcripts.keys())
        return episodes
    
    def set_current_episode(self, episode_num):
        """Set the current episode for context."""
        if episode_num in self.transcripts:
            self.current_episode = episode_num
            return True
        return False
                
    def start_dialogue(self):
        """Start a dialogue with the user."""
        print("Welcome to the Vervaeke Tutor!")
        print("I'll help you learn about the ideas from 'Awakening from the Meaning Crisis'")
        print("\nAvailable commands:")
        print("- episode <number>: Switch to a specific episode")
        print("- list: Show available episodes")
        print("- quit: Exit the application")
        
        if not self.transcripts:
            print("\nWarning: No transcripts loaded. Please load transcripts first.")
            return
        
        print(f"\nLoaded episodes: {', '.join(map(str, sorted(self.transcripts.keys())))}")
        
        while True:
            user_input = input("\nYour question: ").strip()
            
            if user_input.lower() == 'quit':
                self.display_final_usage()
                break
            elif user_input.lower() == 'list':
                episodes = self.list_available_episodes()
                print(f"\nAvailable episodes: {', '.join(map(str, episodes))}")
                continue
            elif user_input.lower().startswith('episode '):
                try:
                    episode_num = int(user_input.split()[1])
                    if self.set_current_episode(episode_num):
                        print(f"\nSwitched to episode {episode_num}")
                    else:
                        print(f"\nEpisode {episode_num} not found")
                except (IndexError, ValueError):
                    print("\nInvalid episode number")
                continue
                
            response = self.generate_response(user_input)
            print("\nTutor:", response)
            self.display_usage()
            
    def display_usage(self):
        """Display current token usage statistics."""
        print("\n---Token Usage---")
        print(f"Input tokens: {self.total_input_tokens:,}")
        print(f"Output tokens: {self.total_output_tokens:,}")
        print(f"Total tokens: {self.total_input_tokens + self.total_output_tokens:,}")
        print("---------------")
        
    def display_final_usage(self):
        """Display final token usage statistics and estimated cost."""
        print("\n===== Final Usage Statistics =====")
        print(f"Total input tokens: {self.total_input_tokens:,}")
        print(f"Total output tokens: {self.total_output_tokens:,}")
        print(f"Total tokens: {self.total_input_tokens + self.total_output_tokens:,}")
        # Claude 3.5 Sonnet pricing (as of 2024)
        input_cost = (self.total_input_tokens / 1000) * 0.003
        output_cost = (self.total_output_tokens / 1000) * 0.015
        total_cost = input_cost + output_cost
        print(f"Estimated cost: ${total_cost:.3f}")
        print("================================")
            
    def generate_response(self, user_input):
        """Generate a tutoring response using Claude."""
        # Update system prompt for direct tutoring style
        system_prompt = """You are a knowledgeable tutor helping someone learn about John Vervaeke's 'Awakening from the Meaning Crisis' lectures. 
        Provide clear explanations, answer questions directly, and help clarify concepts as needed. 
        If asked, test the user on their understanding of the material."""
        
        # Add current episode context if available
        if self.current_episode is not None:
            transcript = self.get_episode_content(self.current_episode)
            if transcript:
                system_prompt += f"\n\nCurrent context - Episode {self.current_episode}:\n{transcript}\n\n"
                system_prompt += "\nUse the above episode content to inform your responses while providing clear explanations."
        else:
            system_prompt += "\n\nNo specific episode selected. You can switch to a specific episode using 'episode <number>' command."
        
        messages = [
            {
                "role": "user",
                "content": user_input
            }
        ]
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=messages,
                system=system_prompt,
                temperature=0.7
            )
            
            # Update token counts
            self.total_input_tokens += response.usage.input_tokens
            self.total_output_tokens += response.usage.output_tokens
            
            return response.content[0].text
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
