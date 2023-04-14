

class WhiteListValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        
        actual_ip = request.META.get('REMOTE_ADDR')
        actual_browser = request.META.get('HTTP_USER_AGENT')
        access_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]