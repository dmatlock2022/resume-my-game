import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from uuid import uuid4

from src.models import GameEntry, PlayerNote, ProgressItem, SourceRecord


def validate_progress_data(data: dict) -> None:
    """Check that progress data follows the prototype JSON format."""

    required_fields = ["game_title", "progress_boundary", "context_items"]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(data["game_title"], str):
        raise ValueError("game_title must be text")

    boundary = data["progress_boundary"]

    if not isinstance(boundary, dict):
        raise ValueError("progress_boundary must be an object")

    if "label" not in boundary or "order" not in boundary:
        raise ValueError("progress_boundary must contain label and order")

    if not isinstance(boundary["label"], str):
        raise ValueError("progress boundary label must be text")

    if type(boundary["order"]) is not int:
        raise ValueError("progress boundary order must be an integer")

    context_items = data["context_items"]

    if not isinstance(context_items, list):
        raise ValueError("context_items must be a list")

    required_item_fields = [
        "category",
        "text",
        "progress_order",
        "spoiler_sensitive",
    ]

    for index, item in enumerate(context_items):
        if not isinstance(item, dict):
            raise ValueError(f"context item {index} must be an object")

        for field in required_item_fields:
            if field not in item:
                raise ValueError(
                    f"context item {index} is missing required field: {field}"
                )

        if not isinstance(item["category"], str):
            raise ValueError(f"context item {index} category must be text")

        if not isinstance(item["text"], str):
            raise ValueError(f"context item {index} text must be text")

        if item["progress_order"] is not None:
            if type(item["progress_order"]) is not int:
                raise ValueError(
                    f"context item {index} progress_order must be an integer or null"
                )

        if not isinstance(item["spoiler_sensitive"], bool):
            raise ValueError(
                f"context item {index} spoiler_sensitive must be true or false"
            )


def load_progress_file(
    file_path: str,
    game_entry_id: str = "game-001",
    player_session_context: str = "prototype-player",
) -> Tuple[GameEntry, SourceRecord, List[ProgressItem]]:
    """Load and validate authorized structured progress data."""

    path = Path(file_path)

    if not path.exists():
        raise ValueError(f"Progress file does not exist: {file_path}")

    original_content = path.read_text(encoding="utf-8")

    try:
        data = json.loads(original_content)
    except json.JSONDecodeError as error:
        raise ValueError("Progress file contains invalid JSON") from error

    validate_progress_data(data)

    submission_time = datetime.now().isoformat()

    source_record = SourceRecord(
        source_id=f"source-{uuid4().hex[:8]}",
        game_entry_id=game_entry_id,
        source_type="progress_json",
        original_content=original_content,
        submission_time=submission_time,
    )

    boundary = data["progress_boundary"]

    game_entry = GameEntry(
        game_entry_id=game_entry_id,
        game_title=data["game_title"],
        player_session_context=player_session_context,
        progress_label=boundary["label"],
        progress_order=boundary["order"],
    )

    progress_items = []

    for item in data["context_items"]:
        progress_item = ProgressItem(
            item_id=f"item-{uuid4().hex[:8]}",
            game_entry_id=game_entry_id,
            category=item["category"],
            value=item["text"],
            source_id=source_record.source_id,
            progress_position=item["progress_order"],
            spoiler_sensitive=item["spoiler_sensitive"],
        )

        progress_items.append(progress_item)

    return game_entry, source_record, progress_items


def load_player_note(
    file_path: str,
    game_entry: GameEntry,
) -> Tuple[SourceRecord, PlayerNote]:
    """Load a plain text or Markdown player note."""

    path = Path(file_path)

    if not path.exists():
        raise ValueError(f"Player note does not exist: {file_path}")

    original_content = path.read_text(encoding="utf-8")

    if not original_content.strip():
        raise ValueError("Player note cannot be empty")

    created_at = datetime.now().isoformat()

    source_record = SourceRecord(
        source_id=f"source-{uuid4().hex[:8]}",
        game_entry_id=game_entry.game_entry_id,
        source_type="player_note",
        original_content=original_content,
        submission_time=created_at,
    )

    player_note = PlayerNote(
        note_id=f"note-{uuid4().hex[:8]}",
        game_entry_id=game_entry.game_entry_id,
        note_text=original_content,
        source_id=source_record.source_id,
        created_at=created_at,
    )

    return source_record, player_note


def ingest_game_data(
    progress_file: str,
    note_file: str,
) -> dict:
    """Run the first prototype ingestion flow."""

    game_entry, progress_source, progress_items = load_progress_file(
        progress_file
    )

    note_source, player_note = load_player_note(
        note_file,
        game_entry,
    )

    return {
        "game_entry": game_entry,
        "source_records": [
            progress_source,
            note_source,
        ],
        "progress_items": progress_items,
        "player_note": player_note,
    }