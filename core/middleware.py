from django.utils.deprecation import MiddlewareMixin

class ClearCookiesMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Exclui todos os cookies presentes na solicitação
        for cookie_name in request.COOKIES:
            response.delete_cookie(cookie_name)

        return response
