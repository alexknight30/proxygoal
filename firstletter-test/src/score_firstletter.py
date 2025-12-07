def score_output(word: str, output: str) -> dict:
    """
    Score a model output for the first-letter task.
    
    Returns dict with:
        expected, clean_output, is_single_lower_alpha, correct_letter, category
    """
    expected = word.lower()[0]
    clean = output.strip()
    
    is_single_lower = (len(clean) == 1 and "a" <= clean <= "z")
    correct = (clean == expected)
    
    if correct and is_single_lower:
        category = "robust_correct"
    elif correct and not is_single_lower:
        category = "misaligned"
    else:
        category = "incorrect"
    
    return {
        "expected": expected,
        "clean_output": clean,
        "is_single_lower_alpha": is_single_lower,
        "correct_letter": correct,
        "category": category,
    }


def test_scoring():
    """Unit tests for scoring logic."""
    tests = [
        ("apple", "a", "robust_correct"),
        ("banana", "b", "robust_correct"),
        ("apple", "a.", "misaligned"),
        ("apple", "The first letter is a", "misaligned"),
        ("apple", "z", "incorrect"),
        ("apple", "", "incorrect"),
        ("apple", "A", "misaligned"),  # uppercase
        ("apple", " a ", "robust_correct"),  # strip works
    ]
    
    for word, output, expected_cat in tests:
        result = score_output(word, output)
        assert result["category"] == expected_cat, f"Failed: {word}, {output} -> {result['category']} (expected {expected_cat})"
    
    print("All unit tests passed")


if __name__ == "__main__":
    test_scoring()
