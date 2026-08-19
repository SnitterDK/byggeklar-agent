import unittest

from app.engine import build_permit_pack
from app.models import BuildingCase, FindingState


class PermitPackTests(unittest.TestCase):
    def test_missing_measurements_are_never_guessed(self):
        pack = build_permit_pack(
            BuildingCase("carport", "Copenhagen", None, None, None, False, False, False)
        )
        owner_tasks = [f for f in pack.findings if f.state is FindingState.NEEDS_OWNER]
        self.assertGreaterEqual(len(owner_tasks), 4)
        self.assertIn("Site plan showing boundaries and distances", pack.documents_missing)

    def test_complete_evidence_pack_is_review_ready_not_approved(self):
        pack = build_permit_pack(
            BuildingCase("shed", "Odense", 12, 2.2, 3, True, True, True)
        )
        self.assertEqual(pack.documents_missing, [])
        self.assertIn("municipality", pack.disclaimer.lower())
        self.assertNotIn("approved", pack.case_summary.lower())

    def test_unknown_project_type_requires_owner_classification(self):
        pack = build_permit_pack(
            BuildingCase("wind turbine", "Aarhus", 10, 5, 4, True, True, True)
        )
        self.assertEqual(pack.findings[0].state, FindingState.NEEDS_OWNER)


if __name__ == "__main__":
    unittest.main()

