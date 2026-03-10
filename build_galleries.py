import glob
import os
import re

def generate_gallery_html(image_dir):
    images = []
    for ext in ('*.jpg', '*.jpeg', '*.png'):
        images.extend(glob.glob(os.path.join(image_dir, ext)))
    
    images.sort()

    html_content = "\n"
    for img in images:
        rel_path = img.split('images/')[-1]
        full_rel_path = f"images/{rel_path}"
        
        caption = os.path.basename(img).rsplit('.', 1)[0]
        
        html_content += f'''        <div class="responsive">
          <div class="gallery">
            <a target="_blank" href="{full_rel_path}">
              <img src="{full_rel_path}" alt="{caption}" width="600" height="400">
            </a>
            <div class="desc">{caption}</div>
          </div>
        </div>\n'''
    return html_content

def update_html_file(file_path, marker_name, new_content):
    with open(file_path, 'r') as f:
        content = f.read()

    pattern = r'(<!-- ' + marker_name + r'_START -->\n).*?(<!-- ' + marker_name + r'_END -->)'
    replacement = r'\1' + new_content + r'      \2'
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(file_path, 'w') as f:
        f.write(updated_content)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    drawings_dir = os.path.join(base_dir, 'images', 'Drawings')
    drawings_html = generate_gallery_html(drawings_dir)
    update_html_file('Fun.html', 'DRAWINGS', drawings_html)
    print("Updated Drawings gallery in Fun.html")

    photos_dir = os.path.join(base_dir, 'images', 'Photographs')
    photos_html = generate_gallery_html(photos_dir)
    update_html_file('Fun.html', 'PHOTOS', photos_html)
    print("Updated Photos gallery in Fun.html")
