from django_components import Component, register

@register("blog_card")
class BlogCard(Component):
    template_file = "base/blogCard/template.html"

    def get_context_data(self, title="", tag="", imageUrl="", excerpt="", articleURL="#"):
        return {
            'title': title,
            'tag': tag,
            'imageUrl': imageUrl,
            'articleURL': articleURL,
            'excerpt': excerpt,
        }