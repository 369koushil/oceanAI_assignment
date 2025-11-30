"""
Streamlit Frontend for Autonomous QA Agent
Modern UI with latest Streamlit features
"""
import streamlit as st
import requests
import json
from typing import List, Dict, Any
import time

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Page config
st.set_page_config(
    page_title="Autonomous QA Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Minimal padding and clean design
st.markdown("""
<style>
    /* Remove top padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    h1 {
        margin-top: 0rem;
    }
    
    /* Sidebar padding */
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }
    
    /* Simple messages */
    .stAlert {
        padding: 0.75rem 1rem;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: start;
        margin-bottom: 2rem;
    }
    
    .test-case-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
    }
    
     section[data-testid="stSidebar"] h2 {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    section[data-testid="stSidebar"] .stButton {
        margin-top: 0rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Remove top padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* REMOVE THE ENTIRE SIDEBAR HEADER (logo, collapse button, spacing) */
[data-testid="stSidebarHeader"] {
    display: none !important;
}

[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

[data-testid="stLogo"] {
    display: none !important;
}

    
    h1 {
        margin-top: 0rem;
    }
    
    /* Sidebar - Remove ALL extra spacing */
    section[data-testid="stSidebar"] > div {
        padding-top: 0.5rem;
    }
    
    /* Sidebar elements - tight spacing */
    section[data-testid="stSidebar"] .element-container {
        margin-bottom: 0rem !important;
    }
    
    /* Sidebar alerts - no margin */
    section[data-testid="stSidebar"] .stAlert {
        margin-bottom: 0.25rem !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    /* Sidebar headers - tight spacing */
    section[data-testid="stSidebar"] .stHeading {
        margin-top: 0.5rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Sidebar dividers - minimal spacing */
    section[data-testid="stSidebar"] hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Sidebar buttons - no margin */
    section[data-testid="stSidebar"] .stButton {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    /* Sidebar vertical blocks - tight */
    section[data-testid="stSidebar"] .stVerticalBlock {
        gap: 0.25rem !important;
    }
    
    /* Simple messages */
    .stAlert {
        padding: 0.75rem 1rem;
    }
    
    /* Main header */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: start;
        margin-bottom: 2rem;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'knowledge_base_built' not in st.session_state:
    st.session_state.knowledge_base_built = False
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'generated_script' not in st.session_state:
    st.session_state.generated_script = ""
if 'html_uploaded' not in st.session_state:
    st.session_state.html_uploaded = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1


def check_backend_health() -> Dict[str, Any]:
    """Check if backend is running and healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"status": "unhealthy"}
    except:
        return {"status": "offline"}


def upload_documents(files: List) -> Dict[str, Any]:
    """Upload support documents to backend"""
    try:
        files_data = []
        for file in files:
            files_data.append(('files', (file.name, file.getvalue(), file.type)))
        
        response = requests.post(
            f"{API_BASE_URL}/api/upload-documents",
            files=files_data,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def upload_html(file) -> Dict[str, Any]:
    """Upload HTML file to backend"""
    try:
        files = {'file': (file.name, file.getvalue(), 'text/html')}
        response = requests.post(
            f"{API_BASE_URL}/api/upload-html",
            files=files,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_test_cases(query: str, max_cases: int = 10) -> Dict[str, Any]:
    """Generate test cases using RAG"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/generate-test-cases",
            json={"query": query, "max_test_cases": max_cases},
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_selenium_script(test_case: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Selenium script for a test case"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/generate-selenium-script",
            json={"test_case": test_case, "html_content": ""},
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">Autonomous QA Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar - System Status
    with st.sidebar:
        st.header("System Status")

        health = check_backend_health()

        ok_backend = health.get("status") == "healthy"
        ok_qdrant = health.get("qdrant_connected")
        ok_llm = health.get("LLM_available")
        ok_embed = health.get("embedding_model_loaded")

        all_ok = ok_backend and ok_qdrant and ok_llm and ok_embed

        status_text = f"""
        **Backend:** {"Online" if ok_backend else "Offline"}  
        **Qdrant:** {"Connected" if ok_qdrant else "Disconnected"}  
        **LLM:** {"Available" if ok_llm else "Unavailable"}  
        **Embeddings:** {"Loaded" if ok_embed else "Not Loaded"}  
        """

        if all_ok:
            st.success(status_text)
        else:
            st.error(status_text)


        
        st.divider()
        
        st.header("Knowledge Base")
        if st.session_state.knowledge_base_built:
            st.success("Knowledge Base Built")
        else:
            st.warning("Knowledge Base Not Built")
        
        if st.session_state.html_uploaded:
            st.success("HTML File Uploaded")
        else:
            st.warning("HTML File Not Uploaded")
        
        st.divider()
        
        st.header("Current Step")
        st.info(f"Step {st.session_state.current_step} of 3")
        
        st.divider()
        
        # Reset button
        if st.button("🔄 Reset Knowledge base"):
            try:
                requests.delete(f"{API_BASE_URL}/api/knowledge-base/reset")
                st.session_state.knowledge_base_built = False
                st.session_state.html_uploaded = False
                st.session_state.test_cases = []
                st.session_state.current_step = 1
                st.success("Reset complete!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Show appropriate step based on current_step
    if st.session_state.current_step == 1:
        show_step1()
    elif st.session_state.current_step == 2:
        show_step2()
    elif st.session_state.current_step == 3:
        show_step3()


def show_step1():
    """Step 1: Knowledge Base Building"""
    st.header("📁 Step 1: Build Knowledge Base")
    st.markdown("Upload your support documents and target HTML file to build the knowledge base.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Support Documents")
        
        uploaded_docs = st.file_uploader(
            "Upload 3-5 documentation files (MD, TXT, JSON, PDF)",
            type=['md', 'txt', 'json', 'pdf'],
            accept_multiple_files=True,
            key="doc_uploader"
        )
        
        if uploaded_docs:
            st.success(f"{len(uploaded_docs)} files selected")
            for doc in uploaded_docs:
                st.text(f"📄 {doc.name}")
    
    with col2:
        st.subheader("🌐 Target HTML File")
        
        uploaded_html = st.file_uploader(
            "Upload the html file",
            type=['html'],
            key="html_uploader"
        )
        
        if uploaded_html:
            st.success(f"{uploaded_html.name} selected")
    
    st.divider()
    
    # Build Knowledge Base Button
    if st.button("Build Knowledge Base", type="primary"):
        if not uploaded_docs:
            st.error("Please upload support documents")
        elif not uploaded_html:
            st.error("Please upload HTML file")
        else:
            with st.spinner("Processing documents..."):
                # Upload documents
                doc_result = upload_documents(uploaded_docs)
                
                if doc_result.get("success"):
                    st.success(f"Processed {doc_result['document_count']} documents into {doc_result['chunks_created']} chunks")
                    
                    # Upload HTML
                    html_result = upload_html(uploaded_html)
                    
                    if html_result.get("success"):
                        st.success(f"HTML file processed: {html_result['chunks_created']} chunks created")
                        st.session_state.knowledge_base_built = True
                        st.session_state.html_uploaded = True
                        st.session_state.current_step = 2
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Error: {html_result.get('error')}")
                else:
                    st.error(f"Error: {doc_result.get('error')}")


def show_step2():
    """Step 2: Test Case Generation"""
    st.header("✅ Step 2: Generate Test Cases")
    
    if not st.session_state.knowledge_base_built:
        st.warning("Please build the knowledge base first")
        if st.button("Go to Step 1"):
            st.session_state.current_step = 1
            st.rerun()
        return
    
    st.markdown("Ask the AI agent to generate test cases based on your documentation.")
    
    # Query input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_area(
            "Test Case Generation Query",
            placeholder="Example: Generate all positive and negative test cases for the discount code feature",
            height=100
        )
    
    with col2:
        max_cases = st.number_input(
            "Max Test Cases",
            min_value=1,
            max_value=20,
            value=10
        )
    
    # Generate button
    if st.button("🚀 Generate Test Cases", type="primary"):
        if not query:
            st.error("Please enter a query")
        else:
            with st.spinner("🤖 AI is generating test cases..."):
                result = generate_test_cases(query, max_cases)
                
                if result.get("success"):
                    st.session_state.test_cases = result.get("test_cases", [])
                    st.success(f"Generated {len(st.session_state.test_cases)} test cases!")
                    
                    # Show sources used
                    sources = result.get("sources_used", [])
                    if sources:
                        st.info(f"Sources used: {', '.join(sources)}")
                    
                    # Auto-advance to next step
                    st.session_state.current_step = 3
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result.get('error')}")
    
    # Display test cases
    if st.session_state.test_cases:
        st.divider()
        st.subheader(f"Generated Test Cases ({len(st.session_state.test_cases)})")
        
        for idx, tc in enumerate(st.session_state.test_cases):
            with st.expander(f"{tc['test_id']} - {tc['feature']}", expanded=False):
                st.markdown(f"**Scenario:** {tc['test_scenario']}")
                st.markdown(f"**Type:** `{tc['test_type']}`")
                st.markdown(f"**Priority:** `{tc.get('priority', 'Medium')}`")
                
                if tc.get('preconditions'):
                    st.markdown(f"**Preconditions:** {tc['preconditions']}")
                
                st.markdown("**Test Steps:**")
                for step_idx, step in enumerate(tc['test_steps'], 1):
                    st.markdown(f"{step_idx}. {step}")
                
                st.markdown(f"**Expected Result:** {tc['expected_result']}")
                st.markdown(f"**Grounded In:** `{tc['grounded_in']}`")
        
        # Option to proceed to next step
        if st.button("Proceed to Generate Scripts"):
            st.session_state.current_step = 3
            st.rerun()


def show_step3():
    """Step 3: Selenium Script Generation"""
    st.header("🤖 Step 3: Generate Selenium Scripts")
    
    if not st.session_state.test_cases:
        st.warning("Please generate test cases first")
        if st.button("Go to Step 2"):
            st.session_state.current_step = 2
            st.rerun()
        return
    
    st.markdown("📄 Select a test case to generate an executable Python Selenium script.")
    
    # Test case selection
    test_case_options = [f"{tc['test_id']} - {tc['feature']}" for tc in st.session_state.test_cases]
    selected_option = st.selectbox(
        "Select Test Case",
        options=test_case_options
    )
    
    selected_idx = test_case_options.index(selected_option)
    selected_tc = st.session_state.test_cases[selected_idx]
    
    # Show selected test case details
    with st.expander("Selected Test Case Details", expanded=True):
        st.markdown(f"**Test ID:** {selected_tc['test_id']}")
        st.markdown(f"**Feature:** {selected_tc['feature']}")
        st.markdown(f"**Scenario:** {selected_tc['test_scenario']}")
        st.markdown(f"**Expected Result:** {selected_tc['expected_result']}")
    
    # Generate script button
    if st.button("Generate Selenium Script", type="primary"):
        with st.spinner("🤖 AI is generating Selenium script..."):
            result = generate_selenium_script(selected_tc)
            
            if result.get("success"):
                st.session_state.generated_script = result.get("script", "")
                st.success("✅ Selenium script generated successfully!")
            else:
                st.error(f"❌ Error: {result.get('error')}")
    
    # Display generated script
    if st.session_state.generated_script:
        st.divider()
        st.subheader("📜 Generated Selenium Script")
        
        st.code(st.session_state.generated_script, language="python")
        
        # Download button
        st.download_button(
            label="💾 Download Script",
            data=st.session_state.generated_script,
            file_name=f"{selected_tc['test_id']}_selenium_test.py",
            mime="text/x-python"
        )


if __name__ == "__main__":
    main()