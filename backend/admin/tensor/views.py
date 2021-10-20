from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from admin.tensor.models import Calculator, FashionClassification, TensorFunction


@api_view(['GET'])
@parser_classes([JSONParser])
def calculator(request):
    Calculator().process()
    return JsonResponse({'calculator': 'SUCCESS'})

@api_view(['GET'])
@parser_classes([JSONParser])
def fashion(request):
    FashionClassification().fashion()
    return JsonResponse({'Fashion Classification ': 'SUCCESS'})

@api_view(['GET'])
@parser_classes([JSONParser])
def hook(request):
    TensorFunction().hook()
    return JsonResponse({'Tensor Hook ': 'SUCCESS'})