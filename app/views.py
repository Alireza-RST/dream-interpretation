import requests
from decouple import config
from openai import OpenAI
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

        client = OpenAI(
            api_key=config('OPENAPI_SECRET_KEY'),
            organization=config('OPENAPI_ORG_ID'),
        )

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                return Response(chunk.choices[0].delta.content)

        return Response(False)

