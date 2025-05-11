## Project Overview

This project aims to leverage artificial intelligence to enhance the adoption, understanding, and application of Islamic finance standards, particularly those established by the Accounting and Auditing Organization for Islamic Financial Institutions (AAOIFI). It was developed as part of a hackathon focused on applying AI to Islamic finance standards.

The project addresses four challenge categories:

1. **Use Case Scenarios**: Process Islamic finance scenarios and generate accounting treatments aligned with AAOIFI standards
2. **Reverse Transactions**: Analyze financial entries and identify relevant AAOIFI standards
3. **Standard Enhancement**: Multi-agent system to review and suggest updates to AAOIFI standards
4. **QA Bot for AAOIFI Standards**: Interactive question-answering system for Islamic finance standards

## Setup Instructions

### Prerequisites

- Python 3.10+
- Git
- OpenAI API key (for some components)
- Google API key (for Gemini model access)

### Installation

1. Clone this repository:
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

## Challenge Components and How to Run

### Challenge 1: Use Case Scenarios (Ijarah MBT Accounting)

This component processes Ijarah Muntahia Bittamleek (lease ending with ownership) scenarios according to AAOIFI standards, extracting financial parameters and generating appropriate journal entries.

**To run:**
1. Open the Jupyter notebook:
   ```bash
   jupyter notebook notebooks/challenge-1.ipynb
   ```
2. Execute the cells sequentially to:
   - Extract text from the AAOIFI standards PDFs
   - Create a vector database for retrieval
   - Process Ijarah MBT scenarios
   - Generate accounting entries and calculations

The notebook demonstrates processing a sample scenario for Alpha Islamic Bank and performs calculations like Right-of-Use (ROU) asset valuation and journal entry generation.

### Challenge 2: Reverse Transactions

This component analyzes journal entries and identifies the relevant AAOIFI Financial Accounting Standards (FAS) that govern such transactions.

**To run:**
1. Open the Jupyter notebook:
   ```bash
   jupyter notebook notebooks/challenge-2-gemini.ipynb
   ```
2. Execute the cells to:
   - Load AAOIFI standards into the vector database
   - Analyze sample journal entries
   - Identify applicable standards with confidence scores
   - Generate reasoning for the identified standards

### Challenge 3: Standard Enhancement

This is a multi-agent system that reviews, suggests, and validates updates to AAOIFI standards. The implementation focuses on FAS 10 (Istisna'a and Parallel Istisna'a).

**To run the analysis:**
1. Open the Jupyter notebook:
   ```bash
   jupyter notebook notebooks/challenge-3/challenge-3.ipynb
   ```
2. Execute the cells to run the multi-agent system

**To view enhancement results:**
```bash
cd notebooks/challenge-3
streamlit run fas_enhancement_viewer.py
```

This will open an interactive viewer showing the standard enhancement suggestions made by the AI agents.

### Challenge 4: QA Bot for AAOIFI Standards

An interactive question-answering system that uses Retrieval-Augmented Generation (RAG) to answer questions about AAOIFI standards.

**Terminal interface:**
```bash
cd challenge-4
python app.py
```

**Web interface:**
```bash
cd challenge-4
python run-streamlit.py
```

After running the web interface, open your browser at http://localhost:8501 to interact with the QA bot.

## Project Structure

```
ISDB/
├── challenge-4/              # QA Bot for AAOIFI Standards
│   ├── app.py                # Terminal interface
│   ├── run-streamlit.py      # Web interface
│   ├── src/                  # Core components
│   └── vector_db/            # Vector database for standards
├── course/                   # LangChain reference materials
├── data/                     # AAOIFI standards documents (PDFs)
├── memory-bank/              # Project documentation
├── notebooks/                # Jupyter notebooks for challenges
│   ├── challenge-1.ipynb     # Use Case Scenarios
│   ├── challenge-2-gemini.ipynb  # Reverse Transactions
│   └── challenge-3/          # Standard Enhancement
│       ├── challenge-3.ipynb     # Multi-agent implementation
│       ├── fas_enhancement_results.json  # Results data
│       └── fas_enhancement_viewer.py     # Results viewer
└── vector_db/                # Vector databases for different components
    ├── MTB_ijarah_standards/           # For Challenge 1
    ├── standards_enhancement/          # For Challenge 3
    └── standards_reverse_transactions_gemini/  # For Challenge 2
```

## Key Features

- **Retrieval-Augmented Generation (RAG)** for accurate standard retrieval and application
- **Financial calculation components** for Ijarah MBT accounting
- **Multi-agent architecture** for standard enhancement
- **Interactive interfaces** for exploring and querying standards
- **Vector databases** for efficient semantic search of standards

## Limitations and Future Work

- Some complex tables and diagrams in standards may not be fully captured
- Arabic text handling may require additional refinement
- Financial calculations would benefit from validation by Islamic finance experts
- The system could be expanded to cover more standards and financial scenarios
- A unified web interface could integrate all four challenge components

## License

[Specify license information]

## Acknowledgments

- AAOIFI for establishing the standards used in this project
- LangChain community for the framework and tools
- [Hackathon organizers and other acknowledgments] 