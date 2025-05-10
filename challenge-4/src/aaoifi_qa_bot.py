import os
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import Document

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in environment variables. Please check your .env file."
    )

# Configure paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(os.path.dirname(PROJECT_DIR), "data")
VECTOR_DB_DIR = os.path.join(PROJECT_DIR, "vector_db", "aaoifi_standards")


class AAOIFIQABot:
    def __init__(self, temperature=0.2, num_results=5):
        print(f"Initializing AAOIFI QA Bot...")
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", temperature=temperature
        )
        self.num_results = num_results

        # Initialize vector store
        if not os.path.exists(VECTOR_DB_DIR) or os.listdir(VECTOR_DB_DIR) == []:
            print("Vector database not found or empty. Creating new database...")
            self.vectorstore = self._create_vector_store()
        else:
            print("Loading existing vector database...")
            self.vectorstore = Chroma(
                persist_directory=VECTOR_DB_DIR, embedding_function=self.embeddings
            )
            print(
                f"Vector database loaded with {self.vectorstore._collection.count()} documents"
            )

        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": self.num_results}
        )

        # Setup the QA chain
        self._setup_qa_chain()

        # Keep track of the last retrieved documents
        self.last_retrieved_docs = []

    def _create_vector_store(self) -> Chroma:
        """Create a vector store from the AAOIFI standards documents"""
        documents = self._load_documents()

        if not documents:
            print(
                "No documents were loaded! Check the data directory and file formats."
            )
            return None

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(documents)

        print(f"Creating vector store with {len(splits)} document chunks...")

        if len(splits) == 0:
            print(
                "Warning: No document chunks were created! Check if documents contain text."
            )
            return None

        # Create and persist the vector store
        vectorstore = Chroma.from_documents(
            documents=splits, embedding=self.embeddings, persist_directory=VECTOR_DB_DIR
        )
        print(f"Vector store created with {vectorstore._collection.count()} documents")
        return vectorstore

    def _load_documents(self) -> List[Document]:
        """Load all FAS and SS documents from the data directory"""
        documents = []

        if not os.path.exists(DATA_DIR):
            raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

        print(f"Loading documents from {DATA_DIR}...")

        # List all files in data directory
        all_files = os.listdir(DATA_DIR)
        fas_ss_files = [f for f in all_files if f.upper().startswith(("FAS", "SS"))]

        print(
            f"Found {len(fas_ss_files)} potential FAS/SS files: {', '.join(fas_ss_files)}"
        )

        total_loaded = 0
        for filename in fas_ss_files:
            file_path = os.path.join(DATA_DIR, filename)

            # Skip directories
            if os.path.isdir(file_path):
                continue

            try:
                if filename.lower().endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    doc_pages = loader.load()
                    # Add source metadata
                    for doc in doc_pages:
                        if "source" not in doc.metadata:
                            doc.metadata["source"] = filename
                    documents.extend(doc_pages)
                    print(f"Loaded PDF: {filename} - {len(doc_pages)} pages")
                    total_loaded += len(doc_pages)
                elif filename.lower().endswith(".txt"):
                    loader = TextLoader(file_path)
                    doc_pages = loader.load()
                    # Add source metadata
                    for doc in doc_pages:
                        if "source" not in doc.metadata:
                            doc.metadata["source"] = filename
                    documents.extend(doc_pages)
                    print(f"Loaded TXT: {filename} - {len(doc_pages)} pages")
                    total_loaded += len(doc_pages)
                else:
                    print(f"Skipping unsupported file format: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {str(e)}")

        if not documents:
            print(
                "WARNING: No documents were loaded. Check your data directory and file formats."
            )
            return []

        print(
            f"Successfully loaded {len(documents)} document pages from {total_loaded} files."
        )
        return documents

    def _setup_qa_chain(self):
        """Set up the QA chain for answering questions about AAOIFI standards"""
        # Template for formatting context and questions
        template = """
        You are an expert assistant specializing in Islamic financial standards, particularly the AAOIFI (Accounting and Auditing Organization for Islamic Financial Institutions) standards. 
        
        Answer the question based on the following context from AAOIFI Financial Accounting Standards (FAS) and Sharia Standards (SS).
        
        If you don't know the answer or the information is not in the context, say "I don't have enough information to answer this question." 
        Do not make up information that is not provided in the context.
        
        Always indicate which specific standard (FAS or SS and its number) you are referencing in your answer.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """

        # Create the prompt from template
        prompt = ChatPromptTemplate.from_template(template)

        # Create the RAG chain
        self.qa_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
        )

    def answer_question(self, question: str) -> str:
        """Answer a question using the QA chain"""
        try:
            print(f"Retrieving relevant documents for: '{question}'")
            # Get retrieval results directly to debug
            retrieved_docs = self.retriever.invoke(question)
            self.last_retrieved_docs = retrieved_docs  # Store for later access
            print(f"Retrieved {len(retrieved_docs)} documents")

            if len(retrieved_docs) == 0:
                return "No relevant information found in the standards. Please try a different question."

            # Print a preview of the first document to verify content
            if retrieved_docs:
                print(
                    f"First document preview: {retrieved_docs[0].page_content[:150]}..."
                )

            # Continue with the chain
            response = self.qa_chain.invoke(question)
            return response.content
        except Exception as e:
            return f"Error processing your question: {str(e)}"

    def get_retrieved_documents(self) -> List[Document]:
        """Get the documents retrieved for the last question"""
        return self.last_retrieved_docs

    def set_temperature(self, temperature: float):
        """Set the temperature for the LLM"""
        if hasattr(self, "llm") and hasattr(self.llm, "temperature"):
            self.llm.temperature = temperature

    def set_num_results(self, num_results: int):
        """Set the number of results to retrieve"""
        self.num_results = num_results
        if hasattr(self, "retriever") and hasattr(self.retriever, "search_kwargs"):
            self.retriever.search_kwargs["k"] = num_results

    def run_interactive_qa(self):
        """Run an interactive QA session in the terminal"""
        print("\n=== AAOIFI Standards QA Bot ===")
        print(
            "Ask questions about AAOIFI Financial Accounting Standards (FAS) and Sharia Standards (SS)."
        )
        print("Type 'exit' or 'quit' to end the session.\n")

        while True:
            question = input("\nEnter your question: ")

            if question.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if not question.strip():
                continue

            print("\nThinking...")
            answer = self.answer_question(question)
            print(f"\nAnswer: {answer}\n")


if __name__ == "__main__":
    try:
        qa_bot = AAOIFIQABot()
        qa_bot.run_interactive_qa()
    except KeyboardInterrupt:
        print("\nSession terminated by user.")
    except Exception as e:
        print(f"Error: {str(e)}")
