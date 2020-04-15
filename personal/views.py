from django.shortcuts import render
from operator import attrgetter

from customer.models import Customer_Order
from customer.views import get_order_queryset
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator 

USER_ORDERS_PER_PAGE = 2

def home_screen_view(request):
	
	context = {}

	query = ""
	if request.GET:
		query = request.GET.get('q','')
		context['query'] = str(query)


	user_orders = sorted(get_order_queryset(query), key=attrgetter('date_updated'), reverse=True)

	#Pagination 
	page = request.GET.get('page',1)
	user_orders_paginator = Paginator(user_orders,USER_ORDERS_PER_PAGE)

	try:
		user_orders  = user_orders_paginator.page(page)	
	except PageNotAnInteger:
		user_orders  = user_orders_paginator.page(USER_ORDERS_PER_PAGE)

	except EmptyPage:
		user_orders = user_orders_paginator.page(user_orders_paginator.num_pages)


	context['user_orders '] = user_orders 

	return render(request, "personal/home.html", context)
