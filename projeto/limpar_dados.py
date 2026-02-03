import pandas as pd
import unicodedata

# 1. Carregar o CSV
df = pd.read_csv('alimentos.csv', encoding='utf-8')
print(f"Total de linhas carregadas: {len(df)}")
print(f"Colunas originais: {list(df.columns)[:5]}...")  # Mostra as 5 primeiras

# 2. Função para normalizar nomes (sem acentos, minúsculas)
def normalizar_nome(texto):
    # Remove acentos
    texto = unicodedata.normalize('NFKD', str(texto))
    texto = texto.encode('ASCII', 'ignore').decode('ASCII')

    # Converte para minúsculas e substitui caracteres problemáticos
    texto = texto.lower()
    texto = texto.replace('..', '_')
    texto = texto.replace('...', '')
    texto = texto.replace('.', '_')
    texto = texto.replace(' ', '_')
    texto = texto.replace('__', '_')  # Remove underscores duplicados
    texto = texto.rstrip('_')  # Remove underscore final

    return texto

# 3. Renomear todas as colunas
novos_nomes = {}
for coluna in df.columns:
    novo_nome = normalizar_nome(coluna)
    novos_nomes[coluna] = novo_nome

df = df.rename(columns=novos_nomes)

print("\nColunas após normalização:")
for i, col in enumerate(df.columns[:10]):  # Mostra 10 primeiras
    print(f"  {i+1}. {col}")

# 4. Verificar tipos de dados
print("\nTipos de dados por coluna:")
print(df.dtypes.head(10))

# 5. Salvar em novo CSV
df.to_csv('alimentos_limpo.csv', index=False, encoding='utf-8')
print("\nArquivo salvo como: alimentos_limpo.csv")

# 6. Preparar para MongoDB
documentos = df.to_dict('records')

# Mostrar exemplo do primeiro documento
print("\nExemplo de documento para MongoDB (primeira linha):")
import json
print(json.dumps(documentos[0], indent=2, ensure_ascii=False))