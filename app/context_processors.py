from .models import Area, Attraction, Category

def common(request):
    area_data = Area.objects.all()
    attraction_data = Attraction.objects.all()
    category_data = Category.objects.all()
    context = {
        'area_data': area_data,
        'attraction_data': attraction_data,
        'category_data': category_data,
    }
    return context
