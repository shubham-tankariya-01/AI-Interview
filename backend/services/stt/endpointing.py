import re

# Sets of lexical markers for determining grammatical completeness
INCOMPLETE_MARKERS = {
    # Conjunctions
    "and", "but", "or", "so", "because", "since", "unless", "although", 
    "though", "whereas", "while", "if", "then", "than",
    # Prepositions (common at end of incomplete thought)
    "with", "to", "for", "from", "in", "on", "at", "by", "about", "as", 
    "into", "like", "through", "after", "over", "between", "out", "against",
    # Articles / Determiners
    "the", "a", "an", "this", "that", "these", "those", "my", "your", "his", 
    "her", "our", "their", "its", "some", "any", "no", "every",
    # Verbs indicating continuation
    "is", "are", "am", "was", "were", "be", "been", "being", "have", "has", 
    "had", "do", "does", "did", "can", "could", "shall", "should", "will", 
    "would", "may", "might", "must"
}

FILLER_WORDS = {
    "um", "uh", "like", "so", "actually", "basically", "literally", 
    "well", "mean", "guess"
}

# Regex to detect if an utterance looks like a direct, short prompt
QUESTION_STARTERS = re.compile(
    r"^(what|how|why|when|where|who|can you|could you|will you|would you|do you|does|is it|are you|tell me|give me|write|explain)\b",
    re.IGNORECASE
)

def determine_pause_threshold(text: str) -> int:
    """
    Analyzes the transcribed text to grammatically deduce the required pause
    before confirming the utterance is finished.
    Returns the threshold in milliseconds.
    """
    if not text:
        return 1350

    # Clean text to examine words
    clean_text = re.sub(r'[^\w\s]', '', text.lower().strip())
    words = clean_text.split()
    
    if not words:
        return 1350

    last_word = words[-1]
    
    # 1. Definite Incomplete (dangling modifiers)
    if last_word in INCOMPLETE_MARKERS:
        return 2350  # Very long pause needed, user is definitely mid-thought
        
    # 2. Filler Words (actively thinking)
    if last_word in FILLER_WORDS:
        return 2050  # User is searching for words
        
    # 3. Direct Prompt / Question (Short and punchy)
    # If it's a short question (under 15 words) and doesn't end in a weird way, snap fast.
    if len(words) < 15 and QUESTION_STARTERS.match(clean_text):
        return 750   # Super snappy response for short queries
        
    # 4. Standard conversational pause
    # If it's a short generic statement, snap reasonably fast
    if len(words) < 8:
        return 1050
        
    # 5. Long paragraph neutral pause
    return 1450
