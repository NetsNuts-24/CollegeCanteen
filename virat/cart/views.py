import random
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.


from django.shortcuts import render
from .models import MenuItem, Category

def menu_view(request):
    categories = Category.objects.all()  # Fetch all categories
    menu_items = MenuItem.objects.all()  # Fetch all menu items

    context = {
        'categories': categories,
        'menu_items': menu_items,
    }
    return render(request, 'cart/menu.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, Cart, Order, OrderItem

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:view_cart')


def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, user=request.user, item_id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')


def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, user=request.user, item_id=item_id)
    
    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()  # If quantity is 0, remove item from cart
            
    return redirect('cart:view_cart')



from django.utils.timezone import now




from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Order, OrderItem
from account.models import Profile 
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('account:login')

    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart:menu_view')

    # Get user details from Profile
    user = request.user
    profile = Profile.objects.filter(user=user).first()  # Get profile safely
    name = user.username if not user.first_name else f"{user.first_name} {user.last_name}"
    mobile = profile.mobile if profile else "Not Provided"

    # Create order with name & mobile
    order = Order.objects.create(
        user=user,
        name=name,
        mobile=mobile,
        token_number=generate_token(user)
    )

    # Move cart items to order
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            item=cart_item.item,
            quantity=cart_item.quantity
        )

    # Clear cart after order
    cart_items.delete()

    return render(request, 'cart/checkout.html', {'order': order})


# 🔥 Function to generate a unique token number
def generate_token(user):
    today = date.today().strftime('%d%m%y')  # Format: DDMMYY
    random_number = random.randint(1000, 9999)  # 4-digit random number
    return f"{user.id}{today}{random_number}"

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Order

@staff_member_required
def admin_orders(request):
    orders = Order.objects.filter(is_completed=False).order_by('-order_date')
    return render(request, 'admin/orders.html', {'orders': orders})



from django.shortcuts import redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order

@staff_member_required
def mark_order_completed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_completed = True
    order.save()
    return redirect('cart:admin_orders')

from django.shortcuts import render, get_object_or_404
from .models import Order

def order_details(request, token_number):
    order = get_object_or_404(Order, token_number=token_number)
    return render(request, 'orders/order_detail.html', {'order': order})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from account.models import Profile

@login_required
def create_order(request):
    user = request.user  # Get the logged-in user
    profile = Profile.objects.filter(user=user).first()  # Fetch user's profile

    if not profile:
        return render(request, "error.html", {"message": "User profile not found!"})  

    # Create the order for this user
    order = Order.objects.create(user=user)

    return redirect("cart/checkout.html")  # Redirect to checkout page

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Favorite

@login_required
def add_to_favorites(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    Favorite.objects.get_or_create(user=request.user, item=item)
    return redirect('cart:menu_view')

@login_required
def remove_from_favorites(request, item_id):
    Favorite.objects.filter(user=request.user, item_id=item_id).delete()
    return redirect('cart:view_favorites')

@login_required
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'cart/favorites.html', {'favorites': favorites})


from .models import QuickOrderItem

@login_required
def add_to_quick_order(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    QuickOrderItem.objects.get_or_create(user=request.user, item=item)
    return redirect('cart:menu_view')

@login_required
def remove_from_quick_order(request, item_id):
    QuickOrderItem.objects.filter(user=request.user, item_id=item_id).delete()
    return redirect('cart:view_quick_order')

@login_required
def view_quick_order(request):
    quick_items = QuickOrderItem.objects.filter(user=request.user)
    return render(request, 'cart/quick_order.html', {'quick_items': quick_items})
