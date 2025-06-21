from django_components import component

@component.register("header")
class Header(component.Component):
    template_name = "layout/header.html"

    def get_context_data(self):
        return {}

@component.register("minimal_header")
class MinimalHeader(component.Component):
    template_name = "layout/minimal-header.html"

    def get_context_data(self):
        return {}
    
@component.register("footer")
class Footer(component.Component):
    template_name = "layout/footer.html"

    def get_context_data(self):
        return {}

@component.register("minimal_footer")
class MinimalFooter(component.Component):
    template_name = "layout/minimal-footer.html"

    def get_context_data(self):
        return {}
    
@component.register("stats_partner")
class StatsAndPartners(component.Component):
    template_file = "layout/stats-partner.html"

    def get_context_data(self):
        return {}