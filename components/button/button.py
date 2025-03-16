from django_components import Component, register

@register("button")
class Buttons(Component):
    template_file = "button/template.html"

    def get_context_data(self, html_tag="a", label="Click Me", href="#", type="primary", extraclass=None):
        return {
            'tag': html_tag,
            'label': label,
            'href': href,
            'type': type,
            'extraclass': extraclass
        }