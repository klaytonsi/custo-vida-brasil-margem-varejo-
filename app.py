
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
    df_hip = carregar_hipoteses()

    st.subheader("Resumo do Processo de Investigação — 9 Hipóteses Testadas")

    def cor_status(status):
        if status == "Refutada":
            return "background-color: #4a1f1f; color: white"
        elif status == "Não-testável":
            return "background-color: #4a3d1f; color: white"
        else:
            return ""

    styled_df = df_hip.style.applymap(cor_status, subset=["status"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    total = len(df_hip)
    refutadas = (df_hip["status"] == "Refutada").sum()
    nao_testaveis = (df_hip["status"] == "Não-testável").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de hipóteses", total)
    col2.metric("Refutadas", refutadas)
    col3.metric("Não-testáveis", nao_testaveis)

elif tela == "Comparativo de Produtos":
    st.info("Em construção — próxima etapa.")
