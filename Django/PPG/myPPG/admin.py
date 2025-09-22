from django.contrib import admin
from .models import (
    Category,
    Product,
    Profile,
    Order,
    OrderItem,
    InventoryMovement,
)

# ---------- CATEGORY ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# ---------- PRODUCT ----------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Campos existentes en tu modelo actual
    list_display = ("id", "name", "category", "price", "stock")
    list_filter = ("category",)
    search_fields = ("name", "description")


# ---------- PROFILE ----------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone")
    search_fields = ("user__username", "phone")


# ---------- ORDER + ITEMS (inline) ----------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "quantity", "price",)
    readonly_fields = ()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "total")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    search_fields = ("user__username",)
    inlines = [OrderItemInline]


# ---------- INVENTORY MOVEMENT ----------
@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    # OJO: tu modelo usa 'change' y 'timestamp' (no quantity_change/reason/created_at)
    list_display = ("id", "product", "change", "timestamp")
    list_filter = ("timestamp",)
    date_hierarchy = "timestamp"
    search_fields = ("product__name",)
