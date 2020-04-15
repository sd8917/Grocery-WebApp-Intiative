from django.db import models

from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.



def upload_location(instance, filename):
  file_path = 'customer/{author_id}/{customer_name}-{filename}'.format(
        author_id=str(instance.author.id),customer_name=str(instance.customer_name), filename=filename)
  return file_path

class Customer_Order(models.Model):
  customer_name 						= models.CharField(max_length=55,null=False, blank=False)
  customer_number 					= models.BigIntegerField(null=False, blank=False)
  image		 			            = models.ImageField(upload_to=upload_location, null=True, blank=True)
  product 									= models.CharField(max_length=20)
  place 										= models.CharField(max_length=20)
  date_published 						= models.DateTimeField(auto_now_add=True, verbose_name="date published")
  date_updated 		          = models.DateTimeField(auto_now=True, verbose_name="date updated")
  author 										= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  slug 											= models.SlugField(blank=True, unique=True)


  def __str__(self):
    return self.customer_name + '  -   ' + str(self.customer_number)



@receiver(post_delete, sender=Customer_Order)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

def pre_save_order_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.customer_name)

pre_save.connect(pre_save_order_post_receiver, sender=Customer_Order)