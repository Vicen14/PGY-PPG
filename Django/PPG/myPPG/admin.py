from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Category, Game, Order, OrderItem

@admin.register(User)
class UserAdmin(BaseUserAdmin):
  fieldsets = BaseUserAdmin.fieldsets + (
    (None, {'fields': ('role',)}),
  )

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Game)
admin.site.register(Order)
admin.site.register(OrderItem)  