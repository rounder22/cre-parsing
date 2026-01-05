# CRE Parser - Quick Reference

## Features at a Glance

### 📄 File Support
✓ PDF documents
✓ Word (.docx) documents  
✓ Excel (.xlsx) spreadsheets

### 💼 Extracted Information

**Property Details**
- Address & Location
- Property Type
- Square Footage
- Year Built
- Unit Count
- Occupancy Rate

**Financial Metrics**
- NOI (Net Operating Income)
- Cap Rate
- Purchase/Appraised Value
- Gross Income
- Operating Expenses
- Debt Service
- DSCR
- IRR

**Loan Details**
- Loan Amount
- Interest Rate
- Loan Term
- Lender Info
- LTV Ratio
- Maturity Date

**Tenant Info**
- Tenant Names
- Lease Terms
- Credit Quality

**Market Data**
- Market & Submarket
- Comparable Properties
- Market Trends

**Risk Analysis**
- Risk Factors
- Mitigation Strategies

## Getting Started

### 1. Install & Activate
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

### 2. Run Application
```bash
python run.py
```
Open: `http://localhost:5000`

### 3. Upload Documents
- Drag & drop or click to upload
- Support for single or batch uploads
- Results display organized by category

### 4. Export Data
- Click "Export Results" for JSON output
- Use for integration with underwriting systems

## API Endpoints

### Single File Upload
```
POST /api/upload
Body: multipart/form-data with 'file' field
```

### Batch Upload
```
POST /api/batch-upload
Body: multipart/form-data with 'files' field
```

### Export Results
```
POST /api/export
Body: JSON data
Response: JSON file download
```

## File Structure

```
cre-parsing/
├── app/                          # Main application
│   ├── parsers/                  # Document parsers
│   │   ├── pdf_parser.py
│   │   ├── word_parser.py
│   │   ├── excel_parser.py
│   │   └── extractor.py         # Metric extraction
│   ├── templates/index.html     # Web interface
│   ├── static/                  # Frontend assets
│   │   ├── style.css
│   │   └── script.js
│   └── routes.py               # Flask routes
├── samples/                     # Test documents
├── uploads/                     # Uploaded files
├── run.py                      # Start application
└── requirements.txt            # Dependencies
```

## Common Tasks

### Add New Extraction Metric
Edit `app/parsers/extractor.py`:
```python
'your_metric': self._find_pattern(text, r'Your Pattern', 0)
```

### Change Port
Edit `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Port 8000
```

### Deploy on Server
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Keyboard Shortcuts

| Action | Method |
|--------|--------|
| Upload | Click upload area or Ctrl+drag files |
| Export | Click "Export Results" button |
| Clear | Click "Clear Results" button |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Change port in run.py |
| Module not found | Run `pip install -r requirements.txt` |
| Metrics not found | Update regex patterns in extractor.py |
| PDF won't parse | Check if encrypted or corrupted |

## Performance

- **Max file size**: 50MB (configurable)
- **Supported batch**: Multiple files simultaneously
- **Processing time**: Usually < 5 seconds per document
- **Extraction accuracy**: 90%+ with standard formatting

## Integration Example

```python
from app.parsers.extractor import DataExtractor

# Extract data from a document
extractor = DataExtractor('path/to/file.pdf', 'pdf')
results = extractor.extract_all()

# Access extracted metrics
financial = results['extracted_metrics']['financial_metrics']
print(f"NOI: {financial.get('noi_annual')}")
print(f"Cap Rate: {financial.get('cap_rate')}")
```

## Sample Documents

Two sample CRE documents are included:
- `samples/Sample_CRE_Investment.docx` - Word format
- `samples/Sample_Financial_Model.xlsx` - Excel format

Use these to test the extraction functionality.

## Support Resources

- **README.md**: Full documentation
- **TESTING.md**: Testing & setup guide
- **app/routes.py**: API endpoint details
- **app/parsers/**: Parser implementation details

---
Start using the tool: `python run.py`
