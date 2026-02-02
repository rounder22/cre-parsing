# Commercial Real Estate Document Parser

A comprehensive tool for extracting key underwriting information from PDF, Word, and Excel documents for commercial real estate investment analysis.

## Features

### Advanced Data Extraction with OpenAI
- **GPT-4 Powered**: Uses OpenAI's latest models for advanced document understanding
- **Structured JSON Output**: Guaranteed schema compliance with JSON Mode
- **Confidence Scoring**: Get extraction confidence metrics and identify missing fields
- **Intelligent Fallback**: Automatically uses regex extraction if OpenAI is unavailable
- **Flexible Configuration**: Choose between OpenAI or regex extraction per document

### Document Parsing
- **PDF Support**: Extract text, tables, and metadata from PDF documents
- **Word Support**: Parse .docx files to extract paragraphs, tables, and formatting
- **Excel Support**: Extract data from multiple sheets with detailed sheet information

### CRE-Specific Data Extraction
The tool automatically identifies and extracts:

#### Property Details
- Address and location information
- Property type and asset class
- Square footage and unit count
- Year built and occupancy rates

#### Financial Metrics
- Net Operating Income (NOI)
- Cap rate and capitalization data
- Purchase and appraised values
- Annual gross income and operating expenses
- Debt service and DSCR
- Internal Rate of Return (IRR)

#### Loan Details
- Loan amount and terms
- Interest rates
- Loan maturity dates
- Lender information
- Loan-to-Value (LTV) ratios

#### Tenant Information
- Major tenant names
- Lease terms
- Tenant quality and credit assessment

#### Market Analysis
- Market and submarket identification
- Comparable property information
- Market trends and analysis

#### Risk Factors
- Identified risks and concerns
- Mitigation strategies

## Installation

### Prerequisites
- Python 3.7+
- pip package manager
- (Optional) OpenAI API key for advanced extraction

### Setup

1. Clone the repository:
```bash
cd cre-parsing
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Configure OpenAI Integration:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

See [OPENAI_INTEGRATION.md](OPENAI_INTEGRATION.md) for detailed setup and configuration.

## Running the Application

### Development Mode
```bash
python run.py
```


The application will start on `http://localhost:5000`

## Usage

### Web Interface

1. **Upload Documents**
   - Drag and drop files into the upload area, or click to browse
   - Supports multiple file uploads simultaneously
   - File types: PDF, Word (.docx), Excel (.xlsx)

2. **View Results**
   - Extracted data is displayed in organized categories
   - Each metric is clearly labeled with extracted values
   - "Not found" indicates metrics not detected in the document

3. **Export Results**
   - Click "Export Results" to download all extracted data as JSON
   - Useful for further analysis or integration with underwriting systems

4. **Clear Results**
   - Click "Clear Results" to reset the interface and upload new files

### API Endpoints

#### Upload Single File
```
POST /api/upload
Content-Type: multipart/form-data

Parameters:
- file: Binary file data (PDF, DOCX, or XLSX)
```

#### Batch Upload
```
POST /api/batch-upload
Content-Type: multipart/form-data

Parameters:
- files: Multiple binary files
```

#### Export Results
```
POST /api/export
Content-Type: application/json

Body: { extracted results data }
```

## Project Structure

```
cre-parsing/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── routes.py                # API endpoints
│   ├── templates/
│   │   └── index.html           # Web interface
│   ├── static/
│   │   ├── style.css            # Frontend styling
│   │   └── script.js            # Frontend logic
│   └── parsers/
│       ├── __init__.py
│       ├── base_parser.py       # Base parser class
│       ├── pdf_parser.py        # PDF parsing logic
│       ├── word_parser.py       # Word document parsing
│       ├── excel_parser.py      # Excel parsing
│       └── extractor.py         # CRE metric extraction
├── uploads/                     # Uploaded files directory
├── run.py                       # Application entry point
└── requirements.txt             # Python dependencies
```

## Technical Stack

### Backend
- **Flask**: Web framework for API and routing
- **pdfplumber**: PDF text and table extraction
- **python-docx**: Word document parsing
- **openpyxl**: Excel file handling
- **pandas**: Data manipulation and analysis
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling and responsive design
- **Vanilla JavaScript**: Client-side logic

## Key Components

### DataExtractor (`extractor.py`)
The core component that:
- Loads documents using appropriate parsers
- Extracts raw text from documents
- Applies regex pattern matching to identify CRE-specific metrics
- Returns structured data with extracted financial and property information

### Parsers
- **PDFParser**: Extracts text and tables from PDF files
- **WordParser**: Processes .docx files with paragraph and table extraction
- **ExcelParser**: Handles multi-sheet Excel workbooks

## Customization

### Adding New Metrics

Edit the `DataExtractor` class in `app/parsers/extractor.py` to add new metrics:

```python
def _extract_property_details(self, text: str) -> Dict[str, Optional[str]]:
    details = {
        'new_metric': self._find_pattern(text, r'(?:Pattern|Alternative):\s*([^\n]+)', 0),
        # ... existing metrics
    }
    return {k: v for k, v in details.items() if v}
```

### Modifying Extraction Patterns

Update regex patterns in extraction methods to match your document formats:

```python
self._find_pattern(text, r'Your Pattern Here', 0)
```

## Supported File Formats

| Format | Extension | Parser |
|--------|-----------|--------|
| PDF | .pdf | pdfplumber |
| Word | .docx | python-docx |
| Excel | .xlsx | openpyxl |

## Limitations

- Maximum file size: 50MB
- Excel files limited to standard .xlsx format (not .xls)
- PDF extraction quality depends on document structure
- Pattern matching works best with consistently formatted documents

## Future Enhancements

- Machine learning-based data extraction
- Support for scanned/image-based PDFs (OCR)
- Integration with CRE databases
- Advanced financial modeling features
- Multi-language support
- Template-based extraction for consistent document formats

## Troubleshooting

### Common Issues

**"File type not supported"**
- Ensure file extension matches supported types (PDF, DOCX, XLSX)
- Check that files are not corrupted

**"Error parsing document"**
- Some PDFs may have encryption or unusual formatting
- Try converting to different format or checking document integrity

**Missing metrics in results**
- Metrics are extracted using pattern matching
- If document uses different terminology, patterns may not match
- Check document formatting and consistency

## License

This project is provided as-is for commercial real estate analysis.

## Support

For issues, questions, or feature requests, please refer to the project documentation or contact the development team.
