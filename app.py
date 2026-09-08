
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Custo de Vida Brasil — Margem no Varejo", layout="wide")

@st.cache_data
def carregar_margem():
    return pd.read_parquet("data/analytics/margem_mensal_com_ruido.parquet")

st.sidebar.title("📊 Navegação")
tela = st.sidebar.radio(
    "Escolha a análise:",
    ["Margem vs. Ruído", "Resumo das Hipóteses", "Comparativo de Produtos"]
)

st.title("Custo de Vida Brasil — Case de Margem no Varejo")

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
    st.info("Em construção — próxima etapa.")

elif tela == "Comparativo de Produtos":
    st.info("Em construção — próxima etapa.")
