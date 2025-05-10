"""
Setup script for the Ijarah Accounting RAG System
"""

import os
import sys
import shutil

def create_folder_structure():
    """Create the necessary folder structure if it doesn't exist"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    # Define folders to create
    folders = [
        os.path.join(parent_dir, "vector_db"),
        os.path.join(parent_dir, "vector_db", "ijarah_standards"),
    ]
    
    # Create folders
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created directory: {folder}")
        else:
            print(f"Directory already exists: {folder}")

def check_data_files():
    """Check if the required data files exist"""
    # Get the parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    # Define files to check
    files = [
        os.path.join(parent_dir, "data", "FAS32.pdf"),
        os.path.join(parent_dir, "data", "SS9.pdf"),
    ]
    
    # Check files
    all_files_exist = True
    for file in files:
        if not os.path.exists(file):
            print(f"WARNING: File not found: {file}")
            all_files_exist = False
    
    if all_files_exist:
        print("All required data files found!")
    else:
        print("\nMake sure you have the following files in the data directory:")
        print("  - FAS32.pdf")
        print("  - SS9.pdf")

def check_env_file():
    """Check if the .env file exists and create a template if it doesn't"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(current_dir, ".env")
    
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write("# OpenAI API Key\n")
            f.write("OPENAI_API_KEY=your-api-key\n")
        print(f"Created template .env file: {env_file}")
        print("IMPORTANT: Edit the .env file and add your OpenAI API key.")
    else:
        print(f".env file already exists: {env_file}")

def main():
    """Main function to set up the environment"""
    print("Setting up the environment for the Ijarah Accounting RAG System...")
    create_folder_structure()
    check_data_files()
    check_env_file()
    print("\nSetup complete!")

if __name__ == "__main__":
    main()
