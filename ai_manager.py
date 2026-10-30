import google.generativeai as genai
from typing import List, Dict, Optional
import json

class GeminiAIManager:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
    
    def generate_code(self, prompt: str, language: str) -> str:
        full_prompt = f"Generate {language} code for: {prompt}\n\nProvide only the code without explanations."
        response = self.chat.send_message(full_prompt)
        return response.text
    
    def edit_code(self, code: str, instructions: str, language: str) -> str:
        prompt = f"Edit this {language} code according to instructions: {instructions}\n\nOriginal code:\n{code}\n\nReturn only the edited code."
        response = self.chat.send_message(prompt)
        return response.text
    
    def explain_code(self, code: str, language: str) -> str:
        prompt = f"Explain this {language} code:\n\n{code}\n\nProvide a clear explanation."
        response = self.chat.send_message(prompt)
        return response.text
    
    def debug_code(self, code: str, error: str, language: str) -> str:
        prompt = f"Debug this {language} code that has the following error: {error}\n\nCode:\n{code}\n\nProvide the fixed code and explanation."
        response = self.chat.send_message(prompt)
        return response.text
    
    def optimize_code(self, code: str, language: str) -> str:
        prompt = f"Optimize this {language} code for performance and best practices:\n\n{code}\n\nReturn only the optimized code."
        response = self.chat.send_message(prompt)
        return response.text
    
    def generate_documentation(self, code: str, language: str) -> str:
        prompt = f"Generate documentation for this {language} code:\n\n{code}\n\nInclude function descriptions, parameters, and return values."
        response = self.chat.send_message(prompt)
        return response.text
