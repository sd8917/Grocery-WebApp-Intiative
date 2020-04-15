from django import forms

from customer.models import Customer_Order


class CreateOrderForm(forms.ModelForm):
	class Meta:
		model = Customer_Order
		fields = ['customer_name','customer_number','image','product','place']


class UpdateOrderForm(forms.ModelForm):
	class Meta:
		model = Customer_Order
		fields = ['customer_name','customer_number','image','product','place']


	def save(self, commit=True):
		user_order = self.instance
		user_order.customer_name = self.cleaned_data['customer_name']
		user_order.customer_number = self.cleaned_data['customer_number']
		user_order.product       = self.cleaned_data['product']
		user_order.place         = self.cleaned_data['place']

		if self.cleaned_data['image']:
			user_order.image = self.cleaned_data['image']

		if commit:
			user_order.save()
		return user_order

