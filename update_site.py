import glob, re

# 1. Update the year to automatically use the current year
html_files = glob.glob('**/*.html', recursive=True)
for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()
    # Replace the hardcoded year with a JS snippet if it hasn't been replaced yet
    if '<script>document.write(new Date().getFullYear())</script>' not in content:
        content = re.sub(r'2022 Mathew Alex', r'&copy; <script>document.write(new Date().getFullYear())</script> Mathew Alex', content)
        with open(filepath, 'w') as f:
            f.write(content)

print("Updated copyright years.")
