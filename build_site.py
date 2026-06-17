import os
import glob
import re
import subprocess

def parse_markdown(filepath):
    """
    Parses a markdown file with YAML frontmatter.
    Currently simply splits the frontmatter from the HTML/Markdown content.
    If you install the 'markdown' package later, you can pass `content` through it here.
    """
    with open(filepath, 'r') as f:
        text = f.read()

    # Match frontmatter between --- and ---
    match = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    
    metadata = {}
    content = text
    
    if match:
        frontmatter = match.group(1)
        content = match.group(2)
        
        # Parse simple frontmatter (key: value)
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip()
                
    return metadata, content

def md_to_html(text):
    """
    A minimal, dependency-free Markdown to HTML converter.
    """
    if not text.strip():
        return ""
        
    # Inline rules
    def image_replacer(match):
        alt = match.group(1)
        url = match.group(2)
        classes = ""
        if '#' in url:
            url, cls = url.split('#', 1)
            classes = f' class="{cls}"'
        return f'<img src="{url}" alt="{alt}"{classes}>'

    def youtube_replacer(match):
        video_id = match.group(1)
        classes = ""
        if '#' in video_id:
            video_id, cls = video_id.split('#', 1)
            classes = f' class="{cls}"'
        return f'<iframe width="100%" {classes} src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'

    def soundcloud_replacer(match):
        track_url = match.group(1)
        return f'<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url={track_url}&color=%23959e96&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true" style="border: 1px solid var(--border-color); border-radius: 8px; aspect-ratio: auto; height: 166px;"></iframe>'

    def gallery_replacer(match):
        name = match.group(1)
        return f'<div id="{name.lower()}-gallery">\n<!-- {name.upper()}_START -->\n<!-- {name.upper()}_END -->\n</div>'

    def github_replacer(match):
        url = match.group(1)
        return f'<button onclick="location.href=\'{url}\'" type="button" style="float: right; font-size: 0.7em; margin-top: 0.2em;">Github</button>'

    text = text.replace('@[toc]', '<!-- TOC_MARKER -->')
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'\!\[(.*?)\]\((.*?)\)', image_replacer, text)
    text = re.sub(r'\@\[youtube\]\((.*?)\)', youtube_replacer, text)
    text = re.sub(r'\@\[soundcloud\]\((.*?)\)', soundcloud_replacer, text)
    text = re.sub(r'\@\[gallery\]\((.*?)\)', gallery_replacer, text)
    text = re.sub(r'\@\[github\]\((.*?)\)', github_replacer, text)
    text = re.sub(r'(?<!\!)\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    
    # Ensure containers are split into their own blocks
    text = re.sub(r'(?m)^(:::.*)$', r'\n\n\1\n\n', text)
    # Clean up excess newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    html_blocks = []
    # Split by double newlines to isolate blocks (paragraphs, headers, HTML divs)
    blocks = text.split('\n\n')
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # Headers (matches 1 to 6 hashes)
        header_match = re.match(r'^(#{1,6})\s+(.*)', block, re.DOTALL)
        if header_match:
            level = len(header_match.group(1))
            content = header_match.group(2).strip()
            html_blocks.append(f"<h{level}>{content}</h{level}>")
        # Horizontal rules
        elif block == '***' or block == '---':
            html_blocks.append('<hr>')
        # Containers
        elif block.startswith('::: '):
            classes = block[4:].strip()
            html_blocks.append(f'<div class="{classes}">')
        elif block == ':::':
            html_blocks.append('</div>')
        # If it already looks like HTML (starts with <), leave it alone
        elif block.startswith('<'):
            html_blocks.append(block)
        # Standard paragraph
        else:
            block = block.replace('\n', '<br>')
            html_blocks.append(f"<p>{block}</p>")
            
    final_html = '\n\n'.join(html_blocks)
    if '<!-- TOC_MARKER -->' in final_html:
        toc_snippet = '''<div class="toc-container">
<nav class="toc">
<b>Contents</b>
<ul id="toc-list"></ul>
</nav>
<div class="toc-content">'''
        final_html = final_html.replace('<!-- TOC_MARKER -->', toc_snippet)
        final_html += '\n</div>\n</div>'
        
    return final_html

def build_site():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    content_dir = os.path.join(base_dir, 'content')
    template_path = os.path.join(base_dir, 'template.html')

    with open(template_path, 'r') as f:
        template = f.read()

    # First pass: Collect all pages for the dynamic navbar
    pages = []
    for md_file in glob.glob(os.path.join(content_dir, '*.md')):
        metadata, _ = parse_markdown(md_file)
        title = metadata.get('title', 'Untitled')
        # Use 'About' instead of 'About me' for the navbar for brevity if desired, 
        # but let's stick to the title. We'll rename it later if needed.
        if title == "About me":
            title = "About"
        output_filename = metadata.get('output', os.path.basename(md_file).replace('.md', '.html'))
        pages.append({'title': title, 'output': output_filename})

    # Sort pages: index.html first, Research second, Fun third, others last.
    order = {'index.html': 0, 'Research.html': 1, 'Fun.html': 2}
    pages.sort(key=lambda x: order.get(x['output'], 99))

    # Second pass: Process and build each page
    for md_file in glob.glob(os.path.join(content_dir, '*.md')):
        metadata, content = parse_markdown(md_file)
        
        title = metadata.get('title', 'Untitled')
        output_filename = metadata.get('output', os.path.basename(md_file).replace('.md', '.html'))
        
        # Build dynamic navbar
        nav_links = []
        for p in pages:
            is_active = (p['output'] == output_filename)
            if is_active:
                style = "text-decoration: underline; text-underline-offset: 6px; color: inherit; opacity: 1; font-weight: bold;"
                hover_out = ""
            else:
                style = "text-decoration: none; color: inherit; opacity: 0.6; transition: opacity 0.2s;"
                hover_out = "this.style.opacity=0.6"
            nav_links.append(f'<a href="{p["output"]}" style="{style}" onmouseover="this.style.opacity=1" onmouseout="{hover_out}">{p["title"]}</a>')
            
        nav_links_str = "\n          ".join(nav_links)
        navbar_html = f'''<header>
        <a href="index.html" style="text-decoration: none; color: inherit; display: block; margin-bottom: 2rem;">
          <h1 style="margin: 0; font-family: ui-serif, Georgia, serif; font-size: 1.5rem;">Mathew Alex</h1>
        </a>
        <nav style="display: flex; flex-direction: column; gap: 1rem; font-size: 0.875rem;">
          {nav_links_str}
        </nav>
      </header>'''
        
        # Convert Markdown to HTML
        html_content = md_to_html(content)
        
        # Inject into template
        final_html = template.replace('{{ TITLE }}', title)
        final_html = final_html.replace('<site-header></site-header>', navbar_html)
        final_html = final_html.replace('{{ CONTENT }}', html_content)
        
        # Save output
        output_path = os.path.join(base_dir, output_filename)
        with open(output_path, 'w') as f:
            f.write(final_html)
            
        print(f"Built {output_filename} from {os.path.basename(md_file)}")

    # Process Posts
    posts_dir = os.path.join(content_dir, 'posts')
    if os.path.exists(posts_dir) and not os.path.exists(os.path.join(posts_dir, 'DONT_COMPILE')):
        out_posts_dir = os.path.join(base_dir, 'posts')
        os.makedirs(out_posts_dir, exist_ok=True)
        
        posts_list = []
        for md_file in glob.glob(os.path.join(posts_dir, '*.md')):
            metadata, content = parse_markdown(md_file)
            title = metadata.get('title', 'Untitled Post')
            date = metadata.get('date', 'Unknown Date')
            output_filename = os.path.basename(md_file).replace('.md', '.html')
            
            # Save post info for index
            posts_list.append({
                'title': title,
                'date': date,
                'url': f'posts/{output_filename}',
            })
            
            html_content = md_to_html(content)
            
            # Inject Utterances Comments (Uses GitHub Issues)
            # If you want to use Discussions instead of Issues, replace this block with the script from giscus.app
            comments_html = """
            <div style="margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border-color);">
                <script src="https://giscus.app/client.js"
                data-repo="letallbewell/letallbewell.github.io"
                data-repo-id="R_kgDOH3Il6A"
                data-category="Announcements"
                data-category-id="DIC_kwDOH3Il6M4C_SXC"
                data-mapping="pathname"
                data-strict="0"
                data-reactions-enabled="1"
                data-emit-metadata="0"
                data-input-position="top"
                data-theme="preferred_color_scheme"
                data-lang="en"
                data-loading="lazy"
                crossorigin="anonymous"
                async>
                </script>
            </div>
            """
            html_content += comments_html
            
            final_html = template.replace('{{ TITLE }}', title)
            # Fix relative links for subfolder locally
            final_html = final_html.replace('href="styles.css"', 'href="../styles.css"')
            final_html = final_html.replace('href="favicon.ico"', 'href="../favicon.ico"')
            final_html = final_html.replace('src="components.js"', 'src="../components.js"')
            final_html = final_html.replace('{{ CONTENT }}', html_content)
            
            output_path = os.path.join(out_posts_dir, output_filename)
            with open(output_path, 'w') as f:
                f.write(final_html)
            print(f"Built post {output_filename}")
            
        # Generate Posts Index Page
        posts_list.sort(key=lambda x: x['date'], reverse=True)
        
        index_content = '<ul>\n'
        for post in posts_list:
            index_content += f'  <li style="margin-bottom: 1em; font-size: 1.1rem;"><a href="{post["url"]}" style="text-decoration: none;"><b>{post["title"]}</b></a> <span style="opacity: 0.6; font-size: 0.9em; margin-left: 0.5rem;">{post["date"]}</span></li>\n'
        index_content += '</ul>\n'
        
        final_index = template.replace('{{ TITLE }}', 'Posts')
        final_index = final_index.replace('{{ CONTENT }}', index_content)
        
        with open(os.path.join(base_dir, 'Posts.html'), 'w') as f:
            f.write(final_index)
        print("Built Posts.html index page")

if __name__ == '__main__':
    print("Building site...")
    build_site()
    
    # Run the gallery builder after generating the HTML files
    print("\nRunning gallery generator...")
    try:
        subprocess.run(["python3", "build_galleries.py"], check=True)
    except Exception as e:
        print(f"Could not build galleries: {e}")
    
    print("\nDone! Site built successfully.")
