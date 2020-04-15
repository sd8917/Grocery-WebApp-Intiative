  
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from customer.models import Customer_Order
from customer.forms import CreateOrderForm, UpdateOrderForm
from account.models import Account


def create_order_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateOrderForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		form = CreateOrderForm()

	context['form'] = form

	return render(request, 'customer/create_order.html', context)



def detail_order_view(request, slug):

	context = {}
	user_order = get_object_or_404(Customer_Order, slug=slug)
	context['user_order'] = user_order

	return render(request, 'customer/detail_order.html', context)




def edit_order_view(request, slug):
	
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	user_order = get_object_or_404(Customer_Order, slug=slug)
	if request.POST:
		form = UpdateOrderForm(request.POST or None, request.FILES or None, instance=order)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			user_order = obj
	
	form = UpdateOrderForm(
			initial={
					"customer_name"   : user_order.customer_name, 
					"customer_number" : user_order.customer_number,
					"image"          : user_order.image,
					"product"        : user_order.product,
					"place"          : user_order.place,
				}
			)
	context['form'] = form

	return render(request, 'customer/edit_order.html', context)


def get_order_queryset(query=None):
	queryset = []
	#split python+course = ['python','course']
	
	queries = query.split(" ") 

	for q in queries:
		orders = Customer_Order.objects.filter(
			Q(customer_name__contains=q)|
			Q(customer_number__icontains=q)|
			Q(product__icontains=q) |
			Q(product__icontains=q)
			).distinct()
		for order in orders:
			queryset.append(order)

	# create unique set and then convert to list
	return list(set(queryset)) 