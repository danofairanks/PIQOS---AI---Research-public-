from verification_lint._code_fences import mask_code_fences


def test_masks_fence_content_preserving_length():
    text = "before\n```python\nx = 1\n```\nafter"
    masked = mask_code_fences(text)
    assert len(masked) == len(text)
    assert "x = 1" not in masked
    assert "before" in masked
    assert "after" in masked


def test_newlines_preserved_inside_fence():
    text = "```\nline1\nline2\n```"
    masked = mask_code_fences(text)
    assert masked.count("\n") == text.count("\n")


def test_no_fence_leaves_text_unchanged():
    text = "Plain prose with no code fence at all."
    assert mask_code_fences(text) == text


def test_multiple_fences_all_masked():
    text = "a ```one``` b ```two``` c"
    masked = mask_code_fences(text)
    assert "one" not in masked
    assert "two" not in masked
    assert masked.startswith("a ")
    assert masked.endswith(" c")


def test_offsets_align_with_original_text():
    text = "prose ```code_block_content``` more prose"
    masked = mask_code_fences(text)
    idx = masked.index("more prose")
    assert text[idx:idx + len("more prose")] == "more prose"
