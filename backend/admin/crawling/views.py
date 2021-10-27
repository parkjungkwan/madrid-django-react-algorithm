from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from admin.common.models import ValueObject, Reader, Printer
import matplotlib.pyplot as plt

from admin.crawling.models import Crawling, NewsCrawling


@api_view(['GET'])
@parser_classes([JSONParser])
def process(request):
    Crawling().process()
    return JsonResponse({'result': 'Create Crawling Success'})


@api_view(['GET'])
@parser_classes([JSONParser])
def process(request):
    NewsCrawling().process()
    return JsonResponse({'result': 'News Crawling Success'})