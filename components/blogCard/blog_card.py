from django_components import Component, register

@register("blog_card")
class BlogCard(Component):
    template_file = "blogCard/template.html"

    def get_context_data(self, title="", tag="", imageUrl="", excerpt=""):
        return {
            'title': title,
            'tag': tag,
            'imageUrl': imageUrl,
            'excerpt': excerpt,
        }