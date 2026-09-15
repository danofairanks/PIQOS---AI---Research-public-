from hedge_dogwhistle.sentences import sentence_containing, split_sentences


def test_split_sentences_basic():
    text = "First sentence here. Second sentence follows. Third one too."
    spans = split_sentences(text)
    assert len(spans) == 3
    assert text[spans[0][0]:spans[0][1]] == "First sentence here."
    assert text[spans[1][0]:spans[1][1]] == "Second sentence follows."
    assert text[spans[2][0]:spans[2][1]] == "Third one too."


def test_split_sentences_single_sentence():
    text = "Just one sentence, no terminal punctuation change"
    spans = split_sentences(text)
    assert len(spans) == 1
    assert spans[0] == (0, len(text))


def test_split_sentences_empty():
    assert split_sentences("") == []


def test_split_sentences_covers_entire_text_no_gaps():
    text = "One. Two. Three."
    spans = split_sentences(text)
    assert spans[0][0] == 0
    assert spans[-1][1] == len(text)
    for i in range(len(spans) - 1):
        assert spans[i][1] < spans[i + 1][0]  # gap is just the whitespace separator


def test_sentence_containing_finds_right_span():
    text = "First sentence. Second sentence. Third sentence."
    spans = split_sentences(text)
    position = text.index("Second")
    start, end = sentence_containing(text, spans, position)
    assert text[start:end] == "Second sentence."
