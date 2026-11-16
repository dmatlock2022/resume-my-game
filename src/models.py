from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class GameEntry:
    """Represents one game being tracked for a player."""

    game_entry_id: str
    game_title: str
    player_session_context: str
    progress_label: str
    progress_order: int


@dataclass
class SourceRecord:
    """Preserves information exactly as it was originally supplied."""

    source_id: str
    game_entry_id: str
    source_type: str
    original_content: str
    submission_time: str


@dataclass
class ProgressItem:
    """Represents one structured piece of gameplay context."""

    item_id: str
    game_entry_id: str
    category: str
    value: str
    source_id: str
    progress_position: Optional[int]
    spoiler_sensitive: bool


@dataclass
class PlayerNote:
    """Stores a note or intended next action written by the player."""

    note_id: str
    game_entry_id: str
    note_text: str
    source_id: str
    created_at: str


@dataclass
class CandidateContextItem:
    """
    Represents information that may later be used in a briefing.

    This structure is included now because it is part of the design,
    but its AI/review behavior will be implemented later.
    """

    candidate_id: str
    game_entry_id: str
    category: str
    candidate_value: str
    source_references: List[str] = field(default_factory=list)
    support_type: str = "unreviewed"
    status: str = "unreviewed"


@dataclass
class ReviewAction:
    """Records a future player review or correction."""

    review_action_id: str
    related_item_id: str
    action: str
    previous_value: str
    reviewed_value: Optional[str]
    timestamp: str


@dataclass
class ReentryBriefing:
    """
    Represents the final player-facing briefing.

    Briefing generation will be implemented in a later checkpoint.
    """

    briefing_id: str
    game_entry_id: str
    sections: dict
    source_references: List[str] = field(default_factory=list)
    unresolved_conditions: List[str] = field(default_factory=list)
    generation_time: Optional[str] = None