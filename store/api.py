# store/api.py

from django.http import JsonResponse
from .models import Phone

def phone_list_api(request):
    brand = request.GET.get('brand')
    storage = request.GET.get('storage')

    phones = Phone.objects.all()

    if brand:
        phones = phones.filter(brand=brand)
    if storage:
        phones = phones.filter(storage=storage)

    data = []
    for phone in phones:
        data.append({
            'id': phone.id,
            'brand': phone.brand,
            'model': phone.model,
            'storage': phone.storage,
            'color': phone.color,
            'price': float(phone.price),
            'stock': phone.stock,
            'image': phone.image.url if phone.image else ''
        })

    return JsonResponse({'phones': data})
