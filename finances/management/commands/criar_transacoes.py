import calendar
import random
from datetime import date

from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError

from accounts.models import Account
from categories.models import Categorie
from finances.models import Transaction


class Command(BaseCommand):
    help = ('Cria dados mocados (contas, categorias e transações) para um '
            'usuário. Contas e categorias usam get_or_create — rodar de novo '
            'não duplica, apenas adiciona novas transações.')

    # (nome, tipo da conta, saldo inicial)
    CONTAS = [
        ('Conta Corrente', 'conta corrente', 3200.00),
        ('Poupança', 'poupanca', 15000.00),
        ('Carteira', 'dinheiro', 350.00),
        ('Investimentos', 'investimentos', 28000.00),
        ('VR Alimentação', 'vale', 900.00),
    ]

    # (nome, tipo)
    CATEGORIAS = [
        ('Salário', 'revenue'),
        ('Freelance', 'revenue'),
        ('Dividendos', 'revenue'),
        ('Vendas Online', 'revenue'),
        ('Aluguel', 'expense'),
        ('Mercado', 'expense'),
        ('Transporte', 'expense'),
        ('Restaurante', 'expense'),
        ('Café', 'expense'),
        ('Saúde', 'expense'),
        ('Educação', 'expense'),
        ('Lazer', 'expense'),
        ('Assinaturas', 'expense'),
        ('Vestuário', 'expense'),
        ('Viagem', 'expense'),
    ]

    # categoria -> (descrições possíveis, valor mín, valor máx,
    #               ocorrências por mês (mín, máx), contas possíveis)
    DESPESAS = {
        'Aluguel': (['Aluguel do apartamento'], 1800, 1800, 1, 1, ['Conta Corrente']),
        'Mercado': (['Compra no mercado', 'Compras do mês', 'Mercearia'],
                    60, 480, 3, 6, ['Conta Corrente', 'VR Alimentação']),
        'Transporte': (['Combustível', 'Uber', 'Passagem de ônibus', 'Estacionamento'],
                       8, 220, 3, 7, ['Conta Corrente', 'Carteira']),
        'Restaurante': (['Almoço', 'Jantar fora', 'Delivery', 'Churrasco'],
                        25, 260, 2, 5, ['Conta Corrente', 'VR Alimentação']),
        'Café': (['Café da manhã', 'Padaria'], 6, 28, 2, 8, ['Carteira', 'VR Alimentação']),
        'Saúde': (['Farmácia', 'Consulta médica', 'Plano de saúde', 'Dentista'],
                  30, 800, 0, 2, ['Conta Corrente']),
        'Educação': (['Curso online', 'Livros', 'Mensalidade'],
                     40, 600, 0, 2, ['Conta Corrente']),
        'Lazer': (['Cinema', 'Show', 'Passeio no fim de semana', 'Streaming de jogo'],
                  20, 350, 1, 3, ['Conta Corrente', 'Carteira']),
        'Assinaturas': (['Netflix', 'Spotify', 'iCloud', 'Academia'],
                        12, 90, 2, 4, ['Conta Corrente']),
        'Vestuário': (['Roupas', 'Tênis novo', 'Presente'],
                      50, 450, 0, 2, ['Conta Corrente', 'Carteira']),
        'Viagem': (['Passagem aérea', 'Hotel', 'Pacote de viagem'],
                   300, 2800, 0, 1, ['Conta Corrente', 'Poupança']),
    }

    RECEITAS = {
        'Salário': (['Salário mensal'], 5500, 7500, 1, 1, ['Conta Corrente']),
        'Freelance': (['Projeto freelance', 'Site para cliente', 'Consultoria'],
                      400, 4500, 0, 2, ['Conta Corrente']),
        'Dividendos': (['Dividendos', 'Rendimento de fundos'],
                       40, 900, 0, 1, ['Investimentos']),
        'Vendas Online': (['Venda no marketplace', 'Venda de item usado'],
                          50, 1200, 0, 2, ['Conta Corrente']),
    }

    # Categorias recorrentes com dia fixo no mês.
    DIA_FIXO = {'Salário': 5, 'Aluguel': 10}

    def add_arguments(self, parser):
        parser.add_argument('--user', required=True,
                            help='Username que receberá os dados')
        parser.add_argument('--meses', type=int, default=6,
                            help='Quantidade de meses retroativos a popular (padrão: 6)')

    def handle(self, *args, **options):
        username = options['user']
        meses = options['meses']

        if meses < 1:
            raise CommandError('--meses deve ser pelo menos 1.')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"Usuário '{username}' não encontrado.")

        contas = self.criar_contas(user)
        categorias = self.criar_categorias(user)
        transacoes = self.criar_transacoes(user, contas, categorias, meses)

        self.stdout.write(self.style.SUCCESS(
            f'Pronto: {len(contas)} contas, {len(categorias)} categorias e '
            f'{len(transacoes)} transações para "{username}" '
            f'(últimos {meses} meses).'))

    def criar_contas(self, user):
        contas = {}
        for nome, tipo, valor in self.CONTAS:
            conta, _ = Account.objects.get_or_create(
                user=user, name=nome,
                defaults={'categorie': tipo, 'value': valor})
            contas[nome] = conta
        return contas

    def criar_categorias(self, user):
        categorias = {}
        for nome, tipo in self.CATEGORIAS:
            categoria, _ = Categorie.objects.get_or_create(
                user=user, category=nome,
                defaults={'category_type': tipo})
            categorias[nome] = categoria
        return categorias

    def criar_transacoes(self, user, contas, categorias, meses):
        hoje = date.today()
        transacoes = []

        for offset in range(meses):
            inicio = self.primeiro_dia_do_mes(hoje, offset)
            ultimo_dia = calendar.monthrange(inicio.year, inicio.month)[1]

            for nome, (descricoes, valor_min, valor_max,
                       ocorrencias_min, ocorrencias_max, nomes_conta) in \
                    {**self.RECEITAS, **self.DESPESAS}.items():

                quantidade = random.randint(ocorrencias_min, ocorrencias_max)
                for _ in range(quantidade):
                    dia = self.DIA_FIXO.get(nome)
                    if dia is None:
                        dia = random.randint(1, ultimo_dia)
                    # Mês corrente: não vencimento além do fim do mês.
                    elif offset == 0:
                        dia = min(dia, ultimo_dia)

                    transacoes.append(Transaction(
                        user=user,
                        account=contas[random.choice(nomes_conta)],
                        category=categorias[nome],
                        description=random.choice(descricoes),
                        value=round(random.uniform(valor_min, valor_max), 2),
                        due_date=date(inicio.year, inicio.month, dia),
                    ))

        #bulk_create é seguro: não há signals em Transaction.
        Transaction.objects.bulk_create(transacoes)
        return transacoes

    @staticmethod
    def primeiro_dia_do_mes(base, offset):
        total = base.year * 12 + (base.month - 1) - offset
        return date(total // 12, total % 12 + 1, 1)
