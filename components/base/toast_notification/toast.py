from django_components import Component, register

@register("toast_notification")
class Modal(Component):
    template_file = "base/toast_notification/template.html"

    def get_context_data(self, notification_type, message):
        return {
            'notification_type': notification_type,
            'message': message,
        }