from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from admin.ai_trader.models import AITrader
from admin.tensor.models import Calculator, FashionClassification, TensorFunction


@api_view(['GET'])
@parser_classes([JSONParser])
def process(request):
    AITrader().process()
    return JsonResponse({'AI Trader process': 'SUCCESS'})

