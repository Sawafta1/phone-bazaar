from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Phone
from .serializers import PhoneSerializer

@api_view(['GET'])
def phone_compare_api(request):
    p1 = request.GET.get('p1')
    p2 = request.GET.get('p2')

    if not p1 or not p2:
        return Response({'error': 'Please provide two product IDs as p1 and p2'}, status=400)

    phone1 = Phone.objects.filter(pk=p1).first()
    phone2 = Phone.objects.filter(pk=p2).first()

    if not phone1 or not phone2:
        return Response({'error': 'One or both phones not found.'}, status=404)

    serializer1 = PhoneSerializer(phone1)
    serializer2 = PhoneSerializer(phone2)

    return Response({
        'product_1': serializer1.data,
        'product_2': serializer2.data
    })
