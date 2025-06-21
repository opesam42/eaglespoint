function slugify(text) {
    /**
     * Converts a given text into a URL-friendly slug (kebab-case).
     * - Converts all characters to lowercase.
     * - Replaces spaces with hyphens (`-`).
     * eg Cross-River to cross-river
    **/
    return text.toLowerCase().replace(/\s+/g, '-');
}

function unslugify(slug) {
    /**
     * Converts a slug (kebab-case) back to a readable text.
     * - Replaces hyphens (`-`) with spaces.
     * - Capitalizes the first letter of each word.
     * eg: "cross-river" → "Cross River"
    **/
    return slug
        .split('-') // Split by hyphens
        .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize each word
        .join(' '); // Join words with spaces
}

function getFileName(fullUrl){
    const url = new URL(fullUrl);
    const pathParts = url.pathname.split('/');
    const fileName = pathParts[pathParts.length - 1]

    return fileName
}


function loadModalForm(url, modalId, onOpenCallback=null){    
    openLoadingModal()

    fetch(url, {
        method: "GET",
        headers: {
        "X-Requested-With": "XMLHttpRequest",
        }
    })
    .then(response => response.text())
    .then(data => {
        // since the data is a full html stuff, we need to extract the innerHTML of the body
        let parser = new DOMParser();
        let doc = parser.parseFromString(data, 'text/html');
        let html = doc.body.innerHTML;

        let modal = document.getElementById(modalId)
        injectHTMLWithScripts(modal.querySelector('.modal-body'), html);
        
        closeLoadingModal()
        
        if (typeof onOpenCallback === 'function') {
            onOpenCallback()
        }
    })
    .catch(error => console.log("Error:", error))
}


/**
 * Injects HTML into a container and re-executes any scripts inside the HTML.
 * @param {HTMLElement} container - The DOM element to inject HTML into.
 * @param {string} html - The HTML string to inject.
 */
function injectHTMLWithScripts(container, html) {
    container.innerHTML = html;

    const scripts = container.querySelectorAll('script');

    scripts.forEach(oldScript => {
        const newScript = document.createElement('script');

        // Copy all attributes from the original script tag
        Array.from(oldScript.attributes).forEach(attr =>
            newScript.setAttribute(attr.name, attr.value)
        );

        // Copy inline script content
        newScript.text = oldScript.textContent;

        // Replace old script with new one to execute it
        oldScript.parentNode.replaceChild(newScript, oldScript);
    });
}


/**
 * Formats a date string to "Month Day, Year" in WAT timezone
 * @param {string} dateString - ISO date string (e.g., "2025-06-02T00:44:42.149454+01:00")
 * @returns {string} Formatted date (e.g., "June 2, 2025")
 */

function formatDateWAT(dateString) {
    if (!dateString) return '';
    
    try {
        // Create date object and force WAT timezone (UTC+1)
        const date = new Date(dateString);
        const options = {
            timeZone: 'Africa/Lagos', // WAT timezone (same as UTC+1)
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        
        return date.toLocaleDateString('en-US', options);
    } catch (e) {
        console.error('Date formatting error:', e);
        return 'Invalid date';
    }
}

window.formatDateWAT = formatDateWAT //making it global to be use with AlpineJS

/**
 * Returns the difference between the present time and the entered dateString
 * @param {string} dateString - ISO date string (e.g., "2025-06-02T00:44:42.149454+01:00")
 * @returns {string}  strings like "3 days ago", "1 hour ago", "just now"
 */
function timesince(dateString) {
  if (!dateString) return '';

  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);
  
  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60
  };

  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);
    if (interval >= 1) {
      return interval === 1 ? `${interval} ${unit} ago` : `${interval} ${unit}s ago`;
    }
  }

  return 'just now';
}

window.timesince = timesince