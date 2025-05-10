# Challenge 3: Standard Enhancement Multi-Agent System

## Overview

This implementation creates a multi-agent AI system for reviewing, suggesting, and validating updates to AAOIFI standards as specified in Challenge 3 of the hackathon. The system focuses on FAS 10 (Istisna'a and Parallel Istisna'a) and consists of three specialized agents:

1. **Review & Extraction Agent**: Processes the selected standard to extract key elements, definitions, principles, scope, recognition criteria, measurement rules, and disclosure requirements.

2. **Enhancement Agent**: Suggests modifications/enhancements by comparing with other standards, analyzing contemporary financial instruments, and identifying improvement areas.

3. **Validation Agent**: Validates proposed changes for compliance with AAOIFI principles and Shariah requirements.

## Implementation Details

### Vector Database Setup

The system creates a vector database from the PDF files of FAS 10 and related standards. This enables efficient retrieval of relevant information during the agent operations. We use:

- **Chroma**: For vector storage
- **HuggingFace Embeddings**: sentence-transformers/all-MiniLM-L6-v2 model
- **RecursiveCharacterTextSplitter**: To chunk the documents

### Agent Architecture

Each agent is implemented as a specialized RAG (Retrieval-Augmented Generation) chain:

1. **Review Agent**: Analyzes FAS 10 and extracts structured information about its key components
2. **Enhancement Agent**: Takes the output from the Review Agent and suggests improvements
3. **Validation Agent**: Takes outputs from both previous agents and validates proposed changes

The system follows a sequential orchestration pattern, where each agent's output becomes input for the next agent.

### Interactive Querying

The implementation also includes an interactive query system that allows users to ask questions about the enhanced standard, drawing from the knowledge produced by all three agents.

## How to Use

1. Open `challenge-3.ipynb` in Jupyter Notebook
2. Execute all cells to run the multi-agent system
3. The system will:
   - Process PDF files and create a vector database
   - Run the three agents in sequence
   - Save results to `fas10_enhancement_results.json`
   - Provide example queries to the enhanced standard

## Dependencies

- langchain
- chromadb
- sentence-transformers
- pypdf2/pdfplumber
- Other common Python libraries

## Future Enhancements

- Extend to other standards (FAS 4, FAS 32)
- Add more specialized agents
- Create a visual interface
- Implement a feedback mechanism
