// Theme is now handled entirely by native CSS @media (prefers-color-scheme)

class SiteHeader extends HTMLElement {
  connectedCallback() {
    // Detect if we are inside a subfolder (like /posts/) so we can adjust relative links for local testing
    const isSubfolder = window.location.pathname.includes('/posts/');
    const p = isSubfolder ? '../' : '';

    const path = window.location.pathname;
    const isResearch = path.endsWith('Research.html');
    const isPosts = path.includes('Posts') || path.includes('/posts/');
    const isFun = path.endsWith('Fun.html');
    // If it's none of the above, we assume it's the index (About) page
    const isAbout = !isResearch && !isPosts && !isFun;

    const getStyle = (isActive) => isActive 
      ? 'text-decoration: underline; text-underline-offset: 6px; color: inherit; opacity: 1; font-weight: bold;' 
      : 'text-decoration: none; color: inherit; opacity: 0.6; transition: opacity 0.2s;';

    this.innerHTML = `
      <header>
        <a href="${p}index.html" style="text-decoration: none; color: inherit; display: block; margin-bottom: 2rem;">
          <h1 style="margin: 0; font-family: ui-serif, Georgia, serif; font-size: 1.5rem;">Mathew Alex</h1>
        </a>
        <nav style="display: flex; flex-direction: column; gap: 1rem; font-size: 0.875rem;">
          <a href="${p}index.html" style="${getStyle(isAbout)}" onmouseover="this.style.opacity=1" onmouseout="if(!${isAbout}) this.style.opacity=0.6">About</a>
          <a href="${p}Research.html" style="${getStyle(isResearch)}" onmouseover="this.style.opacity=1" onmouseout="if(!${isResearch}) this.style.opacity=0.6">Research</a>
          <a href="${p}Posts.html" style="${getStyle(isPosts)}" onmouseover="this.style.opacity=1" onmouseout="if(!${isPosts}) this.style.opacity=0.6">Posts</a>
          <a href="${p}Fun.html" style="${getStyle(isFun)}" onmouseover="this.style.opacity=1" onmouseout="if(!${isFun}) this.style.opacity=0.6">Interests</a>
        </nav>
      </header>
    `;
  }
}
customElements.define('site-header', SiteHeader);

class SiteFooter extends HTMLElement {
  connectedCallback() {
    const year = new Date().getFullYear();
    this.innerHTML = `
      <footer style="display: flex; justify-content: space-between; padding-top: 1.5rem; margin-top: 3rem; border-top: 1px solid var(--text-color);">
        <p style="margin: 0; font-size: 0.875rem;">&copy; ${year} Mathew Alex</p>
      </footer>
    `;
  }
}
customElements.define('site-footer', SiteFooter);

document.addEventListener('DOMContentLoaded', () => {
    // Generate Table of Contents
    const tocList = document.getElementById('toc-list');
    if (tocList) {
        // Find all h2, h3, and h4 elements within .toc-content
        const headers = document.querySelectorAll('.toc-content h2, .toc-content h3, .toc-content h4');
        
        headers.forEach(header => {
            // Clone the header to extract text without the Github button
            const clone = header.cloneNode(true);
            clone.querySelectorAll('button').forEach(btn => btn.remove());
            
            // Use custom short title if provided, otherwise use the actual text
            const text = header.getAttribute('data-toc-title') || clone.textContent.trim();

            // Auto-generate an ID if one is missing
            if (!header.id) {
                header.id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
            }

            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#' + header.id;
            a.textContent = text;
            a.style.textDecoration = 'none';
            a.style.color = 'inherit';
            a.style.opacity = '0.6';
            a.onmouseover = () => a.style.opacity = '1';
            a.onmouseout = () => a.style.opacity = '0.6';

            // Indent based on header level
            if (header.tagName === 'H3') {
                li.style.marginLeft = '1rem';
            } else if (header.tagName === 'H4') {
                li.style.marginLeft = '2rem';
                a.style.fontSize = '0.9em';
            }
            
            li.appendChild(a);
            tocList.appendChild(li);
        });
    }
});