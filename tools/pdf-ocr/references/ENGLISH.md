# PDF OCR Skill（English Version）

> 英文版内容由 `SKILL.md` 按渐进式披露拆分（v2.5.0 同步拆分）；中文团队按需加载，默认读取 `SKILL.md` 中文版。

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Quick Start](#quick-start)
- [Command Line Usage](#command-line-usage)
- [Advanced Usage Examples](#advanced-usage-examples)
- [Supported File Formats](#supported-file-formats)
- [Output Format](#output-format)
- [Use Cases](#use-cases)
- [Notes](#notes)
- [Prompt Words for Different Engines](#prompt-words-for-different-engines)
- [🔧 Technical Implementation](#-technical-implementation)
- [🎯 Best Practices](#-best-practices)
- [Troubleshooting](#troubleshooting)

### Features

- Support text extraction from scanned PDF files
- Support text recognition from multiple image formats (JPG, PNG, BMP, GIF, TIFF, WEBP)
- **Quadruple-engine support**: RapidOCR (local), RapidDoc (enhanced), PaddleOCR (local), and SiliconFlow API (cloud)
- Support Chinese and English text recognition
- Maintain text order and structure
- Automatically convert PDF pages to images for recognition
- Intelligent engine switching: automatically switch to SiliconFlow API when RapidOCR initialization fails

### Installation

#### Dependencies

```bash
pip install pymupdf pillow requests python-dotenv
```

#### Optional Dependencies (Recommended)

Install RapidOCR for local recognition capability:

```bash
pip install rapidocr_onnxruntime
```

### Environment Configuration

1. Copy `.env.example` file and rename it to `.env`
2. Configure the following options as needed:

```env
# OCR engine selection
# - "rapid": Use RapidOCR local engine (default, no API key required)
# - "rapidoc": Use RapidDoc enhanced engine (no API key required)
# - "paddle": Use PaddleOCR local engine (no API key required)
# - "siliconflow": Use SiliconFlow API engine (API key required)
OCR_ENGINE=rapid

# If using SiliconFlow API engine, configure the following options:
SILICON_FLOW_API_KEY=your_api_key_here
SILICON_FLOW_OCR_MODEL=deepseek-ai/DeepSeek-OCR
```

### Quick Start

#### Using Default Engine (RapidOCR Local Recognition)

```python
# Import OCR processor
from scripts.pdf_ocr_processor import PDFOCRProcessor

# Create processor instance (default uses RapidOCR)
processor = PDFOCRProcessor()

# Perform PDF OCR recognition
result = processor.ocr_pdf('path/to/your/scanned.pdf')

# Get recognition result
print(f"Recognition completed, total {result['page_count']} pages")
print(f"Engine used: {result['engine']}")
print(result['text'])
```

#### Using SiliconFlow API Engine

```python
# Import OCR processor
from scripts.pdf_ocr_processor import PDFOCRProcessor

# Create processor instance, specify to use SiliconFlow API
processor = PDFOCRProcessor(engine="siliconflow")

# Perform PDF OCR recognition
result = processor.ocr_pdf('path/to/your/scanned.pdf')

# Get recognition result
print(f"Recognition completed, total {result['page_count']} pages")
print(result['text'])
```

#### Recognizing Image Files

```python
# Import OCR processor
from scripts.pdf_ocr_processor import PDFOCRProcessor

# Create processor instance
processor = PDFOCRProcessor()  # or PDFOCRProcessor(engine="siliconflow")

# Perform image OCR recognition
result = processor.ocr_image_file('path/to/your/image.jpg')

# Get recognition result
print(f"Recognition result: {result['text']}")
```

### Command Line Usage

```bash
# Use default RapidOCR engine
python pdf_ocr_processor.py your_document.pdf

# Use SiliconFlow API engine
python pdf_ocr_processor.py your_document.pdf siliconflow

# Use RapidDoc enhanced engine
python pdf_ocr_processor.py your_document.pdf rapidoc

# Use PaddleOCR engine
python pdf_ocr_processor.py your_document.pdf paddle
```

### Advanced Usage Examples

#### Batch Processing Multiple PDF Files

```python
import os
from scripts.pdf_ocr_processor import PDFOCRProcessor

# Create processor instance
processor = PDFOCRProcessor()

# Batch process all PDF files in directory
pdf_dir = "path/to/pdf/files"
output_dir = "path/to/output"
os.makedirs(output_dir, exist_ok=True)

for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}.txt")
        
        print(f"Processing file: {pdf_file}")
        try:
            result = processor.ocr_pdf(pdf_path)
            
            # Save recognition result to text file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"=== PDF OCR Recognition Result ===\n")
                f.write(f"File name: {pdf_file}\n")
                f.write(f"Pages: {result['page_count']}\n")
                f.write(f"Engine used: {result['engine']}\n\n")
                f.write(result['text'])
            
            print(f"Processing completed, result saved to: {output_path}")
        except Exception as e:
            print(f"Processing failed: {e}")
```

#### Using Both Engines

```python
from scripts.pdf_ocr_processor import PDFOCRProcessor

def process_with_best_engine(pdf_path):
    """Try using RapidOCR, if not good enough then use SiliconFlow API"""
    # First use RapidOCR local engine
    rapid_processor = PDFOCRProcessor(engine="rapid")
    rapid_result = rapid_processor.ocr_pdf(pdf_path)
    
    # Simple evaluation of recognition effect (e.g., check recognized text length)
    text_length = len(rapid_result['text'])
    
    if text_length < 100:  # If recognized text is too short, may not be good enough
        print("RapidOCR recognition effect may not be good enough, trying SiliconFlow API...")
        silicon_processor = PDFOCRProcessor(engine="siliconflow")
        silicon_result = silicon_processor.ocr_pdf(pdf_path)
        return silicon_result
    else:
        return rapid_result

# Usage example
result = process_with_best_engine('path/to/your/document.pdf')
print(f"Recognition completed, engine used: {result['engine']}")
print(result['text'])
```

### Supported File Formats

- **PDF files**: .pdf
- **Image files**: .jpg, .jpeg, .png, .bmp, .gif, .tiff, .webp

### Output Format

```python
{
    "text": "Recognized full text content",
    "page_count": number_of_pages,  # Always 1 for image files
    "engine": "rapid" | "rapidoc" | "paddle" | "siliconflow"  # OCR engine used
}
```

### Use Cases

- Processing scanned contracts, agreements and other documents
- Extracting text from photocopied books and reports
- Processing PDF files with non-copyable text
- Batch processing scanned PDF documents
- Recognizing text in screenshots and scanned images
- Processing handwritten or printed text in images

### Notes

1. **RapidOCR Engine**:
   - Completely free, no network connection required
   - Model files will be automatically downloaded on first use
   - Recognition speed depends on CPU performance

2. **SiliconFlow API Engine**:
   - Requires a valid API key
   - May incur costs
   - Recognition speed depends on number of pages, image size, and network conditions

3. **RapidDoc Engine**:
   - Completely free, no network connection required
   - Supports layout analysis, table recognition, formula recognition, and reading order recovery
   - Provides more structured output including markdown format
   - Processing time may be longer than RapidOCR due to additional analysis

4. **PaddleOCR Engine**:
   - Completely free, no network connection required
   - Uses PP-OCRv5 model with high recognition accuracy
   - Model files will be automatically downloaded on first use
   - Supports text recognition for multiple languages and scenarios

4. Recognition accuracy may vary for complex scanned PDFs or images
5. It is recommended to use high-resolution scanned PDFs or images for better recognition results

### Prompt Words for Different Engines

When interacting with assistants in AI IDEs, you can use the following prompt words to specify different OCR engines:

#### 📍 Prompt Words for RapidOCR (Local Engine)
- "Use local OCR engine to process this PDF"
- "Recognize this file with RapidOCR"
- "Local processing, no API needed"
- "Quickly recognize this document"
- "Process this PDF offline"
- "Don't use SiliconFlow API, use local engine"

#### 📍 Prompt Words for SiliconFlow API (Cloud Engine)
- "Use SiliconFlow API to process this PDF"
- "Recognize this file with large model OCR"
- "High-precision recognition for this document"
- "Process complex scanned documents"
- "Use cloud OCR engine"
- "Use AI large model for recognition"

#### 📍 Prompt Words for RapidDoc (Enhanced Engine)
- "Use RapidDoc to process this PDF"
- "Recognize this file with enhanced OCR"
- "Process PDF with layout analysis"
- "Extract text with table recognition"
- "Use RapidDoc for better formatting"
- "Enhanced OCR with layout analysis"

#### 📍 Prompt Words for PaddleOCR (Local Engine)
- "Use PaddleOCR to process this PDF"
- "Recognize this file with PaddleOCR"
- "Use PP-OCRv5 model for recognition"
- "Use PaddleOCR for high-precision recognition"
- "PaddleOCR local processing"
- "Extract text using PaddleOCR engine"

#### 📍 Example Conversations

**Example 1: Using Local Engine**
```
User: Help me process this scanned PDF, use local OCR engine for quick recognition
Assistant: Sure, I'll use the RapidOCR local engine for you. Please provide the PDF file path.
```

**Example 2: Using Cloud Engine**
```
User: This PDF contains handwritten text, need high-precision recognition, use SiliconFlow API
Assistant: Understood, I'll use the SiliconFlow API large model for you. Please provide the PDF file path and your API key (if not already configured).
```

**Example 3: Automatic Selection**
```
User: Help me recognize this PDF, choose the most suitable engine
Assistant: I'll default to using the RapidOCR local engine for you. If the recognition effect is not ideal, we can try using SiliconFlow API.
```

### 🔧 Technical Implementation

When the AI assistant receives these prompt words, it will:

1. Parse the user's intent to determine the engine to use
2. Call PDFOCRProcessor(engine="rapid"), PDFOCRProcessor(engine="rapidoc"), PDFOCRProcessor(engine="paddle"), or PDFOCRProcessor(engine="siliconflow")
3. Execute OCR recognition and return the result

### 🎯 Best Practices

- **Clearly specify the engine**: If you have specific requirements for the engine, it's best to clearly state it in the prompt
- **Provide context**: Explaining the document type (e.g., handwritten, complex format) helps the assistant choose the appropriate engine
- **Test different engines**: For important documents, you can try both engines and compare the results

By using these prompt words, you can flexibly control the OCR engine selection when interacting with AI IDEs to get the best recognition results

### Troubleshooting

#### Common Issues and Solutions

1. **RapidOCR Initialization Failure**
   - Issue: `ModuleNotFoundError: No module named 'rapidocr_onnxruntime'`
   - Solution: Install RapidOCR dependency: `pip install rapidocr_onnxruntime`

2. **SiliconFlow API 401 Error**
   - Issue: `Unauthorized: 401 Client Error`
   - Solution: Check if the API key is correctly configured in the `.env` file

3. **PDF to Image Conversion Failure**
   - Issue: `ImportError: No module named 'fitz'`
   - Solution: Install PyMuPDF dependency: `pip install pymupdf`

4. **Empty Recognition Result**
   - Issue: Recognition result text length is 0
   - Solution:
     - Check if the PDF is a scanned version (non-text PDF)
     - Try using SiliconFlow API engine
     - Ensure the PDF or image is clear and readable
