from github import Github
from typing import List, Dict, Optional
import os
import shutil
from pathlib import Path

class GitHubManager:
    def __init__(self, token: str = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.github = Github(self.token) if self.token else None
        self.current_repo = None
        self.local_path = None
    
    def authenticate(self) -> bool:
        try:
            if self.token:
                self.github = Github(self.token)
                user = self.github.get_user()
                print(f"Authenticated as: {user.login}")
                return True
            return False
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def get_repositories(self) -> List[Dict]:
        if not self.github:
            return []
        
        repos = []
        try:
            for repo in self.github.get_user().get_repos():
                repos.append({
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'clone_url': repo.clone_url,
                    'description': repo.description,
                    'default_branch': repo.default_branch
                })
        except Exception as e:
            print(f"Error fetching repositories: {e}")
        
        return repos
    
    def clone_repository(self, repo_full_name: str, local_path: str) -> bool:
        try:
            repo = self.github.get_repo(repo_full_name)
            repo.clone_url = repo.clone_url.replace('https://', f'https://{self.token}@')
            
            os.makedirs(local_path, exist_ok=True)
            os.system(f"git clone {repo.clone_url} {local_path}")
            
            self.current_repo = repo
            self.local_path = local_path
            return True
        except Exception as e:
            print(f"Error cloning repository: {e}")
            return False
    
    def pull_changes(self) -> str:
        if not self.local_path:
            return "No local repository path set"
        
        try:
            os.chdir(self.local_path)
            result = os.system("git pull")
            return "Pull successful" if result == 0 else "Pull failed"
        except Exception as e:
            return f"Error pulling changes: {e}"
    
    def push_changes(self, commit_message: str = "Updated by Gemini Coding Manager") -> str:
        if not self.local_path:
            return "No local repository path set"
        
        try:
            os.chdir(self.local_path)
            os.system("git add .")
            os.system(f'git commit -m "{commit_message}"')
            result = os.system("git push")
            return "Push successful" if result == 0 else "Push failed"
        except Exception as e:
            return f"Error pushing changes: {e}"
    
    def fetch_branches(self) -> List[str]:
        if not self.local_path:
            return []
        
        try:
            os.chdir(self.local_path)
            os.system("git fetch --all")
            result = os.popen("git branch -r").read()
            branches = [branch.strip() for branch in result.split('\n') if branch.strip()]
            return branches
        except Exception as e:
            print(f"Error fetching branches: {e}")
            return []
    
    def create_branch(self, branch_name: str) -> str:
        if not self.local_path:
            return "No local repository path set"
        
        try:
            os.chdir(self.local_path)
            result = os.system(f"git checkout -b {branch_name}")
            return "Branch created" if result == 0 else "Failed to create branch"
        except Exception as e:
            return f"Error creating branch: {e}"
    
    def sync_with_remote(self) -> str:
        if not self.local_path:
            return "No local repository path set"
        
        try:
            os.chdir(self.local_path)
            os.system("git fetch --all")
            os.system("git pull")
            return "Sync completed successfully"
        except Exception as e:
            return f"Error syncing: {e}"
