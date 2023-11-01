from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tracking.api.serilizers import LocationSerializer, MetricSerializer


class LocationAPIView(APIView):
    def post(self, request, *args, **kwargs):

        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response("Location Saved", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetricAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MetricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response("Metric Saved", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



