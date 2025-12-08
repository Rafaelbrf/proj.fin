import hashlib  # lib pra gerar hash da senha
#SHA256 como eu posso fala é um algoritmo que transforma a senha em um código seguro 
#Entendeu?

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()  # retorna senha criptografada

# checa se o gmail e a senha estão certos
def login_usuario_arquivo(nome_arquivo, gmail, senha):
    senha_hash = hash_senha(senha)  # criptografa a senha digitada

    try:
        # abre o arquivo de usuários
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo.readlines()[1:]:  # pula o cabeçalho
                partes = linha.strip().split(',')  # separa por vírgula

                if len(partes) >= 4:  # precisa ter id, nome, gmail, senha
                    gmail_arquivo = partes[2]  # terceiro campo é gmail
                    senha_arquivo = partes[3]  # quarto campo é senha hash

                    # compara gmail e senha hash com o que tá no arquivo
                    if gmail == gmail_arquivo and senha_arquivo == senha_hash:
                        print("login ok!")  # msg no terminal
                        return True  # login deu certo

    except FileNotFoundError:  # se não achar o arquivo
        print("arquivo de usuários não encontrado.")  # msg de erro

    return False  # se não bater, login falhou