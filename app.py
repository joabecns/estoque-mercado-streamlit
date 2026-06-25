import streamlit as st
import pandas as pd
import estoque as est

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Supermercado do Seu Zé",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS customizado ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fonte e cores gerais */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Header da sidebar */
    .sidebar-header {
        background: linear-gradient(135deg, #1a472a, #2d6a4f);
        color: white;
        padding: 1.2rem 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sidebar-header h2 { margin: 0; font-size: 1.1rem; font-weight: 700; }
    .sidebar-header p  { margin: 0.2rem 0 0; font-size: 0.78rem; opacity: 0.8; }

    /* Título principal */
    .main-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a472a;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Cards de métricas de alerta */
    .alert-card {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-left: 4px solid #f97316;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
    }
    .alert-card .prod-nome { font-weight: 600; color: #9a3412; }
    .alert-card .prod-qtd  { font-size: 0.85rem; color: #c2410c; }

    /* Separador da sidebar */
    hr { border-top: 1px solid #e5e7eb; margin: 0.8rem 0; }

    /* Botão primário verde */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #2d6a4f;
        border: none;
        color: white;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #1a472a;
    }

    /* Botão de perigo */
    .danger-btn > button {
        background-color: #dc2626 !important;
        color: white !important;
        border: none !important;
    }
    .danger-btn > button:hover {
        background-color: #b91c1c !important;
    }

    /* Tabela limpa */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Estado da sessão ───────────────────────────────────────────────────────────
if "estoque" not in st.session_state:
    st.session_state.estoque = est.carregar_estoque()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>🛒 Supermercado do Seu Zé</h2>
        <p>Painel do Administrador</p>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        ["📊 Visualizar Estoque", "➕ Adicionar / Atualizar", "❌ Remover Produto"],
        label_visibility="collapsed",
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Mini-painel de alertas na sidebar
    alertas = est.produtos_estoque_baixo(st.session_state.estoque)
    if alertas:
        st.markdown(f"**⚠️ Estoque baixo — {len(alertas)} produto(s)**")
        for a in alertas:
            st.markdown(
                f"<div class='alert-card'>"
                f"<span class='prod-nome'>{a['nome']}</span><br>"
                f"<span class='prod-qtd'>Restam apenas {a['quantidade']} unid.</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        st.success("✅ Todos os produtos estão abastecidos.")


# ── Helpers ────────────────────────────────────────────────────────────────────
def estoque_como_dataframe(estoque: dict) -> pd.DataFrame:
    rows = [
        {
            "ID": id_p,
            "Produto": dados["nome"].title(),
            "Preço (R$)": f"{dados['preco']:.2f}",
            "Quantidade": dados["quantidade"],
            "Status": "⚠️ Baixo" if dados["quantidade"] < est.LIMITE_ESTOQUE_BAIXO else "✅ OK",
        }
        for id_p, dados in sorted(estoque.items(), key=lambda x: int(x[0]))
    ]
    return pd.DataFrame(rows)


# ── Página 1 — Visualizar Estoque ─────────────────────────────────────────────
if pagina == "📊 Visualizar Estoque":
    st.markdown("<div class='main-title'>📊 Estoque Completo</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='main-subtitle'>{len(st.session_state.estoque)} produto(s) cadastrado(s)</div>",
        unsafe_allow_html=True,
    )

    # Bloco de alertas de estoque baixo
    alertas = est.produtos_estoque_baixo(st.session_state.estoque)
    if alertas:
        with st.expander(f"⚠️ {len(alertas)} produto(s) com estoque abaixo de {est.LIMITE_ESTOQUE_BAIXO} unidades — clique para ver", expanded=True):
            cols = st.columns(min(len(alertas), 4))
            for i, a in enumerate(alertas):
                with cols[i % 4]:
                    st.metric(
                        label=a["nome"],
                        value=f"{a['quantidade']} unid.",
                        delta=f"{a['quantidade'] - est.LIMITE_ESTOQUE_BAIXO} do limite",
                        delta_color="inverse",
                    )

    # Tabela principal
    df = estoque_como_dataframe(st.session_state.estoque)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.TextColumn("ID", width=60),
            "Produto": st.column_config.TextColumn("Produto", width=180),
            "Preço (R$)": st.column_config.TextColumn("Preço (R$)", width=110),
            "Quantidade": st.column_config.NumberColumn("Quantidade", width=110),
            "Status": st.column_config.TextColumn("Status", width=90),
        },
    )

    # Métricas rápidas
    st.markdown("---")
    total_itens = sum(d["quantidade"] for d in st.session_state.estoque.values())
    valor_total = sum(d["preco"] * d["quantidade"] for d in st.session_state.estoque.values())
    c1, c2, c3 = st.columns(3)
    c1.metric("Produtos cadastrados", len(st.session_state.estoque))
    c2.metric("Total de unidades", f"{total_itens:,}")
    c3.metric("Valor em estoque", f"R$ {valor_total:,.2f}")


# ── Página 2 — Adicionar / Atualizar ──────────────────────────────────────────
elif pagina == "➕ Adicionar / Atualizar":
    st.markdown("<div class='main-title'>➕ Adicionar / Atualizar Produto</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>Selecione um produto existente para atualizar ou escolha \"Novo produto\" para cadastrar.</div>", unsafe_allow_html=True)

    # Selectbox com produtos existentes + opção novo
    opcoes_existentes = {
        f"{dados['nome'].title()} (ID: {id_p})": id_p
        for id_p, dados in sorted(st.session_state.estoque.items(), key=lambda x: int(x[0]))
    }
    opcoes = ["[Novo produto]"] + list(opcoes_existentes.keys())
    selecao = st.selectbox("Produto", opcoes, help="Selecione um produto existente para pré-preencher os campos.")

    # Pré-preenche campos se produto existente selecionado
    if selecao == "[Novo produto]":
        nome_padrao, preco_padrao, qtd_padrao = "", 0.01, 1
    else:
        id_sel = opcoes_existentes[selecao]
        dados_sel = st.session_state.estoque[id_sel]
        nome_padrao = dados_sel["nome"].title()
        preco_padrao = dados_sel["preco"]
        qtd_padrao = dados_sel["quantidade"]

    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        nome_input = st.text_input(
            "Nome do produto",
            value=nome_padrao,
            placeholder="Ex: arroz, feijão, leite...",
        )
    with col2:
        preco_input = st.number_input(
            "Preço (R$)",
            min_value=0.01,
            value=float(preco_padrao),
            step=0.10,
            format="%.2f",
        )

    qtd_input = st.number_input(
        "Quantidade em estoque",
        min_value=1,
        value=int(qtd_padrao),
        step=1,
    )

    st.markdown("")
    if st.button("💾 Salvar produto", type="primary", use_container_width=True):
        if not nome_input.strip():
            st.error("O nome do produto não pode estar vazio.")
        else:
            novo_estoque, status, msg = est.adicionar_item(
                st.session_state.estoque,
                nome_input,
                preco_input,
                qtd_input,
            )
            st.session_state.estoque = novo_estoque
            if status == "adicionado":
                st.success(f"✅ {msg}")
            else:
                st.info(f"🔄 {msg}")
            st.rerun()


# ── Página 3 — Remover Produto ────────────────────────────────────────────────
elif pagina == "❌ Remover Produto":
    st.markdown("<div class='main-title'>❌ Remover Produto</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>Selecione o produto que deseja excluir do estoque.</div>", unsafe_allow_html=True)

    if not st.session_state.estoque:
        st.warning("O estoque está vazio. Nenhum produto para remover.")
    else:
        opcoes_remocao = {
            f"[ID {id_p}] {dados['nome'].title()} — {dados['quantidade']} unid. | R$ {dados['preco']:.2f}": id_p
            for id_p, dados in sorted(st.session_state.estoque.items(), key=lambda x: int(x[0]))
        }

        selecao_rem = st.selectbox("Selecione o produto", list(opcoes_remocao.keys()))
        id_remover = opcoes_remocao[selecao_rem]
        dados_remover = st.session_state.estoque[id_remover]

        # Card de confirmação
        st.markdown("---")
        st.markdown("**Você está prestes a remover:**")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Produto", dados_remover["nome"].title())
        col_b.metric("Quantidade", dados_remover["quantidade"])
        col_c.metric("Preço", f"R$ {dados_remover['preco']:.2f}")

        confirmar = st.checkbox("✅ Confirmo que desejo remover este produto permanentemente.")

        st.markdown("")
        if st.button("🗑️ Remover produto", type="primary", disabled=not confirmar, use_container_width=True):
            novo_estoque, msg = est.remover_item(st.session_state.estoque, id_remover)
            st.session_state.estoque = novo_estoque
            st.success(f"✅ {msg}")
            st.rerun()

        if not confirmar:
            st.caption("Marque a caixa de confirmação para habilitar o botão de remoção.")
