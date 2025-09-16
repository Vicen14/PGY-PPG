from django.contrib import admin
from .models import Category, Product, Profile, Order, OrderItem, InventoryMovement

# --------- CATEGORY ---------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

# --------- PRODUCT ---------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Tus campos actuales: name, description, price, stock, image (URL), category
    list_display = ("name", "category", "price", "stock")
    list_filter = ("category",)
    search_fields = ("name", "description")

# --------- PROFILE ---------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")
    search_fields = ("user__username", "phone")

# --------- ORDER / ORDER ITEM ---------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Tus campos actuales: user, created_at, total  (no tienes 'status' en este models.py)
    list_display = ("id", "user", "created_at", "total")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]

# --------- INVENTORY MOVEMENT ---------
@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    # Tus campos actuales: product, change, timestamp  (no tienes quantity_change/reason/created_at)
    list_display = ("product", "change", "timestamp")
    list_filter = ("timestamp",)
    date_hierarchy = "timestamp"
