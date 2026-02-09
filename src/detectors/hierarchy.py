from collections import Counter
from src.models import SlideNode, LayoutError, ErrorType, Severity


def detect_hierarchy_violations(slides: list[SlideNode]) -> list[LayoutError]:
    errors = []
    all_styles = []

    for slide in slides:
        for elem in slide.text_elements:
            if elem.style.font_size:
                all_styles.append((elem.id, elem.slide_index, elem.style.font_size))

    if len(all_styles) < 5:
        return errors

    sizes = [s[2] for s in all_styles]
    size_counts = Counter(sizes)
    common_sizes = {size for size, count in size_counts.items() if count >= 2}

    for elem_id, slide_idx, font_size in all_styles:
        if font_size not in common_sizes:
            closest = min(common_sizes, key=lambda x: abs(x - font_size), default=None)
            if closest and abs(font_size - closest) <= 2:
                errors.append(LayoutError(
                    type=ErrorType.HIERARCHY,
                    severity=Severity.WARNING,
                    elements=[elem_id],
                    message=f"Font size {font_size}pt is close but not matching {closest}pt"
                ))

    return errors
