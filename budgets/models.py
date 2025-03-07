from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

class Budget(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    service_type = models.CharField(max_length=50, choices=[
        ('Manutenção', 'Manutenção'),
        ('Instalação', 'Instalação'),
        ('Limpeza', 'Limpeza'),
    ])
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    #author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budget')
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
    #service_provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='provided_services')
    #tags = models.ManyToManyField('Tag', blank=True)
    cover = models.ImageField(upload_to='budgets/covers/%Y/%m/%d/',  blank=True, default='')

    def __str__(self):
            return self.title
    


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
