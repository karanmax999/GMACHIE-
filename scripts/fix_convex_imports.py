import glob
import os

def fix_convex():
    convex_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../convex"))
    print(f"Scanning for convex/validation in: {convex_path}")
    
    for filepath in glob.glob(os.path.join(convex_path, '**/*.ts'), recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = content.replace('"convex/validation"', '"convex/values"')
        modified = modified.replace("'convex/validation'", "'convex/values'")
        
        if modified != content:
            print(f"[FIXED] {os.path.relpath(filepath, convex_path)}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified)

if __name__ == "__main__":
    fix_convex()
