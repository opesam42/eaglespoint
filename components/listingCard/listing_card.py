from django_components import Component, register

@register("listing_card")
class Buttons(Component):
    template_file = "listingCard/template.html"

    def get_context_data(self, imageUrl, href, title, price, size, type, address):
        return {
            'imageUrl': imageUrl,
            'href': href,
            'title': title,
            'price': price,
            'size': size,
            'type': type,
            'address': address,
        }