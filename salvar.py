import csv
import os
from datetime import datetime

# Função para salvar receitas ou despesas na linha 2 do CSV
def salvar_em_csv(usuario, tipo, descricao, valor):
    try:
        valor = round(float(valor), 2)
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        nova_linha = [data_hora, usuario.strip(), tipo.strip(), descricao.strip(), valor]
        nome_arquivo = f"{usuario}_dados.csv"

        if not os.path.exists(nome_arquivo):
            # cria o arquivo com cabeçalho e a nova linha
            with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["DataHora", "Usuario", "Tipo", "Descricao", "Valor"])
                writer.writerow(nova_linha)
        else:
            # lê todas as linhas existentes
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                linhas = list(csv.reader(f))

            # garante que o cabeçalho existe
            if not linhas or linhas[0] != ["DataHora", "Usuario", "Tipo", "Descricao", "Valor"]:
                linhas.insert(0, ["DataHora", "Usuario", "Tipo", "Descricao", "Valor"])

            # insere a nova linha na posição 1 (logo após o cabeçalho)
            linhas.insert(1, nova_linha)

            # regrava o arquivo inteiro
            with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(linhas)

    except Exception as e:
        print(f"Erro ao salvar no CSV: {e}")

# Função para remover uma linha específica do CSV
def remover_do_csv(usuario, tipo, descricao, valor):
    caminho = f"{usuario}_dados.csv"
    if not os.path.exists(caminho):
        return

    linhas_novas = []
    encontrado = False

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for linha in reader:
                if len(linha) < 5:
                    linhas_novas.append(linha)
                    continue
                data, user, tipo_linha, desc, val = linha[:5]
                try:
                    val_float = round(float(val), 2)
                except ValueError:
                    linhas_novas.append(linha)
                    continue

                if (
                    user.strip().lower() == usuario.strip().lower()
                    and tipo_linha.strip().lower().startswith(tipo.strip().lower())
                    and desc.strip() == descricao.strip()
                    and val_float == round(float(valor), 2)
                    and not encontrado
                ):
                    encontrado = True  # remove apenas a primeira ocorrência
                    continue
                linhas_novas.append(linha)

        with open(caminho, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(linhas_novas)

    except Exception as e:
        print(f"Erro ao remover do CSV: {e}")