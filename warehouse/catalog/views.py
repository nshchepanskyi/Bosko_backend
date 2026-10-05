from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ProductForm
from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/products.html', {'products': products})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар «{product.name}» додано.')
            return redirect('catalog:product_list')
    else:
        form = ProductForm()

    return render(request, 'catalog/product_form.html', {'form': form})