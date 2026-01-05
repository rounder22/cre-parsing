# CRE Parser - Testing & Setup Guide

## Quick Start

### 1. Environment Setup

The Python virtual environment has been automatically configured. To activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 2. Install Dependencies

All dependencies have been pre-installed. Verify by running:
```bash
pip list
```

You should see:
- Flask 2.3.3
- pdfplumber 0.10.3
- python-docx 0.8.11
- openpyxl 3.1.2
- pandas 2.0.3

### 3. Start the Application

**Option A - Windows Batch Script:**
```bash
start.bat
```

**Option B - Manual Start:**
```bash
python run.py
```

The application will start on `http://localhost:5000`

## Testing the Application

### Using Sample Documents

Sample CRE documents have been created in the `samples/` folder:
- `Sample_CRE_Investment.docx` - Word document with CRE metrics
- `Sample_Financial_Model.xlsx` - Excel spreadsheet with financial data

### Test Workflow

1. **Start the Application**
   ```bash
   python run.py
   ```

2. **Open in Browser**
   Navigate to `http://localhost:5000`

3. **Upload Sample Files**
   - Click the upload area or drag-and-drop
   - Select one or both sample files
   - The parser will automatically extract all CRE metrics

4. **Review Extracted Data**
   - View organized metrics in the results panel
   - Property details, financial metrics, loan terms, etc.

5. **Export Results**
   - Click "Export Results" to download extracted data as JSON
   - Use JSON data for integration with underwriting systems

## API Testing

### Upload Single File
```bash
curl -X POST -F "file=@samples/Sample_CRE_Investment.docx" http://localhost:5000/api/upload
```

### Batch Upload
```bash
curl -X POST \
  -F "files=@samples/Sample_CRE_Investment.docx" \
  -F "files=@samples/Sample_Financial_Model.xlsx" \
  http://localhost:5000/api/batch-upload
```

## Extracted Metrics Reference

The parser extracts the following CRE-specific information:

### Property Details
- Address and location
- Property type
- Square footage
- Year built
- Number of units
- Occupancy rate

### Financial Metrics
- Net Operating Income (NOI)
- Cap Rate
- Purchase/Appraised Value
- Gross Income & Operating Expenses
- Debt Service Coverage Ratio (DSCR)
- Internal Rate of Return (IRR)

### Loan Details
- Loan amount and terms
- Interest rates
- Lender information
- Loan-to-Value (LTV) ratio

### Tenant Information
- Tenant names and details
- Lease terms
- Credit quality

### Market Analysis
- Market and submarket info
- Comparable properties
- Market trends

### Risk Factors
- Identified risks
- Mitigation strategies

## Project Structure

```
cre-parsing/
├── app/
│   ├── __init__.py                 # Flask app initialization
│   ├── routes.py                   # API endpoints
│   ├── parsers/
│   │   ├── base_parser.py         # Abstract base class
│   │   ├── pdf_parser.py          # PDF extraction
│   │   ├── word_parser.py         # Word document parsing
│   │   ├── excel_parser.py        # Excel file handling
│   │   └── extractor.py           # CRE metric extraction
│   ├── templates/
│   │   └── index.html             # Web interface
│   └── static/
│       ├── style.css              # Styling
│       └── script.js              # Client-side logic
├── uploads/                        # Uploaded files directory
├── samples/                        # Sample documents
├── run.py                         # Application entry point
├── create_samples.py              # Sample document generator
├── start.bat                      # Windows startup script
├── start.sh                       # Unix startup script
└── requirements.txt               # Python dependencies
```

## Customization

### Adding New Extraction Patterns

Edit `app/parsers/extractor.py`:

```python
def _extract_property_details(self, text: str) -> Dict[str, Optional[str]]:
    details = {
        'custom_metric': self._find_pattern(text, r'Your Regex Pattern', 0),
        # Add your patterns here
    }
    return {k: v for k, v in details.items() if v}
```

### Modifying the Frontend

- **UI Changes**: Edit `app/templates/index.html`
- **Styling**: Modify `app/static/style.css`
- **Logic**: Update `app/static/script.js`

### Adding Support for Additional File Types

1. Create a new parser in `app/parsers/`:
   ```python
   from app.parsers.base_parser import BaseParser
   
   class NewFormatParser(BaseParser):
       def parse(self):
           # Your parsing logic
           pass
       
       def extract_text(self):
           # Your text extraction logic
           pass
   ```

2. Update `app/parsers/__init__.py` to export the new parser

3. Modify `app/parsers/extractor.py` to use the new parser

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change port to 8000
```

### Module Import Errors
Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### PDF Extraction Issues
Some encrypted PDFs may not parse correctly. Try:
- Ensuring PDF is not password-protected
- Converting to different format
- Checking PDF file integrity

## Performance Tips

1. **Batch Processing**: Upload multiple files at once for efficiency
2. **File Size**: Keep files under 50MB (configurable in `app/__init__.py`)
3. **Pattern Matching**: More specific regex patterns = faster extraction
4. **Caching**: Consider implementing result caching for repeated documents

## Next Steps

1. **Customize Extraction Patterns**: Adjust regex patterns in `extractor.py` to match your document formats
2. **Integrate with Systems**: Use the JSON API to connect to your underwriting platform
3. **Add Data Validation**: Implement validation rules for extracted metrics
4. **Create Document Templates**: Build template-specific extractors for consistent formats
5. **Deploy**: Package as Docker container or deploy to cloud platform

## Support & Documentation

For detailed information:
- See `README.md` for full feature documentation
- Check individual parser files for implementation details
- Review the Flask routes in `routes.py` for API specifications

## Deployment

### Docker Deployment (Optional)
Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

Build and run:
```bash
docker build -t cre-parser .
docker run -p 5000:5000 cre-parser
```

### Cloud Deployment
- Heroku: Use `Procfile` with `web: python run.py`
- AWS/Azure: Deploy as containerized app
- Google Cloud: Use App Engine or Cloud Run

---

**Ready to start?** Run `python run.py` and open `http://localhost:5000` in your browser!
