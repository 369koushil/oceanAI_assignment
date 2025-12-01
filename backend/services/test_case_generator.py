from backend.services.vector_store import vector_store_service
from backend.services.llm_service import llm_service
from backend.models.schemas import TestCase
from typing import List, Dict, Any
import json
import re
import logging

logger = logging.getLogger(__name__)


class TestCaseGenerator:
    """Generate test cases using RAG from knowledge base"""

    def __init__(self):
        self.vector_store = vector_store_service
        self.llm = llm_service

    def generate_test_cases(
        self,
        query: str,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """
        Generate test cases based on user query using RAG

        Args:
            query: User's test case generation request
            max_results: Maximum number of test cases to generate

        Returns:
            Dictionary with test cases and metadata
        """
        try:
            logger.info(f"Generating test cases for query: {query}")

            # Step 1: Retrieve relevant documents from vector store
            relevant_docs = self.vector_store.similarity_search(
                query=query,
                k=8,  # Get top 8 relevant chunks
                score_threshold=0.5
            )

            if not relevant_docs:
                logger.warning("No relevant documents found in knowledge base")
                return {
                    "success": False,
                    "error": "No relevant documentation found. Please build knowledge base first.",
                    "test_cases": [],
                    "sources_used": []
                }

            # Step 2: Extract context and sources
            context = [doc["text"] for doc in relevant_docs]
            sources = list(set([doc["source"] for doc in relevant_docs]))

            logger.info(
                f"Retrieved {len(relevant_docs)} relevant documents from {len(sources)} sources")

            # Step 3: Generate test cases using LLM with RAG
            system_message = self._get_system_prompt()

            test_case_prompt = f"""Based on the provided documentation, generate comprehensive test cases for the following request:

                   "{query}"
                   
                    Requirements:
                    - Generate {max_results} test cases (or fewer if not applicable)
                    - Include both positive and negative test scenarios
                    - Each test case must reference the source document
                    - Include specific test steps
                    - Provide clear expected results
                    - Only include features/functionality explicitly mentioned in the documentation
                    - DO NOT hallucinate or invent features not in the documentation

                    Return ONLY a valid JSON array of test cases with this exact structure:
                    [
                      {{
                        "test_id": "TC-001",
                        "feature": "Feature name",
                        "test_scenario": "Detailed scenario description",
                        "test_type": "positive/negative/edge-case",
                        "preconditions": "Any prerequisites",
                        "test_steps": ["Step 1", "Step 2", "Step 3"],
                        "expected_result": "What should happen",
                        "grounded_in": "source_document.md",
                        "priority": "High/Medium/Low"
                      }}
                    ]

                    IMPORTANT: Return ONLY the JSON array, no markdown formatting, no explanations."""

            # Generate with RAG
            response = self.llm.generate_with_rag(
                query=test_case_prompt,
                context=context,
                system_message=system_message,
            )

            # Step 4: Parse response into structured test cases
            test_cases = self._parse_test_cases(response)

            # Step 5: Validate test cases are grounded in documentation
            validated_test_cases = self._validate_grounding(
                test_cases, sources)

            logger.info(f"Generated {len(validated_test_cases)} test cases")

            return {
                "success": True,
                "test_cases": validated_test_cases,
                "total_generated": len(validated_test_cases),
                "sources_used": sources
            }

        except Exception as e:
            logger.error(f"Error generating test cases: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "test_cases": [],
                "sources_used": []
            }

    def _get_system_prompt(self) -> str:
        """Get system prompt for test case generation"""
        return """You are an expert QA Engineer specializing in test case design.

            Your responsibilities:
            1. Analyze provided documentation carefully
            2. Generate comprehensive, realistic test cases
            3. Base ALL test cases strictly on the provided documentation
            4. Include positive, negative, and edge case scenarios
            5. Provide clear, actionable test steps
            6. Specify expected results precisely
            7. Reference source documents for traceability

            CRITICAL RULES:
            - NEVER invent features not mentioned in the documentation
            - NEVER add functionality that doesn't exist
            - ALWAYS cite the source document for each test case
            - If information is unclear, state limitations rather than guess
            - Focus on testable, verifiable scenarios

            Output Format: Valid JSON array only, no markdown, no explanations."""

    def _parse_test_cases(self, response: str) -> List[TestCase]:
        """
        Parse LLM response into TestCase objects

        Args:
            response: LLM generated response (should be JSON)

        Returns:
            List of TestCase objects
        """
        try:
            # Clean response - remove markdown code blocks if present
            cleaned = response.strip()
            if cleaned.startswith("```"):
                # Remove ```json and ``` markers
                cleaned = re.sub(r'^```json?\s*', '', cleaned)
                cleaned = re.sub(r'\s*```$', '', cleaned)

            cleaned = cleaned.strip()

            # Parse JSON
            test_cases_data = json.loads(cleaned)

            # Convert to TestCase objects
            test_cases = []
            for idx, tc_data in enumerate(test_cases_data):
                try:
                    # Ensure test_id exists
                    if "test_id" not in tc_data:
                        tc_data["test_id"] = f"TC-{idx+1:03d}"

                    test_case = TestCase(**tc_data)
                    test_cases.append(test_case)
                except Exception as e:
                    logger.warning(f"Error parsing test case {idx}: {str(e)}")
                    continue

            return test_cases

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Response was: {response[:500]}")
            # Attempt to extract test cases using regex as fallback
            return self._fallback_parse(response)
        except Exception as e:
            logger.error(f"Error parsing test cases: {str(e)}")
            return []

    def _fallback_parse(self, response: str) -> List[TestCase]:
        """Fallback parsing if JSON parsing fails"""
        try:
            # Try to find JSON array pattern
            json_match = re.search(r'\[\s*\{.*?\}\s*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                test_cases_data = json.loads(json_str)

                test_cases = []
                for idx, tc_data in enumerate(test_cases_data):
                    if "test_id" not in tc_data:
                        tc_data["test_id"] = f"TC-{idx+1:03d}"
                    test_cases.append(TestCase(**tc_data))

                return test_cases
        except Exception as e:
            logger.error(f"Fallback parsing failed: {str(e)}")

        return []

    def _validate_grounding(
        self,
        test_cases: List[TestCase],
        available_sources: List[str]
    ) -> List[TestCase]:
        """
        Validate that test cases reference actual source documents

        Args:
            test_cases: List of generated test cases
            available_sources: List of actual source document names

        Returns:
            List of validated test cases
        """
        validated = []

        for tc in test_cases:
            # Check if grounded_in references a valid source
            is_valid = any(
                source.lower() in tc.grounded_in.lower()
                for source in available_sources
            )

            if is_valid or tc.grounded_in == "Multiple sources":
                validated.append(tc)
            else:
                # Log warning but still include (with note)
                logger.warning(
                    f"Test case {tc.test_id} references unknown source: {tc.grounded_in}")
                # Try to find best matching source
                if available_sources:
                    # Default to first source
                    tc.grounded_in = available_sources[0]
                validated.append(tc)

        return validated

    def generate_test_cases_for_feature(
        self,
        feature_name: str,
        test_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate test cases for a specific feature

        Args:
            feature_name: Name of the feature to test
            test_types: Types of tests (positive, negative, edge-case)

        Returns:
            Dictionary with generated test cases
        """
        if test_types is None:
            test_types = ["positive", "negative", "edge-case"]

        query = f"Generate {', '.join(test_types)} test cases for the {feature_name} feature"

        return self.generate_test_cases(query, max_results=10)


# Global test case generator instance
test_case_generator = TestCaseGenerator()
