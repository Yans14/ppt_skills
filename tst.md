from pptx import Presentation
from pptx.opc.package import Part
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
import copy

def transfer_layout(source_path, target_path, output_path, source_layout_index=0):
    source_prs = Presentation(source_path)
    target_prs = Presentation(target_path)

    source_layout = source_prs.slide_layouts[source_layout_index]
    source_layout_part = source_layout.part  # SlideLayoutPart

    # ── For each slide, drop old layout rel and add new one ─────────────────
    layout_reltype = (
        "http://schemas.openxmlformats.org/officeDocument/2006/"
        "relationships/slideLayout"
    )

    for slide in target_prs.slides:
        slide_part = slide.part
        rels = slide_part.rels

        # Remove the existing slideLayout relationship
        for rId, rel in list(rels.items()):
            if "slideLayout" in rel.reltype:
                rels.pop(rId)
                break

        # Add the new layout part as a relationship
        rels.get_or_add(layout_reltype, source_layout_part)

    target_prs.save(output_path)
