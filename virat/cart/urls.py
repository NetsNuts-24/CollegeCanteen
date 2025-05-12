from . import views 
from django.urls import path,include
from .views import admin_orders
from django.contrib.auth import views as auth_views
app_name = "cart"
urlpatterns = [

    path('menu' , views.menu_view , name="menu_view"),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/orders/complete/<int:order_id>/', views.mark_order_completed, name='mark_order_completed'),
    path("create-order/", views.create_order, name="create_order"),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites/add/<int:item_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:item_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('quick-order/', views.view_quick_order, name='view_quick_order'),
    path('quick-order/add/<int:item_id>/', views.add_to_quick_order, name='add_to_quick_order'),
    path('quick-order/remove/<int:item_id>/', views.remove_from_quick_order, name='remove_from_quick_order'),
    path('<str:token_number>/', views.order_details, name='order_details'),
    path('logout/', auth_views.LogoutView.as_view(next_page='account:login'), name='logout'),
]
        
