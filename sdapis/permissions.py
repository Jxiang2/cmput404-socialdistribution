from rest_framework import authentication
import base64

class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_type, _, credentials = auth_header.partition(' ')

        expected = base64.b64encode(b'socialdistribution_t21:c404t21').decode()
        if token_type == 'Basic' and credentials == expected:
            return (True, None)
        else:
            return None

    def authenticate_header(self, request):
        return '{"username" : <username>, "password" : <password>}'