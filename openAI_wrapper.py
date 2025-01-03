from openai import OpenAI
import os
import base64

class OpenAISummariser:
    def __init__(self, messages, model="gpt-4o"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not self.client.api_key:
            raise ValueError("OpenAI API key is not set. Please set the 'OPENAI_API_KEY' environment variable.")
        self.model = model
        self.messages = messages

    def summarise(self):
        # For text-only queries, use the standard format
        prompt = "Summarise the following conversation. Make sure not to miss out any important details. Action items should also be mentioned at the end, point wise. If it is clear from the conversation who is responsible for these action items, mention that too."
        messages = [{"role": "user", "content": prompt}] + self.messages
        model = self.model

        # Call the OpenAI API
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=8192
        )

        assistant_message = response.choices[0].message.content
        # Update conversation history for both vision and text queries

        return assistant_message