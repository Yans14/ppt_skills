import json
from src.models import SlideNode, LayoutError, ErrorReport, SlideReport


def generate_report(slides: list[SlideNode], errors: list[LayoutError]) -> ErrorReport:
    report = ErrorReport()

    errors_by_slide = {}
    for error in errors:
        for elem_id in error.elements:
            for slide in slides:
                for e in slide.text_elements + slide.image_elements:
                    if e.id == elem_id:
                        slide_key = f"slide_{slide.index}"
                        if slide_key not in errors_by_slide:
                            errors_by_slide[slide_key] = []
                        if error not in errors_by_slide[slide_key]:
                            errors_by_slide[slide_key].append(error)
                        break

        if not error.elements:
            for slide in slides:
                slide_key = f"slide_{slide.index}"
                if slide_key not in errors_by_slide:
                    errors_by_slide[slide_key] = []
                if error not in errors_by_slide[slide_key]:
                    errors_by_slide[slide_key].append(error)

    for slide_key, slide_errors in errors_by_slide.items():
        idx = int(slide_key.split("_")[1])
        report.slides[slide_key] = SlideReport(slide_index=idx, errors=slide_errors)

    return report


def report_to_json(report: ErrorReport) -> str:
    data = {}
    for key, slide_report in report.slides.items():
        data[key] = {
            "errors": [
                {
                    "type": e.type.value,
                    "severity": e.severity.value,
                    "elements": e.elements,
                    "message": e.message
                }
                for e in slide_report.errors
            ]
        }
    return json.dumps(data, indent=2)
