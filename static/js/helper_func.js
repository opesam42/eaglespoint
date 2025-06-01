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
