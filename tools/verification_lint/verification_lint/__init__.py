"""Content-level evidentiary-gap scanner: unattributed direct quotes,
uncited high-precision statistics, and missing "what this does not
claim/establish" disclaimer sections.

Quick start::

    from verification_lint import scan_document

    result = scan_document('The number was "definitely 97.14%" of respondents.')
    print(result.gap_count, result.unattributed_quotes, result.uncited_statistics)

Or from the command line::

    verification-lint scan some_file.md
    verification-lint scan-dir case_studies/ --only-gaps
"""

from .disclaimer import DisclaimerCheck, check_disclaimer
from .quotes import QuoteFinding, find_unattributed_quotes
from .scan import VerificationLintResult, scan_document, scan_file, scan_paths
from .sourcing import SourcingCheck, check_sourcing
from .statistics import StatFinding, find_uncited_statistics

__all__ = [
    "DisclaimerCheck", "check_disclaimer",
    "QuoteFinding", "find_unattributed_quotes",
    "SourcingCheck", "check_sourcing",
    "StatFinding", "find_uncited_statistics",
    "VerificationLintResult", "scan_document", "scan_file", "scan_paths",
]

__version__ = "0.1.0"
