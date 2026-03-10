import os
import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Fix footer
    # Replace `<center>\n 2022 Mathew Alex\n <center>` (and variants)
    content = re.sub(r'<center>\s*(Copyright &copy; )?2022 Mathew Alex\s*<center>', r'<footer style="text-align: center; margin-top: 20px;">\n  \12022 Mathew Alex\n</footer>', content)
    content = re.sub(r'<center>\s*(Copyright &copy; )?2022 Mathew Alex\s*</center>', r'<footer style="text-align: center; margin-top: 20px;">\n  \12022 Mathew Alex\n</footer>', content)

    # 2. Fix remaining <center> tags
    content = re.sub(r'<center>', r'<div style="text-align: center;">', content)
    content = re.sub(r'</center>', r'</div>', content)

    # 3. Standardize <br>
    content = re.sub(r'</br>', r'<br>', content)
    
    # 4. Update asset paths for files in Notes/* subdirectories
    if filepath.startswith('Notes/') and '/' in filepath[6:]:
        # It's inside a specific note directory, e.g., Notes/Machine Learning/index.html
        depth = filepath.count('/')
        prefix = '../' * depth
        
        # update styles.css link
        content = re.sub(r'href="styles.css"', f'href="{prefix}styles.css"', content)
        # update favicon link
        content = re.sub(r'href="favicon.ico"', f'href="{prefix}favicon.ico"', content)

    with open(filepath, 'w') as f:
        f.write(content)

print("Refactored HTML files.")
