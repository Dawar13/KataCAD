# PHASE 1 — Geometry Foundation in the Browser

> **Read `CLAUDE.md` at the repo root before reading this file.** That document is the project context. This document is the Phase 1 build brief.

---

## Phase goal

Prove that real B-Rep geometry flows from code, through Replicad (OpenCascade WASM), into a Three.js viewport, and back out as a STEP file that opens cleanly in SolidWorks. Every later phase depends on this round-trip working.

**No AI, no router, no heroes, no API calls in this phase.** Phase 1 is browser-only — `apps/api` is not touched. A single hand-coded parametric L-bracket is the only geometry.

---

## Prerequisites

- Phase 0 is complete (monorepo, `apps/web` scaffolded, `pnpm install` works).
- Node 20.x, pnpm 9.x available.
- A copy of SolidWorks / Fusion 360 / Onshape to verify the exported STEP (manual check).

---

## Deliverables

1. Phase 1 dependencies added to `apps/web`: `replicad`, `replicad-opencascadejs`, `replicad-threejs-helper`, `three`, `@react-three/fiber`, `@react-three/drei`, plus `@types/three` and `tsx` (dev).
2. `apps/web/next.config.js` — webpack `resolve.fallback` so the OpenCascade glue (which statically references Node built-ins) bundles for the browser.
3. `apps/web/scripts/copy-wasm.mjs` — copies `replicad_single.wasm` into `public/wasm/` (runs on `predev` / `prebuild`). The copied wasm is gitignored.
4. `apps/web/lib/replicad/` — WASM init singleton (`oc.ts`), the parametric L-bracket (`bracket.ts`), tessellation (`tessellate.ts`), export helpers (`export.ts`), and an `index.ts` barrel.
5. `apps/web/lib/hooks/useReplicad.ts` — initializes the WASM bundle once and exposes status + a `buildBracket` function.
6. `apps/web/components/Viewport.tsx` and `ReplicadShape.tsx` — the R3F canvas (default lighting only) and the tessellated-shape renderer.
7. `apps/web/app/playground/page.tsx` — loads the client UI via `next/dynamic` with `ssr: false`.
8. `apps/web/scripts/generate-fixture.mts` — headless Node script that builds the default bracket and writes `apps/web/fixtures/bracket-default.step` (committed as a regression fixture).

---

## Hard rules for this phase

1. **Default lighting only.** A `hemisphereLight` + one `directionalLight` so the geometry is readable — nothing cinematic. No bloom, no post-processing, no orbit auto-rotate. Cinematic lighting is Phase 9.
2. **No beautification.** Tailwind defaults, white background, black text, plain HTML buttons. No custom colors, fonts, transitions, or animations.
3. **Real geometry only.** The bracket is real Replicad B-Rep. The STEP and STL exports are real. Nothing is mocked.
4. **Browser-only.** Do not modify `apps/api`. Phase 1 has no network calls.
5. **WASM loads client-side only.** The viewport and anything importing `replicad` must be reached through `dynamic(..., { ssr: false })`. The WASM is initialized once via a singleton promise — never per-render.
6. **`bracket.ts` stays framework-agnostic.** It imports only from `replicad`, so the same module builds geometry in both the browser and the headless Node fixture script.

---

## Implementation order

1. Add dependencies, run `pnpm install`.
2. `next.config.js` webpack fallback + `copy-wasm.mjs` + `predev`/`prebuild` wiring.
3. `lib/replicad/oc.ts` — singleton OpenCascade init (`setOC`).
4. `lib/replicad/bracket.ts` — the parametric L-bracket.
5. `scripts/generate-fixture.mts` — run it headlessly to confirm geometry + STEP export work before touching the UI. Commit `fixtures/bracket-default.step`.
6. `lib/replicad/tessellate.ts` + `export.ts` + `index.ts`.
7. `lib/hooks/useReplicad.ts`.
8. `components/Viewport.tsx` + `ReplicadShape.tsx`.
9. `app/playground/page.tsx` (+ `PlaygroundClient.tsx`).
10. Verify (`pnpm lint`, `tsc --noEmit`, `pnpm dev` → open `/playground`).

---

## Verification checklist

- `pnpm install` completes; `pnpm --filter web lint` and `tsc --noEmit` pass.
- `pnpm --filter web exec tsx scripts/generate-fixture.mts` writes a non-empty `fixtures/bracket-default.step`.
- `pnpm dev` → `http://localhost:3000/playground` renders the L-bracket with no console errors.
- The five bracket parameters change the geometry when edited.
- `[Export STEP]` downloads a file that opens cleanly in SolidWorks / Fusion / Onshape.
- `[Export STL]` downloads a file that opens in a slicer or mesh viewer.
- The Phase 0 placeholder homepage and the `/api/echo` round-trip still work.

---

*Phase 1 instruction file version 1.0. Written against the repository as Phase 0 left it.*
