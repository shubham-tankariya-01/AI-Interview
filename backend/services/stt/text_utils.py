import re

def _is_hallucination(text: str) -> bool:
    """Check if the text is a known Whisper hallucination."""
    lower_text = text.lower().strip(".,!? ")
    hallucinations = {
        "thank you", "it's perfect", "bye", "you", "yes", "yeah",
        "i don't know", "i'm sorry", "am i", "is it", "it is"
    }
    return lower_text in hallucinations or len(lower_text) < 2

def _merge_text(confirmed: str, tail: str) -> str:
    """Combine confirmed prefix with tail transcript, deduplicating overlap."""
    if not confirmed:
        return tail.strip()
    if not tail:
        return confirmed.strip()

    prefix_words = confirmed.strip().split()
    tail_words = tail.strip().split()
    if not prefix_words or not tail_words:
        return f"{confirmed} {tail}".strip()

    best_overlap = 0
    for n in range(1, min(6, len(prefix_words), len(tail_words)) + 1):
        if ([w.lower().strip(".,!?") for w in prefix_words[-n:]]
                == [w.lower().strip(".,!?") for w in tail_words[:n]]):
            best_overlap = n

    if best_overlap > 0:
        return f"{confirmed.strip()} {' '.join(tail_words[best_overlap:])}".strip()
    return f"{confirmed.strip()} {tail.strip()}".strip()
