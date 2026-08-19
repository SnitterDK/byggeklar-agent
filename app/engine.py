from __future__ import annotations

from .models import BuildingCase, Finding, FindingState, PermitPack


SUPPORTED_TYPES = {
    "carport",
    "shed",
    "garage",
    "covered terrace",
    "annex",
    "small extension",
}


def build_permit_pack(case: BuildingCase) -> PermitPack:
    """Create a transparent evidence pack without pretending to grant a permit.

    The checks are intentionally conservative. Missing facts become explicit
    owner tasks and municipality-specific questions rather than guessed answers.
    """
    findings: list[Finding] = []
    ready: list[str] = []
    missing: list[str] = []

    project_type = case.project_type.strip().casefold()
    if project_type not in SUPPORTED_TYPES:
        findings.append(
            Finding(
                "Project classification",
                FindingState.NEEDS_OWNER,
                "The project type is outside the current guided catalogue.",
                "Describe the intended use and construction in more detail.",
            )
        )
    else:
        findings.append(
            Finding(
                "Project classification",
                FindingState.READY,
                f"The case is classified as {project_type} for checklist purposes.",
                "Confirm this classification before using the permit pack.",
            )
        )

    for value, label, action in (
        (case.area_m2, "Area", "Measure the total footprint in square metres."),
        (case.height_m, "Height", "Measure the highest point above terrain."),
        (
            case.boundary_distance_m,
            "Boundary distance",
            "Measure the shortest distance from the structure to the boundary.",
        ),
    ):
        if value is None or value <= 0:
            findings.append(
                Finding(label, FindingState.NEEDS_OWNER, "A required measurement is missing.", action)
            )
        else:
            findings.append(
                Finding(
                    label,
                    FindingState.READY,
                    f"Recorded measurement: {value:g}.",
                    "Keep a dated measurement or drawing as evidence.",
                )
            )

    if case.has_site_plan:
        ready.append("Site plan")
    else:
        missing.append("Site plan showing boundaries and distances")
    if case.has_drawings:
        ready.append("Dimensioned drawings")
    else:
        missing.append("Dimensioned plan, elevation and section drawings")

    if case.has_local_plan_reference:
        ready.append("Local-plan reference")
    else:
        missing.append("Applicable local plan or written municipality confirmation")
        findings.append(
            Finding(
                "Local rules",
                FindingState.NEEDS_AUTHORITY,
                f"No verified local-plan reference is attached for {case.municipality}.",
                "Confirm the address-specific plan and constraints with the municipality.",
            )
        )

    if missing:
        findings.append(
            Finding(
                "Evidence pack",
                FindingState.NEEDS_OWNER,
                f"{len(missing)} document item(s) remain before the pack is review-ready.",
                "Collect the missing items shown in the checklist.",
            )
        )
    else:
        findings.append(
            Finding(
                "Evidence pack",
                FindingState.READY,
                "The configured evidence checklist is complete.",
                "Request professional or municipality review before submission.",
            )
        )

    summary = (
        f"{case.project_type.strip() or 'Unclassified project'} in "
        f"{case.municipality.strip() or 'an unspecified municipality'}"
    )
    return PermitPack(summary, findings, ready, missing)

