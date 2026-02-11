# JSON Schemas for CRE Data Extraction with Citations

CRE_EXTRACTION_SCHEMA = {
    "name": "CRE_Commercial_Real_Estate_Extraction",
    "description": "Structured extraction of Commercial Real Estate underwriting data with source citations",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "property_details": {
                "type": "object",
                "description": "Core property information with citations",
                "properties": {
                    "property_address": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"], "description": "Exact text snippet from document"}
                        }
                    },
                    "property_type": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "square_footage": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "acres": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "land_square_feet": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "gross_building_area": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "net_rentable_area": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "year_built": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["integer", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "units": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["integer", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "occupancy_rate": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    }
                },
                "required": ["property_address", "property_type", "square_footage", "acres", "land_square_feet", "gross_building_area", "net_rentable_area", "year_built", "units", "occupancy_rate"],
                "additionalProperties": False
            },
            "financial_metrics": {
                "type": "object",
                "description": "Key financial metrics with citations",
                "properties": {
                    "noi_annual": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "stabilized_noi": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "cap_rate": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "purchase_price": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "appraised_value": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "annual_gross_income": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "operating_expenses": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "debt_service": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "dscr": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "irr": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "project_cost": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "expected_exit_valuation": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "expected_rents": {
                        "type": "array",
                        "description": "Expected rent figures with citations",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": ["string", "null"]},
                                "value": {"type": ["number", "null"]},
                                "unit": {"type": ["string", "null"]},
                                "source_text": {"type": ["string", "null"]}
                            }
                        },
                        "maxItems": 10
                    }
                },
                "required": ["noi_annual", "stabilized_noi", "cap_rate", "purchase_price", "appraised_value", 
                            "annual_gross_income", "operating_expenses", "debt_service", "dscr", "irr",
                            "project_cost", "expected_exit_valuation", "expected_rents"],
                "additionalProperties": False
            },
            "loan_details": {
                "type": "object",
                "description": "Financing information with citations",
                "properties": {
                    "loan_amount": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "interest_rate": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "loan_term_years": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["integer", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "loan_type": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "lender": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "maturity_date": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "ltv": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    }
                },
                "required": ["loan_amount", "interest_rate", "loan_term_years", "loan_type", 
                            "lender", "maturity_date", "ltv"],
                "additionalProperties": False
            },
            "tenant_information": {
                "type": "object",
                "description": "Tenant and lease information with citations",
                "properties": {
                    "major_tenants": {
                        "type": "array",
                        "description": "List of major/anchor tenants with source citations",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "source_text": {"type": ["string", "null"]}
                            }
                        },
                        "maxItems": 5
                    },
                    "lease_terms": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "tenant_quality": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    }
                },
                "required": ["major_tenants", "lease_terms", "tenant_quality"],
                "additionalProperties": False
            },
            "market_analysis": {
                "type": "object",
                "description": "Market-related information with citations",
                "properties": {
                    "market": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "submarket": {
                        "type": "object",
                        "properties": {
                            "value": {"type": ["string", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "source_text": {"type": ["string", "null"]}
                        }
                    },
                    "comparable_properties": {
                        "type": "array",
                        "description": "List of comparable properties with citations",
                        "items": {
                            "type": "object",
                            "properties": {
                                "property": {"type": "string"},
                                "source_text": {"type": ["string", "null"]}
                            }
                        },
                        "maxItems": 5
                    },
                    "market_trends": {
                        "type": "array",
                        "description": "Key market trends with citations",
                        "items": {
                            "type": "object",
                            "properties": {
                                "trend": {"type": "string"},
                                "source_text": {"type": ["string", "null"]}
                            }
                        },
                        "maxItems": 5
                    }
                },
                "required": ["market", "submarket", "comparable_properties", "market_trends"],
                "additionalProperties": False
            },
            "risk_assessment": {
                "type": "object",
                "description": "Risk factors and mitigation strategies with citations",
                "properties": {
                    "identified_risks": {
                        "type": "array",
                        "description": "Key risks with source citations",
                        "items": {
                            "type": "object",
                            "properties": {
                                "risk": {"type": "string"},
                                "source_text": {"type": ["string", "null"]}
                            }
                        },
                        "maxItems": 5
                    },
                    "mitigation_strategies": {
                        "type": "array",
                        "description": "Mitigation strategies with citations",
                        "items": {
                            "type": "object",
                            "properties": {
                                "strategy": {"type": "string"},
                                "source_text": {"type": ["string", "null"]}
                            }
                        },
                        "maxItems": 5
                    }
                },
                "required": ["identified_risks", "mitigation_strategies"],
                "additionalProperties": False
            },
            "extraction_metadata": {
                "type": "object",
                "description": "Metadata about the extraction including citation statistics",
                "properties": {
                    "confidence_score": {
                        "type": "number",
                        "description": "Confidence score (0-100) based on completeness and citation coverage"
                    },
                    "missing_fields": {
                        "type": "array",
                        "description": "List of fields that are missing or null",
                        "items": {
                            "type": "string"
                        }
                    },
                    "fields_with_citations": {
                        "type": "integer",
                        "description": "Count of fields that include source citations"
                    },
                    "fields_without_citations": {
                        "type": "integer",
                        "description": "Count of extracted fields without citations"
                    },
                    "citation_coverage_percent": {
                        "type": "number",
                        "description": "Percentage of extracted values with citations (0-100)"
                    }
                },
                "required": ["confidence_score", "missing_fields", "fields_with_citations", 
                            "fields_without_citations", "citation_coverage_percent"],
                "additionalProperties": False
            }
        },
        "required": ["property_details", "financial_metrics", "loan_details", "tenant_information", 
                    "market_analysis", "risk_assessment", "extraction_metadata"],
        "additionalProperties": False
    }
}

# Backward compatible schema for regex-based extraction
REGEX_EXTRACTION_SCHEMA = {
    "property_details": {},
    "financial_metrics": {},
    "loan_details": {},
    "tenant_info": {},
    "market_analysis": {},
    "risk_factors": {}
}
