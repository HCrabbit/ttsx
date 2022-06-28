from django.contrib import admin

# Register your models here.
from goods.models import GoodsInfo

class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods_name', 'goods_price']
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['id', 'goods_name']

admin.site.register(GoodsInfo, GoodsInfoAdmin)
