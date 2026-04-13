import glob
import os
import re
from PIL import Image, ImageOps

def generate_gallery_html(image_dir, show_caption=True):
    images = []
    for ext in ('*.jpg', '*.jpeg', '*.png'):
        images.extend(glob.glob(os.path.join(image_dir, ext)))
    
    # Filter out thumbnails from the image list
    original_images = [img for img in images if not img.endswith('_thumb.jpg') and not img.endswith('_thumb.jpeg') and not img.endswith('_thumb.png')]
    original_images.sort()

    html_content = "\n"
    for img_path in original_images:
        rel_path = img_path.split('images/')[-1]
        full_rel_path = f"images/{rel_path}"
        
        # Set up thumbnail path
        filename, ext = os.path.splitext(img_path)
        thumb_path = f"{filename}_thumb{ext}"
        thumb_rel_path = f"images/{thumb_path.split('images/')[-1]}"

        # Generate thumbnail if it doesn't exist
        if not os.path.exists(thumb_path):
            print(f"Generating thumbnail for {os.path.basename(img_path)}...")
            try:
                with Image.open(img_path) as img:
                    # Fix rotation based on EXIF orientation metadata
                    img = ImageOps.exif_transpose(img)
                    
                    # Convert RGBA to RGB for JPEG compatibility (just in case)
                    if img.mode in ("RGBA", "P") and ext.lower() in ('.jpg', '.jpeg'):
                        img = img.convert("RGB")
                    
                    max_width = 800
                    if img.width > max_width:
                        w_percent = (max_width / float(img.width))
                        h_size = int((float(img.height) * float(w_percent)))
                        img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
                    img.save(thumb_path, optimize=True)
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
                thumb_rel_path = full_rel_path  # Fallback to original image if creation fails
        
        caption = os.path.basename(img_path).rsplit('.', 1)[0].replace('_', ' ')

        desc_html = f'\n            <div class="desc">{caption}</div>' if show_caption else ''
        
        html_content += f'''          <div class="gallery">
            <a target="_blank" href="{full_rel_path}">
              <img src="{thumb_rel_path}" alt="{caption}">
            </a>{desc_html}
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
    drawings_html = generate_gallery_html(drawings_dir, show_caption=True)
    update_html_file('Fun.html', 'DRAWINGS', drawings_html)
    print("Updated Drawings gallery in Fun.html")

    photos_dir = os.path.join(base_dir, 'images', 'Photographs')
    photos_html = generate_gallery_html(photos_dir, show_caption=False)
    update_html_file('Fun.html', 'PHOTOS', photos_html)
    print("Updated Photos gallery in Fun.html")
