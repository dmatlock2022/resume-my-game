import json
from pathlib import Path

import pytest

from src.ingestion import ingest_game_data, load_progress_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_valid_sample_data_loads():
    progress_file = PROJECT_ROOT / "data" / "sample_progress.json"
    note_file = PROJECT_ROOT / "data" / "player_notes.md"

    result = ingest_game_data(progress_file, note_file)

    game_entry = result["game_entry"]

    assert game_entry.game_title == "Example Game"
    assert game_entry.progress_label == "Chapter 4"
    assert game_entry.progress_order == 4

    assert len(result["progress_items"]) == 3
    assert len(result["source_records"]) == 2


def test_original_source_content_is_preserved():
    progress_file = PROJECT_ROOT / "data" / "sample_progress.json"
    note_file = PROJECT_ROOT / "data" / "player_notes.md"

    original_progress = progress_file.read_text(encoding="utf-8")
    original_note = note_file.read_text(encoding="utf-8")

    result = ingest_game_data(progress_file, note_file)

    progress_source = result["source_records"][0]
    note_source = result["source_records"][1]

    assert progress_source.original_content == original_progress
    assert note_source.original_content == original_note
    assert result["player_note"].note_text == original_note


def test_missing_required_field_is_rejected(tmp_path):
    bad_data = {
        "game_title": "Broken Example",
        "progress_boundary": {
            "label": "Chapter 2",
            "order": 2
        }
    }

    bad_file = tmp_path / "bad_progress.json"

    bad_file.write_text(
        json.dumps(bad_data),
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="context_items"):
        load_progress_file(bad_file)