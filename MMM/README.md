# Marketing Mix Modeling (MMM) — Simplificado (Portfólio)

Este repositório é um **case didático** de *Marketing Mix Modeling* usando **Python + Pandas + Statsmodels**.
Ele foi feito para portfólio: mostra desde **hipóteses**, **tratamento de dados**, **transformações (adstock + saturação)**,
até **modelagem**, **interpretação** e **recomendações de negócio**.

> Observação: o dataset foi **gerado sinteticamente** (para ser 100% reproduzível).  
> Mesmo assim, a estrutura e as técnicas são equivalentes às usadas em projetos reais de MMM.

## Perguntas que o case responde
- Quais canais de marketing mais contribuem para as vendas?
- Existe efeito carregado no tempo (adstock)?
- Há saturação (retorno marginal decrescente) em algum canal?
- Como traduzir coeficientes e contribuições em recomendações acionáveis?

## Stack
- Python
- Pandas / NumPy
- Statsmodels (OLS)
- Matplotlib (visualizações)

## Estrutura
```
marketing-mix-modeling-simplificado/
├─ data/
│  └─ raw/marketing_sales_weekly.csv
├─ notebooks/
│  └─ 01_mmm_simplificado.ipynb
├─ src/
│  └─ modelagem.py
├─ reports/
└─ requirements.txt
```

## Como rodar
1) Criar ambiente e instalar dependências:
```bash
pip install -r requirements.txt
```

2) Abrir o notebook:
```bash
jupyter notebook notebooks/01_mmm_simplificado.ipynb
```

## O que você vai encontrar no notebook
1. EDA (distribuições, correlações, tendências e sazonalidade)
2. Transformações de mídia:
   - **Adstock** (efeito carregado)
   - **Hill/Saturação** (retorno marginal decrescente)
3. Regressão (OLS) com controles (preço, promo)
4. Decomposição de contribuição por canal ao longo do tempo
5. Recomendações:
   - canais com maior contribuição
   - onde há saturação
   - ideias de realocação de orçamento

## Próximos passos (para evoluir o case)
- Ajustar automaticamente os parâmetros (decay/alpha/gamma) com busca em grade
- Validação temporal (train/test por período)
- Métricas (MAE/MAPE) e intervalos de confiança
- Otimização de orçamento com restrições
