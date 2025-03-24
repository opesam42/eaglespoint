from django_components import Component, register

@register("stats_partner")
class StatsAndPartners(Component):
    template_file = "misc/stats-partner.html"

    def get_context_data(self):
        return {}