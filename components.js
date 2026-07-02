// Theme is now handled entirely by native CSS @media (prefers-color-scheme)


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
        // Find all h2 and h3 elements within .toc-content
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
            a.classList.add('toc-link');

            // Indent based on header level
            if (header.tagName === 'H3') {
                li.style.marginLeft = '1rem';
                a.textContent = '— ' + text;
            } else if (header.tagName === 'H4') {
                li.style.marginLeft = '2rem';
                a.style.fontSize = '0.9em';
                a.textContent = '— ' + text;
            }
            
            li.appendChild(a);
            tocList.appendChild(li);
        });

        // Scrollspy logic
        const tocLinks = tocList.querySelectorAll('.toc-link');
        const scrollSpy = () => {
            let currentId = '';
            // Find the last header that is at or above the top of the viewport
            headers.forEach(header => {
                const rect = header.getBoundingClientRect();
                if (rect.top <= 100) { 
                    currentId = header.id;
                }
            });

            // If we are at the very top, highlight the first section
            if (!currentId && headers.length > 0) {
                currentId = headers[0].id;
            }

            tocLinks.forEach(link => {
                if (link.getAttribute('href') === '#' + currentId) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        };

        window.addEventListener('scroll', scrollSpy);
        scrollSpy(); // Initial call
    }
});