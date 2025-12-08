import os       # Biblioteca nativa do Python para manipular arquivos
import hashlib  # Biblioteca nativa do Python para gerar hash (criptografia) da senha

# SHA-256 é um algoritmo que transforma a senha em um código fixo e seguro
# Esse código (hash) não pode ser revertido, protegendo a senha original
# Mesmo que alguém veja o hash, não consegue descobrir a senha real

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

# Função que cria uma nova conta e salva no arquivo CSV
def criar_conta(nome_arquivo: str, nome_conta: str, gmail: str, senha: str) -> bool:
    # Validação da senha
    if len(senha) < 6:
        print("Erro: A senha deve ter pelo menos 6 caracteres.")
        return False
    if not any(c in "#$_-" for c in senha):
        print("Erro: A senha deve conter pelo menos um dos símbolos #, $, _, -.")
        return False

    # Garante que o arquivo existe com cabeçalho
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("id,nome,gmail,senha\n")

    # Verifica se o Gmail já está cadastrado
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo.readlines()[1:]:
            partes = linha.strip().split(',')
            if len(partes) >= 4 and partes[2] == gmail:
                print("Erro: Gmail já cadastrado.")
                return False

    # Gera ID automático ignorando linhas vazias no arquivo
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        # Lê todas as linhas (exceto o cabeçalho) e remove espaços e quebras de linha
        linhas = [linha.strip() for linha in arquivo.readlines()[1:] if linha.strip()]

        # Se houver linhas válidas, pega o último ID e incrementa
        if linhas:
            # Divide a última linha por vírgula e converte o primeiro campo (ID) para inteiro
            ultimo_id = int(linhas[-1].split(',')[0])
            novo_id = ultimo_id + 1  # Incrementa o ID

        # Se não houver nenhuma linha válida, começa com ID 1
        else:
            novo_id = 1

    # Criptografa a senha antes de salvar
    senha_hash = hash_senha(senha)

    # Salva novo usuário
    with open(nome_arquivo, 'a', encoding='utf-8') as arquivo:
        arquivo.write(f"{novo_id},{nome_conta},{gmail},{senha_hash}\n")

    print(f"Conta criada com sucesso! ID: {novo_id}")
    return True