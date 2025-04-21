import os
import random
import string
from collections import defaultdict
from random import SystemRandom

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image

from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

class BudgetManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id')\
        .select_related('category', 'author') \
        .prefetch_related('tags')
    

class Budget(models.Model):
    objects = BudgetManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True, null=True, blank=True)
    service_type = models.CharField(max_length=50, choices=[
        ('Manutenção', 'Manutenção'),
        ('Instalação', 'Instalação'),
        ('Limpeza', 'Limpeza'),
        ('Elétrica', 'Elétrica'),
    ])
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    equipment_brand = models.CharField(max_length=50)
    equipment_model = models.CharField(max_length=50)
    equipment_btus = models.IntegerField()
    budget_detail = models.TextField()
    budget_detail_is_html = models.BooleanField(default=False)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[
        ('Pendente', 'Pendente'),
        ('Em andamento', 'Em andamento'),
        ('Concluído', 'Concluído'),
        ('Cancelado', 'Cancelado'),
    ], default='Pendente')
    cover = models.ImageField(upload_to='budgets/covers/%Y/%m/%d/', blank=True, default='')
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('budgets:budget', args=(self.id,))

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Executa apenas se o campo 'slug' estiver vazio
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.title}-{rand_letters}')
            
        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                ...

        return saved
        



    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        budget_from_db = Budget.objects.filter(
            title__iexact=self.title
        ).first()

        if budget_from_db:
            if budget_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found budgets with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)
        
    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#     slug = models.SlugField(unique=True)

#     def __str__(self):
#         return self.name


# EDITED
# title description slug
# preparation_time preparation_time_unit
# servings servings_unit
# preparation_step
# preparation_step_is_html
# created_at updated_at
# is_published
# cover
# category (Relação)
# Author (Relação)

# Client = Author (Mantendo partes do script original)


""" title, description, service_type, scheduled_date, scheduled_time, 
street, number, neighborhood, city, state, zipcode, equipment_brand, 
equipment_model, equipment_btus, created_at, status, e cover foram adicionados 
com os tipos de campos apropriados.
client e service_provider são ForeignKey para o modelo User, permitindo relacionar 
solicitações de serviço a clientes e provedores de serviço.
service_type e status usam o parâmetro choices para limitar as opções disponíveis.
Foi adicionado o campo tags ManyToManyField, com a criação da model Tag. """
