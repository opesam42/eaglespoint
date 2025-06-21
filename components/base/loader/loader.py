from django_components import Component, register

@register("loading_modal")
class LoadingModal(Component):
    template_file = "base/loader/loading-modal.html"

    def get_context_data(self):
        return {}