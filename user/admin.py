from django.contrib import admin
# Register your models here.
from .models import *
class contactAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile", "email", "message")
admin.site.register(contact, contactAdmin)

class brandAdmin(admin.ModelAdmin):
    list_display = ("bname", "bpic", "bdate")
admin.site.register(brand, brandAdmin)

class productAdmin(admin.ModelAdmin):
    list_display = ( "id", "pname", "ppic", "pcolor", "category", "tprice", "disprice", "pdes", "brand","pdate")
admin.site.register(product,productAdmin)

class profileAdmin(admin.ModelAdmin):
    list_display = ( "Name", "Dob", "Gender", "Mobile", "Email", "Password", "Address","Photo")
admin.site.register(profile,profileAdmin)

class orderAdmin(admin.ModelAdmin):
    list_display = ( "id", "pid", "userid", "remarks", "status", "odate")
admin.site.register(order,orderAdmin)

class addtocartAdmin(admin.ModelAdmin):
    list_display = ( "id", "pid", "userid", "status", "cdate")
admin.site.register(addtocart,addtocartAdmin)
