import os
import google.generativeai as genai


class GeminiClient:
    """
    Description:
    A client class for interacting with the Gemini API. 
    It handles initialization with the appropriate model and API key, and provides a method for generating content based on prompts.
    """
    def __init__(self) -> None:
        """
        Description:
        Initializes the GeminiClient by setting up the Generative Model and configuring it 
        with the API key obtained from environment variables.
        """
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.api_key = os.getenv("API_KEY")
        genai.configure(api_key=self.api_key)
    
    def generate(self, prompt: str) -> str:
        """
        Description:
        Generates content based on the provided prompt using the Gemini API.

        Parameters:
        prompt (str): The prompt string to be sent to the Gemini API for content generation.

        Returns:
        str: The generated content from the Gemini API.

        Raises:
        Exception: If the API request times out or if an unexpected error occurs during the content generation process.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.candidates[0].content.parts[0].text
        except TimeoutError:
            raise Exception("Gemini API request timed out.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")
 