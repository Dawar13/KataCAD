# PHASE 4 — Feature Tree and the Remaining Five Heroes

> **Read `CLAUDE.md` at the repo root before reading this file.** Then read `docs/phases/PHASE_2.md` (the hero scene-graph pattern) and `docs/phases/PHASE_3.md`. This document is the Phase 4 build brief.

---

## Phase goal

Two things: add the **feature tree sidebar** (the demo's most distinctive UI element) and complete the Layer 1 gallery with the **remaining five heroes** — quadcopter, V-twin engine, differential, bicycle, NEMA mount.

All five are built as **detailed parametric Replicad code**, same scene-graph pattern as Phase 2. No imported CAD — every hero is animated where the real mechanism moves, slider-driven, and exports its own clean STEP.

---

## Prerequisites

- Phase 3 complete: `/studio` loads heroes from prompt + gallery.
- No new dependencies — Phase 4 uses the Phase 1/2 stack.

---

## Architecture decisions

1. **All five heroes are coded, not imported.** Imported third-party CAD was rejected: non-commercial licensing on GrabCAD/Thingiverse, no animation, no parameters, and foreign metadata in the exported STEP. Detailed coded heroes keep the Layer 1 contract (parametric + animated + own STEP).
2. **Feature tree = the scene graph.** `FeatureTree` renders the current hero's `HeroNode` tree as a collapsible, monospace list. It needs no new data — Phase 2 nodes already carry semantic names.
3. **Highlight is per-node, not per-face.** Clicking a tree node highlights that whole part in the viewport (a swapped material). The scene graph is per-part, so per-part is the correct granularity.
4. **Sliders reuse the existing rebuild path.** `ParameterSliders` reads `HeroModel.sliders`; changing a value updates the studio's hero request, which already triggers a rebuild.
5. **New geometry helpers** (`tubeBetween`, `makeTorus`, `revolveOn`) go in `heroes/util.ts` — frames and wheels need tubes and tori.

---

## Deliverables

- `apps/web/lib/replicad/heroes/util.ts` — `tubeBetween`, `makeTorus`, `revolveOn`.
- `apps/web/lib/replicad/heroes/nema-mount.ts` — NEMA motor-mount bracket (static).
- `apps/web/lib/replicad/heroes/quadcopter.ts` — frame + four spinning propellers.
- `apps/web/lib/replicad/heroes/differential.ts` — ring gear + carrier + spider/side gears.
- `apps/web/lib/replicad/heroes/v-twin.ts` — crankcase + two finned cylinders + cycling pistons.
- `apps/web/lib/replicad/heroes/bicycle.ts` — frame + two wheels + crankset.
- `apps/web/lib/animations/{quadcopter,differential,v-twin,bicycle}.ts`.
- `apps/web/lib/replicad/heroes/registry.ts` — all eight heroes registered and available.
- `apps/web/components/FeatureTree.tsx` — collapsible tree, click-to-highlight.
- `apps/web/components/ParameterSliders.tsx` — slider panel, rebuilds on change.
- `apps/web/components/HeroScene.tsx` — node highlight support.
- `apps/web/app/studio/StudioClient.tsx` — sidebar layout, selection + slider wiring.

---

## Hard rules for this phase

1. **No beautification.** Tailwind defaults; functional viewport lighting only. Cinematic rendering is Phase 9.
2. **Real geometry only** — every hero is real Replicad B-Rep; STEP exports are real.
3. **No imported CAD** — all heroes are coded.
4. **Browser-only** — `apps/api` is not touched.
5. **Animations are in scope** (propellers, pistons, gears, wheels); cinematic lighting is not.
6. **Simplify if a hero overruns** — a recognizable, animated, robust hero beats an intricate, fragile one (the Phase 2 gearbox-teeth lesson).

---

## Verification checklist

- `pnpm --filter web lint`, `tsc --noEmit`, `next build` pass.
- The headless `check-heroes` script builds and STEP-exports all eight heroes.
- All eight load from the gallery and from prompts.
- The feature tree updates per hero; clicking a node highlights that part.
- Sliders regenerate the model in under one second.
- `/playground` still works.

---

*Phase 4 instruction file version 1.0. Written against the repository as Phase 3 left it.*
