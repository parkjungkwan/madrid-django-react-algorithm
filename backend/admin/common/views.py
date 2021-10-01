from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

@api_view(['GET'])
@parser_classes([JSONParser])
def connection(request):
    return JsonResponse({'connection': 'SUCCESS'})

