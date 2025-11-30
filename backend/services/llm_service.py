from openai import OpenAI
from typing import Optional, Dict, Any, List
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):
        self.model_name = OPENAI_MODEL
        self.api_key = OPENAI_API_KEY
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        try:
            self.client = OpenAI(api_key=self.api_key)
            logger.info(
                f"OpenAI client initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error initializing OpenAI: {e}")
            raise

    # ========================== BASIC GENERATION ==========================
    def generate(self, prompt: str, temperature: float = 0.3, system_message: Optional[str] = None) -> str:
        """Simple LLM call"""
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=2048,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise

    # ========================== RAG GENERATION ==========================
    def generate_with_rag(self, query: str, context: List[str], system_message: Optional[str] = None) -> str:
        """Enhanced RAG generation"""

        context_text = "\n\n---DOCUMENT---\n\n".join([
            f"[Document {i+1}]\n{ctx}" for i, ctx in enumerate(context)
        ])

        if not system_message:
            system_message = (
                "You are a QA expert. ONLY use the documentation provided.\n"
                "Rules:\n"
                "1. Never invent features not in the docs.\n"
                "2. If information is missing, say: 'Not specified in documentation'.\n"
                "3. Reference the source document for each fact.\n"
            )

        user_prompt = f"""
User Query:
{query}

========= DOCUMENTATION =========
{context_text}
========= END =========

Instructions:
- Use ONLY the information above.
- Be accurate with numbers, labels, UI text, rules, validations.
- If missing, explicitly state it.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=2048,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error in RAG generation: {e}")
            raise

    # ========================== STRUCTURED JSON ==========================
    def generate_structured_output(self, prompt: str, system_message: str, temperature: float = 0.1) -> str:
        """Strict JSON output"""

        enhanced_system = (
            system_message
            + "\n\nSTRICT RULES:\n"
              "1. Return ONLY valid JSON.\n"
              "2. No markdown, no ```json code blocks.\n"
              "3. Double quotes only.\n"
              "4. Must be parseable.\n"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": enhanced_system},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=2048,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating structured JSON: {e}")
            raise

    # ========================== SELENIUM GENERATION ==========================
    def generate_selenium_script(
        self,
        test_case: Dict[str, Any],
        html_elements: Dict[str, Any],
        context: List[str],
    ) -> str:
        """Generate bulletproof Selenium Python script"""

        # Case: Missing selectors → prevent hallucinations
        if not html_elements:
            return (
                "# ERROR: html_elements is empty or missing.\n"
                "# A Selenium script cannot be generated without selectors.\n"
            )

        elements_json = json.dumps(html_elements, indent=2)
        steps = test_case.get("test_steps", [])
        steps_text = "\n".join([f"- {s}" for s in steps])

        sys_msg = """
You are a senior automation engineer (10+ years experience).
Generate a production-grade Python Selenium script.

NON-NEGOTIABLE RULES:
1. Use ONLY element selectors provided in html_elements. NEVER invent selectors.
2. Forbidden selectors: generic XPaths (//button, //*). Do NOT use them.
3. Always use WebDriverWait (no time.sleep).
4. Use webdriver-manager for Chrome.
5. Every script MUST include at least one assertion validating the expected result.
6. If a required selector is missing, include:
   # ERROR: Selector missing in html_elements
7. Load checkout page using:
   driver.get("file://" + os.path.abspath("checkout.html"))
8. Output ONLY Python code (no markdown).
"""

        user_prompt = f"""
Generate Selenium script for the following test case:

=== TEST CASE ===
Test ID: {test_case.get("test_id")}
Feature: {test_case.get("feature")}
Scenario: {test_case.get("test_scenario")}
Type: {test_case.get("test_type")}
Preconditions: {test_case.get("preconditions")}
Steps:
{steps_text}
Expected Result:
{test_case.get("expected_result")}

=== HTML ELEMENTS ===
{elements_json}

=== CONTEXT (Documentation) ===
{context[0] if context else "No context"}

Output:
- ONLY Python code
- No markdown
- No comments outside the Python script
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=3072,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating Selenium script: {e}")
            raise

    # ========================== HEALTH CHECK ==========================
    def health_check(self) -> bool:
        try:
            # Simple check - just verify client exists
            if self.client and self.api_key:
                logger.info(
                    f"✓ OpenAI client initialized with model: {self.model_name}")
                return True
            return False

        except Exception as e:
            logger.error(f"OpenAI health check failed: {str(e)}")
            return False


# Global instance
llm_service = LLMService()
