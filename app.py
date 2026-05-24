import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geobr
import unicodedata
import json

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="IQV-ES | Interativo", 
    page_icon="🗺️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .title-text {
        font-size: 2.8rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    .subtitle-text {
        font-size: 1.1rem;
        color: #b0bec5;
        margin-bottom: 20px;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #90a4ae;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def carregar_dados():
    df = pd.read_csv('data/processed/IQV_ES_Final.csv', sep=';', encoding='utf-8')
    df['IQV_ES_Score'] = df['IQV_ES_Score'].round(2)
    df['POPULAÇÃO ESTIMADA'] = df['POPULAÇÃO ESTIMADA'].astype(str).str.replace('.', '').astype(int)
    
    cluster_names = {
        0: 'Alta Eficiência',
        1: 'Alerta/Atenção',
        2: 'Diferenciado/Complexo',
        3: 'Risco Social'
    }
    if 'Cluster' in df.columns:
        df['Perfil_Municipio'] = df['Cluster'].map(cluster_names).fillna(df['Cluster'])
    return df

@st.cache_data
def carregar_mapa():
    es_muni = geobr.read_municipality(code_muni='ES', year=2020)
    def padronizar(nome):
        nome = str(nome).lower().strip()
        return ''.join(ch for ch in unicodedata.normalize('NFKD', nome) if not unicodedata.combining(ch))
    es_muni['municipio_chave'] = es_muni['name_muni'].apply(padronizar)
    map_json = json.loads(es_muni.geometry.to_json())
    return es_muni, map_json

with st.spinner("Carregando inteligência de dados..."):
    df_iqv = carregar_dados()
    es_map, map_json = carregar_mapa()
    map_data = es_map.merge(df_iqv, on='municipio_chave', how='left')

# Mapeamento de métricas para o seletor dinâmico
opcoes_metricas = {
    "Score IQV-ES (Qualidade Global)": ("IQV_ES_Score", "RdYlGn", "Score"),
    "Taxa de Furtos (por 100k hab)": ("taxa_furtos_100k", "Reds", "Taxa"),
    "Taxa de Roubos (por 100k hab)": ("taxa_roubos_100k", "Reds", "Taxa"),
    "Taxa de Homicídios (por 100k hab)": ("taxa_homicidios_100k", "Reds", "Taxa"),
    "Violência Doméstica (por 100k hab)": ("taxa_violencia_100k", "Reds", "Taxa"),
    "Despesas Públicas Per Capita (R$)": ("despesas_per_capita", "Blues", "R$"),
    "Receitas Arrecadadas Per Capita (R$)": ("receitas_per_capita", "Greens", "R$"),
    "População Estimada": ("POPULAÇÃO ESTIMADA", "Purples", "Habitantes")
}

# ==========================================
# HEADER
# ==========================================
st.markdown('<div class="title-text">Índice de Qualidade de Vida (IQV-ES)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Explore os indicadores capixabas selecionando as métricas e cruzando dados livremente.</div>', unsafe_allow_html=True)

# ==========================================
# MAIN CONTENT (TABS)
# ==========================================
tab_mapa, tab_duelo, tab_dados = st.tabs(["🗺️ Exploração Espacial", "⚔️ Comparador de Cidades", "📊 Dados e Dispersão"])

# ------------------------------------------
# TAB 1: EXPLORAÇÃO ESPACIAL (O MAPA DINÂMICO)
# ------------------------------------------
with tab_mapa:
    col_ctrl, col_map = st.columns([3, 7])
    
    with col_ctrl:
        st.markdown("### Controles do Mapa")
        st.write("Escolha qual indicador deseja visualizar geograficamente.")
        
        selecao_metrica = st.selectbox(
            "Métrica em Exibição:", 
            list(opcoes_metricas.keys()), 
            index=0
        )
        
        # Filtro de População extra para o mapa
        min_pop = int(df_iqv['POPULAÇÃO ESTIMADA'].min())
        max_pop = int(df_iqv['POPULAÇÃO ESTIMADA'].max())
        pop_filter = st.slider("Esconder cidades menores que (Habitantes):", min_value=min_pop, max_value=max_pop, value=min_pop, step=10000)
        
        # Info card sobre a métrica
        coluna_alvo, paleta, unidade = opcoes_metricas[selecao_metrica]
        media_estado = df_iqv[coluna_alvo].mean()
        
        st.markdown(f'''
        <div class="metric-card" style="margin-top: 20px;">
            <div class="metric-title">Média do Estado ({unidade})</div>
            <div class="metric-value">{media_estado:,.1f}</div>
        </div>''', unsafe_allow_html=True)
        
    with col_map:
        # Filtrando
        map_data_filtered = map_data.copy()
        map_data_filtered.loc[map_data_filtered['POPULAÇÃO ESTIMADA'] < pop_filter, coluna_alvo] = None
        
        fig_map = px.choropleth(
            map_data_filtered,
            geojson=map_json,
            locations=map_data_filtered.index,
            color=coluna_alvo,
            hover_name='name_muni',
            hover_data={
                coluna_alvo: ':.2f', 
                'Perfil_Municipio': True,
                'POPULAÇÃO ESTIMADA': True,
                'IQV_ES_Score': ':.1f'
            },
            color_continuous_scale=paleta,
            labels={coluna_alvo: unidade}
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(
            height=650,
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            geo=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_map, use_container_width=True)

# ------------------------------------------
# TAB 2: COMPARADOR DE CIDADES (DUELO)
# ------------------------------------------
with tab_duelo:
    st.markdown("### Duelo Municipal: Lado a Lado")
    st.write("Selecione dois municípios para comparar seus indicadores de segurança, finanças e o perfil no qual se encaixam.")
    
    lista_cidades = df_iqv['NOME DO MUNICÍPIO'].sort_values().tolist()
    
    colA, colB = st.columns(2)
    with colA:
        cidade_A = st.selectbox("Selecione a Cidade A", lista_cidades, index=lista_cidades.index("Vitória") if "Vitória" in lista_cidades else 0)
    with colB:
        cidade_B = st.selectbox("Selecione a Cidade B", lista_cidades, index=lista_cidades.index("Vila Velha") if "Vila Velha" in lista_cidades else 1)
        
    if cidade_A and cidade_B:
        dados_A = df_iqv[df_iqv['NOME DO MUNICÍPIO'] == cidade_A].iloc[0]
        dados_B = df_iqv[df_iqv['NOME DO MUNICÍPIO'] == cidade_B].iloc[0]
        
        # Exibindo os Scores Principais
        cA1, cA2, cA3 = colA.columns(3)
        cB1, cB2, cB3 = colB.columns(3)
        
        cA1.metric("Score IQV-ES", f"{dados_A['IQV_ES_Score']:.1f}")
        cA2.metric("Despesa Per Capita", f"R$ {dados_A['despesas_per_capita']:.0f}")
        cA3.metric("Perfil", dados_A['Perfil_Municipio'])
        
        cB1.metric("Score IQV-ES", f"{dados_B['IQV_ES_Score']:.1f}")
        cB2.metric("Despesa Per Capita", f"R$ {dados_B['despesas_per_capita']:.0f}")
        cB3.metric("Perfil", dados_B['Perfil_Municipio'])
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Gráfico Radar Comparativo
        cols_radar = ['taxa_furtos_100k', 'taxa_roubos_100k', 'taxa_violencia_100k', 'despesas_per_capita', 'receitas_per_capita']
        
        # Normalizando as colunas para o radar (min-max global)
        df_radar_norm = df_iqv.copy()
        for c in cols_radar:
            min_v = df_radar_norm[c].min()
            max_v = df_radar_norm[c].max()
            df_radar_norm[c] = (df_radar_norm[c] - min_v) / (max_v - min_v)
            
        dados_A_norm = df_radar_norm[df_radar_norm['NOME DO MUNICÍPIO'] == cidade_A].iloc[0]
        dados_B_norm = df_radar_norm[df_radar_norm['NOME DO MUNICÍPIO'] == cidade_B].iloc[0]
        
        labels_radar = ['Furtos', 'Roubos', 'Violência', 'Despesas', 'Receitas', 'Furtos']
        
        fig_duel = go.Figure()
        fig_duel.add_trace(go.Scatterpolar(
            r=dados_A_norm[cols_radar].values.tolist() + [dados_A_norm[cols_radar].values.tolist()[0]],
            theta=labels_radar,
            fill='toself',
            name=cidade_A,
            line_color='#00f2fe'
        ))
        fig_duel.add_trace(go.Scatterpolar(
            r=dados_B_norm[cols_radar].values.tolist() + [dados_B_norm[cols_radar].values.tolist()[0]],
            theta=labels_radar,
            fill='toself',
            name=cidade_B,
            line_color='#ff1744'
        ))
        fig_duel.update_layout(
            polar=dict(radialaxis=dict(visible=False, range=[0, 1])),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            template='plotly_dark',
            title=f"Comparação de Indicadores Normalizados (0 a 1)",
            height=500
        )
        st.plotly_chart(fig_duel, use_container_width=True)

# ------------------------------------------
# TAB 3: DADOS E DISPERSÃO
# ------------------------------------------
with tab_dados:
    st.markdown("### Dispersão dos Perfis (Clusters)")
    
    fig_scatter = px.scatter(
        df_iqv, 
        x='despesas_per_capita', 
        y='IQV_ES_Score', 
        color='Perfil_Municipio',
        hover_name='NOME DO MUNICÍPIO',
        size='POPULAÇÃO ESTIMADA',
        labels={
            'despesas_per_capita': 'Despesas Públicas Per Capita (R$)',
            'IQV_ES_Score': 'Pontuação IQV-ES'
        },
        template='plotly_dark',
        height=500
    )
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("### Tabela Bruta Consolidada")
    colunas_tabela = [
        'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA', 'IQV_ES_Score', 'Perfil_Municipio', 
        'taxa_furtos_100k', 'taxa_roubos_100k', 'taxa_homicidios_100k', 'taxa_violencia_100k', 
        'despesas_per_capita', 'receitas_per_capita'
    ]
    df_tabela = df_iqv[colunas_tabela].sort_values('IQV_ES_Score', ascending=False).reset_index(drop=True)
    df_tabela.index += 1
    st.dataframe(df_tabela, use_container_width=True)
