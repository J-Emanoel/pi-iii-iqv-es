import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geobr
import unicodedata
import json
from streamlit_option_menu import option_menu

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="IQV-ES | Painel Interativo",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM CSS — PREMIUM THEME
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* === RESET & BASE === */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* === REMOVE STREAMLIT PADDING TOP === */
    .block-container {
        padding-top: 1rem !important;
    }

    /* === HERO SECTION === */
    .hero-section {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 18px;
        padding: 40px 45px 30px 45px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(255, 107, 107, 0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(78, 205, 196, 0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFC371 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 6px;
        line-height: 1.1;
        position: relative;
        z-index: 1;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #8e99a4;
        font-weight: 400;
        max-width: 700px;
        line-height: 1.5;
        position: relative;
        z-index: 1;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255, 107, 107, 0.15);
        color: #FF6B6B;
        padding: 4px 14px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 107, 107, 0.2);
        position: relative;
        z-index: 1;
    }

    /* === KPI CARDS === */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }
    .kpi-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px 20px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        border-radius: 14px 14px 0 0;
    }
    .kpi-card:nth-child(1)::before { background: linear-gradient(90deg, #FF6B6B, #FF8E53); }
    .kpi-card:nth-child(2)::before { background: linear-gradient(90deg, #4ECDC4, #44CF6C); }
    .kpi-card:nth-child(3)::before { background: linear-gradient(90deg, #F7DC6F, #F0B27A); }
    .kpi-card:nth-child(4)::before { background: linear-gradient(90deg, #BB8FCE, #85C1E9); }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    .kpi-icon {
        font-size: 1.6rem;
        margin-bottom: 6px;
    }
    .kpi-label {
        font-size: 0.72rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #ecf0f1;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #636e72;
        margin-top: 4px;
        font-weight: 500;
    }

    /* === SECTION DIVIDER === */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 107, 107, 0.3), rgba(255, 142, 83, 0.3), transparent);
        margin: 10px 0 25px 0;
        border: none;
    }

    /* === METRIC CARD (for sidebar/panels) === */
    .metric-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 16px;
        text-align: center;
        margin-bottom: 12px;
        transition: all 0.25s ease;
    }
    .metric-card:hover {
        border-color: rgba(255, 107, 107, 0.3);
    }
    .metric-title {
        font-size: 0.7rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 4px;
    }

    /* === RANKING CARDS === */
    .ranking-item {
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        transition: all 0.25s ease;
        gap: 16px;
    }
    .ranking-item:hover {
        background: rgba(255, 255, 255, 0.06);
        transform: translateX(4px);
        border-color: rgba(255, 255, 255, 0.12);
    }
    .ranking-pos {
        min-width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .pos-gold { background: linear-gradient(135deg, #f9ca24, #f0932b); color: #1a1a2e; }
    .pos-silver { background: linear-gradient(135deg, #dfe6e9, #b2bec3); color: #1a1a2e; }
    .pos-bronze { background: linear-gradient(135deg, #e17055, #d63031); color: #fff; }
    .pos-normal { background: rgba(255, 255, 255, 0.08); color: #b2bec3; }
    .ranking-info {
        flex: 1;
        min-width: 0;
    }
    .ranking-name {
        font-weight: 700;
        color: #ecf0f1;
        font-size: 0.92rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .ranking-profile {
        font-size: 0.72rem;
        color: #7f8c8d;
        margin-top: 2px;
    }
    .ranking-score {
        font-weight: 800;
        font-size: 1.15rem;
        flex-shrink: 0;
        min-width: 60px;
        text-align: right;
    }
    .score-good { color: #00b894; }
    .score-bad { color: #e17055; }
    .ranking-bar-container {
        width: 100px;
        height: 6px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 3px;
        overflow: hidden;
        flex-shrink: 0;
    }
    .ranking-bar {
        height: 100%;
        border-radius: 3px;
        transition: width 0.5s ease;
    }
    .bar-good { background: linear-gradient(90deg, #00b894, #55efc4); }
    .bar-bad { background: linear-gradient(90deg, #e17055, #fab1a0); }

    /* === VERSUS CARD === */
    .vs-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px;
        margin-bottom: 25px;
        padding: 25px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .vs-city {
        text-align: center;
        flex: 1;
    }
    .vs-city-name {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ecf0f1;
    }
    .vs-city-score {
        font-size: 2.2rem;
        font-weight: 900;
        margin-top: 4px;
    }
    .vs-city-profile {
        font-size: 0.8rem;
        color: #7f8c8d;
        margin-top: 4px;
    }
    .vs-badge {
        font-size: 2rem;
        font-weight: 900;
        color: #636e72;
        background: rgba(255, 255, 255, 0.06);
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    .color-a { color: #00b8d4; }
    .color-b { color: #ff1744; }

    /* === COMPARISON TABLE === */
    .comp-row {
        display: flex;
        align-items: center;
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 6px;
        transition: background 0.2s ease;
    }
    .comp-row:hover {
        background: rgba(255, 255, 255, 0.04);
    }
    .comp-row:nth-child(even) {
        background: rgba(255, 255, 255, 0.02);
    }
    .comp-label {
        flex: 1;
        font-size: 0.85rem;
        color: #b2bec3;
        font-weight: 500;
    }
    .comp-val {
        min-width: 120px;
        text-align: center;
        font-weight: 700;
        font-size: 0.95rem;
        padding: 4px 12px;
        border-radius: 6px;
    }
    .comp-winner {
        background: rgba(0, 184, 148, 0.15);
        color: #55efc4;
    }
    .comp-loser {
        color: #636e72;
    }

    /* === SECTION TITLE === */
    .section-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ecf0f1;
        margin-bottom: 5px;
    }
    .section-desc {
        font-size: 0.9rem;
        color: #636e72;
        margin-bottom: 20px;
    }

    /* === OPTION MENU OVERRIDE === */
    .nav-link {
        font-weight: 600 !important;
    }
    .nav-link-selected {
        font-weight: 700 !important;
    }

    /* === SCROLLBAR DARK === */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def carregar_dados():
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, 'data', 'processed', 'IQV_ES_Final.csv')
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
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
# HERO SECTION
# ==========================================
melhor = df_iqv.loc[df_iqv['IQV_ES_Score'].idxmax()]
pior = df_iqv.loc[df_iqv['IQV_ES_Score'].idxmin()]
media_iqv = df_iqv['IQV_ES_Score'].mean()

st.markdown(f'''
<div class="hero-section">
    <div class="hero-badge">📊 PAINEL ANALÍTICO v2.0</div>
    <div class="hero-title">Índice de Qualidade de Vida</div>
    <div class="hero-title" style="font-size: 1.8rem; margin-top: -5px;">Espírito Santo — IQV-ES</div>
    <div class="hero-subtitle">
        Explore os indicadores de segurança, finanças e perfil sociodemográfico dos
        78 municípios capixabas. Cruze dados livremente e descubra padrões ocultos.
    </div>
</div>
''', unsafe_allow_html=True)

# KPI Cards
st.markdown(f'''
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon">📈</div>
        <div class="kpi-label">Score Médio IQV</div>
        <div class="kpi-value">{media_iqv:.1f}</div>
        <div class="kpi-sub">de 100 pontos possíveis</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🏆</div>
        <div class="kpi-label">Melhor Município</div>
        <div class="kpi-value" style="font-size: 1.2rem;">{melhor['NOME DO MUNICÍPIO']}</div>
        <div class="kpi-sub">Score {melhor['IQV_ES_Score']:.1f}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-label">Menor Score</div>
        <div class="kpi-value" style="font-size: 1.2rem;">{pior['NOME DO MUNICÍPIO']}</div>
        <div class="kpi-sub">Score {pior['IQV_ES_Score']:.1f}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🏙️</div>
        <div class="kpi-label">Municípios Analisados</div>
        <div class="kpi-value">{len(df_iqv)}</div>
        <div class="kpi-sub">Estado do Espírito Santo</div>
    </div>
</div>
''', unsafe_allow_html=True)

# ==========================================
# NAVIGATION MENU
# ==========================================
pagina = option_menu(
    menu_title=None,
    options=["Mapa Interativo", "Ranking Municipal", "Comparador", "Dados & Dispersão"],
    icons=["map-fill", "trophy-fill", "arrow-left-right", "bar-chart-line-fill"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "8px 12px",
            "background-color": "rgba(255,255,255,0.03)",
            "border-radius": "14px",
            "border": "1px solid rgba(255,255,255,0.06)",
            "margin-bottom": "20px",
        },
        "icon": {"color": "#FF8E53", "font-size": "16px"},
        "nav-link": {
            "font-size": "14px",
            "font-weight": "600",
            "color": "#7f8c8d",
            "border-radius": "10px",
            "padding": "10px 18px",
            "--hover-color": "rgba(255,255,255,0.05)",
        },
        "nav-link-selected": {
            "background": "linear-gradient(135deg, rgba(255,107,107,0.2), rgba(255,142,83,0.2))",
            "color": "#FF8E53",
            "font-weight": "700",
            "border": "1px solid rgba(255,142,83,0.25)",
        },
    },
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ==========================================
# PAGE 1: MAPA INTERATIVO
# ==========================================
if pagina == "Mapa Interativo":
    col_panel, col_map = st.columns([1.5, 8.5])

    with col_panel:
        st.markdown('<div class="section-title">🎛️ Controles</div>', unsafe_allow_html=True)

        selecao_metrica = st.selectbox(
            "Indicador:",
            list(opcoes_metricas.keys()),
            index=0
        )

        coluna_alvo, paleta, unidade = opcoes_metricas[selecao_metrica]

        # Filtro de população
        min_pop = int(df_iqv['POPULAÇÃO ESTIMADA'].min())
        max_pop = int(df_iqv['POPULAÇÃO ESTIMADA'].max())
        pop_filter = st.slider(
            "Pop. mínima:",
            min_value=min_pop,
            max_value=max_pop,
            value=min_pop,
            step=10000,
            format="%d"
        )

        # Stats da métrica selecionada
        media_val = df_iqv[coluna_alvo].mean()
        max_val = df_iqv[coluna_alvo].max()
        min_val = df_iqv[coluna_alvo].min()

        st.markdown(f'''
        <div class="metric-card" style="margin-top: 15px;">
            <div class="metric-title">Média do Estado</div>
            <div class="metric-value">{media_val:,.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Máximo</div>
            <div class="metric-value" style="color: #55efc4; font-size: 1.3rem;">{max_val:,.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Mínimo</div>
            <div class="metric-value" style="color: #e17055; font-size: 1.3rem;">{min_val:,.1f}</div>
        </div>
        ''', unsafe_allow_html=True)

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
            height=750,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            geo=dict(bgcolor='rgba(0,0,0,0)'),
            coloraxis_colorbar=dict(
                title=dict(text=unidade, font=dict(color='#b2bec3')),
                tickfont=dict(color='#b2bec3'),
                bgcolor='rgba(0,0,0,0)',
                outlinewidth=0,
                len=0.6,
            )
        )
        st.plotly_chart(fig_map, width='stretch')


# ==========================================
# PAGE 2: RANKING MUNICIPAL
# ==========================================
elif pagina == "Ranking Municipal":
    st.markdown('<div class="section-title">🏆 Ranking dos Municípios</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Veja os melhores e piores desempenhos por indicador selecionado.</div>', unsafe_allow_html=True)

    # Seletor de métrica para ranking
    opcoes_rank = {
        "Score IQV-ES": "IQV_ES_Score",
        "Taxa de Furtos (100k)": "taxa_furtos_100k",
        "Taxa de Roubos (100k)": "taxa_roubos_100k",
        "Taxa de Homicídios (100k)": "taxa_homicidios_100k",
        "Violência Doméstica (100k)": "taxa_violencia_100k",
        "Despesas Per Capita": "despesas_per_capita",
        "Receitas Per Capita": "receitas_per_capita",
    }

    col_sel, _ = st.columns([3, 7])
    with col_sel:
        rank_metrica_nome = st.selectbox("Ordenar por:", list(opcoes_rank.keys()))
    rank_col = opcoes_rank[rank_metrica_nome]

    # Para IQV-ES, maior = melhor. Para taxas de crime, menor = melhor.
    invertido = rank_col in ['taxa_furtos_100k', 'taxa_roubos_100k', 'taxa_homicidios_100k', 'taxa_violencia_100k']

    df_sorted_best = df_iqv.sort_values(rank_col, ascending=invertido).head(10).reset_index(drop=True)
    df_sorted_worst = df_iqv.sort_values(rank_col, ascending=not invertido).head(10).reset_index(drop=True)

    max_score = df_iqv[rank_col].max()

    col_best, col_worst = st.columns(2)

    with col_best:
        st.markdown('<div class="section-title" style="color: #55efc4;">🏅 Top 10 — Melhores</div>', unsafe_allow_html=True)
        for i, row in df_sorted_best.iterrows():
            pos = i + 1
            pos_class = "pos-gold" if pos == 1 else "pos-silver" if pos == 2 else "pos-bronze" if pos == 3 else "pos-normal"
            pct = (row[rank_col] / max_score * 100) if max_score > 0 else 0
            st.markdown(f'''
            <div class="ranking-item">
                <div class="ranking-pos {pos_class}">{pos}</div>
                <div class="ranking-info">
                    <div class="ranking-name">{row['NOME DO MUNICÍPIO']}</div>
                    <div class="ranking-profile">{row['Perfil_Municipio']}</div>
                </div>
                <div class="ranking-bar-container">
                    <div class="ranking-bar bar-good" style="width: {pct:.0f}%;"></div>
                </div>
                <div class="ranking-score score-good">{row[rank_col]:,.1f}</div>
            </div>
            ''', unsafe_allow_html=True)

    with col_worst:
        st.markdown('<div class="section-title" style="color: #e17055;">⚠️ Top 10 — Piores</div>', unsafe_allow_html=True)
        for i, row in df_sorted_worst.iterrows():
            pos = i + 1
            pos_class = "pos-gold" if pos == 1 else "pos-silver" if pos == 2 else "pos-bronze" if pos == 3 else "pos-normal"
            pct = (row[rank_col] / max_score * 100) if max_score > 0 else 0
            st.markdown(f'''
            <div class="ranking-item">
                <div class="ranking-pos {pos_class}">{pos}</div>
                <div class="ranking-info">
                    <div class="ranking-name">{row['NOME DO MUNICÍPIO']}</div>
                    <div class="ranking-profile">{row['Perfil_Municipio']}</div>
                </div>
                <div class="ranking-bar-container">
                    <div class="ranking-bar bar-bad" style="width: {pct:.0f}%;"></div>
                </div>
                <div class="ranking-score score-bad">{row[rank_col]:,.1f}</div>
            </div>
            ''', unsafe_allow_html=True)

    # Gráfico de barras horizontais com todos os municípios
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Visão Geral — Todos os Municípios</div>', unsafe_allow_html=True)

    df_bar = df_iqv.sort_values(rank_col, ascending=invertido).reset_index(drop=True)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=df_bar['NOME DO MUNICÍPIO'],
        x=df_bar[rank_col],
        orientation='h',
        marker=dict(
            color=df_bar[rank_col],
            colorscale='RdYlGn' if not invertido else 'RdYlGn_r',
            line=dict(width=0),
        ),
        hovertemplate='<b>%{y}</b><br>' + rank_metrica_nome + ': %{x:,.1f}<extra></extra>',
    ))
    fig_bar.update_layout(
        height=max(600, len(df_bar) * 22),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=20, t=10, b=10),
        xaxis=dict(
            title=dict(text=rank_metrica_nome, font=dict(color='#b2bec3')),
            gridcolor='rgba(255,255,255,0.05)',
            tickfont=dict(color='#7f8c8d'),
        ),
        yaxis=dict(
            autorange='reversed',
            tickfont=dict(color='#b2bec3', size=11),
        ),
        bargap=0.15,
    )
    st.plotly_chart(fig_bar, width='stretch')


# ==========================================
# PAGE 3: COMPARADOR DE CIDADES
# ==========================================
elif pagina == "Comparador":
    st.markdown('<div class="section-title">⚔️ Duelo Municipal</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Selecione dois municípios para comparar lado a lado todos os indicadores.</div>', unsafe_allow_html=True)

    lista_cidades = df_iqv['NOME DO MUNICÍPIO'].sort_values().tolist()

    colA, colB = st.columns(2)
    with colA:
        cidade_A = st.selectbox("Cidade A", lista_cidades, index=lista_cidades.index("Vitória") if "Vitória" in lista_cidades else 0)
    with colB:
        cidade_B = st.selectbox("Cidade B", lista_cidades, index=lista_cidades.index("Vila Velha") if "Vila Velha" in lista_cidades else 1)

    if cidade_A and cidade_B:
        dados_A = df_iqv[df_iqv['NOME DO MUNICÍPIO'] == cidade_A].iloc[0]
        dados_B = df_iqv[df_iqv['NOME DO MUNICÍPIO'] == cidade_B].iloc[0]

        # VS Header
        score_a_color = "color-a"
        score_b_color = "color-b"
        st.markdown(f'''
        <div class="vs-header">
            <div class="vs-city">
                <div class="vs-city-name">{cidade_A}</div>
                <div class="vs-city-score {score_a_color}">{dados_A['IQV_ES_Score']:.1f}</div>
                <div class="vs-city-profile">{dados_A['Perfil_Municipio']}</div>
            </div>
            <div class="vs-badge">VS</div>
            <div class="vs-city">
                <div class="vs-city-name">{cidade_B}</div>
                <div class="vs-city-score {score_b_color}">{dados_B['IQV_ES_Score']:.1f}</div>
                <div class="vs-city-profile">{dados_B['Perfil_Municipio']}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # Radar Chart
        cols_radar = ['taxa_furtos_100k', 'taxa_roubos_100k', 'taxa_violencia_100k', 'despesas_per_capita', 'receitas_per_capita']
        labels_radar_map = {
            'taxa_furtos_100k': 'Furtos',
            'taxa_roubos_100k': 'Roubos',
            'taxa_violencia_100k': 'Violência',
            'despesas_per_capita': 'Despesas',
            'receitas_per_capita': 'Receitas'
        }

        # Normalizando
        df_radar_norm = df_iqv.copy()
        for c in cols_radar:
            min_v = df_radar_norm[c].min()
            max_v = df_radar_norm[c].max()
            if max_v > min_v:
                df_radar_norm[c] = (df_radar_norm[c] - min_v) / (max_v - min_v)
            else:
                df_radar_norm[c] = 0.5

        dados_A_norm = df_radar_norm[df_radar_norm['NOME DO MUNICÍPIO'] == cidade_A].iloc[0]
        dados_B_norm = df_radar_norm[df_radar_norm['NOME DO MUNICÍPIO'] == cidade_B].iloc[0]

        labels_display = [labels_radar_map[c] for c in cols_radar] + [labels_radar_map[cols_radar[0]]]

        col_radar, col_table = st.columns([5, 5])

        with col_radar:
            fig_duel = go.Figure()
            fig_duel.add_trace(go.Scatterpolar(
                r=dados_A_norm[cols_radar].values.tolist() + [dados_A_norm[cols_radar].values.tolist()[0]],
                theta=labels_display,
                fill='toself',
                name=cidade_A,
                line=dict(color='#00b8d4', width=2.5),
                fillcolor='rgba(0, 184, 212, 0.15)',
            ))
            fig_duel.add_trace(go.Scatterpolar(
                r=dados_B_norm[cols_radar].values.tolist() + [dados_B_norm[cols_radar].values.tolist()[0]],
                theta=labels_display,
                fill='toself',
                name=cidade_B,
                line=dict(color='#ff1744', width=2.5),
                fillcolor='rgba(255, 23, 68, 0.15)',
            ))
            fig_duel.update_layout(
                polar=dict(
                    radialaxis=dict(visible=False, range=[0, 1]),
                    angularaxis=dict(
                        tickfont=dict(size=12, color='#b2bec3'),
                        gridcolor='rgba(255,255,255,0.06)',
                    ),
                    bgcolor='rgba(0,0,0,0)',
                ),
                showlegend=True,
                legend=dict(
                    font=dict(color='#b2bec3'),
                    bgcolor='rgba(0,0,0,0)',
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                template='plotly_dark',
                height=450,
                margin=dict(l=60, r=60, t=40, b=40),
            )
            st.plotly_chart(fig_duel, width='stretch')

        with col_table:
            st.markdown('<div class="section-title" style="font-size: 1.1rem; margin-bottom: 15px;">📋 Indicadores Detalhados</div>', unsafe_allow_html=True)

            # Indicadores para comparar (label, coluna, maior_é_melhor)
            indicadores = [
                ("Score IQV-ES", "IQV_ES_Score", True),
                ("Furtos (100k hab)", "taxa_furtos_100k", False),
                ("Roubos (100k hab)", "taxa_roubos_100k", False),
                ("Homicídios (100k hab)", "taxa_homicidios_100k", False),
                ("Violência Dom. (100k hab)", "taxa_violencia_100k", False),
                ("Despesas Per Capita", "despesas_per_capita", True),
                ("Receitas Per Capita", "receitas_per_capita", True),
                ("População", "POPULAÇÃO ESTIMADA", None),
            ]

            for label, col, maior_melhor in indicadores:
                val_a = dados_A[col]
                val_b = dados_B[col]

                if maior_melhor is not None:
                    if maior_melhor:
                        a_wins = val_a >= val_b
                    else:
                        a_wins = val_a <= val_b
                    class_a = "comp-winner" if a_wins else "comp-loser"
                    class_b = "comp-winner" if not a_wins else "comp-loser"
                else:
                    class_a = "comp-loser"
                    class_b = "comp-loser"

                if col == 'POPULAÇÃO ESTIMADA':
                    fmt_a = f"{val_a:,.0f}"
                    fmt_b = f"{val_b:,.0f}"
                else:
                    fmt_a = f"{val_a:,.1f}"
                    fmt_b = f"{val_b:,.1f}"

                st.markdown(f'''
                <div class="comp-row">
                    <div class="comp-val {class_a}">{fmt_a}</div>
                    <div class="comp-label" style="text-align: center;">{label}</div>
                    <div class="comp-val {class_b}">{fmt_b}</div>
                </div>
                ''', unsafe_allow_html=True)


# ==========================================
# PAGE 4: DADOS & DISPERSÃO
# ==========================================
elif pagina == "Dados & Dispersão":
    st.markdown('<div class="section-title">🔬 Dispersão dos Perfis (Clusters)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Cada bolha representa um município. O tamanho reflete a população estimada.</div>', unsafe_allow_html=True)

    # Cores customizadas por perfil
    cores_perfil = {
        'Alta Eficiência': '#00b894',
        'Alerta/Atenção': '#fdcb6e',
        'Diferenciado/Complexo': '#6c5ce7',
        'Risco Social': '#e17055',
    }

    fig_scatter = px.scatter(
        df_iqv,
        x='despesas_per_capita',
        y='IQV_ES_Score',
        color='Perfil_Municipio',
        hover_name='NOME DO MUNICÍPIO',
        size='POPULAÇÃO ESTIMADA',
        color_discrete_map=cores_perfil,
        labels={
            'despesas_per_capita': 'Despesas Públicas Per Capita (R$)',
            'IQV_ES_Score': 'Pontuação IQV-ES',
            'Perfil_Municipio': 'Perfil',
        },
        template='plotly_dark',
        height=550,
    )
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title=dict(font=dict(color='#b2bec3')), tickfont=dict(color='#7f8c8d')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title=dict(font=dict(color='#b2bec3')), tickfont=dict(color='#7f8c8d')),
        legend=dict(
            font=dict(color='#b2bec3', size=12),
            bgcolor='rgba(0,0,0,0)',
            title=dict(text='Perfil', font=dict(color='#ecf0f1')),
        ),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    fig_scatter.update_traces(
        marker=dict(line=dict(width=1, color='rgba(255,255,255,0.15)')),
        opacity=0.85,
    )
    st.plotly_chart(fig_scatter, width='stretch')

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📄 Tabela Consolidada</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Dados brutos de todos os 78 municípios. Clique nas colunas para ordenar.</div>', unsafe_allow_html=True)

    colunas_tabela = [
        'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA', 'IQV_ES_Score', 'Perfil_Municipio',
        'taxa_furtos_100k', 'taxa_roubos_100k', 'taxa_homicidios_100k', 'taxa_violencia_100k',
        'despesas_per_capita', 'receitas_per_capita'
    ]
    df_tabela = df_iqv[colunas_tabela].sort_values('IQV_ES_Score', ascending=False).reset_index(drop=True)
    df_tabela.index += 1

    st.dataframe(
        df_tabela,
        width='stretch',
        height=500,
        column_config={
            "NOME DO MUNICÍPIO": st.column_config.TextColumn("Município", width="medium"),
            "POPULAÇÃO ESTIMADA": st.column_config.NumberColumn("População", format="%d"),
            "IQV_ES_Score": st.column_config.ProgressColumn("Score IQV-ES", min_value=0, max_value=100, format="%.1f"),
            "Perfil_Municipio": st.column_config.TextColumn("Perfil", width="medium"),
            "taxa_furtos_100k": st.column_config.NumberColumn("Furtos/100k", format="%.1f"),
            "taxa_roubos_100k": st.column_config.NumberColumn("Roubos/100k", format="%.1f"),
            "taxa_homicidios_100k": st.column_config.NumberColumn("Homicídios/100k", format="%.1f"),
            "taxa_violencia_100k": st.column_config.NumberColumn("Violência/100k", format="%.1f"),
            "despesas_per_capita": st.column_config.NumberColumn("Despesas PC", format="R$ %.0f"),
            "receitas_per_capita": st.column_config.NumberColumn("Receitas PC", format="R$ %.0f"),
        }
    )

    # Botão de download
    st.markdown("<br>", unsafe_allow_html=True)
    csv = df_tabela.to_csv(index=False, sep=';', encoding='utf-8').encode('utf-8')
    st.download_button(
        label="📥 Baixar Tabela de Dados (CSV)",
        data=csv,
        file_name='iqv_es_consolidado.csv',
        mime='text/csv',
    )
