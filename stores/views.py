from django.shortcuts import render, redirect
from .models import Store
from .forms import StoreModelForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def store_list(request):
    store_list = Store.objects.all()

    paginator = Paginator(store_list, 4) # Show 4 stores per page
    page = request.GET.get('page')
    try:
        stores = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        stores = paginator.page(1)
    except EmptyPage:
        stores = paginator.page(paginator.num_pages)

    

    context = {
        "stores": stores
    }
    return render(request, 'store_list.html', context)

def store_create(request):
    store_form = StoreModelForm()
    if request.method == "POST":
        store_form = StoreModelForm(request.POST)
        if store_form.is_valid():
            store_form.save()
            return redirect('list')
    return render(request, 'store_create.html', {"store_form": store_form})

def store_detail(request, store_slug):
    context = {
        "store": Store.objects.get(slug=store_slug)
            }
    return render(request, 'store_details.html', context)



