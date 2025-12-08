import os   # pra checar se os arquivos existem e manipular
import csv  # pra ler e escrever dados em formato CSV (planilhinha simples)
from datetime import datetime  # pra registrar data e hora das receitas/despesas
from salvar import salvar_em_csv, remover_do_csv  # funções auxiliares pra salvar/remover dados no arquivo

class sistema_de_controle_financeiro:
    def __init__(X, usuario):
        X.__usuario = usuario      # guarda o nome do usuário
        X.__receita = []           # lista de receitas
        X.__despesas = []          # lista de despesas
        X.__saldo = 0.0            # saldo inicial
        X._carregar_historico()    

    def _carregar_historico(X):
        arquivos = [f"{X.__usuario}_dados.csv", "dados_usuario.csv"]
        for path in arquivos:# é so um nome para arquivo
            if not os.path.exists(path):  # se o arquivo não existe, pula
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) < 5:  # linha incompleta, ignora
                            continue
                        data_str, user_row, tipo, descricao, valor_str = row[:5]
                        if user_row.strip().lower() != X.__usuario.strip().lower():
                            continue  # só carrega dados do usuário atual
                        try:
                            valor = float(valor_str)
                        except ValueError:
                            continue  # se não for número, ignora
                        registro = {"descricao": descricao, "valor": valor, "data": data_str}
                        if tipo.lower().startswith("receit"):
                            X.__receita.append(registro)
                            X.__saldo += valor
                        elif tipo.lower().startswith("desp"):
                            X.__despesas.append(registro)
                            X.__saldo -= valor
            except Exception as e:
                print(f"Erro ao carregar {path}: {e}")

    def nova_receita(X, descricao, valor):
        if valor <= 0:
            raise ValueError("Valor da receita deve ser positivo.")
        data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        X.__receita.append({"descricao": descricao, "valor": valor, "data": data})
        X.__saldo += valor
        salvar_em_csv(X.__usuario, "Receita", descricao, round(valor, 2))

    def nova_despesa(X, descricao, valor):
        if valor <= 0:
            raise ValueError("Valor da despesa deve ser positivo.")
        data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        X.__despesas.append({"descricao": descricao, "valor": valor, "data": data})
        X.__saldo -= valor
        salvar_em_csv(X.__usuario, "Despesa", descricao, round(valor, 2))

    def calcular_saldo(X):
        return X.__saldo

    def listar_receitas(X):
        print("Lista de Receitas:")
        if X.__receita:
            for r in X.__receita:
                print(f"{r['descricao']}: R$ {r['valor']:.2f}")
        else:
            print("Nenhuma receita registrada.")

    def listar_despesas(X):
        print("Lista de Despesas:")
        if X.__despesas:
            for d in X.__despesas:
                print(f"{d['descricao']}: R$ {d['valor']:.2f}")
        else:
            print("Nenhuma despesa registrada.")

    def get_receitas(X):
        return X.__receita

    def get_despesas(X):
        return X.__despesas

    def remover_receita(X, indice):
        if 0 <= indice < len(X.__receita):
            item = X.__receita[indice]
            X.__saldo -= item["valor"]
            remover_do_csv(X.__usuario, "Receita", item["descricao"], item["valor"])
            del X.__receita[indice]

    def remover_despesa(X, indice):
        if 0 <= indice < len(X.__despesas):
            item = X.__despesas[indice]
            X.__saldo += item["valor"]
            remover_do_csv(X.__usuario, "Despesa", item["descricao"], item["valor"])
            del X.__despesas[indice]

    def saldo_totais(X):
        total_receita = sum(r["valor"] for r in X.__receita)
        total_despesa = sum(d["valor"] for d in X.__despesas)
        total_saldo = total_receita - total_despesa
        return total_receita, total_despesa, total_saldo