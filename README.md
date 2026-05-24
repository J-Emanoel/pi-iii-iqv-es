# 📊 Projeto Integrador III: IQV-ES
ENTREGA C2 : https://www.youtube.com/watch?v=JZOxNYqBbYU
# 📊 MVP: IQV-ES (Índice de Qualidade de Vida Municipal - Espírito Santo)

## 🎯 Sobre o Produto Final
O **IQV-ES** é uma ferramenta analítica desenvolvida para avaliar o impacto da execução orçamental da saúde pública nos índices de segurança dos 78 municípios capixabas. Este repositório contém a demonstração completa da solução, exigida como entrega C3 do Projeto Integrador III.

O MVP entrega uma métrica normalizada de 0 a 100 para o Estado e segmenta estrategicamente as cidades utilizando inteligência artificial, ajudando na identificação de gargalos de gestão pública.

## 🛠️ Tecnologias, Metodologia e Modelos (Ciência da Computação)
* **Engenharia de Dados (ETL):** Uso de Pandas em Python para padronização rigorosa de strings e integração entre bases heterogêneas do Governo e do IBGE.
* **Cálculo de Indicadores:** Padronização estatística através do processamento de gastos absolutos em gastos *per capita* e taxas proporcionais de criminalidade.
* **Normalização (MinMaxScaler):** Equalização das dimensões com a biblioteca `Scikit-Learn` para calcular e inverter corretamente as pontuações que geram o `Nota_IQV_ES` definitivo.
* **Machine Learning:** Aplicação do algoritmo **K-Means Clustering**. O modelo de aprendizado não supervisionado detectou padrões tridimensionais ocultos e agrupou automaticamente os municípios em três zonas de alerta orçamental/criminal.
🔗Link vizualização : https://visualizacaoproj.streamlit.app

🔗 **[ASSISTA AO VÍDEO DE APRESENTAÇÃO DO MVP AQUI]** *(Insira o link de vídeo do Youtube/Drive)*
