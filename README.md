# SRAG AI Reporter

Sistema de análise automatizada de dados epidemiológicos de Síndrome Respiratória Aguda Grave (SRAG) com geração de relatórios estruturados para suporte à tomada de decisão em saúde pública.

## Base utilizada : https://opendatasus.saude.gov.br/dataset/srag-2021-a-2024
## Descrição Técnica

O SRAG AI Reporter é uma aplicação desenvolvida como Prova de Conceito (PoC) para automação de análise epidemiológica, implementando algoritmos de processamento de dados de vigilância em saúde e métricas estatísticas relevantes para monitoramento de surtos respiratórios.

### Funcionalidades Principais

#### Processamento de Dados
- Ingestão e processamento de dados DATASUS/INFLUD
- Validação e normalização de registros epidemiológicos
- Cálculo automatizado de indicadores epidemiológicos
- Agregação temporal de séries históricas

#### Análise Epidemiológica
- Taxa de mortalidade específica por SRAG
- Taxa de ocupação de leitos de terapia intensiva
- Cobertura vacinal populacional
- Análise de tendências temporais
- Detecção de padrões sazonais

#### Geração de Relatórios
- Relatórios estruturados em formato HTML
- Visualizações interativas de séries temporais
- Exportação de dados analíticos em JSON
- Dashboard com métricas consolidadas

### Arquitetura do Sistema

#### Componentes Principais

**Agent Layer (Camada de Agentes)**
- `SRAGAgent`: Orquestrador principal responsável pela coordenação do pipeline de análise
- Implementa lógica de negócio para interpretação epidemiológica
- Gerencia fluxo de dados entre componentes

**Tool Layer (Camada de Ferramentas)**
- `DatabaseTool`: Interface para operações de consulta no banco de dados SQLite
- `NewsTool`: Módulo para coleta de informações contextuais de fontes externas
- `ChartGenerator`: Engine de geração de visualizações baseado em Plotly
- `ReportGenerator`: Gerador de relatórios HTML com templates customizáveis

**Data Layer (Camada de Dados)**
- `DataProcessor`: Processador de dados brutos com validação e limpeza
- `DatabaseManager`: Gerenciador de conexões e operações do banco SQLite
- `DataDownloader`: Interface para aquisição de dados de fontes externas

**MCP Layer (Model Context Protocol)**
- `HealthcareContextProvider`: Provider especializado em contexto clínico
- Interpretação de métricas baseada em thresholds epidemiológicos
- Recomendações automatizadas baseadas em evidências

#### Tecnologias Utilizadas

**Backend**
- Python 3.9+
- SQLite para persistência de dados
- Pandas para manipulação de dados tabulares
- NumPy para operações matemáticas

**Visualização**
- Plotly para gráficos interativos
- Matplotlib/Seaborn para análises estatísticas
- HTML/CSS para templates de relatório

**Integração**
- LangChain para orquestração de agentes
- OpenAI API para processamento de linguagem natural
- Requests para integração com APIs externas

### Especificações de Dados

#### Estrutura do Banco de Dados

**Tabela: srag_cases**
```sql
CREATE TABLE srag_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_date DATE,
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

**Tabela: daily_metrics**
```sql
CREATE TABLE daily_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE,
    total_cases INTEGER,
    uti_cases INTEGER,
    deaths INTEGER,
    vaccination_rate REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Métricas Calculadas

**Taxa de Mortalidade (%)**
```
mortality_rate = (total_deaths / total_cases) * 100
```

**Taxa de Ocupação UTI (%)**
```
uti_rate = (uti_cases / total_cases) * 100
```

**Taxa de Crescimento (%)**
```
growth_rate = ((current_period - previous_period) / previous_period) * 100
```

**Taxa de Vacinação (%)**
```
vaccination_rate = (vaccinated_cases / total_cases) * 100
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.9 ou superior
- Ambiente virtual Python (recomendado)
- Arquivo de dados INFLUD19 no formato CSV

### Processo de Instalação

1. **Clonagem do Repositório**
```bash
git clone <repository-url>
cd srag-ai-reporter
```

2. **Configuração do Ambiente Virtual**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate   # Linux/macOS
```

3. **Instalação de Dependências**
```bash
pip install -r requirements.txt
```

4. **Configuração de Variáveis de Ambiente**
```bash
copy .env.example .env
# Editar .env com as chaves de API necessárias
```

### Execução do Sistema

#### Configuração Inicial
```bash
python main.py --setup
```
Este comando executa:
- Detecção automática de arquivo INFLUD19 em Downloads
- Processamento e validação dos dados
- Criação e população do banco SQLite
- Geração de métricas agregadas

#### Geração de Relatórios
```bash
python main.py --report      # Relatório completo
python main.py --charts      # Apenas visualizações
python main.py --all         # Pipeline completo
```

### Estrutura de Arquivos

```
srag-ai-reporter/
├── src/
│   ├── agents/
│   │   └── srag_agent.py          # Agente principal de orquestração
│   ├── tools/
│   │   ├── database_tool.py       # Interface para consultas no banco
│   │   └── news_tool.py          # Coleta de informações externas
│   ├── mcp/
│   │   └── health_context_provider.py  # Provider de contexto clínico
│   ├── utils/
│   │   ├── data_processor.py      # Processamento de dados INFLUD
│   │   ├── database_manager.py    # Gerenciamento do banco SQLite
│   │   └── simple_data_generator.py  # Gerador de dados sintéticos
│   ├── visualizations/
│   │   └── chart_generator.py     # Geração de gráficos e visualizações
│   ├── reports/
│   │   └── report_generator.py    # Geração de relatórios HTML
│   └── data/
│       ├── raw/                   # Dados brutos de entrada
│       ├── processed/             # Dados processados e validados
│       └── srag_database.db       # Banco de dados SQLite
├── reports/                       # Relatórios gerados
├── docs/                         # Documentação técnica
├── tests/                        # Testes unitários (futuro)
├── requirements.txt              # Dependências Python
├── setup.py                     # Configuração do pacote
├── main.py                      # Ponto de entrada da aplicação
└── README.md                    # Este arquivo
```

## Configuração de Dados

### Fonte de Dados INFLUD19
O sistema está configurado para processar arquivos INFLUD19 do DATASUS. O arquivo deve estar localizado em:
```
C:/Users/[Usuario]/Downloads/INFLUD19-26-06-2025.csv
```

### Formato de Dados Esperado
O arquivo CSV deve conter as seguintes colunas mínimas:
- Data de notificação
- Data de sintomas
- Data de internação
- Município
- Idade e sexo do paciente
- Sintomas (febre, tosse, dispneia)
- Evolução do caso
- Status de vacinação

### Validação de Dados
O sistema implementa validação automática incluindo:
- Verificação de integridade de datas
- Validação de campos obrigatórios
- Detecção de registros duplicados
- Normalização de códigos de município

## Saídas do Sistema

### Relatórios HTML
Relatórios interativos contendo:
- Resumo executivo com situação atual
- Métricas epidemiológicas principais
- Visualizações de séries temporais
- Recomendações baseadas em evidências
- Análise de qualidade dos dados

### Visualizações
- Gráfico de casos diários (últimos 30 dias)
- Gráfico de casos mensais (últimos 12 meses)
- Análises de tendências e sazonalidade

### Dados Analíticos
Exportação em formato JSON contendo:
- Métricas calculadas com metadados
- Séries temporais estruturadas
- Interpretações clínicas automatizadas
- Dados de qualidade e cobertura

## Extensibilidade

### Adição de Novas Métricas
Para adicionar novas métricas epidemiológicas:
1. Implementar cálculo em `DatabaseTool`
2. Adicionar interpretação em `HealthcareContextProvider`
3. Incluir visualização em `ChartGenerator`

### Integração com Novas Fontes
Para integrar novas fontes de dados:
1. Criar processor específico em `utils/`
2. Adaptar schema do banco se necessário
3. Atualizar validações em `DataProcessor`

### Customização de Relatórios
Templates de relatório podem ser customizados editando:
- `src/reports/report_generator.py` para estrutura
- CSS inline para estilos visuais
- Seções de conteúdo conforme necessário

## Limitações Conhecidas

- Suporte limitado a dados anteriores a 2019
- Dependência de estrutura específica do INFLUD19
- Análises baseadas em dados retrospectivos
- Requer configuração de APIs externas para funcionalidades completas

## Considerações de Performance

- Processamento otimizado para datasets de até 100.000 registros
- Consultas indexadas no banco SQLite
- Cache de resultados para análises repetitivas

- Processamento em lote para operações de agregação
