import streamlit as st
import json
import os
import re
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="AAOIFI FAS Enhancement Viewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS for better formatting
st.markdown("""
<style>
:root {
  --main-bg: #fff;
  --main-text: #222;
  --card-bg: #f5f5f5;
  --section-title: #1E88E5;
  --subsection-title: #43A047;
  --standard-title-bg: #E3F2FD;
  --standard-title-text: #0D47A1;
  --enhancement-border: #1976D2;
  --approved: #43A047;
  --modified: #FB8C00;
  --rejected: #E53935;
  --highlight: #FFF9C4;
}
@media (prefers-color-scheme: dark) {
  :root {
    --main-bg: #23272f;
    --main-text: #e0e0e0;
    --card-bg: #2c313a;
    --section-title: #90caf9;
    --subsection-title: #81c784;
    --standard-title-bg: #1a2233;
    --standard-title-text: #bbdefb;
    --enhancement-border: #90caf9;
    --approved: #66bb6a;
    --modified: #ffb74d;
    --rejected: #ef5350;
    --highlight: #fff176;
  }
}
body, .main {
  background: var(--main-bg) !important;
  color: var(--main-text) !important;
}
.section-title { color: var(--section-title) !important; }
.subsection-title { color: var(--subsection-title) !important; }
.standard-title {
  background: var(--standard-title-bg) !important;
  color: var(--standard-title-text) !important;
}
.enhancement-card {
  background: var(--card-bg) !important;
  border-left: 5px solid var(--enhancement-border) !important;
  color: var(--main-text) !important;
}
.validation-approved { border-left: 5px solid var(--approved) !important; }
.validation-modified { border-left: 5px solid var(--modified) !important; }
.validation-rejected { border-left: 5px solid var(--rejected) !important; }
.search-highlight {
  background: var(--highlight) !important;
  color: var(--main-text) !important;
}

/* Improve expander styling */
.streamlit-expanderHeader {
    background: linear-gradient(to right, #F5F5F5, #EEEEEE) !important;
    border-radius: 8px !important;
    padding: 12px !important;
    font-weight: 600 !important;
    color: #1E88E5 !important;
    border-left: 4px solid #1976D2 !important;
    transition: all 0.3s ease !important;
}

.streamlit-expanderHeader:hover {
    background: linear-gradient(to right, #EEEEEE, #E0E0E0) !important;
}

.streamlit-expanderContent {
    border-left: 1px solid #E0E0E0 !important;
    border-right: 1px solid #E0E0E0 !important;
    border-bottom: 1px solid #E0E0E0 !important;
    border-radius: 0 0 8px 8px !important;
    padding: 20px !important;
    background-color: #FFFFFF !important;
}

/* Global text styles to ensure visibility */
body, p, li, ul, ol, span, a, div, h1, h2, h3, h4, h5, h6 {
    color: #424242 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

/* Fix markdown formatting */
strong, em {
    color: #1E88E5 !important;
    font-weight: 600 !important;
}

code, pre {
    color: #424242 !important;
    background-color: #F5F5F5 !important;
    padding: 3px 6px !important;
    border-radius: 4px !important;
    border: 1px solid #E0E0E0 !important;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace !important;
}

/* Fix list items and asterisks */
ul, ol, li {
    color: #424242 !important;
    line-height: 1.6 !important;
}

/* Improve bullet points */
ul li::before {
    content: "• ";
    color: #1976D2 !important;
    font-weight: bold;
    display: inline-block; 
    width: 1em;
}

/* Main container styling */
.main {
    padding: 24px;
    color: #424242;
    background-color: #FFFFFF;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #1E88E5;
    margin-bottom: 20px;
    padding: 8px 0;
    border-bottom: 2px solid #1976D2;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.subsection-title {
    font-size: 22px;
    font-weight: 600;
    color: #43A047;
    margin-bottom: 15px;
    margin-top: 25px;
    padding-bottom: 8px;
    border-bottom: 1px solid #81C784;
}

.standard-title {
    font-size: 30px;
    font-weight: 700;
    color: #0D47A1;
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
    border-radius: 8px;
    margin-bottom: 30px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.enhancement-card {
    background-color: #F5F5F5;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border-left: 5px solid #1976D2;
    color: #424242 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.enhancement-card:hover {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
}

/* Fix for Markdown in enhancement cards */
.enhancement-card * {
    color: #424242 !important;
}

/* Fix bullet points and lists */
.enhancement-card ul, 
.enhancement-card ol, 
.enhancement-card li {
    color: #424242 !important;
}

.validation-approved {
    border-left: 5px solid #43A047;
    background: linear-gradient(to right, #E8F5E9, #C8E6C9);
    border-top: 1px solid #43A047;
    border-right: 1px solid #43A047;
    border-bottom: 1px solid #43A047;
}

.validation-modified {
    border-left: 5px solid #FB8C00;
    background: linear-gradient(to right, #FFF3E0, #FFE0B2);
    border-top: 1px solid #FB8C00;
    border-right: 1px solid #FB8C00;
    border-bottom: 1px solid #FB8C00;
}

.validation-rejected {
    border-left: 5px solid #E53935;
    background: linear-gradient(to right, #FFEBEE, #FFCDD2);
    border-top: 1px solid #E53935;
    border-right: 1px solid #E53935;
    border-bottom: 1px solid #E53935;
}

.search-highlight {
    background-color: #FFF9C4;
    color: #424242 !important;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 600;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.agent-tag {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    margin-right: 8px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
}

.agent-tag:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.review-agent {
    background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
    color: #1565C0;
    border: 1px solid #1565C0;
}

.enhancement-agent {
    background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
    color: #2E7D32;
    border: 1px solid #2E7D32;
}

.validation-agent {
    background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
    color: #E65100;
    border: 1px solid #E65100;
}

.fas-badge {
    background: linear-gradient(135deg, #ECEFF1, #CFD8DC);
    color: #455A64;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
    margin-right: 12px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.fas-badge:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown("<h1 style='text-align: center; color: #003366; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); padding: 10px; margin-bottom: 10px;'>AAOIFI FAS Enhancement & Analysis</h1>",
            unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 15px; margin: 0 auto 30px auto; max-width: 800px; background-color: #E6EFF9; border-radius: 10px; color: #003366; font-size: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
This application shows the multi-agent system analysis of AAOIFI Financial Accounting Standards (FAS), 
including standard reviews, proposed enhancements, and validation results.
</div>
""", unsafe_allow_html=True)

# Display information about the multi-agent system
with st.expander("ℹ️ About The Multi-Agent System", expanded=False):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='agent-tag review-agent'>Review & Extraction Agent</div>
        <p>Analyzes standard documents to extract key elements, definitions, principles, and identify unclear areas.</p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='agent-tag enhancement-agent'>Enhancement Agent</div>
        <p>Proposes improvements to the standards based on the analysis, focusing on clarity, contemporary practices, and usability.</p>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='agent-tag validation-agent'>Validation Agent</div>
        <p>Evaluates proposed enhancements for Shariah compliance, consistency, practicality, clarity, relevance, and thoroughness.</p>
        """, unsafe_allow_html=True)

# Path to the JSON file
try:
    # First try the same directory
    json_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "fas_enhancement_results.json")
    if not os.path.exists(json_path):
        # Then try parent directory's notebooks folder
        project_root = Path(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        json_path = project_root / "notebooks" / "fas_enhancement_results.json"

    # Load the JSON data
    with open(json_path, 'r') as f:
        results = json.load(f)
except FileNotFoundError:
    st.error("Error: Could not find the FAS enhancement results file. Make sure 'fas_enhancement_results.json' is in the same directory.")
    st.stop()
except json.JSONDecodeError:
    st.error("Error: Invalid JSON format in the results file.")
    st.stop()

# Display standards in sidebar for navigation
st.sidebar.header("Navigation")
standard_options = {
    "FAS4": "FAS 4 (Murabaha)",
    "FAS10": "FAS 10 (Istisna'a)",
    "FAS32": "FAS 32 (Ijarah)"
}
selected_key = st.sidebar.radio("Select a standard to view:", list(
    standard_options.keys()), format_func=lambda x: standard_options[x])

# Get the standard data
if selected_key in results:
    standard_data = results[selected_key]

    # Display the standard name as a header
    st.markdown(
        f"<div class='standard-title'>{standard_data['standard_name']}</div>", unsafe_allow_html=True)

    # Create tabs for different sections
    tabs = st.tabs(["Standard Information", "Enhancements",
                   "Validation Results", "All Content"])

    # Tab 1: Standard Information
    with tabs[0]:
        st.markdown(
            "<div class='section-title'>Standard Information</div>", unsafe_allow_html=True)
        st.markdown(standard_data["standard_info"])

    # Tab 2: Enhancements
    with tabs[1]:
        st.markdown(
            "<div class='section-title'>Proposed Enhancements</div>", unsafe_allow_html=True)

        # Try to identify separate enhancements in the text
        enhancement_text = standard_data["enhancements"]

        # Extract sections using a better pattern that matches the actual JSON structure
        import re

        # Look for patterns like "**1. Title**" or "**Section:**" which are common in the enhancement content
        # This pattern matches the heading format used in the enhancement sections
        enhancement_sections = re.findall(
            r'(?:\*\*\d+\.\s+[^*]+\*\*|\*\*Section:\*\*)[^\*]+(?=\*\*\d+\.|\*\*Section:\*\*|$)',
            enhancement_text
        )

        # Try to extract the introduction separately
        intro_match = re.search(
            r'^(.*?)(?:\*\*\d+\.|\*\*Section:\*\*)', enhancement_text, re.DOTALL)
        intro_text = intro_match.group(1).strip() if intro_match else ""

        if enhancement_sections:
            # If we found introduction text, display it first
            if intro_text:
                st.markdown(intro_text)

            # Display each enhancement in a card
            for i, section in enumerate(enhancement_sections, 1):
                # Extract the title from the section if possible
                title_match = re.search(r'\*\*([^*]+)\*\*', section)
                title = title_match.group(
                    1) if title_match else f"Enhancement {i}"

                with st.expander(title):
                    # Convert markdown asterisks to HTML for better styling
                    formatted_section = section.strip()
                    # Replace markdown bold with HTML
                    formatted_section = re.sub(
                        r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_section)
                    # Replace markdown italic with HTML
                    formatted_section = re.sub(
                        r'\*(.*?)\*', r'<em>\1</em>', formatted_section)

                    st.markdown(
                        f"<div class='enhancement-card'>{formatted_section}</div>",
                        unsafe_allow_html=True
                    )
        else:
            # If our pattern matching didn't work, try another approach
            # Look for numbered bullet points like "**1. Title**"
            numbered_sections = re.split(
                r'(\*\*\d+\.\s+[^*]+\*\*)', enhancement_text)

            if len(numbered_sections) > 2:  # More than 2 means we found matches
                # First element might be an introduction
                if numbered_sections[0].strip():
                    st.markdown(numbered_sections[0].strip())

                # Process the sections in pairs (heading + content)
                for i in range(1, len(numbered_sections), 2):
                    if i+1 < len(numbered_sections):
                        heading = numbered_sections[i].strip().replace(
                            '**', '')
                        content = numbered_sections[i+1].strip()

                        with st.expander(heading):
                            # Combine the heading and content
                            combined_content = numbered_sections[i] + content
                            # Convert markdown asterisks to HTML for better styling
                            formatted_content = combined_content.strip()
                            # Replace markdown bold with HTML
                            formatted_content = re.sub(
                                r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_content)
                            # Replace markdown italic with HTML
                            formatted_content = re.sub(
                                r'\*(.*?)\*', r'<em>\1</em>', formatted_content)
                            # Handle bullet points
                            formatted_content = re.sub(
                                r'\n\s*\*\s+', r'<br>• ', formatted_content)

                            st.markdown(
                                f"<div class='enhancement-card'>{formatted_content}</div>",
                                unsafe_allow_html=True
                            )
            else:
                # If we still can't split it nicely, just show the whole thing
                st.markdown(enhancement_text)

    # Tab 3: Validation Results
    with tabs[2]:
        st.markdown(
            "<div class='section-title'>Validation Results</div>", unsafe_allow_html=True)

        validation_text = standard_data["validation_results"]

        # Look for common patterns in validation results
        approved_items = []
        modified_items = []
        rejected_items = []

        # Try to extract sections for Approved, Approved with Modifications, and Rejected
        approved_pattern = r'(?:Approved|APPROVED)[:\s]+(.*?)(?=(?:Approved with Modifications|APPROVED WITH MODIFICATIONS|Rejected|REJECTED|\Z))'
        modified_pattern = r'(?:Approved with Modifications|APPROVED WITH MODIFICATIONS)[:\s]+(.*?)(?=(?:Approved|APPROVED|Rejected|REJECTED|\Z))'
        rejected_pattern = r'(?:Rejected|REJECTED)[:\s]+(.*?)(?=(?:Approved|APPROVED|Approved with Modifications|APPROVED WITH MODIFICATIONS|\Z))'

        approved_match = re.search(
            approved_pattern, validation_text, re.DOTALL)
        modified_match = re.search(
            modified_pattern, validation_text, re.DOTALL)
        rejected_match = re.search(
            rejected_pattern, validation_text, re.DOTALL)

        # Create columns for the validation categories
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<div class='subsection-title'>Approved</div>",
                        unsafe_allow_html=True)
            if approved_match:
                # Format the content for better visibility
                approved_content = approved_match.group(1).strip()
                # Replace markdown bold with HTML
                approved_content = re.sub(
                    r'\*\*(.*?)\*\*', r'<strong>\1</strong>', approved_content)
                # Replace markdown italic with HTML
                approved_content = re.sub(
                    r'\*(.*?)\*', r'<em>\1</em>', approved_content)
                # Handle bullet points
                approved_content = re.sub(
                    r'\n\s*\*\s+', r'<br>• ', approved_content)

                st.markdown(
                    f"<div class='enhancement-card validation-approved'>{approved_content}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div style='background-color: #E3F2FD; padding: 15px; border-radius: 5px; border-left: 4px solid #1976D2; color: #0D47A1; text-align: center;'>
                    No explicitly approved enhancements found.
                    </div>
                    """, unsafe_allow_html=True
                )

        with col2:
            st.markdown(
                "<div class='subsection-title'>Approved with Modifications</div>", unsafe_allow_html=True)
            if modified_match:
                # Format the content for better visibility
                modified_content = modified_match.group(1).strip()
                # Replace markdown bold with HTML
                modified_content = re.sub(
                    r'\*\*(.*?)\*\*', r'<strong>\1</strong>', modified_content)
                # Replace markdown italic with HTML
                modified_content = re.sub(
                    r'\*(.*?)\*', r'<em>\1</em>', modified_content)
                # Handle bullet points
                modified_content = re.sub(
                    r'\n\s*\*\s+', r'<br>• ', modified_content)

                st.markdown(
                    f"<div class='enhancement-card validation-modified'>{modified_content}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div style='background-color: #E3F2FD; padding: 15px; border-radius: 5px; border-left: 4px solid #1976D2; color: #0D47A1; text-align: center;'>
                    No enhancements approved with modifications found.
                    </div>
                    """, unsafe_allow_html=True
                )

        with col3:
            st.markdown("<div class='subsection-title'>Rejected</div>",
                        unsafe_allow_html=True)
            if rejected_match:
                # Format the content for better visibility
                rejected_content = rejected_match.group(1).strip()
                # Replace markdown bold with HTML
                rejected_content = re.sub(
                    r'\*\*(.*?)\*\*', r'<strong>\1</strong>', rejected_content)
                # Replace markdown italic with HTML
                rejected_content = re.sub(
                    r'\*(.*?)\*', r'<em>\1</em>', rejected_content)
                # Handle bullet points
                rejected_content = re.sub(
                    r'\n\s*\*\s+', r'<br>• ', rejected_content)

                st.markdown(
                    f"<div class='enhancement-card validation-rejected'>{rejected_content}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div style='background-color: #E6EFF9; padding: 15px; border-radius: 5px; border-left: 4px solid #003366; color: #003366; text-align: center;'>
                    No rejected enhancements found.
                    </div>
                    """, unsafe_allow_html=True
                )

        # If we couldn't parse the validation structure nicely, show the full text
        st.markdown(
            "<div class='subsection-title'>Full Validation Report</div>", unsafe_allow_html=True)
        with st.expander("View Full Validation Report"):
            # Format the validation text for better visibility
            formatted_validation = validation_text
            # Replace markdown bold with HTML
            formatted_validation = re.sub(
                r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_validation)
            # Replace markdown italic with HTML
            formatted_validation = re.sub(
                r'\*(.*?)\*', r'<em>\1</em>', formatted_validation)
            # Handle bullet points
            formatted_validation = re.sub(
                r'\n\s*\*\s+', r'<br>• ', formatted_validation)

            st.markdown(
                f"<div style='background-color: #FFFFFF; padding: 20px; color: #000000; border: 1px solid #DDDDDD; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>{formatted_validation}</div>",
                unsafe_allow_html=True
            )

    # Tab 4: All Content
    with tabs[3]:
        st.markdown(
            "<div class='section-title'>Complete Analysis</div>", unsafe_allow_html=True)

        st.markdown(
            "<div class='subsection-title'>Standard Information</div>", unsafe_allow_html=True)
        with st.expander("View Standard Information", expanded=False):
            # Format the content for better visibility
            standard_info = standard_data["standard_info"]
            # Replace markdown bold with HTML
            standard_info = re.sub(
                r'\*\*(.*?)\*\*', r'<strong>\1</strong>', standard_info)
            # Replace markdown italic with HTML
            standard_info = re.sub(r'\*(.*?)\*', r'<em>\1</em>', standard_info)
            # Handle bullet points
            standard_info = re.sub(r'\n\s*\*\s+', r'<br>• ', standard_info)

            st.markdown(
                f"<div style='background-color: #FFFFFF; padding: 20px; color: #000000; border: 1px solid #DDDDDD; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>{standard_info}</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "<div class='subsection-title'>Proposed Enhancements</div>", unsafe_allow_html=True)
        with st.expander("View Proposed Enhancements", expanded=False):
            # Format the content for better visibility
            enhancements = standard_data["enhancements"]
            # Replace markdown bold with HTML
            enhancements = re.sub(
                r'\*\*(.*?)\*\*', r'<strong>\1</strong>', enhancements)
            # Replace markdown italic with HTML
            enhancements = re.sub(r'\*(.*?)\*', r'<em>\1</em>', enhancements)
            # Handle bullet points
            enhancements = re.sub(r'\n\s*\*\s+', r'<br>• ', enhancements)

            st.markdown(
                f"<div style='background-color: #FFFFFF; padding: 20px; color: #000000; border: 1px solid #DDDDDD; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>{enhancements}</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "<div class='subsection-title'>Validation Results</div>", unsafe_allow_html=True)
        with st.expander("View Validation Results", expanded=False):
            # Format the content for better visibility
            validation = standard_data["validation_results"]
            # Replace markdown bold with HTML
            validation = re.sub(
                r'\*\*(.*?)\*\*', r'<strong>\1</strong>', validation)
            # Replace markdown italic with HTML
            validation = re.sub(r'\*(.*?)\*', r'<em>\1</em>', validation)
            # Handle bullet points
            validation = re.sub(r'\n\s*\*\s+', r'<br>• ', validation)

            st.markdown(
                f"<div style='background-color: #F8F9FA; padding: 15px; color: #333333;'>{validation}</div>",
                unsafe_allow_html=True
            )

# Add a search functionality
st.sidebar.markdown("---")
st.sidebar.header("Search")
search_term = st.sidebar.text_input("Search for specific topics:")

# Function to highlight search terms


def highlight_text(text, search):
    if not search or search.strip() == "":
        return text

    # Escape special regex characters in the search term
    escaped_search = re.escape(search)
    highlighted_text = re.sub(
        f'({escaped_search})',
        r'<span class="search-highlight">\1</span>',
        text,
        flags=re.IGNORECASE
    )
    return highlighted_text


# Display search results if search term is provided
if search_term:
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### Search Results for '{search_term}'")

    results_found = False
    for std_key, std_data in results.items():
        hits = 0

        # Search in standard info
        if search_term.lower() in std_data["standard_info"].lower():
            hits += std_data["standard_info"].lower().count(search_term.lower())

        # Search in enhancements
        if search_term.lower() in std_data["enhancements"].lower():
            hits += std_data["enhancements"].lower().count(search_term.lower())

        # Search in validation results
        if search_term.lower() in std_data["validation_results"].lower():
            hits += std_data["validation_results"].lower().count(search_term.lower())

        if hits > 0:
            results_found = True
            st.sidebar.markdown(
                f"<div class='fas-badge'>{standard_options[std_key]}</div> {hits} occurrences", unsafe_allow_html=True)

    if not results_found:
        st.sidebar.markdown(
            """
            <div style='background-color: #E3F2FD; padding: 10px; border-radius: 5px; border-left: 4px solid #1976D2; color: #0D47A1; margin-top: 10px;'>
            No matching results found.
            </div>
            """, unsafe_allow_html=True
        )

if search_term:
    st.sidebar.markdown("### Search Results")
    for key, value in results.items():
        found = False
        locations = []

        # Search in standard info
        if search_term.lower() in value["standard_info"].lower():
            found = True
            locations.append("Standard Information")

        # Search in enhancements
        if search_term.lower() in value["enhancements"].lower():
            found = True
            locations.append("Enhancements")

        # Search in validation
        if search_term.lower() in value["validation_results"].lower():
            found = True
            locations.append("Validation Results")

        if found:
            st.sidebar.markdown(
                f"**{value['standard_name']}**: Found in {', '.join(locations)}")

# About section
st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color: #0D47A1;'>About</h2>",
                    unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div style='background-color: #E3F2FD; padding: 15px; border-radius: 5px; border-left: 4px solid #1976D2; color: #0D47A1; font-weight: 500;'>
    This app displays the results of the multi-agent system analysis 
    of AAOIFI Financial Accounting Standards (FAS) from Challenge 3 
    of the Islamic Development Bank AI Hackathon.
    </div>
    """, unsafe_allow_html=True
)
