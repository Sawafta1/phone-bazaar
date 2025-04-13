from django.shortcuts import render
from store.models import Phone
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Phone, Review, Order, OrderItem, UserProfile
from .forms import ReviewForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import ContactForm
from django.contrib.auth.decorators import login_required

def home(request):
    phones = Phone.objects.all()
    brand = request.GET.get('brand')
    if brand:
        phones = phones.filter(brand=brand)
    return render(request, 'store/home.html', {'phones': phones})

def product_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    reviews = Review.objects.filter(phone=phone)
    can_review = False

    if request.user.is_authenticated:
        has_ordered = OrderItem.objects.filter(
            order__user=request.user, phone=phone
        ).exists()
        can_review = has_ordered

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.phone = phone
            review.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'store/product_detail.html', {
        'phone': phone,
        'reviews': reviews,
        'form': form,
        'can_review': can_review
    })
def signup_view(request):
 if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()

            # create UserProfile
            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )

            login(request, user)  # log them in after signup
            return redirect('home')
 else:
        form = SignUpForm()
 return render(request, 'store/signup.html', {'form': form})

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    phones = Phone.objects.filter(id__in=cart.keys())
    cart_items = []

    for phone in phones:
        quantity = cart[str(phone.id)]
        cart_items.append({
            'phone': phone,
            'quantity': quantity,
            'subtotal': phone.price * quantity
        })

    total = sum(item['subtotal'] for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')
@require_POST
@login_required
def remove_from_cart(request):
    phone_id = request.POST.get('phone_id')
    amount = int(request.POST.get('amount', 1))
    
    cart = request.session.get('cart', {})
    if phone_id in cart:
        cart[phone_id] -= amount
        if cart[phone_id] <= 0:
            del cart[phone_id]
        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})
def suggest_phone_view(request):
    suggestions = []

    if request.method == 'POST':
        max_price = request.POST.get('max_price')
        storage = request.POST.get('storage')
        color = request.POST.get('color')

        # Fallback to case-insensitive search
        phones = Phone.objects.filter(
            storage__icontains=storage,
            color__icontains=color,
            price__lte=max_price
        ).order_by('price')[:3]

        suggestions = list(phones)

    return render(request, 'store/suggest.html', {'suggestions': suggestions})
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Optionally, save or send email here
            messages.success(request, "Thanks for contacting us! We'll respond soon.")
            form = ContactForm()  # reset form
    else:
        form = ContactForm()
    
    return render(request, 'store/contact.html', {'form': form})