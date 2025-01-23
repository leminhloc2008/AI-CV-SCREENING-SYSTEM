def check_bias(text: str) -> bool:
    """
    Check for bias in the text (e.g., gender, ethnicity).
    """
    bias_keywords = ["male", "female", "asian", "black", "white"]
    return any(keyword in text.lower() for keyword in bias_keywords)