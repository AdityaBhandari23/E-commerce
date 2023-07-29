from django.shortcuts import render
from .models import Product,Contact,Orders
from math import ceil


# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    # print(allProds)
    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    # print(params)
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    # if 'email' in request.POST:
    #     print("YES BOSS")  ## it is used to check whether this field is present or not
    if request.method=="POST":
        print(request)
        nameV=request.POST.get('name', '')
        emailV=request.POST.get('email', '')
        phoneV=request.POST.get('phone', '')
        descV=request.POST.get('desc', '')
        contact = Contact(name=nameV, email=emailV, phone=phoneV, desc=descV)## normal name,email.... are for databse and one with V is indicating that we have made variables in views
        contact.save()
        # print(name,email,phone, desc )
    return render(request, "shop/contact.html")

def tracker(request):
    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def productView(request, myid):
    #Fetch the product using the id
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request, "shop/prodView.html",{'product':product[0]})#ye product list ke format me hai isliye isme 0 lagaya hai list ka pehla element access karne ke liye

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')  #agar user blank rehne deta hai to default value likh do jo ki blank string hai
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        thank = True
        id = order.order_id #order ID hamare model me hai joki auto increment ho rahi hai usi ko hum access kar rahe hai
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')  # tis is when if statement didn't run

