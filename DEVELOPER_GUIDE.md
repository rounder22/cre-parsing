# CRE Parsing Tool - Developer Guide

## System Status

✅ **All systems operational** - Verification script confirms all components are installed and working correctly.

## Quick Access

### Running the Application
```bash
python run.py
```
Access at: **http://localhost:5000**

### Verification
```bash
python verify.py
```

### Creating Sample Documents
```bash
python create_samples.py
```

## Architecture Overview

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Parsers**: pdfplumber, python-docx, openpyxl
- **Data Processing**: pandas for analysis
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: REST API with JSON responses

### Component Architecture

```
User Interface (HTML/CSS/JS)
        ↓
  Flask Routes (API)
        ↓
  DataExtractor (Main Logic)
        ↓
  Specialized Parsers (PDF/Word/Excel)
        ↓
  Document Files
```

## Document Flow

### Upload Process
1. User uploads file(s) via web interface
2. Flask receives multipart/form-data request
3. File validated (type, size)
4. File saved to `uploads/` directory
5. Appropriate parser initialized based on file extension

### Processing Pipeline
```
Raw Document
    ↓
Parser (extracts text, tables, metadata)
    ↓
Text Content
    ↓
DataExtractor (applies regex patterns)
    ↓
Structured JSON with extracted metrics
    ↓
Web Interface (displays results)
```

### Data Extraction Flow

The `DataExtractor` class applies intelligent pattern matching:

```python
Text Document
    ↓
Property Details Extractor
    ├─ Address patterns
    ├─ Property type patterns
    ├─ Size patterns
    └─ ...
    ↓
Financial Metrics Extractor
    ├─ NOI patterns
    ├─ Cap rate patterns
    ├─ Valuation patterns
    └─ ...
    ↓
Loan Details Extractor
    ├─ Loan amount patterns
    ├─ Rate patterns
    └─ ...
    ↓
[Continue for other categories]
    ↓
Compiled Results (JSON)
```

## File Organization

### Core Application Files
| File | Purpose |
|------|---------|
| `run.py` | Application entry point |
| `app/__init__.py` | Flask app factory |
| `app/routes.py` | API endpoints & request handling |

### Parser System
| File | Purpose |
|------|---------|
| `app/parsers/base_parser.py` | Abstract base class for all parsers |
| `app/parsers/pdf_parser.py` | PDF extraction logic |
| `app/parsers/word_parser.py` | Word document extraction |
| `app/parsers/excel_parser.py` | Excel file processing |
| `app/parsers/extractor.py` | CRE-specific metric extraction |

### Frontend Files
| File | Purpose |
|------|---------|
| `app/templates/index.html` | Web interface markup |
| `app/static/style.css` | Responsive styling |
| `app/static/script.js` | Client-side logic & AJAX |

## API Endpoints

### POST /api/upload
Single file upload endpoint.

**Request:**
```
POST /api/upload
Content-Type: multipart/form-data

file: Binary file data
```

**Response:**
```json
{
  "file_info": {
    "file_type": "pdf|word|excel",
    "pages": 5,
    "file_path": "uploads/document.pdf"
  },
  "extracted_metrics": {
    "property_details": { ... },
    "financial_metrics": { ... },
    "loan_details": { ... },
    "tenant_info": { ... },
    "market_analysis": { ... },
    "risk_factors": { ... }
  }
}
```

### POST /api/batch-upload
Multiple file upload endpoint.

**Request:**
```
POST /api/batch-upload
Content-Type: multipart/form-data

files: Multiple binary files
```

**Response:**
```json
{
  "results": [
    { /* First file results */ },
    { /* Second file results */ }
  ],
  "errors": [
    { "file": "filename", "error": "Error message" }
  ]
}
```

### POST /api/export
Export extracted data as JSON file.

**Request:**
```
POST /api/export
Content-Type: application/json

{ /* Extracted data object */ }
```

**Response:** JSON file download

## Customization Guide

### Adding New Metrics

1. **Identify the pattern** in your documents
2. **Add extraction method** to `DataExtractor` class
3. **Define regex pattern** that matches the metric
4. **Test** with sample documents

Example:
```python
def _extract_property_details(self, text: str) -> Dict[str, Optional[str]]:
    details = {
        'new_metric': self._find_pattern(
            text, 
            r'(?:New Metric Label):\s*([^\n]+)', 
            0
        ),
    }
    return {k: v for k, v in details.items() if v}
```

### Modifying Regex Patterns

Current patterns in `extractor.py`:
```python
# NOI extraction
r'(?:Net Operating Income|NOI):\s*\$?([\d,]+\.?\d*)'

# Cap Rate extraction
r'(?:Cap Rate|Capitalization Rate):\s*([\d.]+)%?'
```

Customize for your documents:
```python
# Your custom pattern
r'Your Custom Label:\s*([^\n]+)'

# Multiple variations
r'(?:Label1|Label2|Label3):\s*([^\n]+)'

# Extract from tables
r'NOI\s+\$?([\d,]+\.?\d*)'
```

### Adding Support for New File Types

1. Create new parser in `app/parsers/`:
```python
from app.parsers.base_parser import BaseParser

class NewFormatParser(BaseParser):
    def parse(self) -> Dict[str, Any]:
        # Your parsing logic
        pass
    
    def extract_text(self) -> str:
        # Extract text
        pass
```

2. Update `app/parsers/__init__.py`:
```python
from app.parsers.new_format_parser import NewFormatParser
```

3. Update `app/parsers/extractor.py`:
```python
def _get_parser(self):
    if self.file_type.lower() == 'new_format':
        return NewFormatParser(self.file_path)
```

4. Update `app/routes.py`:
```python
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'new_ext'}

def get_file_type(filename):
    # Add new format mapping
    if ext == 'new_ext':
        return 'new_format'
```

## Parser Implementation Details

### PDF Parser (pdfplumber)
- Extracts text from each page
- Identifies and extracts tables
- Preserves metadata
- Handles multi-page documents

### Word Parser (python-docx)
- Extracts paragraphs with styling
- Identifies document structure (headings, sections)
- Extracts tables with cell-level data
- Preserves formatting information

### Excel Parser (openpyxl)
- Reads multiple sheets
- Maintains sheet structure
- Provides cell-level data access
- Returns sheet dimensions and statistics

## Regex Pattern Guide

### Basic Patterns

**Dollar amounts:**
```regex
\$?([\d,]+\.?\d*)
```

**Percentages:**
```regex
([\d.]+)%?
```

**Dates:**
```regex
(\d{1,2}/\d{1,2}/\d{4})
```

**Years:**
```regex
(\d{4})
```

**Text until newline:**
```regex
([^\n]+)
```

### Complex Patterns

**Case-insensitive with alternatives:**
```regex
(?i)(?:label1|label2|label3):\s*([^\n]+)
```

**Multiple possible formats:**
```regex
(?:Format1:\s*([^\n]+)|Format2\s*([^\n]+))
```

**Multiline patterns:**
```regex
(?:Label1|Label2):\s*\n\s*([^\n]+)
```

## Performance Optimization

### File Size Limits
Current: 50MB per file

To increase, edit `app/__init__.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### Batch Processing Optimization
- Process files sequentially (current)
- Consider async processing for large batches
- Implement caching for repeated documents

### Pattern Matching
- More specific patterns = faster matching
- Order patterns from most to least specific
- Cache compiled regex patterns if needed

## Debugging

### Enable Debug Logging
Edit `run.py`:
```python
app = create_app()
app.logger.setLevel(logging.DEBUG)
```

### Test Individual Parsers
```python
from app.parsers.pdf_parser import PDFParser

parser = PDFParser('path/to/file.pdf')
data = parser.parse()
print(data)
```

### Test DataExtractor
```python
from app.parsers.extractor import DataExtractor

extractor = DataExtractor('path/to/file.pdf', 'pdf')
results = extractor.extract_all()
print(results)
```

## Common Issues & Solutions

### Issue: File upload fails
**Solution**: Check file size, extension, and `uploads/` folder permissions

### Issue: Metrics not extracted
**Solution**: Update regex patterns in `extractor.py` to match your document format

### Issue: Slow processing
**Solution**: Optimize regex patterns, reduce file size, or implement async processing

### Issue: Memory errors with large files
**Solution**: Increase available RAM or process files in chunks

## Testing Strategy

### Unit Tests
Test individual parsers with sample documents:
```python
def test_pdf_parser():
    parser = PDFParser('samples/test.pdf')
    data = parser.parse()
    assert data['pages'] > 0
```

### Integration Tests
Test full extraction pipeline:
```python
def test_extraction():
    extractor = DataExtractor('samples/test.pdf', 'pdf')
    results = extractor.extract_all()
    assert 'extracted_metrics' in results
```

### Manual Testing
1. Run `verify.py` to confirm setup
2. Use sample documents to test extraction
3. Upload your own documents to validate patterns
4. Export and verify JSON structure

## Deployment Considerations

### Security
- Validate file uploads (type, size, content)
- Sanitize file paths
- Implement rate limiting
- Use HTTPS in production

### Performance
- Implement caching
- Use async processing for batch uploads
- Monitor resource usage
- Implement request timeouts

### Scalability
- Consider async workers (Celery)
- Implement job queue (Redis)
- Load balance API requests
- Use CDN for static assets

## Code Style

### Python Standards
- PEP 8 compliance
- Type hints recommended
- Docstring for all functions/classes
- Clear variable naming

### Documentation
- Inline comments for complex logic
- Docstrings explaining parameters and returns
- README files in subdirectories
- API documentation in code

## Version Control

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-metric

# Commit changes
git commit -m "Add new metric extraction"

# Push to remote
git push origin feature/new-metric
```

### .gitignore
Already configured to exclude:
- Virtual environment (`.venv/`)
- Uploaded files (`uploads/`)
- Python cache (`__pycache__/`)
- Log files

## Support & Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [python-docx](https://python-docx.readthedocs.io/)
- [openpyxl](https://openpyxl.readthedocs.io/)

### Python Regular Expressions
- [Python regex documentation](https://docs.python.org/3/library/re.html)
- [regex101.com](https://regex101.com/) - Online regex tester

## Tools & Utilities

### Verification Script
```bash
python verify.py
```
Checks all components and dependencies

### Sample Generator
```bash
python create_samples.py
```
Creates test documents

### Application Runner
```bash
python run.py
```
Starts the Flask development server

---

**Ready to customize and deploy your CRE parser!**
