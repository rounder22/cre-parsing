# Quick Start: OpenAI Integration

Get up and running with OpenAI-powered CRE document parsing in 5 minutes.

## 1. Get OpenAI API Key (2 minutes)

1. Go to [https://platform.openai.com/api/keys](https://platform.openai.com/api/keys)
2. Click "Create new secret key"
3. Copy the key (you won't see it again!)

## 2. Configure Environment (1 minute)

```bash
# In project directory
cp .env.example .env

# Edit .env with your favorite editor and paste your API key:
# OPENAI_API_KEY=sk-your-key-here
```

## 3. Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## 4. Run Application (1 minute)

```bash
python run.py
```

Open browser to: **http://localhost:5000**

## 5. Test Extraction

### Via Web Interface
1. Click "Upload Document"
2. Select a PDF, Word, or Excel file
3. View structured extraction results

### Via API
```bash
# Single file
curl -X POST -F "file=@sample.pdf" http://localhost:5000/api/upload

# Check configuration
curl http://localhost:5000/api/config

# Force regex extraction (no OpenAI)
curl -X POST -F "file=@sample.pdf" "http://localhost:5000/api/upload?use_openai=false"
```

## Default Configuration

```env
OPENAI_MODEL=gpt-4-turbo-preview     # Most capable, higher cost
OPENAI_MAX_TOKENS=4096               # Sufficient for most documents
USE_OPENAI_EXTRACTION=true           # Uses OpenAI by default
ENABLE_FALLBACK=true                 # Falls back to regex if OpenAI fails
```

## Cost Savings Tips

**Option 1: Cheaper Model**
```env
OPENAI_MODEL=gpt-3.5-turbo           # 10x cheaper, still accurate
```

**Option 2: Smaller Response**
```env
OPENAI_MAX_TOKENS=2048               # Cuts costs in half
```

## What You Get

### Response Example
```json
{
  "file_info": {
    "file_type": "pdf",
    "extraction_method": "openai",
    "confidence_score": 87.3
  },
  "extracted_metrics": {
    "property_details": {
      "property_address": "123 Main St, New York, NY",
      "property_type": "Office",
      "square_footage": 45000,
      "year_built": 2010,
      "occupancy_rate": 92.5
    },
    "financial_metrics": {
      "noi_annual": 2250000,
      "cap_rate": 4.5,
      "purchase_price": 50000000
    },
    ...
  }
}
```

## Extraction Categories

✅ Property Details (6 fields)
✅ Financial Metrics (9 fields)  
✅ Loan Details (7 fields)
✅ Tenant Information (3 fields)
✅ Market Analysis (4 fields)
✅ Risk Assessment (2 fields)

## Troubleshooting

**"OpenAI API key not configured"**
```bash
# Check .env file exists and has OPENAI_API_KEY
cat .env | grep OPENAI_API_KEY
```

**"Invalid API key"**
- Get new key from https://platform.openai.com/api/keys
- Paste into .env without quotes

**Slow extraction?**
- Try `gpt-3.5-turbo` (faster, cheaper)
- Reduce `OPENAI_MAX_TOKENS` to 2048

**Want to test without API key?**
```bash
# Force regex extraction
curl -X POST -F "file=@sample.pdf" "http://localhost:5000/api/upload?use_openai=false"
```

## Need More Help?

📖 **Full Guide**: See `OPENAI_INTEGRATION.md`
📋 **Enhancement Details**: See `ENHANCEMENT_SUMMARY.md`
💻 **API Examples**: Check `app/routes.py`
⚙️ **Configuration**: See `app/config.py`

## Example Use Cases

### Real Estate Fund Analysis
```bash
# Upload multiple property documents
curl -X POST \
  -F "files=@property1.pdf" \
  -F "files=@property2.pdf" \
  -F "files=@property3.docx" \
  http://localhost:5000/api/batch-upload
```

### Due Diligence
```bash
# Get confidence scores for extraction quality
# Response includes "confidence_score" (0-100%) and "missing_fields"
```

### Portfolio Review
```bash
# Export all extracted data as JSON for analysis
curl -X POST \
  -d @extracted_data.json \
  http://localhost:5000/api/export > portfolio_analysis.json
```

---

**Ready to extract? Start the server and go to http://localhost:5000!**
