# Microserviço de Processamento de Datasets com Código Customizado

## Visão Geral

Este projeto implementa um microserviço para permitir que usuários processem datasets armazenados no MinIO através de scripts Python customizados. Os usuários podem enviar uma função Python que será executada em um ambiente sandbox seguro, com acesso a bibliotecas específicas para manipulação de dados. O resultado do processamento é salvo como arquivo Parquet no MinIO, e o caminho do arquivo resultante é retornado ao usuário.

## Objetivo

Permitir aos usuários aplicar transformações personalizadas em datasets utilizando código Python, mantendo controle sobre a execução e garantindo a segurança da plataforma.

## Arquitetura

O sistema foi projetado para ser executado em um cluster Kubernetes e utiliza diversas tecnologias modernas para garantir segurança, eficiência e escalabilidade.

### Componentes Principais

1. **FastAPI Service**
   - Fornece endpoints RESTful para receber requisições
   - Gerencia o fluxo de processamento
   - Implementa validação de inputs via Pydantic

2. **Code Validator**
   - Utiliza o módulo `ast` do Python para análise estática de código
   - Verifica importações não permitidas
   - Detecta operações potencialmente perigosas (chamadas de sistema, acesso a arquivos, etc.)
   - Garante a presença da função `process` no código

3. **MinIO Client**
   - Interface para buscar datasets do MinIO
   - Converte dados brutos para DataFrames pandas
   - Salva resultados em formato Parquet

4. **Sandbox Manager**
   - Gerencia a criação e execução dos ambientes isolados
   - Aplica limites de recursos (CPU, memória)
   - Monitora tempo de execução

5. **Code Executor**
   - Executa o código Python em ambiente controlado
   - Carrega as bibliotecas permitidas
   - Valida entradas e saídas (DataFrames)

### Fluxo de Processamento

1. Usuário envia requisição POST com:
   - Caminho do dataset no MinIO (`dataset_path`)
   - Código Python contendo uma função `process(df) -> df`
   - Parâmetros opcionais (timeout, recursos)

2. O sistema valida estaticamente o código do usuário
3. O dataset é carregado do MinIO como DataFrame pandas
4. O código é executado em ambiente sandbox com recursos limitados
5. O DataFrame resultante é salvo como Parquet no MinIO
6. A API retorna o caminho do arquivo Parquet gerado

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework Python para desenvolvimento de APIs RESTful
- **Pandas**: Manipulação de dados estruturados
- **NumPy**: Computação numérica
- **AST**: Módulo Python para análise sintática de código
- **MinIO SDK**: Cliente Python para interação com o MinIO
- **Pydantic**: Validação de dados e configuração
- **Docker**: Containers para isolamento

### Infraestrutura
- **Kubernetes**: Orquestração de containers
- **MinIO**: Armazenamento de objetos compatível com S3
- **Resource Limits**: Controle de recursos via Kubernetes

### Bibliotecas Disponíveis para Usuários
- **Pandas**: Para manipulação de DataFrames
- **NumPy**: Para operações numéricas eficientes
- **Catch22**: Para extração de características de séries temporais

## Implementação

### Componente de Validação de Código

O componente de validação de código usa AST (Abstract Syntax Tree) para analisar estaticamente o código Python do usuário, verificando:

- Importações permitidas (apenas numpy, pandas, catch22)
- Ausência de chamadas de sistema perigosas (system, exec, eval)
- Ausência de acesso a arquivos
- Ausência de acesso à rede
- Presença da função `process` esperada


### Exemplo de Uso pelo Cliente

```python
import requests
import json

# Endpoint da API
url = "http://seu-servico/process/"

# Exemplo de código que processa o DataFrame
code = """
import pandas as pd
import numpy as np

def process(df):
    # Adiciona uma nova coluna com a média móvel de uma coluna existente
    df['rolling_mean'] = df['valor'].rolling(window=3).mean()
    
    # Remove linhas com valores nulos
    df = df.dropna()
    
    # Adiciona uma coluna de timestamp
    df['timestamp'] = pd.Timestamp.now()
    
    return df
"""

# Dados da requisição
payload = {
    "dataset_path": "meu-bucket/dados/vendas.csv",
    "code": code,
    "timeout": 120,
    "max_memory": 2048
}

# Faz a requisição
response = requests.post(url, json=payload)
result = response.json()

print(f"Status: {result['status']}")
print(f"Arquivo Parquet: {result['parquet_path']}")
print(f"Linhas: {result['rows']}")
print(f"Colunas: {result['columns']}")
print(f"Tempo de execução: {result['execution_time']} segundos")
```

## Considerações de Segurança

### Análise Estática de Código
- Verificação de importações permitidas
- Detecção de chamadas de sistema perigosas
- Validação da estrutura esperada do código

### Isolamento de Execução
- Execução em ambiente sandbox controlado
- Acesso apenas às bibliotecas permitidas
- Sem acesso a sistema de arquivos, rede ou recursos do sistema

### Limites de Recursos
- Timeout para prevenir execução infinita
- Limite de memória configurável
- Limite de CPU configurável

## Extensões Futuras

### Processamento Assíncrono
- Implementar fila de mensagens (RabbitMQ/Redis)
- Adicionar endpoints para verificação de status
- Notificações de conclusão

### Monitoramento e Observabilidade
- Logs detalhados de execução
- Métricas de performance
- Rastreamento de execuções

## Conclusão

Este microserviço fornece uma solução segura e flexível para que usuários possam processar datasets usando código Python personalizado. A arquitetura garante isolamento e segurança enquanto permite transformações de dados complexas utilizando bibliotecas populares de análise de dados.

A implementação como microserviço em Kubernetes facilita a integração com sistemas existentes e permite escalabilidade para atender a diferentes cargas de trabalho. O uso do formato Parquet para armazenamento dos resultados garante eficiência tanto no armazenamento quanto na leitura posterior dos dados processados.