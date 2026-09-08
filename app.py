
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Custo de Vida Brasil — Margem no Varejo", layout="wide")

@st.cache_data
def carregar_margem():
    return pd.read_parquet("data/analytics/margem_mensal_com_ruido.parquet")

@st.cache_data
def carregar_hipoteses():
    return pd.read_parquet("data/analytics/resumo_hipoteses.parquet")

@st.cache_data
def carregar_produtos():
    return pd.read_parquet("data/analytics/comparativo_produtos.parquet")

st.sidebar.title("📊 Navegação")
tela = st.sidebar.radio(
    "Escolha a análise:",
    ["Margem vs. Ruído", "Resumo das Hipóteses", "Comparativo de Produtos"]
)

st.title("Custo de Vida Brasil — Case de Margem no Varejo")

# --- Bloco fixo: Conclusões / Recomendações de Negócio ---
with st.container():
    st.markdown("### 💡 Conclusões / Recomendações de Negócio")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Achado central**")
        st.write("A margem nunca caiu de fato. A oscilação real (~0.4pp) fica bem dentro do ruído natural do negócio (~1.27pp) — não há queda estrutural de margem.")
    with col2:
        st.markdown("**Causa da percepção**")
        st.write("O alarme surgiu ao analisar abril isoladamente (mês mais baixo do ano) sem comparar com a variação normal esperada.")
    with col3:
        st.markdown("**Recomendação**")
        st.write("Adotar 1.27pp como benchmark oficial de ruído, evitando alarmes falsos em análises futuras de margem.")
st.divider()

if tela == "Margem vs. Ruído":
    df = carregar_margem()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["mes_referencia"], y=df["margem_pct"],
                              mode="lines+markers", name="Margem mensal"))
    fig.add_trace(go.Scatter(x=df["mes_referencia"], y=df["limite_superior_pct"],
                              mode="lines", line=dict(dash="dash", color="gray"),
                              name="Limite superior (ruído)"))
    fig.add_trace(go.Scatter(x=df["mes_referencia"], y=df["limite_inferior_pct"],
                              mode="lines", line=dict(dash="dash", color="gray"),
                              name="Limite inferior (ruído)", fill="tonexty"))

    fig.update_layout(title="Margem mensal vs. faixa de ruído natural (±1.27pp)",
                       xaxis_title="Mês", yaxis_title="Margem (%)")
    st.plotly_chart(fig, use_container_width=True)

elif tela == "Resumo das Hipóteses":
    df_hip = carregar_hipoteses()

    st.subheader("Resumo do Processo de Investigação — 9 Hipóteses Testadas")

    def cor_status(status):
        refutada = "Refutada" in status
        nao_testavel = "Não-testável" in status
        if refutada and nao_testavel:
            return "background-color: #4a2f1f; color: white"
        elif refutada:
            return "background-color: #4a1f1f; color: white"
        elif nao_testavel:
            return "background-color: #4a3d1f; color: white"
        else:
            return ""

    styled_df = df_hip.style.map(cor_status, subset=["status"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    total = len(df_hip)
    refutadas = df_hip["status"].str.contains("Refutada").sum()
    nao_testaveis = df_hip["status"].str.contains("Não-testável").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de hipóteses", total)
    col2.metric("Refutadas", refutadas)
    col3.metric("Não-testáveis", nao_testaveis)

elif tela == "Comparativo de Produtos":
    df_prod = carregar_produtos()

    st.subheader("Comparativo de Produtos — Variação Máxima Mês a Mês")

    categorias = ["Todas"] + sorted(df_prod["categoria_id"].unique().tolist())
    categoria_selecionada = st.selectbox("Filtrar por categoria:", categorias)

    if categoria_selecionada != "Todas":
        df_filtrado = df_prod[df_prod["categoria_id"] == categoria_selecionada]
    else:
        df_filtrado = df_prod

    df_ordenado = df_filtrado.sort_values("variacao_maxima_pp", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_ordenado["variacao_maxima_pp"],
        y=df_ordenado["nome_produto"],
        orientation="h",
        marker_color="#4a90d9"
    ))
    fig.add_vline(x=1.27, line_dash="dash", line_color="orange",
                  annotation_text="Benchmark de ruído (1.27pp)")

    fig.update_layout(
        title="Variação máxima mensal por produto (pp)",
        xaxis_title="Variação máxima (pp)",
        yaxis_title="",
        height=max(400, len(df_ordenado) * 25)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.dataframe(
        df_filtrado[["nome_produto", "categoria_id", "variacao_maxima_pp", "preco_base"]]
        .sort_values("variacao_maxima_pp", ascending=False),
        use_container_width=True,
        hide_index=True
    )
