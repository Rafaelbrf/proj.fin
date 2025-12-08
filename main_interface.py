import streamlit as st  # da interface web, é quem mostra tudo na tela
import sistema
import grafico

# eu coloquei st como apelido para biblioteca streamlit
# assim não preciso escrever streamlit toda hora só st

# formata valores em reais com vírgula decimal
def format_br(valor: float) -> str:
    # str aqui indica que a função retorna um texto (string)
    # serve pra deixar o número bonitinho no formato brasileiro de moeda
    # resumido para não ficar 10000,002
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# função principal da interface
def inicia(usuario):
    sistema_controle = sistema.sistema_de_controle_financeiro(usuario)  # cria o controle financeiro pro usuário
    st.title("Sistema de Controle Financeiro")  # título grandão na página

    # inicializa o estado do botão se ainda não existir
    if "mostrar_saldo" not in st.session_state:
        st.session_state.mostrar_saldo = False

    # botão de alternância (mostra/esconde saldo)
    if st.button(" 👀 Ver Saldo Atual"):
        st.session_state.mostrar_saldo = not st.session_state.mostrar_saldo

    # mostra ou esconde o saldo dependendo do estado
    if st.session_state.mostrar_saldo:
        saldo = sistema_controle.calcular_saldo()
        st.info(f"Saldo atual: {format_br(saldo)}")  
        
    # menu de opções
    menu = st.selectbox(
        "Escolha uma opção:",
        [
            "Adicionar Receita",
            "Adicionar Despesa",
            "Listar Receitas",
            "Listar Despesas",
            "Gráfico de receitas e despesas",
        ],
    )

    if menu == "Adicionar Receita":
        descricao = st.text_input("Descrição da receita")
        valor = st.number_input("Valor da receita (R$)", min_value=0.0, format="%.2f")
        if st.button("Adicionar Receita"):
            if descricao and valor > 0:
                sistema_controle.nova_receita(descricao, valor)
                st.success("Receita adicionada com sucesso!")  # mensagem verde de sucesso
            else:
                st.warning("Preencha a descrição e o valor corretamente.")  # alerta amarelo

    elif menu == "Adicionar Despesa":
        descricao = st.text_input("Descrição da despesa")
        valor = st.number_input("Valor da despesa (R$)", min_value=0.0, format="%.2f")
        if st.button("Adicionar Despesa"):
            if descricao and valor > 0:
                sistema_controle.nova_despesa(descricao, valor)
                st.success("Despesa adicionada com sucesso!")
            else:
                st.warning("Preencha a descrição e o valor corretamente.")

    elif menu == "Listar Receitas":
        receitas = sistema_controle.get_receitas()
        st.subheader("Receitas")
        if receitas:
            for i, item in enumerate(receitas):
                col1, col2, col3 = st.columns([3, 2, 1])  # divide em 3 colunas
                col1.write(f"**Descrição:** {item['descricao']}")
                col2.write(f"**Valor:** {format_br(float(item['valor']))}")
                if col3.button("✖", key=f"del_receita_{i}"):  # botão de excluir
                    sistema_controle.remover_receita(i)
                    st.success("Receita removida com sucesso!")
                    st.rerun()  # recarrega a página
        else:
            st.info("Nenhuma receita registrada.")

    elif menu == "Listar Despesas":
        despesas = sistema_controle.get_despesas()
        st.subheader("Despesas")
        if despesas:
            for i, item in enumerate(despesas):
                col1, col2, col3 = st.columns([3, 2, 1])
                col1.write(f"**Descrição:** {item['descricao']}")
                col2.write(f"**Valor:** {format_br(float(item['valor']))}")
                if col3.button("✖", key=f"del_despesa_{i}"):
                    sistema_controle.remover_despesa(i)
                    st.success("Despesa removida com sucesso!")
                    st.rerun()
        else:
            st.info("Nenhuma despesa registrada.")

    # opção: gráfico de receitas e despesas
    elif menu == "Gráfico de receitas e despesas":
        st.subheader("Gráfico de receitas e despesas")
        try:
            grafico.inicia(sistema_controle)  # chama função que desenha o gráfico

            # mostra resumo financeiro total
            receita_total, despesa_total, saldo_total = sistema_controle.saldo_totais()
            st.markdown("---")  # linha separadora
            st.subheader("Resumo financeiro total")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Receitas", format_br(receita_total))
            col2.metric("Total de Despesas", format_br(despesa_total))
            col3.metric("Saldo Acumulado", format_br(saldo_total))

        except Exception as e:
            st.error(f"Erro ao gerar gráfico: {e}")  # mensagem vermelha se der erro