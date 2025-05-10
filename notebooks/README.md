# Chroma Vector Store Setup Guide

This guide will help you set up and run the updated Ijarah accounting notebook that uses Chroma for vector storage.

## Prerequisites

1. Make sure you have installed all the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. You should have the PDF files in the correct location:
   - `data/FAS32.pdf` - Financial Accounting Standard 32 (Ijarah)
   - `data/SS9.pdf` - Shariah Standard 9 (Ijarah)

3. Make sure your OpenAI API key is set as an environment variable.
   - Create a `.env` file in the `notebooks` directory with:
     ```
     OPENAI_API_KEY=your-api-key
     ```

## Running the Notebook

1. Open the notebook `notebooks/langchain_case1.ipynb` in VSCode or Jupyter.
2. Run each cell in sequence.
3. The first time you run, a new Chroma vector database will be created in the `vector_db/ijarah_standards` directory.
4. On subsequent runs, the notebook will load the existing vector database.

## Key Features

- **Persistent Storage**: The vector database is saved to disk and can be reused.
- **Metadata Filtering**: You can query only specific documents using filters.
- **Helper Functions**: 
  - `add_document_to_vector_store()`: Add new documents to the vector store
  - `clear_vector_store()`: Reset the vector store
  - `query_with_metadata_filter()`: Search with source filtering

## Example Scenario

The notebook includes an example scenario about an Ijarah MBT (lease ending with ownership transfer) for a generator. The AI agent:
1. Retrieves relevant information from the standards
2. Extracts parameters from the scenario
3. Calculates the journal entries
4. Presents the accounting treatment

This implementation showcases how AI can assist in applying Islamic finance standards to real-world scenarios.
