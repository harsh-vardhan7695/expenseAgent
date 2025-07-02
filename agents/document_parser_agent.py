import os
import base64
import json
from autogen import Agent, AssistantAgent
from typing import List, Dict

class DocumentParserAgent(Agent):
    def __init__(self, name="DocumentParserAgent"):
        super().__init__(name)
        # 1. Use a modern, capable multimodal model like gpt-4o
        config_list = [
            {
                'model': 'gpt-4o',
                'api_key': os.environ.get('OPENAI_API_KEY'),
            }
        ]

        # 2. Define a more detailed prompt for structured JSON output.
        # Field names are lowercase to align with downstream processing in other agents.
        self.extraction_instructions = """
                                        You are an intelligent expense document parser. Given an image of a receipt or invoice, extract the following structured fields:
                                        - amount: The total amount of the transaction as a number.
                                        - date: The date of the transaction in YYYY-MM-DD format.
                                        - vendor_name: The name of the vendor or merchant.
                                        - currency: The 3-letter currency code (e.g., USD, EUR).
                                        - event_id: The event or project ID if mentioned, otherwise null.
                                        - participant: The name of the person who incurred the expense, if mentioned, otherwise null.

                                        Return the information as a single JSON object. Do not include any other text, comments, or markdown.
                                        Example of a valid response:
                                        {
                                            "amount": 125.50,
                                            "date": "2023-10-26",
                                            "vendor_name": "The Grand Hotel",
                                            "currency": "USD",
                                            "event_id": "EVT-12345",
                                            "participant": "John Doe"
                                        }
                                        If a field is not found, its value must be null.
                                    """

        # 3. Create an internal AssistantAgent to perform the parsing.
        # Enforcing JSON output is a key improvement for reliability.
        self.parser_agent = AssistantAgent(
            name="InternalParser",
            system_message=self.extraction_instructions,
            llm_config={
                "seed": 42,
                "config_list": config_list,
                "temperature": 0,
                "request_timeout": 240,
                "response_format": {"type": "json_object"},
            },
        )

    def _encode_image(self, image_path: str) -> str:
        """Encodes an image file to a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _parse_document(self, image_path: str) -> Dict:
        """Sends an image to the agent and returns the parsed JSON data."""
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at {image_path}")
            return {"error": "File not found", "file": image_path}

        base64_image = self._encode_image(image_path)
        
        # Construct a message for the agent. The 'image_url' format is standard.
        user_proxy_message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Parse the attached expense document: {os.path.basename(image_path)}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        response = self.parser_agent.generate_reply(messages=user_proxy_message)
        
        try:
            # The LLM is configured for JSON output, so we parse the response string.
            parsed_content = json.loads(response)
            parsed_content['source_file'] = os.path.basename(image_path)
            return parsed_content
        except (json.JSONDecodeError, TypeError):
            print(f"Error: Failed to parse JSON from LLM response for {image_path}. Response: {response}")
            return {"error": "Invalid JSON response", "file": image_path, "raw_response": response}

    def run(self, documents_path: str = 'data/documents') -> List[Dict]:
        """
        Scans a directory for expense documents, parses them, and returns a list of structured expenses.
        This method provides the interface expected by the OrchestratorAgent.
        """
        if not os.path.isdir(documents_path):
            print(f"Error: Documents directory not found at '{documents_path}'")
            return []

        parsed_expenses = []
        supported_extensions = ('.png', '.jpg', '.jpeg', '.webp')
        print(f"Scanning for documents in '{documents_path}'...")

        for filename in os.listdir(documents_path):
            if filename.lower().endswith(supported_extensions):
                image_path = os.path.join(documents_path, filename)
                print(f"Parsing document: {filename}...")
                extracted_data = self._parse_document(image_path)
                if "error" not in extracted_data:
                    parsed_expenses.append(extracted_data)
        
        print(f"Successfully parsed {len(parsed_expenses)} documents.")
        return parsed_expenses

