# Implementation Plan: Auto-Remediation Module (Slide Doctor)

## Goal
Add a `remediators/` module that can automatically fix detected layout errors. Implement geometric fixes first (alignment, margin, aspect ratio), then style fixes (hierarchy). Integrate with `main.py` via `--fix` flag.

## Assumptions
- Existing detectors work correctly and return structured `LayoutError` objects.
- `python-pptx` can modify and save presentations without major formatting loss.
- Users will review fixes before applying (via `--fix --dry-run` default).

---

## Plan

### Step 1: Create Remediators Module Structure
**Files**: `src/remediators/__init__.py`, `src/remediators/base.py`
**Change**: Create package with abstract `Remediator` base class defining `fix(slide, error) -> bool`.
**Verify**: `python -c "from src.remediators.base import Remediator"`

---

### Step 2: Implement Alignment Fixer
**Files**: `src/remediators/alignment.py`
**Change**: For near-aligned elements, snap to the mean coordinate (left, top, or center).
**Verify**: Manual test with a sample PPTX containing misaligned elements.

---

### Step 3: Implement Margin Fixer
**Files**: `src/remediators/margin.py`
**Change**: Nudge elements inside safe zone (add/subtract offset to `shape.left` or `shape.top`).
**Verify**: Manual test with element at slide edge.

---

### Step 4: Implement Aspect Ratio Fixer
**Files**: `src/remediators/aspect_ratio.py`
**Change**: Reset image dimensions to native ratio (preserve width, adjust height).
**Verify**: Manual test with stretched image.

---

### Step 5: Implement Hierarchy Fixer
**Files**: `src/remediators/hierarchy.py`
**Change**: Standardize font sizes to nearest cluster center (e.g., 31pt → 32pt).
**Verify**: Manual test with inconsistent font sizes.

---

### Step 6: Create Fix Orchestrator
**Files**: `src/fixer.py`
**Change**: Maps error types to remediators. Applies fixes in order. Saves backup `_original.pptx`.
**Verify**: `python -c "from src.fixer import apply_fixes"`

---

### Step 7: Integrate with CLI
**Files**: `src/main.py`
**Change**: Add `--fix` and `--dry-run` flags. If `--fix`, call `apply_fixes()` after detection.
**Verify**: `python src/main.py --help` shows new flags.

---

### Step 8: Update Documentation
**Files**: `README.md`
**Change**: Document `--fix` usage and backup behavior.
**Verify**: Read `README.md` for accuracy.

---

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Fixes cause new overlaps | Check bounding boxes after each fix; skip if conflict |
| Formatting loss on save | Test with complex PPTX; document known limitations |
| User applies bad fixes | Default to `--dry-run`; require explicit `--apply` |

## Rollback Plan
- Original file is always backed up as `filename_original.pptx`.
- If all fixes fail, report errors and exit without saving.
- User can revert by renaming `_original.pptx` back.

---

**Approve this plan? Reply APPROVED if it looks good.**
