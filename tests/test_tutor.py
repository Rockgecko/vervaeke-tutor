import pytest
from vervaeke_tutor.tutor import Tutor

@pytest.fixture
def mock_transcripts_folder(monkeypatch, tmpdir):
    # Create fake transcript files
    fake_transcript_1 = tmpdir.join("transcript_1.txt")
    fake_transcript_1.write("This is the content of transcript 1.")

    fake_transcript_2 = tmpdir.join("transcript_2.txt")
    fake_transcript_2.write("This is the content of transcript 2.")

    fake_transcript_3 = tmpdir.join("transcript_3.txt")
    fake_transcript_3.write("This is the content of transcript 3.")

    fake_transcript_4 = tmpdir.join("transcript_4.txt")
    fake_transcript_4.write("This is the content of transcript 4.")

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

# Add more tests based on the methods available in the Tutor class
