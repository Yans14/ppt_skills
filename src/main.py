from src.parsers.xml_parser import parse_presentation
from src.detectors.hierarchy import detect_hierarchy_violations
from src.detectors.margin import detect_margin_violations
from src.detectors.contrast import detect_contrast_violations
from src.detectors.aspect_ratio import detect_aspect_ratio_violations
from src.detectors.alignment import detect_alignment_violations
from src.reporter import generate_report, report_to_json


def analyze(pptx_path: str) -> str:
    slides = parse_presentation(pptx_path)
    
    errors = []
    errors.extend(detect_hierarchy_violations(slides))
    errors.extend(detect_margin_violations(slides))
    errors.extend(detect_contrast_violations(slides))
    errors.extend(detect_aspect_ratio_violations(slides, pptx_path))
    errors.extend(detect_alignment_violations(slides))

    report = generate_report(slides, errors)
    return report_to_json(report)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <pptx_path>")
        sys.exit(1)
    
    result = analyze(sys.argv[1])
    print(result)
