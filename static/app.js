const form = document.querySelector("#case-form");
const results = document.querySelector("#results");

const labels = {
  ready: "Ready",
  needs_owner: "Owner action",
  needs_authority: "Authority check",
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button");
  button.disabled = true;
  button.textContent = "Assembling evidence…";
  const data = new FormData(form);
  const number = (name) => data.get(name) ? Number(data.get(name)) : null;
  const payload = {
    project_type: data.get("project_type"),
    municipality: data.get("municipality"),
    area_m2: number("area_m2"),
    height_m: number("height_m"),
    boundary_distance_m: number("boundary_distance_m"),
    has_site_plan: data.has("has_site_plan"),
    has_drawings: data.has("has_drawings"),
    has_local_plan_reference: data.has("has_local_plan_reference"),
  };
  try {
    const response = await fetch("/api/assess", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify(payload)});
    if (!response.ok) throw new Error(`Request failed (${response.status})`);
    const pack = await response.json();
    results.innerHTML = `
      <div class="result-head"><div><p class="eyebrow">PERMIT PACK</p><h2>${pack.case_summary}</h2></div><span>${pack.documents_ready.length} ready · ${pack.documents_missing.length} missing</span></div>
      <div class="finding-list">${pack.findings.map(item => `<article class="finding ${item.state}"><div><p class="state">${labels[item.state]}</p><h3>${item.title}</h3><p>${item.explanation}</p></div><strong>${item.next_action}</strong></article>`).join("")}</div>
      <div class="disclaimer">${pack.disclaimer}</div>`;
  } catch (error) {
    results.innerHTML = `<div class="empty error">${error.message}</div>`;
  } finally {
    button.disabled = false;
    button.textContent = "Run agent workflow";
  }
});

