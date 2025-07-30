# TCEQ Regulatory Data ETL Pipeline

## Overview

A production-ready ETL pipeline that extracts, transforms, and loads proposed regulation data from the Texas Commission on Environmental Quality (TCEQ) into a standardized JSON format. This pipeline demonstrates scalable approaches for government data integration and regulatory compliance monitoring.

**Data Source**: [TCEQ Proposed Rules](https://www.tceq.texas.gov/rules/prop.html)

## Key Features

- **Automated Web Scraping**: Extracts regulation metadata from HTML tables
- **PDF Text Processing**: Downloads and parses regulatory documents for full content
- **Intelligent Date Extraction**: Uses regex pattern matching to extract proposal dates from natural language
- **Data Normalization**: Converts data into standardized JSON format with consistent field structure
- **Error Resilience**: Graceful handling of network timeouts, malformed PDFs, and missing data
- **Memory Efficient**: In-memory processing using BytesIO to minimize disk I/O

## Technical Stack

- **Python 3.10+**
- **requests** - HTTP client for web scraping and file downloads
- **BeautifulSoup4** - HTML parsing and data extraction
- **pdfminer.six** - Robust PDF text extraction
- **re** - Regular expression pattern matching for date extraction
- **json** - Structured data serialization

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Quick Start
```bash
# Clone or download the project
cd tceq_etl_project

# Install dependencies
pip install -r requirements.txt

# Run the ETL pipeline
python main.py
```

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run pipeline
python main.py
```

## Project Structure

```
tceq_etl_project/
├── main.py              # Main ETL pipeline script
├── output.json          # Generated structured data output
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── report.md           # Technical approach and analysis
└── venv/               # Virtual environment (optional)
```

## Output Schema

The pipeline generates a JSON file with the following structure for each regulation:

```json
{
  "identifier": "2024-003-039-LS",
  "title": "Updates to Public Participation Rules for Environmental Permitting",
  "date_proposed": "2025-07-03",
  "source_url": "https://www.tceq.texas.gov/downloads/rules/current/24003039_pex.pdf",
  "full_text": "Texas Commission on Environmental Quality Interoffice Memorandum..."
}
```

### Field Descriptions
- **identifier**: Unique regulation identifier from TCEQ
- **title**: Full regulation title/description
- **date_proposed**: Extracted proposal date in YYYY-MM-DD format (or "unknown")
- **source_url**: Direct link to the PDF document
- **full_text**: Complete extracted text content from the PDF

## Pipeline Process

1. **Extract**: Downloads TCEQ webpage and parses HTML table containing regulation metadata
2. **Transform**: 
   - Normalizes text fields and converts relative URLs to absolute paths
   - Downloads PDF documents and extracts full text content
   - Applies regex patterns to identify and standardize proposal dates
3. **Load**: Serializes structured data to JSON format for downstream consumption

## Error Handling

The pipeline includes comprehensive error handling for:
- Network connectivity issues and timeouts
- Malformed or corrupted PDF documents
- Missing or unparseable date information
- HTML structure changes on the source website

Failed operations are logged with descriptive error messages while allowing the pipeline to continue processing remaining records.

## Performance Considerations

- **Memory Management**: Uses BytesIO for in-memory file processing
- **Network Optimization**: Implements 15-second timeouts for HTTP requests
- **Data Validation**: Validates minimum required fields before data storage
- **Scalability**: Dynamic URL resolution supports reuse across similar agencies

## Usage Examples

### Basic Execution
```bash
python main.py
```

### Viewing Results
```bash
# View structured output
cat output.json | python -m json.tool

# Count extracted regulations
python -c "import json; data=json.load(open('output.json')); print(f'Extracted {len(data)} regulations')"
```

## Extending the Pipeline

The pipeline architecture supports extension for:
- Additional state regulatory agencies
- Different document formats (Word, HTML, etc.)
- Database integration (PostgreSQL, MongoDB)
- Real-time monitoring and alerting
- Parallel processing for improved throughput

## Contributing

For questions, issues, or contributions, please refer to the technical approach documented in `report.md`.
