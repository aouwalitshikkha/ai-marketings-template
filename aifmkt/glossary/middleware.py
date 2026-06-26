import re


class HtmlMinifyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.get('Content-Type', '').startswith('text/html'):
            content = response.content.decode('utf-8')
            minified = re.sub(r'\s+', ' ', content)
            minified = re.sub(r'>\s+<', '><', minified)
            response.content = minified.encode('utf-8')
            response['Content-Length'] = len(response.content)
        return response
