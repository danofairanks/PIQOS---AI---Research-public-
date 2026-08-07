"""Domain-agnostic paper-rigor scanner: placeholder/hand-wave phrases,
falsifiability, self-citation ratio, formal-vs-informal citation mix,
uncited empirical-certainty claims, credential-substituted-for-evidence
claims, unsupported consensus claims, and a missing limitations
section -- none of it tied to this project's own Law 0 vocabulary,
unlike `bifp` (bound to basin_attractors_v1.md's BIFP protocol) and
`attractor_scan` (bound to that paper's named maneuver/laundering
taxonomy). Applies to any paper.

Quick start::

    from paper_rigor import scan_paper

    result = scan_paper(text, byline_authors=["Smith", "Jones"])
    print(result.structural_gap_count, result.external_verification_worklist)

Or from the command line::

    paper-rigor scan some_paper.md --authors "Smith,Jones"
"""

from .citations import (
    CitabilityClaimCheck, CitationEntry, SelfCitationResult, VenueMixResult, UncitedEmpiricalClaim,
    check_citability_claim, compute_self_citation, compute_venue_mix, find_uncited_empirical_claims,
    parse_references,
)
from .consensus import ConsensusMatch, find_unsupported_consensus_claims
from .credentialing import CredentialMatch, find_credential_substitution
from .disclaimer import LimitationsCheck, check_limitations_section
from .falsifiability import FalsifiabilityCheck, check_falsifiability
from .headings import Heading, find_section, has_heading_matching, iter_headings
from .placeholders import PlaceholderMatch, find_placeholder_issues
from .scan import PaperRigorResult, scan_file, scan_paper

__all__ = [
    "CitabilityClaimCheck", "CitationEntry", "SelfCitationResult", "VenueMixResult", "UncitedEmpiricalClaim",
    "check_citability_claim", "compute_self_citation", "compute_venue_mix",
    "find_uncited_empirical_claims", "parse_references",
    "ConsensusMatch", "find_unsupported_consensus_claims",
    "CredentialMatch", "find_credential_substitution",
    "LimitationsCheck", "check_limitations_section",
    "FalsifiabilityCheck", "check_falsifiability",
    "Heading", "find_section", "has_heading_matching", "iter_headings",
    "PlaceholderMatch", "find_placeholder_issues",
    "PaperRigorResult", "scan_file", "scan_paper",
]

__version__ = "0.1.0"
