from django_components import Component, register

@register("button")
class Buttons(Component):
    template_file = "base/button/button.html"

    def get_context_data(self, html_tag="a", label="Click Me", href="#", type="primary", extraclass="", function=None, width="max", attr=None):
        """ 
    Generates context data for a button or hyperlink component.

    Parameters:
    -----------
    html_tag : str, optional (default: "a")
        Determines whether the component is a hyperlink (`<a>`) or a button (`<button>`).
    
    label : str, optional (default: "Click Me")
        The text displayed on the button or link.

    href : str, optional (default: "#")
        The URL for the hyperlink (`<a>` tag). Ignored if `html_tag` is `"button"`.

    type : str, optional (default: "primary")
        The button style type (e.g., "primary", "secondary", etc.).

    extraclass : str or None, optional (default: None)
        Additional CSS classes to apply for custom styling.

    function : str or None, optional (default: None)
        Specifies the button's behavior (e.g., `"submit"` for form submission).
        This is only applicable if `html_tag` is `"button"`.

    Returns:
    --------
    dict
        A dictionary containing the processed context variables for rendering the component.
    """
        return {
            'tag': html_tag,
            'label': label,
            'href': href,
            'type': type,
            'extraclass': extraclass,
            'function': function,
            'width': width,
            'attr': attr,
        }
