from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.api.serializers import UserSerializer, CustomTokenObtainPairSerializer


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Create a new user and return their data along with access and refresh tokens.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            user.registration_step = 2
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GetUserRegistrationStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        registration_step = request.user.registration_step

        return Response({'registration_step': registration_step}, status=status.HTTP_200_OK)
