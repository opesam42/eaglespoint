from django_components import Component, register

@register("listing_card")
class Buttons(Component):
    template_file = "listingCard/template.html"

    def get_context_data(self, imageUrl, title, price, size, type, address):
        return {
            'imageUrl': imageUrl,
            'title': title,
            'price': price,
            'size': size,
            'type': type,
            'address': address,
        }