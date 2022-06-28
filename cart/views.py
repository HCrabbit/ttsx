import time

from django.shortcuts import render, redirect


# Create your views here.
from cart.models import OrderInfo, OrderGoods
from goods.models import GoodsInfo


def add_cart(request):

    goods_id = request.GET.get('id', '')

    if goods_id:

        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)

        goods_count = request.COOKIES.get(goods_id)
        if goods_count:
            goods_count = int(goods_count) + 1
        else:
            goods_count = 1

        response.set_cookie(goods_id, goods_count)

    return response

def show_cart(request):

    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0

    for goods_id,goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue

        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price
        cart_goods_list.append(cart_goods)

        cart_goods_count += int(goods_num)

        cart_goods_money += int(goods_num) * cart_goods.goods_price

    return render(request, 'cart.html', {'cart_goods_list': cart_goods_list,
                                         'cart_goods_count': cart_goods_count,
                                         'cart_goods_money': cart_goods_money,})

def remove_cart(request):

    goods_id = request.GET.get('id', '')
    if goods_id:
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id, '')
        if goods_count:
            response.delete_cookie(goods_id)

    return response

def place_order(request):

    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0

    for goods_id,goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods.total_money = cart_goods.goods_price * int(goods_num)
        cart_goods_list.append(cart_goods)
        cart_goods_count += int(goods_num)
        cart_goods_money += cart_goods.goods_price * int(goods_num)

    return render(request, 'place_order.html', {'cart_goods_list': cart_goods_list,
                                                'cart_goods_count': cart_goods_count,
                                                'cart_goods_money': cart_goods_money})

def submit_order(request):

    # 收货地址
    addr = request.POST.get('addr', '')
    # 收货人
    recv = request.POST.get('recv', '')
    # 联系电话
    tele = request.POST.get('tele', '')
    # 备注
    extra = request.POST.get('extra', '')

    # 实例化订单对象
    order_info = OrderInfo()
    order_info.order_addr = addr
    order_info.order_tele = tele
    order_info.order_recv = recv
    order_info.order_extra = extra

    # 生成订单编号
    order_info.order_id = str(time.time() * 1000) + str(time.process_time()  * 1000000)

    # 保存订单信息到数据库
    order_info.save()

    response = redirect('/cart/submit_success/?id=%s' % order_info.order_id)

    for goods_id,goods_num in request.COOKIES.items():
        if goods_id == 'csrftoken':
            continue
        # 生成订单商品的对象
        order_goods = OrderGoods()
        # 获取购物车商品的对象
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        # 把商品对象添加到订单对象里
        order_goods.goods_info = cart_goods
        order_goods.goods_num = goods_num
        order_goods.goods_order = order_info
        order_goods.save()
        response.delete_cookie(goods_id)

    return response

# 订单提交成功页面
def submit_success(request):

    # 获取传过来的订单号
    order_id = request.GET.get('id')
    #获取订单对象
    orderinfo = OrderInfo.objects.get(order_id=order_id)
    order_goods_list = OrderGoods.objects.filter(goods_order=orderinfo)

    # 商品总价
    total_money = 0
    # 商品总数量
    total_num = 0

    for goods in order_goods_list:
        goods.total_price = goods.goods_info.goods_price * goods.goods_num
        total_money += goods.total_price
        total_num += goods.goods_num

    return render(request, 'success.html', {'orderinfo': orderinfo,
                                'order_goods_list': order_goods_list,
                                'total_money': total_money,
                                'total_num': total_num})