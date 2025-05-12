
from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem, Cart


# -----------------------------
# Category Admin
# -----------------------------
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)


# -----------------------------
# MenuItem Admin
# -----------------------------
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available')
    list_editable = ('is_available',)  # Allows toggling availability
    list_filter = ('category', 'is_available')
    search_fields = ('name',)

admin.site.register(MenuItem, MenuItemAdmin)


# -----------------------------
# Order Admin
# -----------------------------
class OrderAdmin(admin.ModelAdmin):
    list_display = ('token_number', 'get_name', 'get_mobile', 'order_date', 'is_completed')
    list_filter = ('is_completed', 'order_date')
    search_fields = ('token_number', 'name', 'mobile')

    def get_name(self, obj):
        return obj.name if obj.name else "N/A"
    get_name.short_description = "Customer Name"

    def get_mobile(self, obj):
        return obj.mobile if obj.mobile else "N/A"
    get_mobile.short_description = "Mobile Number"

admin.site.register(Order, OrderAdmin)


# -----------------------------
# OrderItem Admin
# -----------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity')
    search_fields = ('order__token_number', 'item__name')


# -----------------------------
# Cart Admin
# -----------------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')
    search_fields = ('user__username', 'item__name')
