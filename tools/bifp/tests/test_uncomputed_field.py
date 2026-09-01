from bifp.uncomputed_field import (
    AssignmentSite,
    FieldTrace,
    FieldTraceResult,
    trace_field_assignments,
)


# --- literal-only detection, via trace_field_assignments -------------------

def test_flags_field_assigned_only_a_literal():
    src = "class Fabric:\n    def compute(self):\n        self.topology_shift_score = 0.83\n"
    result = trace_field_assignments({"fabric.py": src}, ["topology_shift_score"])
    assert result.flagged_field_names == ["topology_shift_score"]
    trace = result.traces[0]
    assert trace.status == "never_proven_input_derived"
    assert trace.site_count == 1
    assert trace.literal_only_count == 1


def test_does_not_flag_field_assigned_from_a_computation():
    src = (
        "class Fabric:\n"
        "    def compute(self, state):\n"
        "        self.topology_shift_score = compute_shift(state.vector)\n"
    )
    result = trace_field_assignments({"fabric.py": src}, ["topology_shift_score"])
    assert result.flagged_field_names == []
    trace = result.traces[0]
    assert trace.status == "input_derived_or_unknown"
    assert trace.not_proven_literal_count == 1


def test_does_not_flag_field_assigned_from_a_name_reference():
    src = "def build(x):\n    score = x\n    return score\n"
    result = trace_field_assignments({"m.py": src}, ["score"])
    assert result.flagged_field_names == []
    assert result.traces[0].status == "input_derived_or_unknown"


def test_no_assignment_found_is_distinct_from_flagged():
    src = "x = 1\n"
    result = trace_field_assignments({"m.py": src}, ["never_appears_here"])
    trace = result.traces[0]
    assert trace.status == "no_assignment_found"
    assert trace.field_name not in result.flagged_field_names


def test_one_non_literal_site_prevents_flag_even_with_other_literal_sites():
    """A field assigned a literal in one branch and a computed value in
    another must not be flagged -- any not-proven-literal site rules it
    out, per the module's conservative-bias design."""
    src = (
        "def f(cond, x):\n"
        "    if cond:\n"
        "        score = 0.0\n"
        "    else:\n"
        "        score = x\n"
    )
    result = trace_field_assignments({"m.py": src}, ["score"])
    trace = result.traces[0]
    assert trace.site_count == 2
    assert trace.literal_only_count == 1
    assert trace.not_proven_literal_count == 1
    assert trace.status == "input_derived_or_unknown"
    assert result.flagged_field_names == []


# --- literal-only expression forms ------------------------------------------

def test_literal_only_container_forms_are_flagged():
    src = (
        "class C:\n"
        "    def __init__(self):\n"
        "        self.envelope = (1, -2.5, True, None)\n"
        "        self.mapping = {\"a\": 1, \"b\": [1, 2, 3]}\n"
    )
    result = trace_field_assignments({"m.py": src}, ["envelope", "mapping"])
    assert set(result.flagged_field_names) == {"envelope", "mapping"}


def test_binop_of_literals_is_flagged():
    src = "class C:\n    def __init__(self):\n        self.margin = 1.0 - 0.17\n"
    result = trace_field_assignments({"m.py": src}, ["margin"])
    assert result.flagged_field_names == ["margin"]


def test_binop_with_a_name_is_not_flagged():
    src = "def f(delta):\n    margin = 1.0 - delta\n"
    result = trace_field_assignments({"m.py": src}, ["margin"])
    assert result.flagged_field_names == []


def test_dataclass_field_default_literal_is_flagged():
    src = (
        "from dataclasses import dataclass, field\n\n"
        "@dataclass\n"
        "class State:\n"
        "    recoverability_margin: float = field(default=0.83)\n"
    )
    result = trace_field_assignments({"m.py": src}, ["recoverability_margin"])
    assert result.flagged_field_names == ["recoverability_margin"]


def test_dataclass_field_default_factory_lambda_literal_is_flagged():
    src = (
        "from dataclasses import dataclass, field\n\n"
        "@dataclass\n"
        "class State:\n"
        "    tags: list = field(default_factory=lambda: [])\n"
    )
    result = trace_field_assignments({"m.py": src}, ["tags"])
    assert result.flagged_field_names == ["tags"]


def test_dataclass_field_default_factory_non_lambda_is_not_flagged():
    """A default_factory referencing a callable (e.g. list, or a named
    function) is not provably literal without tracing that callable --
    conservative default, not flagged."""
    src = (
        "from dataclasses import dataclass, field\n\n"
        "@dataclass\n"
        "class State:\n"
        "    tags: list = field(default_factory=list)\n"
    )
    result = trace_field_assignments({"m.py": src}, ["tags"])
    assert result.flagged_field_names == []


def test_ordinary_call_is_not_flagged():
    src = "class C:\n    def __init__(self):\n        self.value = compute_default()\n"
    result = trace_field_assignments({"m.py": src}, ["value"])
    assert result.flagged_field_names == []


# --- augmented assignment ---------------------------------------------------

def test_augmented_assignment_is_never_flagged_even_with_literal_rhs():
    """`x += 1` depends on the prior value of x, which this module does
    not trace across statements -- must never be treated as literal-only
    regardless of the increment's own shape."""
    src = "class C:\n    def step(self):\n        self.counter += 1\n"
    result = trace_field_assignments({"m.py": src}, ["counter"])
    trace = result.traces[0]
    assert trace.site_count == 1
    assert trace.not_proven_literal_count == 1
    assert result.flagged_field_names == []


# --- keyword-argument sites (constructor call keyword args) ----------------
# The pattern found in the specimen that motivated this module: a
# dataclass field declared only as a type annotation, with every actual
# value supplied via constructor keyword arguments at each call site,
# never through a `self.x = ...` statement or a `field(default=...)`.

def test_keyword_argument_literal_value_is_flagged():
    src = (
        "class StateVector:\n"
        "    topology_shift_score: float\n"
        "    recoverability_margin: float\n\n"
        "def fixture_a():\n"
        "    return StateVector(topology_shift_score=0.82, recoverability_margin=0.16)\n"
    )
    result = trace_field_assignments({"m.py": src}, ["topology_shift_score", "recoverability_margin"])
    assert set(result.flagged_field_names) == {"topology_shift_score", "recoverability_margin"}
    for trace in result.traces:
        assert trace.sites[0].site_shape == "keyword_argument"


def test_keyword_argument_non_literal_value_is_not_flagged():
    src = (
        "def build(x):\n"
        "    return StateVector(topology_shift_score=x, recoverability_margin=0.16)\n"
    )
    result = trace_field_assignments({"m.py": src}, ["topology_shift_score", "recoverability_margin"])
    assert result.flagged_field_names == ["recoverability_margin"]


def test_keyword_argument_across_multiple_call_sites_all_literal_is_flagged():
    src = (
        "def a():\n    return S(score=0.12)\n\n"
        "def b():\n    return S(score=0.54)\n"
    )
    result = trace_field_assignments({"m.py": src}, ["score"])
    trace = result.traces[0]
    assert trace.site_count == 2
    assert result.flagged_field_names == ["score"]


def test_keyword_argument_mixed_with_non_literal_call_site_is_not_flagged():
    src = (
        "def a():\n    return S(score=0.12)\n\n"
        "def b(x):\n    return S(score=x)\n"
    )
    result = trace_field_assignments({"m.py": src}, ["score"])
    trace = result.traces[0]
    assert trace.site_count == 2
    assert result.flagged_field_names == []


def test_double_star_kwargs_expansion_is_not_treated_as_a_named_site():
    src = "def a(extra):\n    return S(**extra)\n"
    result = trace_field_assignments({"m.py": src}, ["score"])
    assert result.traces[0].status == "no_assignment_found"


def test_field_default_call_keyword_default_is_not_itself_traced_as_a_site():
    """`field(default=...)`'s own `default` keyword must not be
    mistaken for a site of a field literally named "default" -- only
    relevant if the caller happens to be tracing that name, included
    here to pin the (correct, narrow) behavior explicitly."""
    src = (
        "from dataclasses import dataclass, field\n\n"
        "@dataclass\nclass C:\n    score: float = field(default=0.5)\n"
    )
    result = trace_field_assignments({"m.py": src}, ["score"])
    assert result.flagged_field_names == ["score"]
    # exactly one site: the AnnAssign, not a duplicate from the nested Call
    assert result.traces[0].site_count == 1


def test_real_world_shape_end_to_end_matches_manual_finding():
    """Mirrors the exact structural pattern this module was built to
    automate (see uncomputed_field.py module docstring): a dataclass
    with fields declared only as annotations, values supplied only via
    constructor keyword arguments at several fixture call sites, and a
    downstream comparison reading the field off an instance -- never a
    computation. Must be flagged."""
    src = (
        "from dataclasses import dataclass\n\n"
        "@dataclass\n"
        "class StateVector:\n"
        "    topology_shift_score: float\n"
        "    recoverability_margin: float\n\n"
        "def evaluate(state):\n"
        "    if state.topology_shift_score >= 0.75 or state.recoverability_margin <= 0.0:\n"
        "        return 'FAIL'\n"
        "    return 'HOLDS'\n\n"
        "def fixture_a():\n"
        "    return StateVector(recoverability_margin=0.82, topology_shift_score=0.12)\n\n"
        "def fixture_b():\n"
        "    return StateVector(recoverability_margin=0.19, topology_shift_score=0.81)\n"
    )
    result = trace_field_assignments({"fabric.py": src}, ["topology_shift_score", "recoverability_margin"])
    assert set(result.flagged_field_names) == {"topology_shift_score", "recoverability_margin"}


# --- multi-file, target shapes, parse errors --------------------------------

def test_traces_across_multiple_files():
    sources = {
        "a.py": "class C:\n    def __init__(self):\n        self.score = 1.0\n",
        "b.py": "class C:\n    def recompute(self, x):\n        self.score = x\n",
    }
    result = trace_field_assignments(sources, ["score"])
    trace = result.traces[0]
    assert trace.site_count == 2
    assert {s.file_label for s in trace.sites} == {"a.py", "b.py"}
    assert result.flagged_field_names == []  # b.py's site rules it out


def test_tuple_unpacking_all_literal_rhs_is_flagged_for_both_targets():
    src = "def f():\n    a, b = 1, 2\n"
    result = trace_field_assignments({"m.py": src}, ["a", "b"])
    assert set(result.flagged_field_names) == {"a", "b"}


def test_tuple_unpacking_checks_whole_rhs_not_per_element():
    """Each name bound by a tuple-unpacking target is classified
    against the *entire* right-hand side expression, not matched
    element-by-element against it -- a conservative simplification: if
    any part of the unpacked RHS is not provably literal, no name it
    unpacks into is flagged, even a name whose own positional element
    looks literal. Precise per-element matching is a plausible future
    refinement, not built out here."""
    src = "def f():\n    a, b = 1, compute()\n"
    result = trace_field_assignments({"m.py": src}, ["a", "b"])
    by_name = {t.field_name: t for t in result.traces}
    assert by_name["a"].status == "input_derived_or_unknown"
    assert by_name["b"].status == "input_derived_or_unknown"
    assert result.flagged_field_names == []


def test_annotated_assignment_without_value_is_not_a_site():
    """`x: int` with no `= ...` is a bare annotation, not an assignment
    -- must not be counted as a literal-only site."""
    src = "class C:\n    score: float\n"
    result = trace_field_assignments({"m.py": src}, ["score"])
    assert result.traces[0].status == "no_assignment_found"


def test_syntax_error_recorded_not_raised():
    result = trace_field_assignments({"broken.py": "def f(:\n"}, ["x"])
    assert len(result.parse_errors) == 1
    assert result.parse_errors[0]["file_label"] == "broken.py"
    # the field trace is still returned, just with no sites found
    assert result.traces[0].status == "no_assignment_found"


def test_unrelated_field_names_are_untouched():
    src = "class C:\n    def __init__(self):\n        self.other = 1\n"
    result = trace_field_assignments({"m.py": src}, ["score"])
    assert result.traces[0].status == "no_assignment_found"


# --- to_dict round trips / shapes ------------------------------------------

def test_field_trace_result_to_dict_shape():
    src = "class C:\n    def __init__(self):\n        self.score = 1\n"
    result = trace_field_assignments({"m.py": src}, ["score"])
    d = result.to_dict()
    assert d["flagged_field_names"] == ["score"]
    assert d["parse_errors"] == []
    assert "note" in d
    assert d["traces"][0]["field_name"] == "score"
    assert d["traces"][0]["sites"][0]["site_kind"] == "literal_only"


def test_assignment_site_to_dict():
    site = AssignmentSite(file_label="m.py", line=3, field_name="score",
                           site_kind="literal_only", source_snippet="self.score = 1")
    d = site.to_dict()
    assert d == {
        "file_label": "m.py", "line": 3, "field_name": "score",
        "site_kind": "literal_only", "source_snippet": "self.score = 1",
        "site_shape": "assignment",
    }


def test_field_trace_result_default_construction_is_empty():
    result = FieldTraceResult()
    assert result.traces == []
    assert result.parse_errors == []
    assert result.flagged_field_names == []


def test_field_trace_default_construction_is_empty():
    trace = FieldTrace(field_name="x")
    assert trace.site_count == 0
    assert trace.status == "no_assignment_found"
