"""Named-field input-derivation trace for source code.

Operationalizes a sharper, more mechanically checkable variant of
closed_path.py's closed/open distinction: a claimed detection or
measurement field (a variable, attribute, or dataclass field whose name
a README or paper claims is *computed*) that is never assigned from any
expression referencing input -- only ever a literal constant -- cannot
vary with input at all. That is a stronger finding than "closed-loop"
(checked against the system's own declared rule, but at least computed
from something): the field is not computed from anything. This module
automates the AST trace that kind of finding requires: given a
caller-supplied list of field names and a caller-supplied mapping of
source files, find every assignment site and classify its right-hand
side as a literal-only expression or not.

Generic by construction: nothing here refers to any named project,
repository, or individual. Callers supply their own source text, file
labels, and field names -- typically field names identified by reading a
specimen's own prose (a README, a paper) for claimed-capability language
and cross-referencing the code symbol that prose points to. Matching a
prose claim to a code symbol is a human/agent judgment call this module
does not attempt; it only traces a symbol once named.

Deliberately conservative in one direction only, mirroring
scan_for_hardcoded_assertion_style's stated false-positive posture: this
flags a field as "never proven input-derived" ONLY when every assignment
site found is provably literal -- constants, and literal-only
containers/unary-ops/binops built from constants, plus the common
`dataclasses.field(default=<literal>)` / `field(default_factory=lambda:
<literal>)` idiom. Any site containing a Name, Attribute, Subscript,
comprehension, or other Call is classified NOT_PROVEN_LITERAL and
excludes the field from the flag -- even though some such expressions
are also constant in practice (e.g. a call to a pure zero-argument
function that always returns the same value). Proving that statically is
out of scope; a false "never input-derived" accusation is a worse error
here than a missed one. Augmented assignment (`x += ...`) is always
treated as NOT_PROVEN_LITERAL regardless of its right-hand side, because
it depends on the target's prior value, which this module does not trace
across statements.

A field with zero assignment sites found is reported separately
(status "no_assignment_found") -- the field may be set dynamically
(setattr, exec), via a mechanism outside plain assignment syntax, or in
a file the caller did not include. That is a gap in the scan's inputs,
not a finding about the field, and must not be read as equivalent to
"never proven input-derived."
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field

#: The three trace outcomes for one field name. "no_assignment_found":
#: the name never appeared as an assignment target in the supplied
#: sources -- an input gap, not a finding. "never_proven_input_derived":
#: at least one assignment site was found and every site found is
#: literal-only -- the lead this module exists to surface. "input_
#: derived_or_unknown": at least one site could not be proven literal,
#: so the field cannot be flagged.
TRACE_STATUSES = ("no_assignment_found", "never_proven_input_derived", "input_derived_or_unknown")

SITE_LITERAL_ONLY = "literal_only"
SITE_NOT_PROVEN_LITERAL = "not_proven_literal"


def _field_call_literal_default(node: ast.Call) -> bool | None:
    """If `node` looks like a `dataclasses.field(...)` / `field(...)`
    call, return whether its default is provably literal. Returns None
    if `node` is not shaped like a field() call (falls through to the
    general Call = NOT_PROVEN_LITERAL rule in `_is_literal_only`)."""
    func = node.func
    if isinstance(func, ast.Name):
        func_name = func.id
    elif isinstance(func, ast.Attribute):
        func_name = func.attr
    else:
        return None
    if func_name != "field":
        return None
    for kw in node.keywords:
        if kw.arg == "default":
            return _is_literal_only(kw.value)
        if kw.arg == "default_factory":
            if isinstance(kw.value, ast.Lambda):
                return _is_literal_only(kw.value.body)
            return False
    return None


def _is_literal_only(node: ast.AST) -> bool:
    """True only if `node` is provably a constant expression. False
    (not proven, not disproven) for any Name, Attribute, Subscript,
    ordinary Call, comprehension, Starred, or anything else this
    function does not explicitly recognize -- conservative by design,
    see module docstring."""
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return all(_is_literal_only(elt) for elt in node.elts)
    if isinstance(node, ast.Dict):
        return all(
            (k is None or _is_literal_only(k)) and _is_literal_only(v)
            for k, v in zip(node.keys, node.values)
        )
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub, ast.Not, ast.Invert)):
        return _is_literal_only(node.operand)
    if isinstance(node, ast.BinOp):
        return _is_literal_only(node.left) and _is_literal_only(node.right)
    if isinstance(node, ast.Call):
        field_default = _field_call_literal_default(node)
        return bool(field_default) if field_default is not None else False
    return False


def _target_names(target: ast.AST) -> list[str]:
    """Names this assignment target binds -- plain Name, attribute
    access (keyed by the final attribute name, e.g. `self.x` -> "x"),
    and tuple/list unpacking, recursively. Note: every name unpacked
    from a tuple/list target is classified against the *entire*
    right-hand side expression, not matched element-by-element against
    it -- a conservative simplification (see trace_field_assignments'
    caller loop). Precise per-element matching is a plausible future
    refinement, not built out here."""
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, ast.Attribute):
        return [target.attr]
    if isinstance(target, (ast.Tuple, ast.List)):
        names: list[str] = []
        for elt in target.elts:
            names.extend(_target_names(elt))
        return names
    return []


def _line_snippet(source_lines: list[str], lineno: int) -> str:
    if 1 <= lineno <= len(source_lines):
        return source_lines[lineno - 1].strip()
    return ""


#: What syntactic shape produced a given AssignmentSite. "assignment"
#: covers `=`, annotated `x: T = ...`, and augmented `x += ...`.
#: "keyword_argument" covers a call's `name=value` keyword argument
#: (e.g. a dataclass constructor call `StateVector(score=0.83, ...)`)
#: -- in real code this is at least as common a way a named field's
#: value gets set as a `self.x = ...` statement, and was in fact the
#: shape found in the specimen that first motivated this module: fields
#: declared only as dataclass type annotations, with every actual value
#: supplied via constructor keyword arguments at each call site.
SITE_SHAPE_ASSIGNMENT = "assignment"
SITE_SHAPE_KEYWORD_ARGUMENT = "keyword_argument"


@dataclass
class AssignmentSite:
    file_label: str
    line: int
    field_name: str
    site_kind: str
    source_snippet: str = ""
    site_shape: str = SITE_SHAPE_ASSIGNMENT

    def to_dict(self) -> dict:
        return {
            "file_label": self.file_label,
            "line": self.line,
            "field_name": self.field_name,
            "site_kind": self.site_kind,
            "source_snippet": self.source_snippet,
            "site_shape": self.site_shape,
        }


@dataclass
class FieldTrace:
    field_name: str
    sites: list[AssignmentSite] = field(default_factory=list)

    @property
    def site_count(self) -> int:
        return len(self.sites)

    @property
    def literal_only_count(self) -> int:
        return sum(1 for s in self.sites if s.site_kind == SITE_LITERAL_ONLY)

    @property
    def not_proven_literal_count(self) -> int:
        return sum(1 for s in self.sites if s.site_kind == SITE_NOT_PROVEN_LITERAL)

    @property
    def status(self) -> str:
        if self.site_count == 0:
            return "no_assignment_found"
        if self.not_proven_literal_count == 0:
            return "never_proven_input_derived"
        return "input_derived_or_unknown"

    def to_dict(self) -> dict:
        return {
            "field_name": self.field_name,
            "status": self.status,
            "site_count": self.site_count,
            "literal_only_count": self.literal_only_count,
            "not_proven_literal_count": self.not_proven_literal_count,
            "sites": [s.to_dict() for s in self.sites],
        }


@dataclass
class FieldTraceResult:
    traces: list[FieldTrace] = field(default_factory=list)
    parse_errors: list[dict] = field(default_factory=list)

    @property
    def flagged_field_names(self) -> list[str]:
        """Fields with status "never_proven_input_derived" -- a lead for
        review, not a verdict that the field is fabricated; see module
        docstring for the conservative-bias rationale."""
        return [t.field_name for t in self.traces if t.status == "never_proven_input_derived"]

    def to_dict(self) -> dict:
        return {
            "traces": [t.to_dict() for t in self.traces],
            "flagged_field_names": self.flagged_field_names,
            "parse_errors": self.parse_errors,
            "note": (
                "A flagged field name has every assignment site found in "
                "the supplied sources classified as a literal constant -- "
                "it was never observed being assigned from an expression "
                "referencing a name, attribute, subscript, or (ordinary) "
                "call. This is a lead for manual review, not proof the "
                "field is fabricated: it may be set outside the sources "
                "supplied, via a mechanism this scanner does not parse "
                "(setattr, exec, a C extension), or the literal may be "
                "correct and intentional. Read every site directly."
            ),
        }


def trace_field_assignments(sources: dict[str, str], field_names: list[str]) -> FieldTraceResult:
    """Parse each `sources[file_label]` as Python and find every site
    that sets a value for one of `field_names`: an assignment (plain
    `=`, annotated `x: T = ...`, or augmented `x += ...`), or a call's
    keyword argument (`SomeCall(field_name=value, ...)` -- covers the
    common case of a dataclass whose fields are declared only as type
    annotations, with every actual value supplied at each constructor
    call site; see SITE_SHAPE_KEYWORD_ARGUMENT's docstring). Each site
    is classified per the module docstring's literal-only rule.
    Augmented assignment is always NOT_PROVEN_LITERAL regardless of its
    right-hand side (see module docstring).

    A source file that fails to parse is recorded in
    `FieldTraceResult.parse_errors` rather than raised, so one bad file
    does not prevent tracing the rest.
    """
    result = FieldTraceResult()
    traces_by_name = {name: FieldTrace(field_name=name) for name in field_names}
    wanted = set(field_names)

    for file_label, source_text in sources.items():
        try:
            tree = ast.parse(source_text, filename=file_label)
        except SyntaxError as exc:
            result.parse_errors.append({"file_label": file_label, "error": str(exc)})
            continue
        source_lines = source_text.splitlines()

        def _record(name: str, lineno: int, is_literal: bool, shape: str) -> None:
            if name not in wanted:
                return
            traces_by_name[name].sites.append(AssignmentSite(
                file_label=file_label,
                line=lineno,
                field_name=name,
                site_kind=SITE_LITERAL_ONLY if is_literal else SITE_NOT_PROVEN_LITERAL,
                source_snippet=_line_snippet(source_lines, lineno),
                site_shape=shape,
            ))

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets, value, force_not_literal = node.targets, node.value, False
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                targets, value, force_not_literal = [node.target], node.value, False
            elif isinstance(node, ast.AugAssign):
                targets, value, force_not_literal = [node.target], node.value, True
            elif isinstance(node, ast.Call):
                lineno = getattr(node, "lineno", 0)
                for kw in node.keywords:
                    if kw.arg is None:  # **kwargs expansion -- not a named field
                        continue
                    _record(kw.arg, lineno, _is_literal_only(kw.value), SITE_SHAPE_KEYWORD_ARGUMENT)
                continue
            else:
                continue

            for target in targets:
                for name in _target_names(target):
                    is_literal = (not force_not_literal) and _is_literal_only(value)
                    _record(name, getattr(node, "lineno", 0), is_literal, SITE_SHAPE_ASSIGNMENT)

    result.traces = [traces_by_name[name] for name in field_names]
    return result
