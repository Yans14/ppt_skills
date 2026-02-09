from pptx import Presentation
from pptx.util import Emu
from pptx.dml.color import RGBColor
from src.models import SlideNode, TextElement, ImageElement, TextStyle, BoundingBox


def emu_to_px(emu: int) -> float:
    return emu / 914400 * 96


def rgb_to_hex(rgb: RGBColor) -> str:
    return f"#{rgb.red:02x}{rgb.green:02x}{rgb.blue:02x}"


def parse_presentation(path: str) -> list[SlideNode]:
    prs = Presentation(path)
    slide_width = emu_to_px(prs.slide_width)
    slide_height = emu_to_px(prs.slide_height)
    slides = []

    for idx, slide in enumerate(prs.slides):
        node = SlideNode(index=idx, width=slide_width, height=slide_height)
        
        bg_color = None
        if slide.background.fill.type is not None:
            try:
                bg_color = rgb_to_hex(slide.background.fill.fore_color.rgb)
            except:
                pass
        node.background_color = bg_color

        for shape in slide.shapes:
            shape_id = str(shape.shape_id)
            bbox = BoundingBox(
                x=emu_to_px(shape.left),
                y=emu_to_px(shape.top),
                width=emu_to_px(shape.width),
                height=emu_to_px(shape.height)
            )

            if shape.has_text_frame:
                text = shape.text_frame.text
                style = TextStyle()
                
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.size:
                            style.font_size = run.font.size.pt
                        if run.font.name:
                            style.font_name = run.font.name
                        if run.font.bold:
                            style.bold = run.font.bold
                        if run.font.color and run.font.color.rgb:
                            style.color = rgb_to_hex(run.font.color.rgb)
                        break
                    break

                node.text_elements.append(TextElement(
                    id=shape_id,
                    slide_index=idx,
                    text=text,
                    style=style,
                    bbox=bbox
                ))

            if hasattr(shape, "image"):
                node.image_elements.append(ImageElement(
                    id=shape_id,
                    slide_index=idx,
                    bbox=bbox,
                    rendered_width=bbox.width,
                    rendered_height=bbox.height
                ))

        slides.append(node)

    return slides
