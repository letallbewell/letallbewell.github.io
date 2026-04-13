// Check local storage immediately to prevent flash of unstyled content
const storedTheme = localStorage.getItem('theme');
if (storedTheme) {
    document.documentElement.setAttribute('data-theme', storedTheme);
}

window.toggleTheme = function() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    let newTheme = 'dark';
    
    if (currentTheme === 'dark') {
        newTheme = 'light';
    } else if (currentTheme === 'light') {
        newTheme = 'dark';
    } else {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            newTheme = 'light';
        }
    }
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
};

class SiteHeader extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <a href="#" onclick="toggleTheme(); return false;" style="float: right; text-decoration: none; opacity: 0.8; margin-top: 0.5em;" title="Toggle dark/light mode">🌗</a>
      <h1>Mathew Alex</h1>
      <a href="index.html">About me</a> &nbsp;
      <a href="Research.html">Research</a> &nbsp;
      <a href="Fun.html">Interests</a>
      <hr style="width:100%;">
    `;
  }
}
customElements.define('site-header', SiteHeader);

class SiteFooter extends HTMLElement {
  connectedCallback() {
    const year = new Date().getFullYear();
    this.innerHTML = `
      <hr style="width:100%;">
      <footer style="text-align: center; margin-top: 20px;">
        &copy; ${year} Mathew Alex
      </footer>
    `;
  }
}
customElements.define('site-footer', SiteFooter);

document.addEventListener('DOMContentLoaded', () => {
    const tocList = document.getElementById('toc-list');
    if (!tocList) return; // Exit quietly if the page doesn't have an index
    
    const headers = document.querySelectorAll('.toc-content h2, .toc-content h3');
    
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

        // Add visual hierarchy based on heading level
        if (header.tagName.toLowerCase() === 'h2') {
            li.style.marginTop = '1.2em';
            a.style.fontWeight = 'bold';
            a.style.textDecoration = 'none';
        } else if (header.tagName.toLowerCase() === 'h3') {
            li.style.marginLeft = '1em';
        }
        
        li.appendChild(a);
        tocList.appendChild(li);
    });
});