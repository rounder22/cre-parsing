# OpenAI Integration Guide

## Overview

The CRE Parsing tool has been enhanced with OpenAI integration to provide advanced structured data extraction using GPT-4. This document explains how to set up and use OpenAI for parsing and extracting commercial real estate data.

## Features

### OpenAI-Powered Extraction
- **Advanced NLP**: Uses GPT-4 Turbo to understand complex document structures
- **Structured Output**: Returns JSON with guaranteed schema compliance using OpenAI's JSON Mode
- **Confidence Scoring**: Provides extraction confidence metrics based on data completeness
- **Smart Fallback**: Automatically falls back to regex extraction if OpenAI API is unavailable

### Extraction Capabilities
Extracts and structures:
- Property details (address, type, square footage, year built, units, occupancy)
- Financial metrics (NOI, cap rate, purchase price, valuations, DSCR, IRR)
- Loan information (amount, rate, term, lender, LTV)
- Tenant data (names, lease terms, quality assessment)
- Market analysis (market, submarket, comparables, trends)
- Risk assessment (identified risks and mitigation strategies)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The updated `requirements.txt` includes:
- `openai>=1.0.0` - OpenAI Python client
- `python-dotenv>=1.0.0` - Environment variable management

### 2. Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API keys section
4. Create a new API key
5. Copy the key (you won't be able to see it again)

### 3. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_MAX_TOKENS=4096
USE_OPENAI_EXTRACTION=true
ENABLE_FALLBACK=true
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (required) | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4-turbo-preview` | GPT model to use (can use `gpt-4`, `gpt-3.5-turbo`) |
| `OPENAI_MAX_TOKENS` | `4096` | Maximum tokens for API response |
| `USE_OPENAI_EXTRACTION` | `true` | Enable OpenAI extraction by default |
| `ENABLE_FALLBACK` | `true` | Fallback to regex if OpenAI fails |

## Usage

### Running the Application

```bash
python run.py
```

Access the web interface at `http://localhost:5000`

### API Endpoints

#### Check Configuration
```bash
GET /api/config
```

Returns current extraction configuration:
```json
{
  "use_openai": true,
  "openai_configured": true,
  "openai_model": "gpt-4-turbo-preview",
  "enable_fallback": true
}
```

#### Upload and Extract (Single File)

**Using OpenAI (default):**
```bash
curl -X POST -F "file=@document.pdf" http://localhost:5000/api/upload
```

**Force Regex Extraction:**
```bash
curl -X POST -F "file=@document.pdf" "http://localhost:5000/api/upload?use_openai=false"
```

**Response includes:**
```json
{
  "file_info": {
    "file_type": "pdf",
    "pages": 10,
    "extraction_method": "openai"
  },
  "raw_data": {...},
  "extracted_metrics": {
    "property_details": {...},
    "financial_metrics": {...},
    "loan_details": {...},
    "tenant_information": {...},
    "market_analysis": {...},
    "risk_assessment": {...},
    "extraction_metadata": {
      "confidence_score": 85.5,
      "missing_fields": [...]
    }
  }
}
```

#### Batch Upload

**Using OpenAI:**
```bash
curl -X POST -F "files=@doc1.pdf" -F "files=@doc2.docx" http://localhost:5000/api/batch-upload
```

**Force Regex:**
```bash
curl -X POST -F "files=@doc1.pdf" -F "files=@doc2.docx" "http://localhost:5000/api/batch-upload?use_openai=false"
```

#### Export Results
```bash
curl -X POST -d @extracted_data.json http://localhost:5000/api/export
```

## Extraction Methods

### OpenAI Method (Recommended)
**Advantages:**
- Better understanding of complex document structures
- More accurate extraction of contextual information
- Handles variations in document formats gracefully
- Returns confidence scores
- Identifies missing fields
- Structured JSON output with guaranteed schema

**Considerations:**
- Requires OpenAI API key and internet connection
- API calls incur costs (based on token usage)
- Slightly slower than regex (but more accurate)

### Regex Method (Fallback)
**Advantages:**
- No API costs
- No internet dependency
- Fast processing
- Good for well-structured documents

**Disadvantages:**
- Less accurate with unstructured documents
- Requires predefined patterns
- Limited context awareness

## Cost Optimization

### Reduce API Costs
1. Use `gpt-3.5-turbo` instead of `gpt-4-turbo-preview` (cheaper, slightly less accurate)
2. Reduce `OPENAI_MAX_TOKENS` if you don't need lengthy extractions
3. Enable `ENABLE_FALLBACK` to avoid costs on failed extractions
4. Batch process documents to optimize token usage

### Estimated Costs
Using GPT-4 Turbo (as of Feb 2026):
- Input: ~$0.01 per 1K tokens
- Output: ~$0.03 per 1K tokens

A typical CRE document (5-10 pages) = ~2-4K tokens = ~$0.05-0.15 per document

## Error Handling

### Common Issues

**"OpenAI API key not configured"**
- Ensure `.env` file exists with valid `OPENAI_API_KEY`
- Check that key is not expired

**"OpenAI API error: 401 Unauthorized"**
- API key is invalid or expired
- Generate a new key from OpenAI platform

**"OpenAI API error: 429 Rate limit exceeded"**
- Too many API calls in short time
- Implement request queuing or increase time between calls

**Fallback Extraction**
- If OpenAI fails and `ENABLE_FALLBACK=true`, regex extraction is used automatically
- Response will have `"extraction_method": "regex_fallback"`

## Advanced Usage

### Custom Extraction with OpenAI

```python
from app.parsers.openai_extractor import OpenAIExtractor

extractor = OpenAIExtractor()

# Extract with confidence scoring
result = extractor.extract_with_confidence(document_text)

# Check confidence and missing fields
confidence = result['extraction_metadata']['confidence_score']
missing = result['extraction_metadata']['missing_fields']

print(f"Confidence: {confidence}%")
print(f"Missing fields: {missing}")
```

### Switching Extraction Methods at Runtime

```python
from app.parsers.extractor import DataExtractor

# Use OpenAI
extractor_ai = DataExtractor('document.pdf', 'pdf', use_openai=True)
result_ai = extractor_ai.extract_all()

# Use Regex
extractor_regex = DataExtractor('document.pdf', 'pdf', use_openai=False)
result_regex = extractor_regex.extract_all()
```

## Output Schema

The extraction returns data in this structure:

```json
{
  "property_details": {
    "property_address": "string or null",
    "property_type": "string or null",
    "square_footage": "number or null",
    "year_built": "integer or null",
    "units": "integer or null",
    "occupancy_rate": "number (0-100) or null"
  },
  "financial_metrics": {
    "noi_annual": "number or null",
    "cap_rate": "number or null",
    "purchase_price": "number or null",
    "appraised_value": "number or null",
    "annual_gross_income": "number or null",
    "operating_expenses": "number or null",
    "debt_service": "number or null",
    "dscr": "number or null",
    "irr": "number or null"
  },
  "loan_details": {
    "loan_amount": "number or null",
    "interest_rate": "number or null",
    "loan_term_years": "integer or null",
    "loan_type": "string or null",
    "lender": "string or null",
    "maturity_date": "string or null",
    "ltv": "number or null"
  },
  "tenant_information": {
    "major_tenants": ["string array"],
    "lease_terms": "string or null",
    "tenant_quality": "string or null"
  },
  "market_analysis": {
    "market": "string or null",
    "submarket": "string or null",
    "comparable_properties": ["string array"],
    "market_trends": ["string array"]
  },
  "risk_assessment": {
    "identified_risks": ["string array"],
    "mitigation_strategies": ["string array"]
  },
  "extraction_metadata": {
    "confidence_score": "number (0-100)",
    "missing_fields": ["string array"]
  }
}
```

## Troubleshooting

### Enable Debug Logging

Add to your Flask app:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test OpenAI Configuration

```bash
python -c "from app.config import Config; print(Config.validate_openai_config())"
```

### Test Extraction Directly

```bash
python -c "
from app.parsers.openai_extractor import OpenAIExtractor
extractor = OpenAIExtractor()
result = extractor.extract_structured_data('Your sample text here')
print(result)
"
```

## Security Notes

- **Never commit `.env` file** - Add to `.gitignore`
- **Rotate API keys regularly** - especially after deployment
- **Monitor API usage** - Check OpenAI dashboard for unusual activity
- **Use environment variables** - Don't hardcode API keys in code
- **Validate input** - The app validates file types and sizes

## Support & Troubleshooting

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review OpenAI documentation: https://platform.openai.com/docs
3. Check application logs for error details
4. Verify environment configuration with `/api/config` endpoint

## Performance Tips

1. **Batch Processing**: Use `/api/batch-upload` for multiple documents
2. **Model Selection**: Use `gpt-3.5-turbo` for speed, `gpt-4` for accuracy
3. **Token Optimization**: Reduce document size if possible
4. **Caching**: Consider caching results for identical documents
5. **Async Processing**: For production, implement async job queue for long documents

## Future Enhancements

- Support for additional document formats (images, scanned PDFs)
- Fine-tuned models for CRE-specific extraction
- Real-time processing with webhooks
- Custom confidence thresholds
- Extraction result validation and correction UI
