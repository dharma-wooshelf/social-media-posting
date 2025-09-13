from django.utils.deprecation import MiddlewareMixin

class UserDataMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        """
        Runs before rendering the template and injects user info into context.
        """
        if hasattr(request, "user"):
            response.context_data = response.context_data or {}
            response.context_data["user_data"] = {
                "is_authenticated": request.user.is_authenticated,
                "username": request.user.username if request.user.is_authenticated else None,
                "email": request.user.email if request.user.is_authenticated else None,
            }
        return response
