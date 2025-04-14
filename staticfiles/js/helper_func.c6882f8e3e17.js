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


DOMAIN_URL = 'http://127.0.0.1:8000'