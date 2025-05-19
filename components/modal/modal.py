from django_components import Component, register

@register("modal")
class Modal(Component):
    template_file = "modal/template.html"

    def get_context_data(self, modal_type, modal_title, classes=""):
        return {
            'modal_type': modal_type,
            'modal_title': modal_title,
            'classes': classes,
        }