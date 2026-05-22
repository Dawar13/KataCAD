# PHASE 5 — Layer 2 Programmatic Families

> **Read `CLAUDE.md` at the repo root before reading this file.** Then read `docs/phases/PHASE_3.md` (the router) and `docs/phases/PHASE_4.md`. This document is the Phase 5 build brief.

---

## Phase goal

Cover the long tail of generic mechanical archetypes — bracket, flange, plate, shaft, gear, housing, pulley, hub, manifold, clamp — with parametric **CadQuery** scripts, so a prompt like *"flange with ten holes"* produces a real flange with exactly ten holes.

A new endpoint `POST /api/generate/layer2` runs the chosen archetype's CadQuery generator and returns a base64 STEP plus metadata. The web app imports that STEP with Replicad and renders it through the same viewport as the heroes.

---

## Prerequisites

- Phase 4 complete.
- **Python 3.10–3.13** for `apps/api` — CadQuery's OpenCascade binding (`cadquery-ocp`) has no Python 3.14 wheel. The API venv is built with Python 3.12.

---

## Architecture decisions

1. **Paths follow the repo.** Generators live under `apps/api/app/lib/cadquery/`; the route is `app/routes/generate.py`.
2. **One generator per archetype.** Each is a function `params -> ArchetypeBuild` (a CadQuery model + a semantic tree + slider defs). A registry maps archetype name to generator.
3. **STEP export via a temp file.** CadQuery's `exporters.export` writes to a path; the endpoint exports to a temp file, reads the bytes, and base64-encodes them.
4. **Params are clamped.** Every generator sanitizes its inputs so no parameter value (from a slider or the router) can produce degenerate geometry.
5. **Layer 2 parts reuse the hero pipeline on the web.** The imported STEP becomes the geometry of a single-node `HeroModel`; the existing `HeroScene`, `FeatureTree`, `ParameterSliders`, and export path render it unchanged. Layer 2 parts are static (no animation).
6. **Sliders regenerate via the API.** Changing a Layer 2 slider re-calls `/api/generate/layer2` — the geometry is rebuilt server-side by CadQuery, not locally.

---

## Deliverables

- `apps/api/pyproject.toml` — add `cadquery`.
- `apps/api/app/lib/cadquery/base.py` — shared types, STEP export, bounding box, param helper.
- `apps/api/app/lib/cadquery/<archetype>.py` — ten generators.
- `apps/api/app/lib/cadquery/registry.py` — the archetype registry.
- `apps/api/app/schemas/generate.py` — `GenerateRequest`, `GenerateResponse`.
- `apps/api/app/routes/generate.py` — `POST /api/generate/layer2`; registered in `main.py`.
- `apps/api/app/prompts/router.txt` — extended with each archetype's parameter schema.
- `apps/api/tests/test_generate.py` — round-trip test, every archetype at three parameter sets.
- `packages/shared/src/api.ts` — `GenerateRequest`, `GenerateResponse`, metadata types.
- `apps/web/lib/api/generate.ts` — typed client.
- `apps/web/lib/replicad/heroes/archetype.ts` — wraps an imported STEP as a renderable model.
- `apps/web/app/studio/StudioClient.tsx` — Layer 2 prompts load and render archetypes.

---

## Hard rules for this phase

1. **No beautification.** Tailwind defaults, functional lighting.
2. **Real geometry only** — CadQuery B-Rep; STEP exports are real and open in SolidWorks.
3. **OpenAI only at runtime**; no hardcoded model names.
4. **Generators never crash the request** — clamp inputs; the endpoint returns a clear error only for an unknown archetype.
5. **Do not build Layer 3 retrieval** — that is Phase 6.

---

## Verification checklist

- `ruff check .` and `pytest -q` pass in `apps/api` (the round-trip test builds every archetype).
- All ten archetypes produce valid STEP at default parameters.
- "flange with ten holes, eighty millimeter bolt circle, six millimeter thick" yields a flange with exactly ten holes.
- `pnpm --filter web lint`, `tsc --noEmit`, `next build` pass.
- A Layer 2 prompt renders an imported part in the studio; its sliders regenerate it via the API.
- `/playground` and the heroes still work.

---

*Phase 5 instruction file version 1.0. Written against the repository as Phase 4 left it.*
