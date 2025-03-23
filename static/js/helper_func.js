function slugify(text) {
    /**
     * Converts a given text into a URL-friendly slug (kebab-case).
     * - Converts all characters to lowercase.
     * - Replaces spaces with hyphens (`-`).
     * eg Cross-River to cross-river
    **/
    return text.toLowerCase().replace(/\s+/g, '-');
}