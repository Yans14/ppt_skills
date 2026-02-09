# Open Source References for Layout Error Detection

Research into available open-source libraries that could extend this project.

## 1. PPTChecker
- **URL**: https://github.com/nsemmer/PPTChecker
- **Purpose**: dedicated tool for verifying PowerPoint quality guidelines.
- **Key Features**:
  - Text density analysis (detecting "walls of text")
  - Slide numbering checks
  - Font size consistency
- **Integration Potential**: Port their "Text Density" algorithm to `detectors/density.py`.

## 2. LayoutParser
- **URL**: https://layout-parser.readthedocs.io/
- **Purpose**: Deep Learning based document layout analysis (DL-based).
- **Key Features**:
  - Detects Title, Text, Figure, List, Table in images.
- **Integration Potential**: Use if we render slides to images (via `unstructured` or `pdf2image`). Can cross-verify if a "Title" detected by AI matches the XML title.

## 3. TextStat
- **URL**: https://github.com/shivam5992/textstat
- **Purpose**: Calculate readability statistics (Flesch Reading Ease, etc.).
- **Integration Potential**: Add a `readability.py` detector to flag complex language or too-long sentences on slides.

## 4. Unstructured
- **URL**: https://unstructured.io/
- **Purpose**: Ingesting and processing unstructured documents (including PPTX).
- **Status**: Already included in `requirements.txt`.
- **Use Case**: robust text cleaning and partition logic if `python-pptx` misses complex groupings.
