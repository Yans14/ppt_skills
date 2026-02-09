from src.models import SlideNode, LayoutError, ErrorType, Severity


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def linearize(c: int) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = [linearize(c) for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(l1: float, l2: float) -> float:
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def detect_contrast_violations(slides: list[SlideNode], min_ratio: float = 4.5) -> list[LayoutError]:
    errors = []

    for slide in slides:
        if not slide.background_color:
            continue

        bg_lum = luminance(hex_to_rgb(slide.background_color))

        for elem in slide.text_elements:
            if not elem.style.color:
                continue

            text_lum = luminance(hex_to_rgb(elem.style.color))
            ratio = contrast_ratio(text_lum, bg_lum)

            if ratio < min_ratio:
                errors.append(LayoutError(
                    type=ErrorType.CONTRAST,
                    severity=Severity.CRITICAL,
                    elements=[elem.id],
                    message=f"Contrast ratio {ratio:.1f}:1 fails WCAG AA (min {min_ratio}:1)"
                ))

    return errors
