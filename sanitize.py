import re

# Constants for sanitization
MAX_PROMPT_LENGTH = 4000  # Maximum characters allowed in a prompt
SPAM_PATTERNS = [
    r'\b(?:viagra|cialis|\$\$\$|lottery|winner|nigerian prince|free money)\b',
    r'\b(?:click here|buy now|act now|limited time|special offer)\b',
    r'\b(?:congratulations|you\'ve won|you are selected)\b'
]
PERSONAL_DATA_PATTERNS = [
    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone numbers
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email addresses
    r'\b(?:\d[ -]*?){13,16}\b',  # Credit card numbers
    r'\b\d{9}\b',  # Social security numbers (simplified)
    r'\b(?:password|senha|passe)\s*[:=]\s*\S+\b',  # Passwords
    r'\b(?:api[_-]?key|token|secret|credential)\s*[:=]\s*\S+\b'  # API keys and credentials
]

def sanitize_prompt(text):
    """
    Sanitize user input by removing potentially harmful content.
    
    Args:
        text (str): The input text to sanitize
        
    Returns:
        str: Sanitized text
        dict: Issues found during sanitization
    """
    if not text or not isinstance(text, str):
        return "", {"error": "Input must be a non-empty string"}
    
    issues = {}
    sanitized_text = text
    
    # Check for size limits
    if len(text) > MAX_PROMPT_LENGTH:
        sanitized_text = text[:MAX_PROMPT_LENGTH]
        issues["size_limit"] = f"Prompt truncated to {MAX_PROMPT_LENGTH} characters"
    
    # Check for spam content
    spam_found = False
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            spam_found = True
            sanitized_text = re.sub(pattern, "[filtered]", sanitized_text, flags=re.IGNORECASE)
    
    if spam_found:
        issues["spam"] = "Potentially promotional content was filtered"
    
    # Check for personal data
    personal_data_found = False
    for pattern in PERSONAL_DATA_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            personal_data_found = True
            sanitized_text = re.sub(pattern, "[personal data removed]", sanitized_text, flags=re.IGNORECASE)
    
    if personal_data_found:
        issues["personal_data"] = "Personal information was removed for your protection"
    
    # Remove potentially harmful characters (keeping basic formatting)
    sanitized_text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized_text)  # Control chars
    
    # Normalize whitespace (but preserve newlines for formatting)
    sanitized_text = re.sub(r'[ \t]+', ' ', sanitized_text)
    sanitized_text = re.sub(r'\n{3,}', '\n\n', sanitized_text)  # Limit consecutive newlines
    
    return sanitized_text, issues