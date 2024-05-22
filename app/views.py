import requests
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import InterpretationSerializer
from .thorttling import CustomThrottle


class InterpretationView(APIView):
    throttle_classes = [CustomThrottle]

    def post(self, request, *args, **kwargs):
        serializer = InterpretationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = serializer.validated_data.get('content')

        url = config('INTERPRETATION_URL')

        body = {
            "dreamContent": content,
            "methodology": "freud",
            "isPublic": True
        }

        try:
            response = requests.post(url, json=body, timeout=10)
        except requests.exceptions.RequestException:
            return Response({
                "message": "مشکلی در ارسال درخواست شما بوجود آمده لطفا چند دقیقه دیگر دوباره امتحان کنید"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            json_resp = response.json()
        except ValueError:
            return Response({
                "message": "مشکلی در دریافت اطلاعات بوجود آمده لطفا دوباره امتحان کنید"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(json_resp)

