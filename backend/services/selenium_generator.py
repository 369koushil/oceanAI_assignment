"""
Selenium Script Generation Service
Generates executable Python Selenium scripts from test cases
"""
import json
from backend.services.vector_store import vector_store_service
from backend.services.llm_service import llm_service
from backend.models.schemas import TestCase
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import re
import logging


logger = logging.getLogger(__name__)


class SeleniumScriptGenerator:
    """Generate Selenium Python scripts from test cases"""
    
    def __init__(self):
        self.vector_store = vector_store_service
        self.llm = llm_service
    
    def generate_script(
        self,
        test_case: TestCase,
        html_content: str
    ) -> Dict[str, Any]:
        """
        Generate Selenium script for a given test case
        
        Args:
            test_case: TestCase object to convert to script
            html_content: HTML content of the target page
            
        Returns:
            Dictionary with generated script and metadata
        """
        try:
            logger.info(f"Generating Selenium script for {test_case.test_id}")
            
            # Step 1: Analyze HTML to extract element selectors
            element_info = self._analyze_html(html_content)
            
            # Step 2: Retrieve relevant documentation
            relevant_docs = self.vector_store.similarity_search(
                query=f"{test_case.feature} {test_case.test_scenario}",
                k=5,
                score_threshold=0.5
            )
            
            context = [doc["text"] for doc in relevant_docs] if relevant_docs else []
            
            # Step 3: Use enhanced LLM method with better prompts
            script = self.llm.generate_selenium_script(
                test_case=test_case.dict(),
                html_elements=element_info,
                context=context
            )
            
            # Step 4: Validate and clean script
            cleaned_script = self._clean_script(script)
            
            logger.info(f"Successfully generated script for {test_case.test_id}")
            
            return {
                "success": True,
                "script": cleaned_script,
                "test_case_id": test_case.test_id,
                "language": "python"
            }
            
        except Exception as e:
            logger.error(f"Error generating Selenium script: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "script": "",
                "test_case_id": test_case.test_id
            }
    
    def _analyze_html(self, html_content: str) -> Dict[str, Any]:
        """
        Analyze HTML to extract useful element information with detailed selectors
        
        Args:
            html_content: HTML source code
            
        Returns:
            Dictionary with comprehensive element information
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            elements_info = {
                "buttons": [],
                "inputs": [],
                "selects": [],
                "forms": [],
                "radio_buttons": [],
                "textareas": [],
                "all_ids": [],
                "clickable_elements": []
            }
            
            # Extract ALL buttons with detailed info
            for btn in soup.find_all('button'):
                info = {
                    "tag": "button",
                    "id": btn.get('id', ''),
                    "name": btn.get('name', ''),
                    "class": ' '.join(btn.get('class', [])),
                    "onclick": btn.get('onclick', ''),
                    "text": btn.get_text(strip=True),
                    "type": btn.get('type', 'button'),
                    "selector_by_id": f"By.ID, '{btn.get('id')}'" if btn.get('id') else None,
                    "selector_by_text": f"By.XPATH, \"//button[text()='{btn.get_text(strip=True)}']\"" if btn.get_text(strip=True) else None
                }
                elements_info["buttons"].append(info)
                if btn.get('id'):
                    elements_info["all_ids"].append(btn.get('id'))
            
            # Extract ALL input fields with detailed info
            for inp in soup.find_all('input'):
                info = {
                    "tag": "input",
                    "type": inp.get('type', 'text'),
                    "id": inp.get('id', ''),
                    "name": inp.get('name', ''),
                    "placeholder": inp.get('placeholder', ''),
                    "class": ' '.join(inp.get('class', [])),
                    "value": inp.get('value', ''),
                    "selector_by_id": f"By.ID, '{inp.get('id')}'" if inp.get('id') else None,
                    "selector_by_name": f"By.NAME, '{inp.get('name')}'" if inp.get('name') else None
                }
                
                # Separate radio buttons
                if inp.get('type') == 'radio':
                    elements_info["radio_buttons"].append(info)
                else:
                    elements_info["inputs"].append(info)
                
                if inp.get('id'):
                    elements_info["all_ids"].append(inp.get('id'))
            
            # Extract textareas
            for textarea in soup.find_all('textarea'):
                info = {
                    "tag": "textarea",
                    "id": textarea.get('id', ''),
                    "name": textarea.get('name', ''),
                    "class": ' '.join(textarea.get('class', [])),
                    "placeholder": textarea.get('placeholder', ''),
                    "selector_by_id": f"By.ID, '{textarea.get('id')}'" if textarea.get('id') else None,
                    "selector_by_name": f"By.NAME, '{textarea.get('name')}'" if textarea.get('name') else None
                }
                elements_info["textareas"].append(info)
                if textarea.get('id'):
                    elements_info["all_ids"].append(textarea.get('id'))
            
            # Extract forms
            for form in soup.find_all('form'):
                info = {
                    "tag": "form",
                    "id": form.get('id', ''),
                    "name": form.get('name', ''),
                    "action": form.get('action', ''),
                    "method": form.get('method', ''),
                    "selector_by_id": f"By.ID, '{form.get('id')}'" if form.get('id') else None
                }
                elements_info["forms"].append(info)
            
            # Extract clickable elements (with onclick)
            for elem in soup.find_all(onclick=True):
                elements_info["clickable_elements"].append({
                    "tag": elem.name,
                    "id": elem.get('id', ''),
                    "text": elem.get_text(strip=True),
                    "onclick": elem.get('onclick')
                })
            
            return elements_info
            
        except Exception as e:
            logger.error(f"Error analyzing HTML: {str(e)}")
            return {}
    
    def _clean_script(self, script: str) -> str:
        """
        Clean and format the generated script
        
        Args:
            script: Raw generated script
            
        Returns:
            Cleaned script
        """
        # Remove markdown code blocks if present
        script = re.sub(r'^```python\s*', '', script, flags=re.MULTILINE)
        script = re.sub(r'^```\s*$', '', script, flags=re.MULTILINE)
        script = script.strip()
        
        # Ensure proper imports are present
        required_imports = [
            "from selenium import webdriver",
            "from selenium.webdriver.common.by import By",
            "from selenium.webdriver.support.ui import WebDriverWait",
            "from selenium.webdriver.support import expected_conditions as EC"
        ]
        
        # Check if imports are present
        has_imports = any(imp in script for imp in required_imports)
        
        if not has_imports:
            # Add imports at the beginning
            imports_block = """from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

"""
            script = imports_block + script
        
        return script


# Global selenium generator instance
selenium_generator = SeleniumScriptGenerator()