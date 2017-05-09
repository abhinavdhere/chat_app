# Create your models here.
from django.db import models
from django.utils import timezone

class message(models.Model):
	author = models.ForeignKey('auth.User',related_name='Author')
	recipient = models.ForeignKey('auth.User',related_name='Recipient')
	text = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now)

	def send(self):
		self.timestamp=timezone.now()
		self.save()

	def __str__(self):
		return self.text