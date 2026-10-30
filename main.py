import sys
import os
from config import config
from ai_manager import GeminiAIManager
from github_manager import GitHubManager
from file_manager import FileManager
import argparse

class GeminiCodingManager:
    def __init__(self):
        self.ai_manager = None
        self.github_manager = None
        self.file_manager = None
        self.setup_components()
    
    def setup_components(self):
        if config.GEMINI_API_KEY:
            self.ai_manager = GeminiAIManager(config.GEMINI_API_KEY)
        
        if config.GITHUB_TOKEN:
            self.github_manager = GitHubManager(config.GITHUB_TOKEN)
            self.github_manager.authenticate()
        
        self.file_manager = FileManager()
    
    def generate_code(self, prompt: str, language: str, filename: str = None):
        if not self.ai_manager:
            print("AI manager not initialized. Please set GEMINI_API_KEY.")
            return
        
        code = self.ai_manager.generate_code(prompt, language)
        
        if filename:
            self.file_manager.create_file(filename, code, language)
            print(f"Code generated and saved to {filename}")
        else:
            print("Generated Code:")
            print("=" * 50)
            print(code)
    
    def edit_code(self, filename: str, instructions: str):
        if not self.ai_manager:
            print("AI manager not initialized. Please set GEMINI_API_KEY.")
            return
        
        original_code = self.file_manager.read_file(filename)
        if not original_code:
            print(f"File {filename} not found.")
            return
        
        language = filename.split('.')[-1] if '.' in filename else 'txt'
        edited_code = self.ai_manager.edit_code(original_code, instructions, language)
        
        self.file_manager.edit_file(filename, edited_code)
        print(f"Code edited successfully in {filename}")
    
    def sync_with_github(self, repo_name: str = None):
        if not self.github_manager:
            print("GitHub manager not initialized. Please set GITHUB_TOKEN.")
            return
        
        if repo_name:
            if self.github_manager.clone_repository(repo_name, "./workspace"):
                print(f"Repository {repo_name} cloned successfully")
        else:
            result = self.github_manager.sync_with_remote()
            print(result)
    
    def push_to_github(self, message: str = "Updated by Gemini Coding Manager"):
        if not self.github_manager:
            print("GitHub manager not initialized.")
            return
        
        result = self.github_manager.push_changes(message)
        print(result)

def main():
    parser = argparse.ArgumentParser(description='Gemini AI Coding Manager')
    parser.add_argument('--generate', nargs=2, metavar=('PROMPT', 'LANGUAGE'), 
                       help='Generate code with AI')
    parser.add_argument('--edit', nargs=2, metavar=('FILE', 'INSTRUCTIONS'),
                       help='Edit existing code file')
    parser.add_argument('--sync', nargs='?', const='default', metavar='REPO',
                       help='Sync with GitHub repository')
    parser.add_argument('--push', nargs='?', const='Updated by Gemini', metavar='MESSAGE',
                       help='Push changes to GitHub')
    parser.add_argument('--list', action='store_true', help='List project files')
    parser.add_argument('--structure', action='store_true', help='Show project structure')
    
    args = parser.parse_args()
    
    manager = GeminiCodingManager()
    
    if args.generate:
        prompt, language = args.generate
        manager.generate_code(prompt, language)
    elif args.edit:
        filename, instructions = args.edit
        manager.edit_code(filename, instructions)
    elif args.sync:
        repo_name = None if args.sync == 'default' else args.sync
        manager.sync_with_github(repo_name)
    elif args.push:
        manager.push_to_github(args.push)
    elif args.list:
        files = manager.file_manager.list_files()
        for file in files:
            print(f"{file['name']} ({file['size']} bytes)")
    elif args.structure:
        structure = manager.file_manager.get_project_structure()
        for path, info in structure.items():
            print(f"{path} - {info['type']}")
    else:
        print("Gemini AI Coding Manager")
        print("Available commands:")
        print("  --generate 'prompt' language  : Generate code")
        print("  --edit file instructions      : Edit code")
        print("  --sync [repo]                 : Sync with GitHub")
        print("  --push [message]              : Push to GitHub")
        print("  --list                        : List files")
        print("  --structure                   : Show structure")

if __name__ == "__main__":
    main()
