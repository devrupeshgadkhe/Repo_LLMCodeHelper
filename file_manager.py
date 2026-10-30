import os
from pathlib import Path
from typing import List, Dict, Optional
import shutil

class FileManager:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
    
    def create_file(self, filename: str, content: str, language: str = "txt") -> bool:
        try:
            file_path = self.base_path / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    
    def read_file(self, filename: str) -> Optional[str]:
        try:
            file_path = self.base_path / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def edit_file(self, filename: str, new_content: str) -> bool:
        try:
            file_path = self.base_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"Error editing file: {e}")
            return False
    
    def delete_file(self, filename: str) -> bool:
        try:
            file_path = self.base_path / filename
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def list_files(self, extension: str = None) -> List[Dict]:
        files = []
        try:
            for file_path in self.base_path.rglob("*"):
                if file_path.is_file():
                    if extension is None or file_path.suffix == f".{extension}":
                        files.append({
                            'name': file_path.name,
                            'path': str(file_path.relative_to(self.base_path)),
                            'size': file_path.stat().st_size,
                            'modified': file_path.stat().st_mtime
                        })
        except Exception as e:
            print(f"Error listing files: {e}")
        
        return files
    
    def get_project_structure(self) -> Dict:
        structure = {}
        try:
            for item in self.base_path.rglob("*"):
                if item.is_file():
                    rel_path = str(item.relative_to(self.base_path))
                    structure[rel_path] = {
                        'type': 'file',
                        'size': item.stat().st_size
                    }
                elif item.is_dir():
                    rel_path = str(item.relative_to(self.base_path))
                    structure[rel_path] = {
                        'type': 'directory',
                        'files': len(list(item.glob("*")))
                    }
        except Exception as e:
            print(f"Error getting project structure: {e}")
        
        return structure
