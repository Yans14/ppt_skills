# Superpowers Brainstorm: Deep Dive with Slide Doctor (Auto-Remediation)

## Goal
Expand the current layout error detection system to include **automatic remediation (auto-fix)** and **content enhancement** capabilities, inspired by "Slide Doctor". Transform the tool from a passive detector into an active "Doctor" that diagnoses and prescribes fixes.

## Constraints
- **Safety First**: Auto-fixes must be non-destructive or reversible (backup original file).
- **Deterministic Fixes**: Geometric errors (alignment, margin) should have geometric solutions.
- **AI Fixes**: Semantic errors (clarity, tone) require AI/LLM intervention.
- **User Control**: Users must approve fixes before application (Review Mode).

## Known Context
- We have a robust **Detection Engine** (Hierarchy, Margin, Contrast, Aspect Ratio, Alignment).
- We have **VLM Validation** (Azure OpenAI) for legibility.
- "Slide Doctor" typically implies improving slide content and design, not just technical errors.

## Risks
- **Broken Layouts**: Auto-fixing alignment might overlap other elements.
- **Hallucinated Content**: AI rewriting text might change meaning.
- **Formatting Loss**: `python-pptx` sometimes drops advanced formatting when saving.
- **Performance**: Generating AI fixes for every slide is slow and costly.

## Options

### Option 1: The "Chiropractor" (Geometric Alignment Only)
- Focus purely on fixing geometric issues.
- **Actions**: Snap to grid, align edges, resize images to native ratio, move text into safe zones.
- **Pros**: Fast, deterministic, low risk.
- **Cons**: Doesn't address content quality or complex design issues.

### Option 2: The "Copy Editor" (Text & Content)
- Focus on text content improvement via LLM.
- **Actions**: Summarize text, fix grammar, reduce word count (density), improve visual hierarchy (headings).
- **Pros**: High value for readability.
- **Cons**: Subjective, requires human review.

### Option 3: The "Full Surgeon" (Hybrid Neuro-Symbolic Fixer) - **Recommended**
- Combine Geometric fixes (Option 1) with Content/Design suggestions (Option 2).
- **Workflow**:
    1. **Diagnose**: Run existing detectors.
    2. **Prescribe**: Generate a "Treatment Plan" (JSON with proposed fixes).
    3. **Operate**: Apply deterministic fixes automatically; present AI fixes for specific approval.
- **Pros**: Most comprehensive, aligns with "Doctor" metaphor.
- **Cons**: Most complex to implement.

## Recommendation
**Option 3 (The Full Surgeon)**.
Build a `remediators/` module that mirrors the `detectors/` module. Each error type should have a corresponding `fix()` strategy.

## Acceptance Criteria
1.  **Backup Mechanism**: Always save `_fixed.pptx` separately.
2.  **Geometric Fixes**:
    *   `fix_alignment()`: Snap near-aligned elements to the mean coordinate.
    *   `fix_aspect_ratio()`: Reset image dimensions to native ratio (maintain width or height).
    *   `fix_margin()`: Nudge elements into safe zone (if possible without overlap).
3.  **Content Fixes**:
    *   `fix_hierarchy()`: Standardize font sizes (e.g., all titles to 32pt).
4.  **Integration**: Add `--fix` flag to `main.py` that applies safe fixes and reports on unsafe ones.
