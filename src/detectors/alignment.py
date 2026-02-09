import numpy as np
from src.models import SlideNode, LayoutError, ErrorType, Severity


def detect_alignment_violations(slides: list[SlideNode], threshold: float = 5.0) -> list[LayoutError]:
    errors = []

    for slide in slides:
        elements = slide.text_elements + slide.image_elements
        if len(elements) < 2:
            continue

        lefts = [(e.id, e.bbox.x) for e in elements]
        tops = [(e.id, e.bbox.y) for e in elements]
        rights = [(e.id, e.bbox.x2) for e in elements]
        centers_x = [(e.id, e.bbox.x + e.bbox.width / 2) for e in elements]

        for coords, edge_name in [(lefts, "left"), (tops, "top"), (rights, "right"), (centers_x, "center")]:
            if len(coords) < 2:
                continue

            values = np.array([c[1] for c in coords])
            
            for i, (elem_id, val) in enumerate(coords):
                diffs = np.abs(values - val)
                diffs[i] = np.inf
                min_diff = np.min(diffs)
                
                if 0 < min_diff <= threshold:
                    closest_idx = np.argmin(diffs)
                    errors.append(LayoutError(
                        type=ErrorType.ALIGNMENT,
                        severity=Severity.INFO,
                        elements=[elem_id, coords[closest_idx][0]],
                        message=f"Elements nearly aligned on {edge_name} (off by {min_diff:.1f}px)"
                    ))

    return errors
