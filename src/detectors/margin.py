from src.models import SlideNode, LayoutError, ErrorType, Severity


def detect_margin_violations(slides: list[SlideNode], margin_pct: float = 0.05) -> list[LayoutError]:
    errors = []

    for slide in slides:
        margin_x = slide.width * margin_pct
        margin_y = slide.height * margin_pct
        x_min, x_max = margin_x, slide.width - margin_x
        y_min, y_max = margin_y, slide.height - margin_y

        all_elements = slide.text_elements + slide.image_elements
        total_area = 0

        for elem in all_elements:
            bbox = elem.bbox
            total_area += bbox.width * bbox.height

            if bbox.x < x_min or bbox.x2 > x_max or bbox.y < y_min or bbox.y2 > y_max:
                errors.append(LayoutError(
                    type=ErrorType.MARGIN,
                    severity=Severity.WARNING,
                    elements=[elem.id],
                    message=f"Element outside safe zone (5% margin)"
                ))

        slide_area = slide.width * slide.height
        coverage = total_area / slide_area if slide_area > 0 else 0

        if coverage > 0.7:
            errors.append(LayoutError(
                type=ErrorType.MARGIN,
                severity=Severity.INFO,
                elements=[],
                message=f"Slide {slide.index} is overcrowded ({coverage:.0%} coverage)"
            ))

    return errors
