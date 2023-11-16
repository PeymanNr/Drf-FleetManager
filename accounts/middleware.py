from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 'HTTP_AUTHORIZATION' in request.META:
            authorization = request.META['HTTP_AUTHORIZATION'].split()
            if (len(authorization) == 2 and authorization[0].lower() ==
                    'bearer'):
                token = authorization[1]
                refresh = RefreshToken(token)
                user = refresh.user
                if not user.is_active:
                    return Response({'detail': _('User is not active.')},
                                    status=status.HTTP_401_UNAUTHORIZED)
                if refresh.access_token.is_expired():
                    return Response({'detail': _('Token has expired.')},
                                    status=status.HTTP_401_UNAUTHORIZED)
                request.user = user
                return Response({'detail': _('Token is invalid or expired.')},
                                status=status.HTTP_401_UNAUTHORIZED)

        return response
