from django_components import Component, register

@register("stats_partner")
class StatsAndPartners(Component):
    template_file = "misc/stats-partner.html"

    def get_context_data(self):
        return {}

@register("listing_skeleton")
class ListingSkeleton(Component):
    template_file = "misc/listing-skeleton.html"

    def get_context_data(self):
        return {}