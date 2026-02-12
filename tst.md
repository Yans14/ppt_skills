from pptx import Presentation
from pptx.oxml.ns import qn
from lxml import etree
import copy

def transfer_layout(source_path, target_path, output_path, source_layout_index=0):
    source_prs = Presentation(source_path)
    target_prs = Presentation(target_path)

    source_layout = source_prs.slide_layouts[source_layout_index]
    source_master = source_layout.slide_master

    # ── Step 1: Clone the source master part into target ────────────────────
    cloned_master_elm = copy.deepcopy(source_master.element)
    cloned_layout_elm = copy.deepcopy(source_layout.element)

    # ── Step 2: Add master to target presentation ───────────────────────────
    # The cleanest way: add as a new slide master
    target_master = target_prs.slide_masters[0]  # use existing master as base
    
    # Inject the cloned layout XML into the target master
    # Remove existing sldLayoutIdLst entries if you want a clean slate (optional)
    sp_tree = target_master.element
    
    # Add layout to the master's part
    from pptx.opc.part import Part
    from pptx.opc.packuri import PackURI
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT

    layout_uri = PackURI(f'/ppt/slideLayouts/slideLayoutCustom.xml')
    
    content_type = (
        'application/vnd.openxmlformats-officedocument'
        '.presentationml.slideLayout+xml'
    )
    
    new_layout_part = Part(layout_uri, content_type, 
                           etree.tostring(cloned_layout_elm), 
                           target_prs.part.package)

    # Relate the new layout to the target master
    rId = target_master.part.relate_to(new_layout_part, 
          'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout')

    # ── Step 3: Point target slides to the new layout ───────────────────────
    for slide in target_prs.slides:
        slide_part = slide.part
        for rel in slide_part.rels.values():
            if "slideLayout" in rel.reltype:
                rel._target = new_layout_part
                break

    target_prs.save(output_path)
    print(f"Saved to {output_path}")


# Usage
transfer_layout(
    source_path="source.pptx",
    target_path="target.pptx",
    output_path="result.pptx",
    source_layout_index=1       # which layout from source to copy
)
