import random
from django.db.models.signals import post_save
from django.core.cache import cache
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from FleetManager.local_settings import api_key
from company.api.serilizers import CompanySerializer
from company.models import Car
from company.sms_utils import SMSUtil
from rest_framework.permissions import IsAuthenticated


class SendOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receptor = request.data.get('phone_number')

        if not receptor:
            return Response({'error': 'Phone Number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_code = ''.join(random.choices("0123456789", k=6))
            sender = '10008663'
            message = f'Code OTP: {otp_code}'
            sms_util = SMSUtil(api_key)

            # ارسال پیامک
            response = sms_util.send_sms(sender, receptor, message)

            if response:
                cache_key = f'otp:{request.user.id}'
                cache.set(cache_key, otp_code, 120)

                request.user.registration_step = 3
                request.user.save()

                return Response({'message': 'Code OTP Sent.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Error sending SMS.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPView(APIView):
    def post(self, request):
        otp_code = request.data.get('otp_code')
        registration_step = request.user.registration_step

        try:
            cache_key = f'otp:{request.user.id}'
            stored_otp = cache.get(cache_key)

            if stored_otp and stored_otp == otp_code:
                cache.delete(cache_key)

                if registration_step == 3:
                    return Response({'message': 'The OTP code has been successfully verified.'},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid registration step for OTP verification.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'The OTP code is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateCompanyView(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():
            company = serializer.save(user=request.user)

            post_save.send(sender=Car, instance=company, created=True)

            return Response({'message': 'Company created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
