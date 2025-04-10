from django_components import Component, register

@register("listing_card")
class Buttons(Component):
    template_file = "listingCard/template.html"

    def get_context_data(self, id, listing, user_favourites, imageUrl, href, title, price, size, type, address, images_count=0):
        if size is None:
            size = "---"
        elif type == "land":
            size = f"{size} Sq.m"
        else:
            size = f"{size} Units"

        

        return {
            'id': id,
            'listing': listing,
            'imageUrl': imageUrl,
            'user_favourites': user_favourites,
            'href': href,
            'title': title,
            'price': format(price, ','),
            'size': size,
            'type': type,
            'address': address,
            'images_count': images_count + 1,
        }