from pathlib import Path

from src.ingestion import ingest_game_data


def main():
    project_root = Path(__file__).resolve().parents[1]

    progress_file = project_root / "data" / "sample_progress.json"
    note_file = project_root / "data" / "player_notes.md"

    result = ingest_game_data(progress_file, note_file)

    game = result["game_entry"]

    print("\nResume My Game - Checkpoint 2 Prototype")
    print("---------------------------------------")
    print(f"Game: {game.game_title}")
    print(f"Confirmed Progress: {game.progress_label}")
    print()

    print("Stored Progress Items:")
    for item in result["progress_items"]:
        print(f"- [{item.category}] {item.value}")

    print("\nPlayer Note:")
    print(result["player_note"].note_text)

    print(f"\nSource Records Preserved: {len(result['source_records'])}")


if __name__ == "__main__":
    main()