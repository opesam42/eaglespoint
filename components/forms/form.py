from django_components import Component, register

@register("login_form")
class LoginForm(Component):
    template_file = "forms/login_form.html"

    def get_context_data(self, form_title="Login", form_class="p-4", is_js_submission=True, show_signup_link=False, autofocus=True):
        return {
            "form_title": form_title,
            "form_class": form_class,
            "is_js_submission": is_js_submission,
            "show_signup_link": show_signup_link,
            "autofocus": autofocus,
        }

@register("signup_form")
class LoginForm(Component):
    template_file = "forms/signup_form.html"

    def get_context_data(self, form_title="Sign Up", form_class="p-4", is_js_submission=True, show_login_link=False, autofocus=True):
        return {
            "form_title": form_title,
            "form_class": form_class,
            "is_js_submission": is_js_submission,
            "show_login_link": show_login_link,
            "autofocus": autofocus,
        }