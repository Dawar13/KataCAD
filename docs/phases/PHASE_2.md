# PHASE 2 — First Three Heroes

> **Read `CLAUDE.md` at the repo root before reading this file.** Then read `docs/phases/PHASE_1.md` for what Phase 1 produced. This document is the Phase 2 build brief.

---

## Phase goal

Build the three Layer 1 heroes that carry the booth — **planetary gearbox**, **five-finger gripper**, **six-axis robot arm** — as parametric Replicad modules with looping mechanism animations. No AI yet: heroes load from direct button clicks in a hero gallery.

**No router, no OpenAI, no API calls.** That is Phase 3. Phase 2 is browser-only.

---

## Prerequisites

- Phase 1 is complete: Replicad → Three.js → STEP round-trip works at `/playground`.
- No new dependencies — Phase 2 uses what Phase 1 installed (`replicad`, `three`, `@react-three/fiber`, `@react-three/drei`).

---

## Architecture decisions (resolved against Phase 1)

1. **Heroes are scene graphs, not single solids.** A hero `build()` returns a tree of `HeroNode`s. Each node carries optional geometry (a Replicad `Shape3D` in a canonical local frame, pivot at the origin), a rest transform (position + euler rotation relative to its parent), and child nodes. This lets gears spin, fingers curl, and arm joints articulate independently.
2. **Animation is runtime-only.** `animate(elapsed)` returns per-node rotation/translation deltas. Three.js `useFrame` applies them to nested `<group>`s — geometry is tessellated once and never rebuilt for animation.
3. **Export bakes the rest pose.** The scene graph is flattened — world transforms composed with Three.js matrix math — into one Replicad compound, exported as STEP/STL at rest.
4. **`Viewport.tsx` becomes `children`-based.** Phase 1's `Viewport` took a `mesh` prop; it now renders arbitrary children inside the canvas. `/playground` is updated to match and keeps working.
5. **New route `/studio`.** The hero experience lives at `/studio`. Phase 1's `/playground` (bracket sandbox) and the Phase 0 `/` placeholder are left untouched.
6. **`HeroId` moves to `packages/shared`** — the router will need it in Phase 3.
7. Animations use `useFrame` only; **GSAP is not added** in Phase 2.

---

## Deliverables

- `packages/shared/src/domain.ts` — `HeroId` union (eight heroes).
- `apps/web/lib/replicad/heroes/types.ts` — `HeroNode`, `HeroModel`, `HeroDefinition`, animation types.
- `apps/web/lib/replicad/heroes/gear.ts` — parametric spur/ring gear geometry.
- `apps/web/lib/replicad/heroes/gearbox.ts`, `gripper.ts`, `robot-arm.ts` — the three heroes.
- `apps/web/lib/replicad/heroes/flatten.ts` — scene graph → compound (export) + bounding box.
- `apps/web/lib/replicad/heroes/registry.ts` + `index.ts` — hero lookup.
- `apps/web/lib/animations/gearbox.ts`, `gripper.ts`, `robot-arm.ts` — one animation function per hero.
- `apps/web/components/HeroScene.tsx` — recursive scene-graph renderer with `useFrame` animation.
- `apps/web/components/HeroGallery.tsx` — bottom strip: 3 live buttons + 5 disabled placeholders.
- `apps/web/components/Viewport.tsx` — refactored to `children`.
- `apps/web/app/studio/page.tsx` + `StudioClient.tsx` — the hero page (`dynamic`, `ssr: false`).

---

## Hard rules for this phase

1. **No beautification.** Default lighting, Tailwind defaults. Mechanism animations *are* in scope (a Phase 2 deliverable); cinematic lighting and bloom are not.
2. **Real geometry only.** Every hero is real Replicad B-Rep. STEP exports are real.
3. **Don't break Phase 1.** `/playground` must still render the bracket and export. The only Phase 1 files Phase 2 touches are `Viewport.tsx` (sanctioned extension) and `PlaygroundClient.tsx` (to match the new `Viewport` API).
4. **Browser-only.** Do not modify `apps/api`.
5. **Heroes load by button click.** No prompt, no router — that is Phase 3.
6. **Gearbox teeth:** simplified (trapezoidal) tooth profiles are acceptable and expected — they must read as a gear and animate smoothly, not be involute-accurate.

---

## Verification checklist

- `pnpm --filter web lint` and `tsc --noEmit` pass.
- `/studio` renders; clicking each of the three hero buttons loads that hero in under three seconds.
- Each hero animates smoothly (gearbox gears spin, gripper fingers cycle, arm runs a pick-and-place loop).
- STEP export works for all three and opens cleanly in SolidWorks / Fusion / Onshape.
- The five not-yet-built heroes appear as disabled placeholder buttons.
- `/playground` (Phase 1) still renders the bracket and exports.

---

*Phase 2 instruction file version 1.0. Written against the repository as Phase 1 left it.*
