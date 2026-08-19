from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .engine import build_permit_pack
from .models import BuildingCase


ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"

app = FastAPI(title="Byggeklar Agent", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


class CasePayload(BaseModel):
    project_type: str = "carport"
    municipality: str = "Copenhagen"
    area_m2: Optional[float] = 28
    height_m: Optional[float] = 2.4
    boundary_distance_m: Optional[float] = 1.8
    has_site_plan: bool = False
    has_drawings: bool = True
    has_local_plan_reference: bool = False


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": "evidence-first"}


@app.post("/api/assess")
def assess(payload: CasePayload) -> dict:
    case = BuildingCase(**payload.model_dump())
    return asdict(build_permit_pack(case))
