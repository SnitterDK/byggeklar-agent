from __future__ import annotations

from dataclasses import asdict

from .engine import build_permit_pack
from .models import BuildingCase


SYSTEM_PROMPT = """
You are Byggeklar Agent, an evidence-first assistant for small Danish building
projects. Do the repetitive preparation work end to end: structure the case,
run the deterministic checklist, assemble missing-evidence tasks, and produce a
review-ready permit pack. Never claim that a municipality has approved a case.
Never invent measurements, local-plan rules, documents, or professional advice.
Surface only the decisions that require the owner or the relevant authority.
""".strip()


def create_strands_agent():
    """Create the real Strands Agents SDK integration used by the demo."""
    try:
        from strands import Agent, tool
    except ImportError as exc:  # pragma: no cover - optional in tests
        raise RuntimeError("Install requirements.txt to run the Strands agent") from exc

    @tool
    def assemble_permit_pack(
        project_type: str,
        municipality: str,
        area_m2: float | None = None,
        height_m: float | None = None,
        boundary_distance_m: float | None = None,
        has_site_plan: bool = False,
        has_drawings: bool = False,
        has_local_plan_reference: bool = False,
    ) -> dict:
        """Build a deterministic evidence checklist for a small building case."""
        case = BuildingCase(
            project_type,
            municipality,
            area_m2,
            height_m,
            boundary_distance_m,
            has_site_plan,
            has_drawings,
            has_local_plan_reference,
        )
        return asdict(build_permit_pack(case))

    return Agent(system_prompt=SYSTEM_PROMPT, tools=[assemble_permit_pack])

