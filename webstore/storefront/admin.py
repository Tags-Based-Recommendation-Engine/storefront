from django.contrib import admin
from . import models


class sellerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("store_name",)}

class listingAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("id",)}

admin.site.register(models.User)
admin.site.register(models.Seller, sellerAdmin)
admin.site.register(models.Image)
admin.site.register(models.Product)
admin.site.register(models.Listing, listingAdmin)





# Register your models here.
