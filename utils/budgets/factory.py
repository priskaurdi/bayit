# from inspect import signature
from random import randint

from faker import Faker


def rand_ratio():
    return randint(840, 900), randint(473, 573)


fake = Faker('pt_BR')
# print(signature(fake.random_number))


def make_budget():
    return {
        'title': fake.sentence(nb_words=6), # Título da solicitação
        'description': fake.sentence(nb_words=12), # Descrição do problema
        'service_type': fake.random_element(elements=('Manutenção', 'Instalação', 'Limpeza')), # Tipo de serviço
        'scheduled_date': fake.future_date(), # Data agendada
        'scheduled_time': fake.time(), # Horário agendado
        'address': {
            'street': fake.street_name(),
            'number': fake.building_number(),
            'neighborhood': fake.bairro(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zipcode': fake.postcode()
        },
        'preparation_time': fake.random_number(digits=2, fix_len=True),
        'preparation_time_unit': 'Minutos',
        'servings': fake.random_number(digits=2, fix_len=True),
        'servings_unit': 'Porção',
        'preparation_steps': fake.text(3000),
        'created_at': fake.date_time(),
        'author': {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'phone': fake.phone_number(),
            'email': fake.email()
        },
        'equipment': {
            'brand': fake.random_element(elements=('LG', 'Samsung', 'Electrolux', 'Consul')),
            'model': fake.random_element(elements=('Split', 'Janela', 'Portátil')),
            'btus': fake.random_element(elements=(9000, 12000, 18000, 24000))
        },
        'category': {
            'name': fake.word()
        },
        'status': fake.random_element(elements=('Pendente', 'Em andamento', 'Concluído', 'Cancelado')),
        'service_provider': { # Prestador de serviço (opcional)
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'phone': fake.phone_number(),
            'email': fake.email()
        },
        'cover': {
            'url': 'https://loremflickr.com/%s/%s/airconditioner,repair' % rand_ratio(),
        }
    }



if __name__ == '__main__':
    from pprint import pprint
    pprint(make_budget())