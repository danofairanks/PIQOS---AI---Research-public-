from basin_depth.vocabulary import (
    VocabPool, coefficient_of_variation, jaccard, validate_against_seed,
    default_ai_discourse_pools, CLAIM_SEED, IMMUNE_SEED, NEUTRAL_SEED,
)


def test_default_pools_match_protocol_seed_lists():
    pools = default_ai_discourse_pools()
    assert pools["claim"].terms == CLAIM_SEED
    assert pools["immune"].terms == IMMUNE_SEED
    assert pools["neutral"].terms == NEUTRAL_SEED


def test_coefficient_of_variation_constant_series_is_zero():
    assert coefficient_of_variation([0.5, 0.5, 0.5, 0.5]) == 0.0


def test_coefficient_of_variation_zero_series_is_zero():
    assert coefficient_of_variation([0.0, 0.0, 0.0]) == 0.0


def test_coefficient_of_variation_high_variance_is_high():
    # a term that appears heavily in one quarter and not at all in others
    # should register as high-CV, matching a claim-vocabulary profile
    cv = coefficient_of_variation([0.0, 0.0, 1.0, 0.0])
    assert cv > 1.5


def test_vocab_pool_count_in_phrase_and_word():
    pool = VocabPool("test", {"alignment", "large language model"})
    text = "We discuss alignment and the large language model paradigm; alignment matters."
    assert pool.count_in(text) == 3  # 2x "alignment" + 1x "large language model"
    assert pool.contains(text) is True
    assert pool.contains("nothing relevant here") is False


def test_vocab_pool_single_word_does_not_match_inside_other_words():
    pool = VocabPool("test", {"safety"})
    assert pool.count_in("unsafety is not safety") == 1  # only the standalone token counts


def test_jaccard_matches_reference():
    assert jaccard({"a", "b"}, {"a", "b", "c"}) == 2 / 3


def test_validate_against_seed_pass_and_fail():
    seed = {"a", "b", "c", "d"}
    good = validate_against_seed({"a", "b", "c"}, seed, min_overlap=0.5)
    assert good.passed
    bad = validate_against_seed({"x", "y"}, seed, min_overlap=0.5)
    assert not bad.passed
    assert bad.missing_from_derived == seed  # none of the seed terms were recovered
