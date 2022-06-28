from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from goods.models import GoodsCategary,GoodsInfo


def index(request):

    # 首页分类的商品分类
    categories = GoodsCategary.objects.all()

    # 每个商品分类取出最后四个商品

    for cag in categories:
        cag.goods_list = cag.goodsinfo_set.order_by('-id')[:4]

    # 购物车的商品数量列表
    cart_goods_list = []
    # 商品总数量
    cart_goods_count = 0

    for goods_id, goods_num in request.COOKIES.items():

        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num

        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)

    return render(request, 'index.html', {'categories': categories,
                                          'cart_goods_list': cart_goods_list,
                                          'cart_goods_count': cart_goods_count})

# 商品详情页面
def detail(request):

    categories = GoodsCategary.objects.all()

    cart_goods_list = []
    cart_goods_count = 0
    for goods_id,goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)

    goods_id = request.GET.get('id', 1)
    goods_data = GoodsInfo.objects.get(id=goods_id)

    return render(request, 'detail.html ',{'categories': categories,
                                    'cart_goods_list': cart_goods_list,
                                    'cart_goods_count': cart_goods_count,
                                    'goods_data': goods_data})

# 商品分类页面
def goods(request):

    cag_id = request.GET.get('cag', 1)
    page_id = request.GET.get('page', 1)
    current_cag = GoodsCategary.objects.get(id=cag_id)
    goods_data = GoodsInfo.objects.filter(goods_cag_id=cag_id)

    paginator = Paginator(goods_data, 12)
    page_data = paginator.page(page_id)

    categories = GoodsCategary.objects.all()

    cart_goods_list = []
    cart_goods_count = 0
    for goods_id,goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)

    return render(request, 'goods.html', {'current_cag': current_cag,
                                          'page_data': page_data,
                                          'categories': categories,
                                          'cart_goods_list': cart_goods_list,
                                          'cart_goods_count': cart_goods_count,
                                          'paginator': paginator,
                                          'cag_id': cag_id})

