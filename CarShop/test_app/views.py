from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import ProductType


# получение данных из бд
def index(request):
    product_types = ProductType.objects.all()
    return render(request, "index.html", {"product_types": product_types})


# сохранение данных в бд
def create(request):
    if request.method == "POST":
        product_type = ProductType()
        product_type.name = request.POST.get("name")
        product_type.save()
    return HttpResponseRedirect("/")


# изменение данных в бд
def edit(request, id):
    try:
        product_type = ProductType.objects.get(id=id)

        if request.method == "POST":
            product_type.name = request.POST.get("name")
            product_type.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"product_type": product_type})
    except ProductType.DoesNotExist:
        return HttpResponseNotFound("<h2>Product type not found</h2>")


# удаление данных из бд
def delete(request, id):
    try:
        product_type = ProductType.objects.get(id=id)
        product_type.delete()
        return HttpResponseRedirect("/")
    except ProductType.DoesNotExist:
        return HttpResponseNotFound("<h2>Product type not found</h2>")