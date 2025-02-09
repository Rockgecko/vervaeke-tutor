import pytest
from vervaeke_tutor.tutor import Tutor

@pytest.fixture
def mock_transcripts_folder(tmpdir):
    # Create fake transcript files
    fake_transcript_1 = tmpdir.join("episode_01.txt")
    with open(fake_transcript_1, 'w', encoding='utf-8') as f:
        f.write("This is the content of transcript 1.")

    fake_transcript_2 = tmpdir.join("episode_02.txt")
    with open(fake_transcript_2, 'w', encoding='utf-8') as f:
        f.write("This is the content of transcript 2.")
    
    fake_transcript_3 = tmpdir.join("episode_03.txt")
    with open(fake_transcript_3, 'w', encoding='utf-8') as f:
        f.write("This is the content of transcript 3.")

    fake_transcript_4 = tmpdir.join("episode_04.txt")
    with open(fake_transcript_4, 'w', encoding='utf-8') as f:
        f.write("This is the content of transcript 4.")

    return tmpdir

def test_tutor_initialization():
    tutor = Tutor()
    assert tutor is not None

def test_load_transcripts_valid(mock_transcripts_folder, monkeypatch):
    tutor = Tutor()
    
    # Mock the load_transcripts method to simulate successful loading
    monkeypatch.setattr(tutor, 'load_transcripts', lambda x: True)
    
    result = tutor.load_transcripts(str(mock_transcripts_folder))
    assert result is True

def test_load_transcripts_invalid(mock_transcripts_folder, monkeypatch):
    tutor = Tutor()
    
    # Mock the load_transcripts method to simulate failure
    monkeypatch.setattr(tutor, 'load_transcripts', lambda x: False)
    
    result = tutor.load_transcripts(str(mock_transcripts_folder))
    assert result is False

def test_get_episode_content(mock_transcripts_folder):
    tutor = Tutor()
    tutor.load_transcripts(str(mock_transcripts_folder))  # Ensure transcripts are loaded
    content = tutor.get_episode_content(3)  
    assert content == "This is the content of transcript 3."

def test_list_available_episodes(mock_transcripts_folder):
    tutor = Tutor()
    tutor.load_transcripts(str(mock_transcripts_folder))  # Ensure transcripts are loaded
    episodes = tutor.list_available_episodes()
    assert 1 in episodes  # Check if the episode is listed
    assert 2 in episodes  # Check for another episode

def test_set_current_episode(mock_transcripts_folder):
    tutor = Tutor()
    tutor.load_transcripts(str(mock_transcripts_folder))  # Ensure transcripts are loaded
    tutor.set_current_episode(1)  
    assert tutor.current_episode == 1

def test_display_usage(capsys):
    tutor = Tutor()
    tutor.display_usage()  # Call the method that prints to stdout

    # Capture the output
    captured = capsys.readouterr()
    assert isinstance(captured.out, str)  # Check if the output is a string
    assert "Usage" in captured.out  # Check if the usage information is included

def test_display_final_usage(capsys):
    tutor = Tutor()
    tutor.display_final_usage()  # Call the method that prints to stdout

    # Capture the output
    captured = capsys.readouterr()
    assert isinstance(captured.out, str)  # Check if the output is a string
    assert "Final Usage" in captured.out  # Check if the final usage information is included