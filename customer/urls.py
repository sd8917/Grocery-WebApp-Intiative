from django.urls import path
from customer.views import create_order_view,detail_order_view,edit_order_view


app_name = 'blog'

urlpatterns = [
    path('create/', create_order_view, name="create"),
		path('<slug>/', detail_order_view, name="detail"),
		path('<slug>/edit/', edit_order_view, name="edit"),   
]