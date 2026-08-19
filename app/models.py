from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class FindingState(str, Enum):
    READY = "ready"
    NEEDS_OWNER = "needs_owner"
    NEEDS_AUTHORITY = "needs_authority"


@dataclass(frozen=True)
class BuildingCase:
    project_type: str
    municipality: str
    area_m2: Optional[float]
    height_m: Optional[float]
    boundary_distance_m: Optional[float]
    has_site_plan: bool
    has_drawings: bool
    has_local_plan_reference: bool


@dataclass(frozen=True)
class Finding:
    title: str
    state: FindingState
    explanation: str
    next_action: str


@dataclass
class PermitPack:
    case_summary: str
    findings: List[Finding] = field(default_factory=list)
    documents_ready: List[str] = field(default_factory=list)
    documents_missing: List[str] = field(default_factory=list)
    disclaimer: str = (
        "Decision support only. The relevant municipality remains the authority "
        "and must confirm applicable rules and any permit requirement."
    )
