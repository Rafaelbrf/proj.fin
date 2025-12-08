import csv  # pra ler os dados do arquivo CSV
import matplotlib.pyplot as plt  # pra desenhar o gráfico
import streamlit as st  # pra mostrar tudo na tela do app
#Esse é o cara que transforma o código em uma interface web
from datetime import datetime  # pra lidar com datas
from collections import defaultdict  # pra somar receitas e despesas por mês sem dor de cabeça
# como eu posso fala isso é tipo um dicionário esperto. Se você pedir uma chave que ainda não existe, ele já começa com zero
# perfeito pra ir somando valores mês a mês sem precisar ficar checando se a chave existe.

# função auxiliar para formatar valores em reais
def format_brl(valor: float) -> str:
    # transforma 1234.56 em R$ 1.234,56
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# lê o csv e agrupa receitas e despesas por mês
#  # vai somando receitas e a despesas por mês
def ler_historico_agrupado(csv_path, usuario):
    receitas_mes = defaultdict(float)
    despesas_mes = defaultdict(float)

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # pula cabeçalho
            for row in reader:
                if len(row) < 5:
                    continue # pula linha incompleta
                data_str, user, tipo, _, valor_str = row[:5]
                if user.strip().lower() != usuario.strip().lower():
                    continue # ignora se não for do usuário atual
                try:
                    valor = float(valor_str)
                    data = datetime.strptime(data_str.strip().split()[0], "%d-%m-%Y")
                    chave = f"{data.year}-{data.month:02d}"
                except Exception:
                    continue # se der erro na data ou valor, ignora
                tipo = tipo.strip().lower()
                if tipo.startswith('receit'):
                    receitas_mes[chave] += valor
                elif tipo.startswith('desp'):
                    despesas_mes[chave] += valor
    except FileNotFoundError:
        st.warning("Arquivo de dados não encontrado.")
        return [], [], [], []

    meses = sorted(set(receitas_mes) | set(despesas_mes)) # junta todos os meses
    receitas = [receitas_mes.get(m, 0.0) for m in meses]
    despesas = [despesas_mes.get(m, 0.0) for m in meses]

    # aqui vem o saldo acumulado, mês a mês
    saldo = []
    acumulado = 0.0
    for r, d in zip(receitas, despesas):
        acumulado += r - d
        saldo.append(acumulado)

    return meses, receitas, despesas, saldo

# mostra o gráfico com os dados do arquivo
def inicia(conta):
    try:
        usuario = getattr(conta, '_sistema_de_controle_financeiro__usuario', None)
        if not usuario:
            st.warning("Não foi possível identificar o usuário.")
            return

        csv_path = f"{usuario}_dados.csv"
        meses, receitas, despesas, saldo = ler_historico_agrupado(csv_path, usuario)

        if not meses:
            st.warning("Sem dados para mostrar no gráfico.")
            return

        # define os pontos no eixo X aqui não precisa modificar para nada
        x = list(range(len(meses)))
        rec_x = [xi + 0.0 for xi in x]
        desp_x = [xi + 0.2 for xi in x]
        saldo_x = [xi + 0.4 for xi in x]

        # cria o gráfico
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.plot(rec_x, receitas, marker='o', color='blue', label='Receitas')
        ax.plot(desp_x, despesas, marker='o', color='red', label='Despesas')
        ax.plot(saldo_x, saldo, marker='^', color='green', label='Saldo Acumulado')

        # coloca os nomes dos meses no eixo X
        mid_x = [xi + 0.2 for xi in x]
        ax.set_xticks(mid_x)
        ax.set_xticklabels(meses, rotation=45)

        # ajusta o eixo Y pra caber tudo
        max_valor = max(max(receitas), max(despesas), max(saldo)) if receitas or despesas or saldo else 0
        ax.set_ylim(0, max_valor * 1.2)

        # título e legendas
        ax.set_title('Evolução financeira mensal')
        ax.set_xlabel('Mês')
        ax.set_ylabel('Valor (R$)')
        ax.grid(axis='y', linestyle=':', alpha=0.6)
        ax.legend()
        fig.tight_layout()

        # mostra o gráfico na tela
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {e}")