from django_components import Component, register

@register("button")
class Buttons(Component):
    template_file = "button/template.html"

    def get_context_data(self, tag="a", label="Click Me", href="#", type="primary"):
        return {
            'tag': tag,
            'label': label,
            'href': href,
            'type': type,
        }