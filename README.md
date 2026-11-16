# Resume My Game

Resume My Game is an AI-assisted game re-entry system designed to help players return to unfinished video games after an extended break.

The system will use authorized gameplay progress information and player notes to eventually produce a personalized, spoiler-safe re-entry briefing.

## Current Prototype Status

Checkpoint 2 begins implementation of the system foundation.

The current prototype supports:

- A Game Entry representing the player's game and confirmed progress point
- Structured JSON progress input
- Plain text or Markdown player notes
- Input validation
- Structured progress records
- Source references
- Preservation of the original submitted source information

The prototype does not yet generate an AI briefing or perform spoiler-boundary filtering. Those features will be added in later development phases.

## Project Structure

```text
resume-my-game/
├── data/
│   ├── sample_progress.json
│   └── player_notes.md
├── src/
│   ├── __init__.py
│   ├── models.py
│   └── ingestion.py
├── tests/
│   └── test_ingestion.py
├── .gitignore
├── README.md
└── requirements.txt