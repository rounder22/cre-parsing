# Citation Feature Guide

## Overview

The CRE Parsing tool now includes **source citations** for all extracted data. Every extracted value includes a reference to where it was found in the original document, enabling full traceability and verification of extracted information.

## What Are Citations?

Citations are **source text snippets** from the original document that support each extracted value. They show exactly where the data came from, enabling:

✅ **Verification**: Confirm accuracy of extracted data
✅ **Traceability**: Audit trail of information sources
✅ **Due Diligence**: Support underwriting decisions with evidence
✅ **Compliance**: Document data provenance for regulatory requirements
✅ **Quality Assurance**: Identify extraction accuracy issues

## Citation Structure

### Single-Value Fields

Each scalar field (property address, purchase price, etc.) contains:

```json
{
  "property_address": {
    "value": "123 Main Street, New York, NY 10001",
    "citation": "Property Address: 123 Main Street, New York, NY 10001 (as shown in..."
  }
}
```

### Array Fields

List items (tenants, risks, trends) include citations for each item:

```json
{
  "major_tenants": [
    {
      "name": "Acme Corporation",
      "citation": "Anchor Tenant: Acme Corporation occupies 50,000 SF on..."
    },
    {
      "name": "Tech Industries Inc",
      "citation": "Major Tenant: Tech Industries Inc recently signed a..."
    }
  ]
}
```

## Citation Coverage Statistics

Each extraction includes citation metrics in the metadata:

```json
{
  "extraction_metadata": {
    "confidence_score": 85.5,
    "fields_with_citations": 28,
    "fields_without_citations": 3,
    "citation_coverage_percent": 90.3,
    "missing_fields": [...]
  }
}
```

### Metrics Explanation

| Metric | Meaning |
|--------|---------|
| `fields_with_citations` | Count of extracted values that have source citations |
| `fields_without_citations` | Count of extracted values without citations (incomplete extraction) |
| `citation_coverage_percent` | Percentage of extracted values with citations (0-100%) |
| `confidence_score` | Overall extraction confidence based on completeness |

**Example Interpretation:**
- 28 fields with citations = Strong traceability
- 90.3% coverage = High verification ability
- 85.5% confidence = Good quality extraction

## OpenAI Extraction (Recommended)

When using OpenAI extraction, the API is explicitly instructed to:
1. Find exact text snippets from the document for each value
2. Include 25-150 character citations
3. Only return values that can be cited
4. Return null for values without source evidence

**Advantages:**
- Accurate source identification
- Semantic understanding of context
- Longer, more descriptive citations
- Better handling of paraphrased content

**Example:**
```json
{
  "noi_annual": {
    "value": 2500000,
    "citation": "Annual NOI: The property generated $2,500,000 in Net Operating Income for..."
  }
}
```

## Regex Extraction

Regex extraction also provides citations by capturing the surrounding document context:

**Advantages:**
- Fast, no API calls
- Includes document context
- Shows pattern matches

**Example:**
```json
{
  "cap_rate": {
    "value": "4.5",
    "citation": "...property valuation. Cap Rate: 4.5%. The market rate for similar..."
  }
}
```

## Using Citations in Your Workflow

### 1. Verification

```python
result = extract_data('document.pdf')

for field, data in result['property_details'].items():
    if data['value'] and data['citation']:
        print(f"{field}: {data['value']}")
        print(f"Evidence: {data['citation']}\n")
```

### 2. Audit Trail

```python
# Document all extracted values with their sources
audit_log = {
    'document': 'property_analysis.pdf',
    'timestamp': datetime.now(),
    'extractions': result['extracted_metrics'],
    'citation_coverage': result['extraction_metadata']['citation_coverage_percent']
}
```

### 3. Quality Control

```python
# Flag extractions with low citation coverage
if result['extraction_metadata']['citation_coverage_percent'] < 80:
    print("Warning: Low citation coverage - manual review recommended")
```

### 4. Export with Citations

```json
{
  "property": {
    "address": {
      "value": "123 Main St, NY",
      "citation": "Located at 123 Main Street, New York..."
    }
  },
  "_audit": {
    "extraction_date": "2026-02-02",
    "citation_coverage": 92.1,
    "extraction_method": "openai"
  }
}
```

## Citation Quality Levels

### Excellent (95-100% coverage)
- Almost all values have citations
- Complete documentation
- Full auditability
- Best for compliance

### Good (80-94% coverage)
- Most values cited
- Minor gaps acceptable
- Strong traceability
- Suitable for due diligence

### Acceptable (60-79% coverage)
- Majority of values cited
- Some uncited data
- Manual verification needed
- Consider as preliminary

### Poor (<60% coverage)
- Many values without citations
- Limited traceability
- Requires manual review
- Not suitable for underwriting

## API Response Example

```json
{
  "file_info": {
    "file_type": "pdf",
    "extraction_method": "openai"
  },
  "extracted_metrics": {
    "property_details": {
      "property_address": {
        "value": "456 Oak Avenue, Boston, MA",
        "citation": "Property Location: 456 Oak Avenue, Boston, Massachusetts 02101..."
      },
      "square_footage": {
        "value": 125000,
        "citation": "Total square footage of 125,000 sq ft as stated in the..."
      }
    },
    "financial_metrics": {
      "noi_annual": {
        "value": 3750000,
        "citation": "Year ending 2025 NOI of $3,750,000 per audited..."
      },
      "cap_rate": {
        "value": 5.2,
        "citation": "Market cap rate of 5.2% based on comparable..."
      }
    },
    "extraction_metadata": {
      "confidence_score": 89.2,
      "citation_coverage_percent": 94.5,
      "fields_with_citations": 41,
      "fields_without_citations": 2,
      "missing_fields": [
        "property_details.occupancy_rate",
        "market_analysis.market_trends"
      ]
    }
  }
}
```

## Best Practices

### 1. Always Check Citation Coverage

```python
coverage = result['extraction_metadata']['citation_coverage_percent']
if coverage < 80:
    print(f"Warning: Only {coverage}% citation coverage")
    print("Missing citations for:", result['extraction_metadata']['missing_fields'])
```

### 2. Review Uncited Values

```python
uncited_count = result['extraction_metadata']['fields_without_citations']
if uncited_count > 0:
    print(f"{uncited_count} fields extracted without citations")
    # Perform manual verification for these fields
```

### 3. Document Your Sources

```python
# When using extracted data in reports
report = {
    "extracted_data": result['extracted_metrics'],
    "citation_coverage": result['extraction_metadata']['citation_coverage_percent'],
    "extraction_timestamp": now.isoformat(),
    "reviewer_notes": "All values with >90% citation coverage used directly"
}
```

### 4. Implement Citation Validation

```python
def validate_citation_coverage(result, min_coverage=85):
    actual = result['extraction_metadata']['citation_coverage_percent']
    if actual < min_coverage:
        raise ValueError(f"Citation coverage {actual}% below minimum {min_coverage}%")
    return True
```

## Extraction Method Comparison

### OpenAI (With Citations)

**Pros:**
- Intelligent citation selection
- Contextual understanding
- Semantic accuracy
- Full traceability

**Cons:**
- API costs (~$0.05-0.15/doc)
- Requires internet
- Slightly slower (2-5 sec)

**Citation Quality:** ⭐⭐⭐⭐⭐

### Regex (With Citations)

**Pros:**
- No API costs
- Fast (~0.5 sec)
- No internet required
- Full document context

**Cons:**
- Pattern-based only
- Limited to predefined patterns
- May miss complex data

**Citation Quality:** ⭐⭐⭐⭐

## Troubleshooting

### "Low Citation Coverage"

**Cause:** Document format differs from expected patterns

**Solutions:**
1. Check document formatting
2. Ensure data is visible (not in images)
3. Use OpenAI extraction instead of regex
4. Manually verify and add missing data

### "All Citations Are Null"

**Cause:** Extraction failed or invalid response

**Solutions:**
```python
# Debug
if all(v['citation'] is None for v in result.values()):
    print("Extraction failed - check document quality")
    # Try with different extraction method
    result = extract_with_method(doc, method='regex')
```

### "Incomplete Citations"

**Cause:** Document text incomplete or truncated

**Solutions:**
1. Verify full document uploaded
2. Check for OCR issues
3. Try manual extraction for critical values

## Citation Standards

### Format Guidelines

- **Length**: 25-150 characters
- **Content**: Relevant context + key phrase
- **Accuracy**: Exact text from document
- **Relevance**: Shows why value was extracted

### Good Citation Examples

✅ "Property Address: 123 Main Street, New York, NY 10001 as shown in the..."
✅ "Annual NOI: $2,500,000 per the 2025 audited financial statements..."
✅ "Cap Rate: 4.5% based on comparable property analysis..."

### Poor Citation Examples

❌ "Found in document"
❌ "See attached"
❌ "123 Main Street"
❌ (null values without explanation)

## Compliance & Audit Trail

### Regulatory Requirements

Citations support compliance with:
- **FNMA**: Detailed documentation of property information
- **FHFA**: Appraisal data source documentation
- **SEC**: Material information sourcing
- **Internal Controls**: Audit trail requirements

### Audit Documentation

```python
audit_record = {
    "document_id": "prop_2026_001",
    "extraction_date": "2026-02-02T14:30:00Z",
    "extraction_method": "openai",
    "confidence_score": 87.3,
    "citation_coverage": 92.1,
    "operator": "john.doe@company.com",
    "data_with_high_confidence": {
        field: value 
        for field, value in result.items() 
        if value.get('citation') is not None
    }
}
```

## Advanced Usage

### Citation-Based Filtering

```python
def get_highly_cited_data(result, min_coverage=90):
    """Extract only fields with citations"""
    cited_data = {}
    for category, fields in result['extracted_metrics'].items():
        if category == 'extraction_metadata':
            continue
        cited_data[category] = {
            k: v for k, v in fields.items()
            if isinstance(v, dict) and v.get('citation') is not None
        }
    return cited_data
```

### Citation Analytics

```python
def analyze_citations(result):
    """Generate citation statistics"""
    return {
        'total_fields': result['extraction_metadata']['fields_with_citations'] + 
                       result['extraction_metadata']['fields_without_citations'],
        'cited': result['extraction_metadata']['fields_with_citations'],
        'uncited': result['extraction_metadata']['fields_without_citations'],
        'coverage_percent': result['extraction_metadata']['citation_coverage_percent'],
        'confidence': result['extraction_metadata']['confidence_score']
    }
```

## Configuration

### Adjust Citation Behavior

For OpenAI extraction, the system is pre-configured to prioritize citations. No additional configuration needed.

For regex extraction, citations are automatically captured from document context.

## Support & Questions

For issues with citations:
1. Check citation coverage in metadata
2. Review missing_fields list
3. Verify document quality
4. Try alternative extraction method

---

**Version:** 2.1 with Citations
**Last Updated:** February 2026
