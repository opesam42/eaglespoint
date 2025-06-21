from django_components import Component, register

@register("listing_skeleton")
class ListingSkeleton(Component):
    template_file = "misc/listing-skeleton.html"

    def get_context_data(self):
        return {}
    
@register("table_skeleton")
class TableSkeleton(Component):
    template_file = "misc/table-skeleton.html"

    def get_context_data(self):
        return {}    

@register("no_results")
class NoResults(Component):
    """
        This component will be displayed when a search return no results
        
        Parameters:
            caption : User friendly caption to tell the user about the no result found situatin

    """
    template_file = "misc/no_results.html"

    def get_context_data(self, caption):
        return {
            'caption': caption,
        }    