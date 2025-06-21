from django_components import Component, register

@register("listing_card")
class Buttons(Component):
    template_file = "base/listingCard/template.html"

    def check_if_favourite(self, listing, user_favourites):
        if listing in user_favourites:
            return True
        else:
            return False

    def format_size(self, size, type):
        if size is None:
            return "---"
        if type == "land":
            return f"{size} Sq.m"
        return f"{size} Units"

    def get_context_data(self, id, listing, user_favourites, imageUrl, href, title, price, size, type, address, images_count=0):
        
        is_favourite = self.check_if_favourite(listing, user_favourites)
        size = self.format_size(size, type)
    
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
            'is_favourite': is_favourite
        }