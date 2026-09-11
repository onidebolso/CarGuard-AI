# CarGuard AI

## 1. Sobre o projeto

O CarGuard AI é um sistema de avaliação de risco para compra de veículos usados em leilão. A ideia é usar um modelo de Machine Learning para analisar dados reais do veículo e indicar se a compra parece uma boa oportunidade ou um risco elevado.

A aplicação foi construída seguindo a arquitetura end-to-end:

Dataset → preparação dos dados → treinamento do modelo → avaliação → modelo salvo → API → frontend.

---

## 2. Problema

Comprar um veículo usado em leilão envolve risco de:

- odômetro fraudado;
- histórico oculto de problemas;
- manutenção irregular;
- preço acima do valor de mercado;
- baixa liquidez após a compra.

O objetivo da solução é ajudar compradores e revendedores a decidir com base em dados históricos e em um score de risco.

---

## 3. Dataset

- Nome: Don't Get Kicked!
- Origem: Kaggle
- Registros: 72.983 no conjunto de treinamento
- Colunas: 34
- Tipo de problema: classificação binária
- Arquivo principal: `csv/training.csv`

O dataset contém informações de automóveis, incluindo marca, modelo, ano, preço, quilometragem, condições de aquisição e dados de mercado.

---

## 4. Variável alvo

A variável alvo é `IsBadBuy`.

Codificação confirmada no dataset real:

- `0` → Boa compra
- `1` → Má compra / compra de risco

---

## 5. Features utilizadas

As features foram escolhidas com base nas colunas realmente presentes no dataset e no comportamento do modelo:

- `VehYear`, `VehicleAge`, `VehOdo`
- `Make`, `Model`, `Transmission`, `WheelType`, `Color`, `Size`
- `Auction`, `VNST`, `Nationality`, `TopThreeAmericanName`
- `MMRAcquisitionAuctionAveragePrice`, `MMRAcquisitionAuctionCleanPrice`
- `MMRAcquisitionRetailAveragePrice`, `MMRAcquisitonRetailCleanPrice`
- `MMRCurrentAuctionAveragePrice`, `MMRCurrentAuctionCleanPrice`
- `MMRCurrentRetailAveragePrice`, `MMRCurrentRetailCleanPrice`
- `VehBCost`, `WarrantyCost`, `IsOnlineSale`
- `PRIMEUNIT`, `AUCGUART`

Esses atributos representam tanto a condição do veículo quanto o contexto da compra em leilão.

---

## 6. Público-alvo

A solução pode ser usada por:

- compradores de veículos usados;
- revendedores e concessionárias;
- avaliadores automotivos;
- empresas de leilão e mercado de usados;
- pessoas que desejam reduzir o risco de má compra.

---

## 7. Funcionamento da aplicação

```text
Usuário
  ↓
Frontend React
  ↓
FastAPI
  ↓
Modelo treinado
  ↓
Classificação
  ↓
Resposta ao usuário
```

Fluxo:

1. O usuário preenche os dados do veículo.
2. O frontend envia os dados para a API.
3. A API monta um registro compatível com o modelo.
4. O modelo retorna a probabilidade e a classificação.
5. A interface exibe o resultado final.

---

## 8. Tecnologias

- Python
- Pandas
- Scikit-learn
- Joblib
- FastAPI
- React
- Vite
- Git/GitHub

---

## 9. Estrutura do projeto

```text
CarGuard-AI/
├── app/
│   └── main.py
├── csv/
│   ├── training.csv
│   ├── test.csv
│   └── Carvana_Data_Dictionary.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
├── src/
│   └── train_model.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 10. Resultado do modelo

O modelo treinado com o dataset real obteve:

- Accuracy: 0.6407
- F1-score: 0.3024

Esse resultado é funcional como protótipo e mostra que o problema é relevante e pode ser melhorado com:

- tuning de hiperparâmetros;
- feature engineering;
- balanceamento das classes;
- modelos mais robustos como Random Forest, XGBoost ou LightGBM.

---

## 11. Como executar

### 1) Instalar dependências do backend

```bash
cd /workspaces/CarGuard-AI
python -m pip install -r requirements.txt
```

### 2) Treinar o modelo

```bash
cd /workspaces/CarGuard-AI
python src/train_model.py
```

### 3) Iniciar a API

```bash
cd /workspaces/CarGuard-AI
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4) Iniciar o frontend React

```bash
cd /workspaces/CarGuard-AI/frontend
npm install
npm run dev
```

Depois abra:

```text
http://localhost:5173
```

---

## 12. Observações finais

Este projeto foi refatorado para manter apenas aquilo que é realmente utilizado para execução do fluxo completo: treinamento do modelo, API REST, frontend React e documentação. O objetivo é entregar uma arquitetura limpa, legível e funcional, focada em demonstrar o pipeline end-to-end de um projeto de classificação em Machine Learning.
