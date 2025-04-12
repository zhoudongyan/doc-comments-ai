import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class LLM:
    def __init__(self, model: str = None):
        # Get model from parameter or environment variable, default to gpt-3.5-turbo
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        # Set max tokens based on model
        self.max_tokens = 2048 if "gpt-3.5-turbo" == self.model else 4096
        
        # Initialize OpenAI client
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        # Define system prompt
        self.system_prompt = (
            "You are an AI assistant that generates detailed documentation comments for code. "
            "You analyze the code and create clear, informative documentation that explains what the code does."
        )

    def _llm_completion(self, user_prompt: str, max_retries: int = 3) -> str:
        """
        Send a request to the OpenAI API and get the completion response.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.8,
                    max_tokens=self.max_tokens,
                )
                content = response.choices[0].message.content
                
                logger.debug(f"========== LLM RESPONSE START ==========\n{content}")
                logger.debug(f"========== LLM RESPONSE END ==========")
                
                return content
            except Exception as e:
                logger.warning(f"LLM API call failed on attempt {attempt + 1}/{max_retries}: {str(e)}")
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to get LLM response after {max_retries} attempts: {str(e)}")
                continue

    def generate_doc_comment(self, language, code, inline=False):
        """
        Generates a doc comment for the given method
        """
        # Prepare the prompt
        inline_comments = "Add inline comments to the method body where it makes sense." if inline else ""
        haskell_missing_signature = "and missing type signatures " if language == "haskell" else ""
        
        user_prompt = (
            f"Add a detailed doc comment to the following {language} method:\n{code}\n"
            f"The doc comment should describe what the method does. "
            f"{inline_comments} "
            f"Return the method implementaion with the doc comment as a single markdown code block. "
            f"Don't include any explanations {haskell_missing_signature}in your response."
        )

        # Get completion from OpenAI
        return self._llm_completion(user_prompt)
