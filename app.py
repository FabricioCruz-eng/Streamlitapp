import streamlit as st
import pandas as pd

st.set_page_config(page_title="🍂Gestão de Melhoria de Rede", layout="wide")
# Título customizado com emoji, cor e fonte menor
st.markdown('<h2 style="color:#E9775D; font-size:1.6rem; font-weight:600; margin-bottom: 1.2rem;"> ⚡Gestão de Melhoria de Rede</h2>', unsafe_allow_html=True)

# Upload do arquivo na sidebar
uploaded_file = st.sidebar.file_uploader("Faça upload do arquivo .xlsx", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success(f"Arquivo carregado com sucesso! {df.shape[0]} linhas, {df.shape[1]} colunas.")

        # Filtros na barra lateral
        st.sidebar.header("Filtros")
        # Ano
        anos = df['Ano'].dropna().unique().tolist() if 'Ano' in df.columns else []
        ano_sel = st.sidebar.selectbox("Selecione o ano", options=anos if anos else ["Todos"])
        # Operadora
        operadoras = df['Operadora'].dropna().unique().tolist() if 'Operadora' in df.columns else []
        operadora_sel = st.sidebar.selectbox("Operadora", options=operadoras if operadoras else ["Todas"])
        # Localidade
        localidades = ['AC','AM', 'AL', 'AP', 'BA','CE','ES','GO' ,'MA','MG','MS','MT','PA', 'PB', 'PE', 'PI', 'PR', 'RJ','RN', 'RO','RR', 'RS','SC','SE','SP', 'TO']
        localidade_sel = st.sidebar.selectbox("Selecione a localidade", options=localidades)

        # Filtro de busca
        search = st.text_input("Pesquisar termo (em qualquer coluna):")
        df_filtrado = df.copy()
        # Aplicar filtros
        if anos and ano_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Ano'] == ano_sel]
        if operadoras and operadora_sel != "Todas":
            df_filtrado = df_filtrado[df_filtrado['Operadora'] == operadora_sel]
        if 'Estado' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Estado'] == localidade_sel]
        # Filtro de texto
        if search:
            mask = df_filtrado.apply(lambda row: row.astype(str).str.contains(search, case=False, na=False).any(), axis=1)
            filtered_df = df_filtrado[mask]
            st.write(f"{filtered_df.shape[0]} resultados encontrados.")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(df_filtrado, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
else:
    st.info("Por favor, faça upload de um arquivo .xlsx para começar.")

# Rodapé e informações institucionais no estilo da imagem
st.markdown("""
<div style='margin-top:2.5em; margin-bottom:1.5em;'>
  <span style='font-size:1.05rem;'>Portal desenvolvido e mantido por <a href='mailto:fabricio.cruz@claro.com.br'>fabricio.cruz@claro.com.br</a></span>
</div>

<h2 style='margin-bottom:0.2em;'>Dados Utilizados</h2>
<p>Os arquivos utilizados na análise estão disponíveis em:</p>
<ol style='font-size:1.1rem; margin-left:1.2em;'>
  <li>🗃️ Repositório na pasta Equipes Teams- Eventos N3</li>
  <li>🔓 Arquivos</li>
</ol>

<hr style='margin-top:2.5em; margin-bottom:0.5em; border:0; border-top:1px solid #333;'>
<div style='background:#23232b; color:#fff; padding:0.7em 0; text-align:center; font-size:1rem; border-radius:4px;'>
Copyright © 2025 Todos os direitos reservados - Claro Brasil
</div>
""", unsafe_allow_html=True) 