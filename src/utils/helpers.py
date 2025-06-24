def extract_text_snippets(text: str, query: str, context_length: int = 100) -> list:
    """Extract text snippets around query matches for highlighting"""
    import re
    
    # Find all matches of the query (case insensitive)
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    matches = list(pattern.finditer(text))
    
    snippets = []
    for match in matches:
        start = max(0, match.start() - context_length)
        end = min(len(text), match.end() + context_length)
        snippet = text[start:end]
        
        # Highlight the match
        highlighted = snippet[:match.start()-start] + \
                     f"**{snippet[match.start()-start:match.end()-start]}**" + \
                     snippet[match.end()-start:]
        
        snippets.append({
            "text": highlighted,
            "position": match.start()
        })
    
    return snippets

def validate_file_size(file_size: int, max_size_mb: int = 10) -> bool:
    """Validate file size"""
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    import re
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
    
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        
        if end >= len(text):
            break
    
    return chunks
