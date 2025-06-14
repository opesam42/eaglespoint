from django_components import component

@component.register("header")
class Header(component.Component):
    template_name = "headerFooter/header.html"

    def get_context_data(self):
        return {}

@component.register("minimal_header")
class MinimalHeader(component.Component):
    template_name = "headerFooter/minimal-header.html"

    def get_context_data(self):
        return {}
    
@component.register("footer")
class Footer(component.Component):
    template_name = "headerFooter/footer.html"

    def get_context_data(self):
        return {}

@component.register("minimal_footer")
class MinimalFooter(component.Component):
    template_name = "headerFooter/minimal-footer.html"

    def get_context_data(self):
        return {}