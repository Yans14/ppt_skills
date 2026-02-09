from enum import Enum
from typing import Optional
from pydantic import BaseModel


class ErrorType(str, Enum):
    HIERARCHY = "HIERARCHY"
    MARGIN = "MARGIN"
    CONTRAST = "CONTRAST"
    ASPECT_RATIO = "ASPECT_RATIO"
    ALIGNMENT = "ALIGNMENT"
    OVERLAP = "OVERLAP"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

    @property
    def x2(self) -> float:
        return self.x + self.width

    @property
    def y2(self) -> float:
        return self.y + self.height


class TextStyle(BaseModel):
    font_size: Optional[float] = None
    font_name: Optional[str] = None
    bold: bool = False
    color: Optional[str] = None


class TextElement(BaseModel):
    id: str
    slide_index: int
    text: str
    style: TextStyle
    bbox: BoundingBox


class ImageElement(BaseModel):
    id: str
    slide_index: int
    bbox: BoundingBox
    rendered_width: float
    rendered_height: float
    native_width: Optional[float] = None
    native_height: Optional[float] = None


class SlideNode(BaseModel):
    index: int
    width: float
    height: float
    text_elements: list[TextElement] = []
    image_elements: list[ImageElement] = []
    background_color: Optional[str] = None


class LayoutError(BaseModel):
    type: ErrorType
    severity: Severity
    elements: list[str]
    message: str


class SlideReport(BaseModel):
    slide_index: int
    errors: list[LayoutError] = []


class ErrorReport(BaseModel):
    slides: dict[str, SlideReport] = {}
