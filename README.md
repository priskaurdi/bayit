# bayit
bayit eletrica e ar condicionado

# BayitEnergy – tecnologia e gestão  para serviços elétricos e refrigeração 

## Descrição

O BayitEnergy é uma plataforma completa que auxilia profissionais autônomos na gestão de seus serviços, orçamentos e clientes. Desenvolvido com foco na usabilidade e eficiência, o ServicePro oferece funcionalidades como cadastro de serviços, agendamento, controle financeiro, comunicação direta com clientes e muito mais.

## Funcionalidades Principais

* **Cadastro de Serviços:** Permite cadastrar e gerenciar os serviços oferecidos.
* **Orçamentos:** Criação e envio de orçamentos personalizados para clientes.
* **Agendamento:** Gerenciamento de compromissos e prazos de forma organizada.
* **Controle Financeiro:** Acompanhamento de receitas e despesas.
* **Comunicação:** Mensagens diretas e notificações para interação com clientes.
* **Relatórios e Estatísticas:** Análise do desempenho do negócio.

## Tecnologias

* **Front-end:** HTML, CSS, Javascript, Typescript
* **Back-end:** Python (Django)
* **Banco de Dados:** MySQL
* **Nuvem:** Google Cloud
* **APIs:** Stripe/PayPal (pagamentos), Google Maps (geolocalização), Google Calendar (notificações)

## Configuração

1.  Clone o repositório: `git clone https://github.com/priskaurdi/bayit.git`
2.  verifique o local pwd
3.  crie uma venv ao nivel das pastas externas e ative-a `python -m venv .venv` e `source .venv/Scripts/activate # Ativar ambiente`
5.  Execute o comando: `pip install django-cors-headers`

6. Instale as dependências: `pip install -r requirements.txt` (back-end) 
7.  Configure as variáveis de ambiente (banco de dados, APIs) em um novo arquivo .env de acordo com o exemplo. 
    (sugestão de geração de chave: `from django.core.management.utils import get_random_secret_key print(get_random_secret_key())`
8. Rode as migrações `python manage.py makemigrations && python manage.py migrate`
9. Execute o back-end: `python manage.py runserver` 



## Testes

* Testes unitários: `pytest`, `coverage run`, `coverage html`
* Testes de integração: [Instruções para executar os testes de integração]
* Testes de ponta a ponta: [Instruções para executar os testes de ponta a ponta]

## Contribuição

Contribuições são bem-vindas! Siga estas etapas:

1.  Faça um fork do repositório.
2.  Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
3.  Faça commit das suas mudanças: `git commit -am 'Adiciona minha feature'`
4.  Faça push para a branch: `git push origin feature/minha-feature`
5.  Abra um pull request.

## Licença

[Licença do projeto]

## Contato

[E-mail de contato]
