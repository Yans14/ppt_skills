# PowerPoint Layout Error Detection

Detects layout errors in PowerPoint presentations using geometric rules and VLM validation.

## Detectors

- **Hierarchy**: Style inconsistencies (e.g., 31pt vs 32pt fonts)
- **Margin**: Elements outside safe zone, overcrowding
- **Contrast**: WCAG AA compliance (4.5:1 ratio)
- **Aspect Ratio**: Distorted images (>5% tolerance)
- **Alignment**: Near-aligned elements

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py presentation.pptx
```

## Environment Variables (for VLM)

```bash
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

## Output

JSON report grouped by slide with error type, severity, elements, and message.
