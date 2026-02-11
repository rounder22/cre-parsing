import instructor
import streamlit as st
from openai import OpenAI
import pandas as pd
from markitdown import MarkItDown
import io
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from dotenv import load_dotenv
import os

# Only process files and make API call if files are uploaded
# Load environment variables from .env file
load_dotenv()

class ValueWithSource(BaseModel):
    value: Optional[float] = Field(
        None,
        description="Numeric value extracted from the document. Null if missing."
    )
    unit: Optional[str] = Field(
        None,
        description="Unit associated with the value (e.g., USD, SF, acres)."
    )
    source_text: Optional[str] = Field(
        None,
        description="Exact text snippet from the PDF supporting this value."
    )


class RentEntry(BaseModel):
    type: Optional[str] = Field(
        None,
        description="Type of rent (e.g., 'market', 'stabilized', 'pro forma')."
    )
    value: Optional[float] = Field(
        None,
        description="Rent value extracted from the document."
    )
    unit: Optional[str] = Field(
        None,
        description="Unit for rent (e.g., USD/SF/year, USD/month)."
    )
    source_text: Optional[str] = Field(
        None,
        description="Exact supporting text from the PDF."
    )


class CREExtraction(BaseModel):
    total_project_cost: ValueWithSource
    expected_exit_valuation: ValueWithSource
    stabilized_noi: ValueWithSource
    expected_rents: List[RentEntry]
    operating_expenses: ValueWithSource
    acres: ValueWithSource
    land_square_feet: ValueWithSource
    gross_building_area: ValueWithSource
    net_rentable_area: ValueWithSource

# Initialize and wrap OpenAI client 
raw_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))
client = instructor.from_openai(raw_client)

@st.cache_data(show_spinner="Fetching available models...")
def get_available_chat_models():
    models = client.models.list()
    chat_models = [m.id for m in models.data if m.id.startswith("gpt-")]
    chat_models.sort(reverse=True)
    return chat_models

st.title("Commercial Real Estate Diagnostic Tool")

available_models = get_available_chat_models()

selected_model = st.selectbox(
    "Select Model:",
    available_models,
    index=available_models.index(
        st.session_state.get("openai_model", "gpt-4")
    ) if "openai_model" in st.session_state and st.session_state["openai_model"] in available_models else 0
)
st.session_state["openai_model"] = selected_model

# Upload multiple files
uploaded_files = st.file_uploader(
    "Upload files (CSV, TXT, PDF, Excel, Word)", 
    type=["csv", "txt", "pdf", "xls", "xlsx", "docx"], 
    accept_multiple_files=True
)

max_files = 10
if uploaded_files and len(uploaded_files) > max_files:
    st.warning(f"Please upload no more than {max_files} files.")
    uploaded_files = uploaded_files[:max_files]


# Extract file contents
file_contents = []
converter = MarkItDown()
for file in uploaded_files:
    file_name = file.name
    result = converter.convert_stream(stream=file, filename=file_name)
    markdown_content = result.text_content
    file_contents.append(f"### Document: {file_name}\n[source: {file_name}]\n{markdown_content}\n")

# Create prompt with improved extraction guidance
prompt = {
    "role": "user",
    "content": (
        f"Extract detailed commercial real estate financial and operational metrics from the following document(s). "
        f"For EACH extracted value, provide: the numeric value, its unit, and the EXACT text snippet from the document that supports it. "
        f"If a field is not mentioned in the document, set value to null. "
        f"\n\nKey fields to extract:\n"
        f"- Total Project Cost: The total capital investment or development cost\n"
        f"- Expected Exit Valuation: The projected sale price or property valuation at exit\n"
        f"- Stabilized NOI: Net operating income when the property reaches stabilization\n"
        f"- Expected Rents: All rent figures mentioned (market rent, stabilized rent, pro forma rent, etc.)\n"
        f"- Operating Expenses: Annual or monthly operating costs\n"
        f"- Acres: Total land acreage\n"
        f"- Land Square Feet: Land area in square feet\n"
        f"- Gross Building Area (GBA): Total building square footage\n"
        f"- Net Rentable Area (NRA): Rentable square footage\n\n"
        f"CRITICAL: For each value extracted, ALWAYS include the exact source text from the document. "
        f"This text will be displayed to users as a citation.\n\n"
        f"Documents:\n{file_contents}"
    )
}

response = client.chat.completions.create(
    model=st.session_state["openai_model"], 
    response_model=CREExtraction, 
    messages=[prompt]
)

# Display extracted data with citations
st.subheader("Extracted Commercial Real Estate Data")

# Helper function to display value with source
def display_value_with_source(label: str, value_obj: ValueWithSource):
    if value_obj.value is not None:
        col1, col2 = st.columns([2, 3])
        with col1:
            st.metric(label, f"{value_obj.value:,.2f}" if isinstance(value_obj.value, (int, float)) else value_obj.value)
        with col2:
            if value_obj.source_text:
                st.caption(f"📄 Citation: *{value_obj.source_text}*")
            if value_obj.unit:
                st.caption(f"Unit: {value_obj.unit}")
    else:
        st.caption(f"{label}: Not found in document")

# Display financial metrics
st.markdown("### Financial Metrics")
display_value_with_source("Total Project Cost", response.total_project_cost)
display_value_with_source("Expected Exit Valuation", response.expected_exit_valuation)
display_value_with_source("Stabilized NOI", response.stabilized_noi)
display_value_with_source("Operating Expenses", response.operating_expenses)

# Display property dimensions
st.markdown("### Property Dimensions")
display_value_with_source("Acres", response.acres)
display_value_with_source("Land Square Feet", response.land_square_feet)
display_value_with_source("Gross Building Area (GBA)", response.gross_building_area)
display_value_with_source("Net Rentable Area (NRA)", response.net_rentable_area)

# Display rents
if response.expected_rents:
    st.markdown("### Expected Rents")
    for i, rent in enumerate(response.expected_rents, 1):
        if rent.value is not None:
            with st.expander(f"Rent Entry {i}" + (f" - {rent.type}" if rent.type else "")):
                col1, col2 = st.columns(2)
                with col1:
                    if rent.type:
                        st.write(f"**Type:** {rent.type}")
                    st.write(f"**Value:** {rent.value:,.2f}")
                with col2:
                    if rent.unit:
                        st.write(f"**Unit:** {rent.unit}")
                    if rent.source_text:
                        st.info(f"📄 Citation: {rent.source_text}")
else:
    st.caption("No rent entries found in document")