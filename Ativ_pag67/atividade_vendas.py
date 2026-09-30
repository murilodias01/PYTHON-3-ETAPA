import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =========================================
# 1 - LEITURA DOS DADOS
# =========================================

dados = pd.read_csv("vendas.csv")

print("PRIMEIRAS LINHAS:")
print(dados.head())


# =========================================
# 2 - ORGANIZAÇÃO DOS DADOS
# =========================================

dados["data"] = pd.to_datetime(dados["data"])

dados["quantidade"] = pd.to_numeric(
    dados["quantidade"],
    errors="coerce"
)

dados["preco_unitario"] = pd.to_numeric(
    dados["preco_unitario"],
    errors="coerce"
)


# =========================================
# 3 - VERIFICANDO VALORES VAZIOS
# =========================================

print("\nVALORES VAZIOS:")
print(dados.isna().sum())


# =========================================
# 4 - PREENCHENDO VALORES VAZIOS
# =========================================

dados["quantidade"] = dados["quantidade"].fillna(
    dados["quantidade"].median()
)

dados["preco_unitario"] = dados["preco_unitario"].fillna(
    dados["preco_unitario"].median()
)


# =========================================
# 5 - CRIANDO FATURAMENTO
# =========================================

dados["total"] = (
    dados["quantidade"] *
    dados["preco_unitario"]
)

print("\nDADOS ATUALIZADOS:")
print(dados.head())


# =========================================
# 6 - INFORMAÇÕES GERAIS
# =========================================

print("\nINFORMAÇÕES DO DATASET:")
print(dados.info())

print("\nESTATÍSTICAS:")
print(dados.describe())


# =========================================
# 7 - FATURAMENTO DE CADA LOJA
# =========================================

por_loja = dados.groupby(
    "loja"
)["total"].sum()

print("\nFATURAMENTO POR LOJA:")
print(por_loja)


# =========================================
# 8 - LOJA COM MAIOR FATURAMENTO
# =========================================

loja_top = por_loja.idxmax()
valor_top = por_loja.max()

print("\nLOJA COM MAIOR FATURAMENTO:")
print(loja_top)
print(f"R$ {valor_top:.2f}")


# =========================================
# 9 - LOJA COM MENOR FATURAMENTO
# =========================================

loja_menor = por_loja.idxmin()
valor_menor = por_loja.min()

print("\nLOJA COM MENOR FATURAMENTO:")
print(loja_menor)
print(f"R$ {valor_menor:.2f}")


# =========================================
# 10 - PRODUTOS MAIS VENDIDOS
# =========================================

ranking_produtos = (
    dados.groupby("produto")["quantidade"]
    .sum()
    .sort_values(ascending=False)
)

print("\nPRODUTOS MAIS VENDIDOS:")
print(ranking_produtos.head(5))


# =========================================
# 11 - FATURAMENTO POR CATEGORIA
# =========================================

por_categoria = (
    dados.groupby("categoria")["total"]
    .sum()
    .sort_values(ascending=False)
)

print("\nFATURAMENTO POR CATEGORIA:")
print(por_categoria)


# =========================================
# 12 - FATURAMENTO MENSAL
# =========================================

dados["mes"] = dados["data"].dt.to_period("M")

mensal = (
    dados.groupby("mes")["total"]
    .sum()
)

print("\nFATURAMENTO MENSAL:")
print(mensal)


# =========================================
# 13 - MELHOR MÊS
# =========================================

melhor_mes = mensal.idxmax()
melhor_valor = mensal.max()

print("\nMELHOR MÊS:")
print(melhor_mes)
print(f"R$ {melhor_valor:.2f}")


# =========================================
# 14 - PIOR MÊS
# =========================================

pior_mes = mensal.idxmin()
pior_valor = mensal.min()

print("\nMENOR FATURAMENTO MENSAL:")
print(pior_mes)
print(f"R$ {pior_valor:.2f}")


# =========================================
# 15 - TICKET MÉDIO POR LOJA
# =========================================

ticket = (
    dados.groupby("loja")["total"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTICKET MÉDIO:")
print(ticket)


# =========================================
# 16 - CONFIGURAÇÃO DOS GRÁFICOS
# =========================================

sns.set_theme(style="whitegrid")


# =========================================
# 17 - GRÁFICO DE LOJAS
# =========================================

plt.figure(figsize=(9, 5))

sns.barplot(
    x=por_loja.index,
    y=por_loja.values
)

plt.title("Faturamento das Lojas")
plt.xlabel("Loja")
plt.ylabel("Faturamento (R$)")

plt.tight_layout()
plt.savefig("grafico_lojas.png")
plt.show()


# =========================================
# 18 - GRÁFICO MENSAL
# =========================================

plt.figure(figsize=(11, 5))

plt.plot(
    mensal.index.astype(str),
    mensal.values,
    marker="o"
)

plt.title("Faturamento ao Longo dos Meses")
plt.xlabel("Mês")
plt.ylabel("Faturamento (R$)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("grafico_mensal.png")
plt.show()


# =========================================
# 19 - GRÁFICO DOS PRODUTOS
# =========================================

top_produtos = ranking_produtos.head(5)

plt.figure(figsize=(9, 5))

plt.bar(
    top_produtos.index,
    top_produtos.values
)

plt.title("5 Produtos Mais Vendidos")
plt.xlabel("Produto")
plt.ylabel("Quantidade")

plt.xticks(rotation=25)

plt.tight_layout()
plt.savefig("produtos_vendidos.png")
plt.show()


# =========================================
# 20 - DISTRIBUIÇÃO POR CATEGORIA
# =========================================

plt.figure(figsize=(8, 8))

plt.pie(
    por_categoria.values,
    labels=por_categoria.index,
    autopct="%.1f%%"
)

plt.title("Participação das Categorias no Faturamento")

plt.tight_layout()
plt.savefig("categorias.png")
plt.show()


# =========================================
# 21 - RELAÇÃO ENTRE QUANTIDADE E TOTAL
# =========================================

plt.figure(figsize=(9, 5))

sns.scatterplot(
    data=dados,
    x="quantidade",
    y="total",
    hue="categoria"
)

plt.title("Quantidade Vendida x Faturamento")
plt.xlabel("Quantidade")
plt.ylabel("Faturamento (R$)")

plt.tight_layout()
plt.savefig("quantidade_x_faturamento.png")
plt.show()


# =========================================
# 22 - PREÇOS POR CATEGORIA
# =========================================

plt.figure(figsize=(9, 5))

sns.boxplot(
    data=dados,
    x="categoria",
    y="preco_unitario"
)

plt.title("Preços dos Produtos por Categoria")
plt.xlabel("Categoria")
plt.ylabel("Preço Unitário (R$)")

plt.xticks(rotation=20)

plt.tight_layout()
plt.savefig("precos_categorias.png")
plt.show()


# =========================================
# 23 - CORRELAÇÃO
# =========================================

numeros = dados[
    ["quantidade", "preco_unitario", "total"]
]

matriz = numeros.corr()

plt.figure(figsize=(7, 5))

sns.heatmap(
    matriz,
    annot=True,
    fmt=".2f"
)

plt.title("Correlação das Variáveis")

plt.tight_layout()
plt.savefig("correlacao.png")
plt.show()


# =========================================
# 24 - RESULTADO FINAL
# =========================================

print("\n==============================")
print("        RESULTADO FINAL")
print("==============================")

print(
    f"Faturamento total: "
    f"R$ {dados['total'].sum():.2f}"
)

print(
    f"Melhor loja: {loja_top}"
)

print(
    f"Melhor mês: {melhor_mes}"
)

print(
    f"Produto mais vendido: "
    f"{ranking_produtos.index[0]}"
)

print(
    f"Categoria com maior faturamento: "
    f"{por_categoria.index[0]}"
)

print("\nAtividade concluída!")