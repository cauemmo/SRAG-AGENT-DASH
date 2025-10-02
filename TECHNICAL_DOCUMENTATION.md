# Documentação Técnica - SRAG AI Reporter

## 📋 Visão Geral Técnica

O SRAG AI Reporter é um sistema de análise automatizada que processa dados epidemiológicos de SRAG (Síndrome Respiratória Aguda Grave) e gera relatórios inteligentes usando técnicas de IA Generativa.

## 🏗️ Arquitetura do Sistema

### Componentes Principais

#### 1. Camada de Dados
- **Fonte**: Dados DATASUS SRAG (simulados para PoC)
- **Armazenamento**: SQLite para simplicidade e portabilidade
- **Processamento**: Pipeline ETL customizado

#### 2. Camada de Ferramentas (Tools)
- **DatabaseTool**: Interface para consultas ao banco de dados
- **NewsTool**: Agregador de notícias relacionadas a SRAG
- **ChartGenerator**: Gerador de visualizações HTML/JavaScript
- **ReportGenerator**: Compilador de relatórios finais

#### 3. Camada de Agentes
- **SRAGAgent**: Agente principal orquestrador
- **Lógica de negócio**: Interpretação de métricas e geração de insights

#### 4. Camada de Apresentação
- **Relatórios HTML**: Interface visual para usuários finais
- **Gráficos interativos**: Visualizações usando Chart.js
- **Export JSON**: Dados estruturados para integração

## 🔄 Fluxo de Processamento

### 1. Ingestão de Dados
```python
# Geração de dados de amostra (PoC)
simple_data_generator.py
├── Gera ~28k registros simulados
├── Padrões sazonais realistas
└── Estrutura compatível com DATASUS

# Processamento e limpeza
data_processor.py
├── Validação de datas
├── Normalização de categorias
├── Cálculo de campos derivados
└── Tratamento de valores ausentes
```

### 2. Armazenamento
```python
# Banco de dados
database_manager.py
├── Criação de tabelas otimizadas
├── Índices para performance
├── Métricas agregadas diárias
└── Integridade referencial
```

### 3. Análise e Geração de Insights
```python
# Agente principal
srag_agent.py
├── Coleta de métricas chave
├── Análise de tendências
├── Contexto de notícias
└── Geração de recomendações
```

## 📊 Estrutura do Banco de Dados

### Tabela Principal: `srag_cases`
```sql
CREATE TABLE srag_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_date DATE NOT NULL,
    symptom_date DATE,
    internment_date DATE,
    evolution_date DATE,
    municipality_id TEXT,
    sex TEXT,
    age INTEGER,
    fever INTEGER,
    cough INTEGER,
    dyspnea INTEGER,
    uti INTEGER,
    vaccination INTEGER,
    dose1 INTEGER,
    dose2 INTEGER,
    booster INTEGER,
    hospitalized INTEGER,
    evolution TEXT,
    year INTEGER,
    month INTEGER,
    week INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela Agregada: `daily_metrics`
```sql
CREATE TABLE daily_metrics (
    date DATE PRIMARY KEY,
    total_cases INTEGER,
    new_cases INTEGER,
    uti_cases INTEGER,
    deaths INTEGER,
    vaccinated_cases INTEGER,
    hospitalized_cases INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Índices de Performance
- `idx_notification_date`: Para consultas temporais
- `idx_year_month`: Para agregações mensais
- `idx_evolution`: Para análise de desfechos
- `idx_uti`: Para métricas de UTI

## 🧮 Cálculo de Métricas

### 1. Taxa de Aumento de Casos
```python
def calculate_growth_rate(current_period, previous_period):
    if previous_period > 0:
        return ((current_period - previous_period) / previous_period) * 100
    return 0 if current_period == 0 else 100
```

### 2. Taxa de Mortalidade
```python
def calculate_mortality_rate(total_cases, deaths):
    return (deaths / total_cases) * 100 if total_cases > 0 else 0
```

### 3. Taxa de Ocupação de UTI
```python
def calculate_uti_rate(total_cases, uti_cases):
    return (uti_cases / total_cases) * 100 if total_cases > 0 else 0
```

### 4. Taxa de Vacinação
```python
def calculate_vaccination_rate(total_cases, vaccinated_cases):
    return (vaccinated_cases / total_cases) * 100 if total_cases > 0 else 0
```

## 🎨 Sistema de Visualização

### Geração de Gráficos
- **Tecnologia**: Chart.js via CDN
- **Formato**: HTML standalone
- **Interatividade**: Hover, zoom, legendas clicáveis

### Tipos de Gráficos
1. **Linha**: Casos diários (tendência temporal)
2. **Barras**: Casos mensais (comparação periódica)

### Estrutura de Dados para Charts
```javascript
{
    "title": "Casos Diários de SRAG (Últimos 30 dias)",
    "type": "line",
    "x_axis": {"title": "Data", "data": ["2023-01-01", ...]},
    "y_axis": {"title": "Número de Casos", "data": []},
    "series": [
        {"name": "Casos Totais", "data": [50, 45, 60, ...]},
        {"name": "Casos UTI", "data": [8, 7, 12, ...]},
        {"name": "Óbitos", "data": [5, 4, 8, ...]}
    ]
}
```

## 🤖 Sistema de IA e Interpretação

### Lógica de Interpretação
O sistema usa regras heurísticas para interpretar métricas:

#### Taxa de Crescimento
- `< -10%`: Redução significativa
- `-10% a 0%`: Redução moderada
- `0% a 10%`: Crescimento estável
- `10% a 25%`: Crescimento moderado
- `> 25%`: Crescimento crítico

#### Taxa de Mortalidade
- `< 5%`: Baixa
- `5% a 15%`: Moderada
- `15% a 25%`: Alta
- `> 25%`: Crítica

### Geração de Insights
```python
def generate_insights(metrics, news_context):
    insights = {
        "summary": analyze_overall_situation(metrics),
        "key_findings": extract_key_findings(metrics),
        "recommendations": generate_recommendations(metrics, news_context),
        "risk_assessment": assess_risk_level(metrics),
        "context_analysis": analyze_news_sentiment(news_context)
    }
    return insights
```

## 🔍 Sistema de Notícias

### Estrutura de Notícias (Simulada)
```python
{
    "title": "Título da notícia",
    "content": "Conteúdo completo...",
    "date": "2025-09-25",
    "source": "Fonte",
    "url": "URL da notícia",
    "keywords": ["SRAG", "UTI", "vacinação"],
    "relevance_score": 8,
    "summary": "Resumo automático..."
}
```

### Algoritmo de Relevância
```python
def calculate_relevance(article, query):
    score = 0
    # Título (peso maior)
    if query.lower() in article["title"].lower():
        score += 10
    # Conteúdo (peso médio)
    if query.lower() in article["content"].lower():
        score += 5
    # Keywords (peso menor)
    for keyword in article["keywords"]:
        if query.lower() in keyword.lower():
            score += 2
    return score
```

## 📄 Geração de Relatórios

### Template HTML
O sistema usa templates HTML com:
- **CSS responsivo**: Layout adaptável
- **JavaScript embarcado**: Interatividade
- **Componentes modulares**: Seções reutilizáveis

### Estrutura do Relatório
1. **Header**: Título, subtítulo, timestamp
2. **Resumo Executivo**: Situação atual
3. **Métricas Principais**: Cards com valores e interpretações
4. **Visualizações**: Links para gráficos interativos
5. **Contexto de Notícias**: Artigos relevantes
6. **Insights e Recomendações**: Análises automatizadas
7. **Metodologia**: Transparência dos processos

## 🔒 Segurança e Governança

### Validação de Dados
```python
def validate_record(record):
    # Validação de datas
    if not validate_date(record.get('notification_date')):
        return False
    
    # Validação de idade
    age = record.get('age')
    if age and (age < 0 or age > 120):
        return False
    
    # Validação de categorias
    if not validate_categories(record):
        return False
    
    return True
```

### Logging e Auditoria
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/srag_system.log'),
        logging.StreamHandler()
    ]
)
```

### Guardrails
- **Validação de entrada**: Verificação de tipos e rangos
- **Sanitização**: Limpeza de dados de entrada
- **Limites de recursos**: Controle de uso de memória/CPU
- **Timeout**: Limites de tempo para operações

## 📊 Monitoramento e Métricas

### Métricas de Sistema
- **Tempo de processamento**: Latência das operações
- **Qualidade dos dados**: Percentual de dados válidos
- **Taxa de sucesso**: Relatórios gerados com sucesso
- **Uso de recursos**: CPU, memória, disco

### Alertas e Notificações (Futuro)
- **Degradação de performance**: Alertas de slowdown
- **Falhas de sistema**: Notificações de erro
- **Qualidade de dados**: Alertas de dados inconsistentes

## 🚀 Performance e Otimização

### Otimizações Implementadas
1. **Índices de banco**: Consultas mais rápidas
2. **Cache de resultados**: Reutilização de cálculos
3. **Processamento em lote**: Operações eficientes
4. **Lazy loading**: Carregamento sob demanda

### Otimizações Futuras
- **Paralelização**: Processamento concorrente
- **Cache distribuído**: Redis/Memcached
- **Particionamento**: Divisão de dados por período
- **CDN**: Distribuição de conteúdo estático

## 🧪 Testes e Validação

### Estratégia de Testes (Futuro)
```python
# Testes unitários
def test_calculate_mortality_rate():
    assert calculate_mortality_rate(100, 20) == 20.0
    assert calculate_mortality_rate(0, 0) == 0.0

# Testes de integração
def test_database_integration():
    db = SRAGDatabaseTool()
    result = db.run("get_key_metrics")
    assert result["status"] == "success"

# Testes de sistema
def test_report_generation():
    agent = SRAGAgent()
    report = agent.generate_report()
    assert report["status"] == "completed"
```

### Validação de Dados
- **Consistência temporal**: Datas em ordem lógica
- **Integridade referencial**: Relacionamentos válidos
- **Rangos válidos**: Valores dentro de limites esperados
- **Completude**: Campos obrigatórios preenchidos

## 🔄 CI/CD e Deploy (Futuro)

### Pipeline de Deploy
```yaml
# .github/workflows/deploy.yml
name: Deploy SRAG AI Reporter
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: python -m pytest tests/
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./scripts/deploy.sh
```

### Ambientes
- **Desenvolvimento**: Dados de teste, logs verbosos
- **Homologação**: Dados simulados, validação manual
- **Produção**: Dados reais, monitoramento ativo

## 📚 Referências e Padrões

### Padrões de Código
- **PEP 8**: Style Guide for Python Code
- **Type Hints**: Anotações de tipo para melhor documentação
- **Docstrings**: Documentação de funções e classes
- **Error Handling**: Tratamento adequado de exceções

### Padrões Arquiteturais
- **Tool Pattern**: Ferramentas independentes e reutilizáveis
- **Agent Pattern**: Agentes autônomos com responsabilidades específicas
- **Pipeline Pattern**: Processamento em etapas sequenciais
- **Observer Pattern**: Notificações de eventos (futuro)

---

Esta documentação técnica fornece os detalhes necessários para compreender, manter e evoluir o sistema SRAG AI Reporter.