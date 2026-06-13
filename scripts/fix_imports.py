import glob
import os

def fix_imports():
    backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
    print(f"Scanning for relative imports in: {backend_path}")
    
    for filepath in glob.glob(os.path.join(backend_path, '**/*.py'), recursive=True):
        # Skip virtual environments
        if ".venv" in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = content
        # Replace relative imports with absolute imports
        modified = modified.replace('from ...core.', 'from core.')
        modified = modified.replace('from ..core.', 'from core.')
        modified = modified.replace('from ..integrations.', 'from integrations.')
        modified = modified.replace('from .agent ', 'from core.agent ')
        modified = modified.replace('from .state_store ', 'from core.state_store ')
        
        if modified != content:
            print(f"[FIXED] Fixed imports in: {os.path.relpath(filepath, backend_path)}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified)

if __name__ == "__main__":
    fix_imports()
