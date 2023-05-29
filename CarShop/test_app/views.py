from django.db.models import Model
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Product, Bye, Provider

from .models import ProductType


def index(request):

    sort = request.GET.getlist('sort')

    products = Product.objects.all().order_by(*sort)
    byes = Bye.objects.all()
    providers = Provider.objects.all()

    return render(request, "index.html", {"products": products, "providers": providers, "byes": byes})





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