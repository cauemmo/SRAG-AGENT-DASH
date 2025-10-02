# SRAG AI Reporter - Documentação Completa da Arquitetura

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Arquitetura do Sistema](#2-arquitetura-do-sistema)
3. [Sistema de Agentes](#3-sistema-de-agentes)
4. [Sistema de Guardrails](#4-sistema-de-guardrails)
5. [Sistema de Logging e Auditoria](#5-sistema-de-logging-e-auditoria)
6. [Banco de Dados](#6-banco-de-dados)
7. [Tools e Ferramentas](#7-tools-e-ferramentas)
8. [MCP (Model Context Protocol)](#8-mcp-model-context-protocol)
9. [Fluxo de Dados](#9-fluxo-de-dados)
10. [Segurança e Compliance](#10-segurança-e-compliance)

---

## 1. Visão Geral

### 1.1 Propósito do Sistema

O **SRAG AI Reporter** é um sistema de análise automatizada de dados epidemiológicos de Síndrome Respiratória Aguda Grave (SRAG) com geração de relatórios estruturados para suporte à tomada de decisão em saúde pública. O sistema foi desenvolvido como Prova de Conceito (PoC) implementando princípios de IA generativa responsável com múltiplas camadas de validação e auditoria.

### 1.2 Características Principais

- **Análise Epidemiológica Automatizada**: Processamento de dados DATASUS/INFLUD com cálculo de indicadores epidemiológicos
- **Sistema de Agentes**: Orquestração inteligente de múltiplos componentes
- **Guardrails Médicos**: Validações rigorosas para garantir segurança em contexto de saúde
- **Auditoria Completa**: Rastreabilidade total de todas as decisões do sistema
- **Interpretação Clínica Contextualizada**: Uso de MCP para fornecer contexto médico especializado

### 1.3 Stack Tecnológico

```
Backend:
- Python 3.9+
- SQLite (persistência)
- Pandas/NumPy (análise de dados)

AI/ML:
- LangChain (orquestração de agentes)
- OpenAI API (processamento de linguagem natural)
- LangGraph (fluxo de agentes)

Visualização:
- Plotly (gráficos interativos)
- Matplotlib/Seaborn (análises estatísticas)
- HTML/CSS (relatórios)

Bibliotecas Especializadas:
- ChromaDB (armazenamento vetorial)
- TikToken (tokenização)
- BeautifulSoup4 (web scraping)
- FeedParser (RSS feeds)
```

---

## 2. Arquitetura do Sistema

### 2.1 Visão Arquitetural

O sistema segue uma arquitetura em camadas com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface Layer                           │
│                     (main.py, CLI)                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Agent Layer                               │
│              (SRAGAgent - Orquestrador)                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────┬─────────────────┬─────────────────┬─────────┐
│  Tools Layer  │   MCP Layer     │  Audit Layer    │ Reports │
│  (Database,   │  (Healthcare    │  (Guardrails,   │  Layer  │
│   News)       │   Context)      │   Logger)       │         │
└───────────────┴─────────────────┴─────────────────┴─────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│        (DatabaseManager, DataProcessor, SQLite)              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Estrutura de Diretórios

```
srag-ai-reporter/
├── src/
│   ├── agents/                    # Camada de Agentes
│   │   └── srag_agent.py         # Agente principal orquestrador
│   │
│   ├── audit/                     # Sistema de Auditoria
│   │   ├── medical_guardrails.py # Guardrails médicos
│   │   ├── decision_logger.py    # Logger de decisões
│   │   ├── audit_trail_manager.py # Gerenciador de trilha de auditoria
│   │   └── __init__.py
│   │
│   ├── tools/                     # Ferramentas do Sistema
│   │   ├── database_tool.py      # Interface para consultas DB
│   │   └── news_tool.py          # Coleta de notícias
│   │
│   ├── mcp/                       # Model Context Protocol
│   │   └── health_context_provider.py # Provider de contexto clínico
│   │
│   ├── utils/                     # Utilitários
│   │   ├── data_processor.py     # Processamento de dados INFLUD
│   │   ├── database_manager.py   # Gerenciamento do SQLite
│   │   ├── data_downloader.py    # Download de dados externos
│   │   └── simple_data_generator.py # Gerador de dados sintéticos
│   │
│   ├── visualizations/            # Geração de Visualizações
│   │   └── chart_generator.py    # Gerador de gráficos Plotly
│   │
│   ├── reports/                   # Geração de Relatórios
│   │   └── report_generator.py   # Gerador de relatórios HTML
│   │
│   └── data/                      # Dados e Bancos
│       ├── raw/                   # Dados brutos
│       ├── processed/             # Dados processados
│       ├── srag_database.db       # Banco principal
│       └── decisions_audit.db     # Banco de auditoria
│
├── reports/                       # Relatórios gerados
├── docs/                          # Documentação
├── tests/                         # Testes unitários
├── main.py                        # Ponto de entrada
├── requirements.txt               # Dependências
└── setup.py                       # Configuração do pacote
```

### 2.3 Padrões Arquiteturais

**Factory Pattern**: Utilizado para criação de componentes auditáveis
```python
def create_audit_trail_manager() -> AuditTrailManager
def create_decision_logger() -> DecisionLogger
def create_medical_guardrails() -> MedicalGuardrails
```

**Strategy Pattern**: Diferentes estratégias de validação nos Guardrails
```python
class MedicalRangeValidator
class InputSanitizer
class RateLimiter
class AccessController
```

**Repository Pattern**: DatabaseManager abstrai acesso aos dados
```python
class SRAGDatabaseManager
class DatabaseTool
```

---

## 3. Sistema de Agentes

### 3.1 Arquitetura do Agente Principal

O **SRAGAgent** (`src/agents/srag_agent.py`) é o orquestrador central do sistema, responsável por coordenar todas as etapas de análise e geração de relatórios.

```python
class SRAGAgent:
    """
    Main SRAG AI Agent que orquestra análise de dados e geração de relatórios
    """

    def __init__(self):
        self.db_tool = SRAGDatabaseTool()          # Acesso a dados
        self.news_tool = SRAGNewsTool()            # Contexto de notícias
        self.health_context = HealthcareContextProvider()  # Contexto clínico
        self.audit_manager = create_audit_trail_manager()  # Auditoria
```

### 3.2 Fluxo de Execução do Agente

```
1. generate_report()
   ↓
2. _gather_metrics()              → Coleta métricas do banco de dados
   ↓
3. _gather_news_context()         → Busca notícias relevantes
   ↓
4. _calculate_required_metrics()  → Calcula 4 métricas principais + interpretação clínica
   ↓
5. _generate_insights()           → Gera insights usando MCP + Guardrails
   ↓
6. _prepare_chart_data()          → Prepara dados para visualizações
   ↓
7. _compile_report()              → Compila relatório final
```

### 3.3 Métricas Calculadas

O agente calcula **4 métricas principais** com interpretação clínica contextualizada:

#### 3.3.1 Taxa de Crescimento Epidemiológico (Growth Rate)

```python
def _calculate_required_metrics(self):
    growth_data = self.db_tool.run("get_growth_rate", period_days=30)
    growth_rate = growth_data["data"]["growth_rate"]

    # Interpretação clínica via MCP
    clinical_interp = self.health_context.get_clinical_interpretation(
        "growth_rate", growth_rate
    )

    # Auditoria da interpretação
    audit_decision_id = self.audit_manager.audit_clinical_interpretation(
        metric_type="growth_rate",
        metric_value=growth_rate,
        threshold_used=10.0,
        interpretation=clinical_interp.get("interpretation"),
        confidence_score=0.9,
        user_role="data_analyst"
    )
```

**Interpretação Epidemiológica**:
- `< -15%`: Declínio epidêmico significativo, possível fim de surto
- `-15% a -5%`: Declínio moderado, controle efetivo
- `-5% a 5%`: Estabilização epidemiológica
- `5% a 15%`: Crescimento inicial, monitoramento necessário
- `15% a 30%`: Crescimento acelerado, intervenção necessária
- `> 30%`: Crescimento explosivo, emergência sanitária

#### 3.3.2 Taxa de Mortalidade (Case Fatality Rate)

```python
mortality_rate = key_data["data"]["mortality_rate"]

# Interpretação clínica com auditoria
mortality_interp = self.health_context.get_clinical_interpretation(
    "mortality_rate", mortality_rate
)

mortality_audit_id = self.audit_manager.audit_clinical_interpretation(
    metric_type="mortality_rate",
    metric_value=mortality_rate,
    threshold_used=5.0,
    interpretation=mortality_interp.get("interpretation"),
    confidence_score=0.95,
    user_role="data_analyst"
)
```

**Thresholds Clínicos**:
- `0-2%`: Excelente - Manejo clínico otimizado
- `2-5%`: Bom - Cuidados adequados
- `5-10%`: Aceitável - Requer monitoramento
- `10-20%`: Preocupante - Revisão de protocolos necessária
- `> 20%`: Crítico - Intervenção imediata

#### 3.3.3 Taxa de Ocupação de UTI

```python
uti_rate = key_data["data"]["uti_rate"]

uti_interp = self.health_context.get_clinical_interpretation(
    "uti_rate", uti_rate
)
```

**Interpretação de Capacidade**:
- `< 10%`: Baixa demanda, casos leves/moderados
- `10-25%`: Demanda moderada, capacidade adequada
- `25-40%`: Alta demanda, pressão no sistema
- `> 40%`: Demanda crítica, risco de colapso

#### 3.3.4 Taxa de Vacinação

```python
vaccination_rate = key_data["data"]["vaccination_rate"]

vacc_interp = self.health_context.get_clinical_interpretation(
    "vaccination_coverage", vaccination_rate
)
```

**Níveis de Proteção**:
- `< 40%`: Baixa - População vulnerável
- `40-60%`: Moderada - Proteção parcial
- `60-80%`: Boa - Proteção adequada
- `> 80%`: Excelente - Imunidade populacional efetiva

### 3.4 Sistema de Insights e Recomendações

```python
def _generate_insights(self, metrics, news, specific_metrics):
    # Avaliação de risco clínico usando MCP
    risk_assessment = self.health_context.get_risk_assessment(raw_metrics)

    # Geração de recomendações contextualizadas
    clinical_recommendations = self.health_context.get_contextualized_recommendations(
        raw_metrics
    )

    # Análise de contexto epidemiológico de notícias
    news_context = self._analyze_epidemiological_news_context(news)
```

**Níveis de Risco**:
- **BAIXO** (score < 3): Situação estável
- **MODERADO** (score 3-4): Pontos de atenção
- **ALTO** (score 5-6): Alerta, monitoramento intensivo
- **CRÍTICO** (score ≥ 7): Emergência sanitária

---

## 4. Sistema de Guardrails

### 4.1 Arquitetura de Guardrails

O sistema de Guardrails (`src/audit/medical_guardrails.py`) implementa múltiplas camadas de validação para garantir segurança e integridade dos dados médicos.

```
┌─────────────────────────────────────────┐
│      MedicalGuardrails (Facade)         │
└─────────────────────────────────────────┘
            │
            ├─────→ MedicalRangeValidator
            │       (Validação de ranges médicos)
            │
            ├─────→ InputSanitizer
            │       (Sanitização e segurança)
            │
            ├─────→ RateLimiter
            │       (Controle de taxa)
            │
            └─────→ AccessController
                    (Controle de acesso)
```

### 4.2 MedicalRangeValidator

Valida se valores médicos estão dentro de ranges clinicamente aceitáveis.

```python
class MedicalRangeValidator:
    def __init__(self):
        self.medical_ranges = {
            "age": {"min": 0, "max": 120, "unit": "anos"},
            "mortality_rate": {"min": 0.0, "max": 100.0, "unit": "%"},
            "uti_rate": {"min": 0.0, "max": 100.0, "unit": "%"},
            "vaccination_rate": {"min": 0.0, "max": 100.0, "unit": "%"},
            "growth_rate": {"min": -99.9, "max": 1000.0, "unit": "%"},
            "temperature": {"min": 30.0, "max": 45.0, "unit": "°C"},
            "heart_rate": {"min": 30, "max": 220, "unit": "bpm"},
            "oxygen_saturation": {"min": 50.0, "max": 100.0, "unit": "%"}
        }

        # Thresholds críticos
        self.critical_thresholds = {
            "mortality_rate": 30.0,   # > 30% mortalidade é crítico
            "uti_rate": 50.0,         # > 50% UTI indica colapso
            "growth_rate": 200.0      # > 200% crescimento indica surto severo
        }
```

**Resultado de Validação**:
```python
@dataclass
class ValidationResult:
    is_valid: bool
    level: ValidationLevel  # INFO, WARNING, ERROR, CRITICAL
    message: str
    field: str
    value: Any
    expected_range: Optional[Tuple[float, float]]
    guardrail_triggered: Optional[str]
```

**Exemplo de Uso**:
```python
validator = MedicalRangeValidator()
result = validator.validate_medical_value("mortality_rate", 35.0)

# Output:
# ValidationResult(
#     is_valid=False,
#     level=ValidationLevel.CRITICAL,
#     message="Valor 35.0 % está fora do range médico aceitável (0.0-100.0 %)",
#     field="mortality_rate",
#     value=35.0,
#     expected_range=(0.0, 100.0),
#     guardrail_triggered="CRITICAL_THRESHOLD_EXCEEDED"
# )
```

### 4.3 InputSanitizer

Previne ataques de injeção (SQL, XSS) e valida padrões de entrada.

```python
class InputSanitizer:
    def __init__(self):
        # Padrões de SQL injection
        self.sql_patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)",
            r"(--|\/\*|\*\/)",
            r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
            r"(\')(.*?)(\')",
            r"(;.*)"
        ]

        # Padrões de XSS
        self.xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>"
        ]

        # Padrões permitidos por tipo
        self.allowed_patterns = {
            "alphanumeric": r"^[a-zA-Z0-9\s\-_\.:\(\)]+$",
            "numeric": r"^[\d\.\-\+]+$",
            "date": r"^\d{4}-\d{2}-\d{2}$",
            "database_operation": r"^[a-zA-Z0-9\s\-_\.:\(\)]+$"
        }
```

**Guardrails Detectados**:
- `SQL_INJECTION_ATTEMPT`: Padrão de SQL injection detectado
- `XSS_ATTEMPT`: Padrão de XSS detectado
- `PATTERN_MISMATCH`: Valor não atende ao padrão esperado
- `VALUE_TOO_LONG`: Valor excede 1000 caracteres

### 4.4 RateLimiter

Previne sobrecarga do sistema com rate limiting por operação.

```python
class RateLimiter:
    def __init__(self):
        self.limits = {
            "database_query": {"max_requests": 100, "window_minutes": 10},
            "report_generation": {"max_requests": 10, "window_minutes": 60},
            "data_processing": {"max_requests": 5, "window_minutes": 30}
        }
```

**Exemplo**:
```python
limiter = RateLimiter()
result = limiter.check_rate_limit("database_query", "user123")

# Se exceder limite:
# ValidationResult(
#     is_valid=False,
#     level=ValidationLevel.ERROR,
#     message="Rate limit excedido: 101/100 requests em 10 minutos",
#     guardrail_triggered="RATE_LIMIT_EXCEEDED"
# )
```

### 4.5 AccessController

Controle de acesso baseado em roles e permissões.

```python
class AccessController:
    def __init__(self):
        self.permissions = {
            "data_reader": [
                "read_database",
                "view_reports",
                "generate_charts"
            ],
            "data_analyst": [
                "read_database",
                "view_reports",
                "generate_charts",
                "generate_reports",
                "process_data"
            ],
            "admin": ["*"]  # Todas as permissões
        }

        # Operações sensíveis
        self.sensitive_operations = [
            "process_data",
            "modify_database",
            "export_data",
            "delete_records"
        ]
```

**Guardrails de Acesso**:
- `UNKNOWN_USER_ROLE`: Role não reconhecido
- `ACCESS_DENIED`: Sem permissão para operação
- `ADMIN_ACCESS`: Operação sensível por admin
- `SENSITIVE_OPERATION_ACCESS`: Acesso a operação sensível

### 4.6 Validação Completa de Dados Médicos

```python
class MedicalGuardrails:
    def validate_medical_data(
        self,
        data: Dict[str, Any],
        user_role: str = "data_reader"
    ) -> List[ValidationResult]:
        results = []

        # 1. Verificar permissão
        access_result = self.access_controller.check_permission(
            user_role, "process_data"
        )
        results.append(access_result)

        # 2. Verificar rate limit
        rate_limit_result = self.rate_limiter.check_rate_limit("data_processing")
        results.append(rate_limit_result)

        # 3. Validar cada campo médico
        for field in ["mortality_rate", "uti_rate", "vaccination_rate", "growth_rate"]:
            if field in data:
                # Sanitizar input
                sanitize_result = self.input_sanitizer.sanitize_input(
                    data[field], "numeric"
                )
                results.append(sanitize_result)

                if sanitize_result.is_valid:
                    # Validar range médico
                    range_result = self.range_validator.validate_medical_value(
                        field, data[field]
                    )
                    results.append(range_result)

        return results
```

---

## 5. Sistema de Logging e Auditoria

### 5.1 Arquitetura de Auditoria

```
┌──────────────────────────────────────────────────┐
│        AuditTrailManager (Facade)                │
│  - Integra DecisionLogger + MedicalGuardrails    │
└──────────────────────────────────────────────────┘
              │                    │
              ↓                    ↓
    ┌─────────────────┐    ┌─────────────────┐
    │ DecisionLogger  │    │Medical          │
    │ - Log decisões  │    │Guardrails       │
    │ - Log métricas  │    │ - Validações    │
    │ - Log validações│    │ - Segurança     │
    └─────────────────┘    └─────────────────┘
              │
              ↓
    ┌─────────────────┐
    │ decisions_audit.│
    │ db (SQLite)     │
    └─────────────────┘
```

### 5.2 DecisionLogger

Sistema de logging estruturado para rastreabilidade total.

#### 5.2.1 Estrutura de Decisão

```python
@dataclass
class Decision:
    decision_id: str              # UUID único
    timestamp: str                # ISO 8601
    decision_type: str            # Tipo de decisão
    component: str                # Componente que gerou
    input_data: Dict[str, Any]    # Dados de entrada
    output_data: Dict[str, Any]   # Dados de saída
    reasoning: str                # Justificativa
    confidence_score: Optional[float]  # Confiança (0-1)
    user_context: Optional[str]   # Contexto do usuário
    data_hash: str                # SHA256 para integridade
    version: str = "1.0"
```

#### 5.2.2 Schema do Banco de Auditoria

**Tabela `decisions`**:
```sql
CREATE TABLE decisions (
    decision_id TEXT PRIMARY KEY,
    session_id TEXT,
    timestamp TEXT,
    decision_type TEXT,
    component TEXT,
    input_data TEXT,              -- JSON
    output_data TEXT,             -- JSON
    reasoning TEXT,
    confidence_score REAL,
    user_context TEXT,
    data_hash TEXT,               -- SHA256
    version TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Tabela `decision_metrics`**:
```sql
CREATE TABLE decision_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id TEXT,
    metric_name TEXT,
    metric_value REAL,
    threshold_used REAL,
    validation_result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (decision_id) REFERENCES decisions (decision_id)
)
```

**Tabela `validations`**:
```sql
CREATE TABLE validations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id TEXT,
    validation_type TEXT,
    input_value TEXT,
    validation_result TEXT,       -- PASSED, WARNING, FAILED, CRITICAL
    error_message TEXT,
    guardrail_triggered TEXT,     -- Nome do guardrail
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (decision_id) REFERENCES decisions (decision_id)
)
```

#### 5.2.3 Logging de Decisão

```python
decision_id = logger.log_decision(
    decision_type="clinical_interpretation",
    component="health_context_provider",
    input_data={
        "metric_type": "mortality_rate",
        "metric_value": 22.5,
        "threshold_used": 5.0
    },
    output_data={
        "interpretation": "Taxa de mortalidade crítica",
        "severity": "critical",
        "validation_results": [...]
    },
    reasoning="Interpretação clínica baseada em threshold de 5.0",
    confidence_score=0.95,
    user_context="data_analyst"
)
```

#### 5.2.4 Logging de Métrica

```python
logger.log_metric_decision(
    decision_id=decision_id,
    metric_name="mortality_rate",
    metric_value=22.5,
    threshold_used=5.0,
    validation_result="CRITICAL"
)
```

#### 5.2.5 Logging de Validação

```python
logger.log_validation(
    decision_id=decision_id,
    validation_type="medical_range",
    input_value=22.5,
    validation_result="PASSED",
    error_message=None,
    guardrail_triggered=None
)
```

### 5.3 AuditTrailManager

Gerenciador central que integra logging com guardrails.

#### 5.3.1 Auditoria de Interpretação Clínica

```python
def audit_clinical_interpretation(
    self,
    metric_type: str,
    metric_value: float,
    threshold_used: float,
    interpretation: str,
    confidence_score: float,
    user_role: str
) -> str:
    # 1. Validar dados com guardrails
    validation_results = self.guardrails.validate_medical_data(
        {metric_type: metric_value},
        user_role
    )

    # 2. Verificar violações críticas
    critical_violations = [
        r for r in validation_results
        if not r.is_valid and r.level == ValidationLevel.CRITICAL
    ]

    if critical_violations:
        # Log decisão de rejeição
        decision_id = self.decision_logger.log_decision(
            decision_type="clinical_interpretation_rejected",
            ...
        )

        # Log violações
        for violation in critical_violations:
            self.decision_logger.log_validation(
                decision_id=decision_id,
                validation_type=violation.field,
                validation_result="FAILED",
                error_message=violation.message,
                guardrail_triggered=violation.guardrail_triggered
            )

        raise ValueError("Violações críticas detectadas")

    # 3. Log interpretação aprovada
    decision_id = self.decision_logger.log_decision(
        decision_type="clinical_interpretation",
        component="health_context_provider",
        input_data={...},
        output_data={...},
        reasoning=f"Interpretação baseada em threshold de {threshold_used}",
        confidence_score=confidence_score
    )

    # 4. Log métrica e validações
    self.decision_logger.log_metric_decision(...)

    return decision_id
```

#### 5.3.2 Auditoria de Processamento de Dados

```python
def audit_data_processing(
    self,
    source_file: str,
    records_input: int,
    records_processed: int,
    validation_errors: List[Dict],
    user_role: str
) -> str:
    # Verificar permissões
    access_validation = self.guardrails.access_controller.check_permission(
        user_role, "process_data"
    )

    # Calcular métricas de qualidade
    success_rate = (records_processed / records_input * 100)
    processing_status = "SUCCESS" if success_rate > 80 else "WARNING"

    # Log processamento
    decision_id = self.decision_logger.log_decision(
        decision_type="data_processing",
        component="data_processor",
        input_data={"source_file": source_file, "records_input": records_input},
        output_data={
            "records_processed": records_processed,
            "success_rate": success_rate,
            "processing_status": processing_status
        },
        reasoning=f"Processamento com {success_rate:.1f}% de sucesso",
        confidence_score=success_rate / 100
    )

    return decision_id
```

#### 5.3.3 Auditoria de Consultas de Banco

```python
def audit_database_query(
    self,
    query_type: str,
    sql_query: str,
    results_count: int,
    execution_time_ms: float,
    user_role: str
) -> str:
    # Validar query com guardrails
    validation_results = self.guardrails.validate_database_query(
        sql_query, user_role
    )

    # Verificar violações
    violations = [v for v in validation_results if not v.is_valid]

    if violations:
        # Log query rejeitada
        decision_id = self.decision_logger.log_decision(
            decision_type="database_query_rejected",
            ...
        )
        raise ValueError(f"Query rejeitada: {violations}")

    # Log query bem-sucedida
    decision_id = self.decision_logger.log_decision(
        decision_type="database_query",
        component="database_tool",
        output_data={
            "results_count": results_count,
            "execution_time_ms": execution_time_ms,
            "status": "SUCCESS"
        },
        confidence_score=1.0 if execution_time_ms < 1000 else 0.8
    )

    return decision_id
```

#### 5.3.4 Resumo de Auditoria

```python
def get_audit_summary(
    self,
    hours: int = 24,
    decision_types: Optional[List[str]] = None
) -> Dict[str, Any]:
    decisions = self.decision_logger.get_decision_history(limit=1000)

    # Filtrar por período
    cutoff_time = datetime.now().timestamp() - (hours * 3600)
    recent_decisions = [d for d in decisions if ...]

    # Calcular estatísticas
    return {
        "audit_period_hours": hours,
        "total_decisions": len(recent_decisions),
        "error_rate": (error_count / total * 100),
        "decisions_by_type": {...},
        "decisions_by_component": {...},
        "error_count": error_count,
        "recent_decisions": recent_decisions[:10]
    }
```

### 5.4 Integração com Agente

```python
# No SRAGAgent
def _calculate_required_metrics(self):
    # Cálculo da métrica
    growth_rate = growth_data["data"]["growth_rate"]

    # Interpretação clínica
    clinical_interp = self.health_context.get_clinical_interpretation(
        "growth_rate", growth_rate
    )

    # AUDITORIA AUTOMÁTICA
    try:
        audit_decision_id = self.audit_manager.audit_clinical_interpretation(
            metric_type="growth_rate",
            metric_value=growth_rate,
            threshold_used=10.0,
            interpretation=clinical_interp.get("interpretation"),
            confidence_score=0.9,
            user_role="data_analyst"
        )
        logger.info(f"Interpretation audited - Decision ID: {audit_decision_id}")
    except Exception as audit_error:
        logger.error(f"Audit failed: {audit_error}")

    # Armazenar ID de auditoria na métrica
    metrics["growth_rate"]["audit_decision_id"] = audit_decision_id
```

---

## 6. Banco de Dados

### 6.1 Arquitetura de Dados

O sistema utiliza **SQLite** com dois bancos de dados separados:

1. **`srag_database.db`**: Dados epidemiológicos principais
2. **`decisions_audit.db`**: Trilha de auditoria

### 6.2 Schema do Banco Principal

#### 6.2.1 Tabela `srag_cases`

```sql
CREATE TABLE srag_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Datas
    notification_date DATE NOT NULL,
    symptom_date DATE,
    internment_date DATE,
    evolution_date DATE,

    -- Dados demográficos
    municipality_id TEXT,
    sex TEXT,
    age INTEGER,

    -- Sintomas (0=Não, 1=Sim)
    fever INTEGER,
    cough INTEGER,
    dyspnea INTEGER,

    -- Internação
    uti INTEGER,              -- UTI
    hospitalized INTEGER,

    -- Vacinação
    vaccination INTEGER,
    dose1 INTEGER,
    dose2 INTEGER,
    booster INTEGER,

    -- Evolução
    evolution TEXT,           -- '1'=Cura, '2'=Óbito, '3'=Em tratamento

    -- Temporalidade
    year INTEGER,
    month INTEGER,
    week INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Índices**:
```sql
CREATE INDEX idx_notification_date ON srag_cases(notification_date);
CREATE INDEX idx_year_month ON srag_cases(year, month);
CREATE INDEX idx_evolution ON srag_cases(evolution);
CREATE INDEX idx_uti ON srag_cases(uti);
```

#### 6.2.2 Tabela `daily_metrics`

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

### 6.3 DatabaseManager

Gerenciador de conexões e operações do banco SQLite.

```python
class SRAGDatabaseManager:
    def __init__(self, db_path="src/data/srag_database.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self) -> bool:
        """Cria conexão com banco"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Acesso por nome de coluna
        return True

    def create_tables(self) -> bool:
        """Cria tabelas e índices"""
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS srag_cases ...""")
        cursor.execute("""CREATE INDEX IF NOT EXISTS ...""")
        self.conn.commit()
        return True

    def load_processed_data(self, csv_path) -> bool:
        """Carrega dados processados do CSV"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM srag_cases")  # Limpa dados antigos

        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            records = [...]  # Parse CSV
            cursor.executemany(insert_query, records)

        self.conn.commit()
        self._generate_daily_metrics()  # Gera agregações
        return True

    def _generate_daily_metrics(self):
        """Gera métricas diárias agregadas"""
        cursor.execute("""
            INSERT INTO daily_metrics (date, total_cases, uti_cases, deaths, ...)
            SELECT
                notification_date,
                COUNT(*),
                SUM(CASE WHEN uti = 1 THEN 1 ELSE 0 END),
                SUM(CASE WHEN evolution = '2' THEN 1 ELSE 0 END),
                ...
            FROM srag_cases
            GROUP BY notification_date
        """)
        self.conn.commit()
```

### 6.4 Operações de Consulta

#### 6.4.1 Métricas Principais

```python
def get_key_metrics(self) -> Dict:
    cursor.execute("""
        SELECT
            COUNT(*) as total_cases,
            SUM(CASE WHEN uti = 1 THEN 1 ELSE 0 END) as total_uti_cases,
            SUM(CASE WHEN evolution = '2' THEN 1 ELSE 0 END) as total_deaths,
            SUM(CASE WHEN vaccination = 1 THEN 1 ELSE 0 END) as total_vaccinated,
            MIN(notification_date) as first_case_date,
            MAX(notification_date) as last_case_date
        FROM srag_cases
    """)

    overall = dict(cursor.fetchone())

    # Calcular taxas
    overall['uti_rate'] = (overall['total_uti_cases'] / overall['total_cases']) * 100
    overall['mortality_rate'] = (overall['total_deaths'] / overall['total_cases']) * 100
    overall['vaccination_rate'] = (overall['total_vaccinated'] / overall['total_cases']) * 100

    return overall
```

#### 6.4.2 Taxa de Crescimento

```python
def get_growth_rate(self, period_days=30) -> Dict:
    # Casos do período atual
    cursor.execute("""
        SELECT COUNT(*) FROM srag_cases
        WHERE notification_date >= date('now', '-{} days')
    """.format(period_days))
    current_cases = cursor.fetchone()[0]

    # Casos do período anterior
    cursor.execute("""
        SELECT COUNT(*) FROM srag_cases
        WHERE notification_date >= date('now', '-{} days')
          AND notification_date < date('now', '-{} days')
    """.format(period_days * 2, period_days))
    previous_cases = cursor.fetchone()[0]

    # Calcular crescimento
    growth_rate = ((current_cases - previous_cases) / previous_cases) * 100

    return {
        "current_period_cases": current_cases,
        "previous_period_cases": previous_cases,
        "growth_rate": growth_rate
    }
```

#### 6.4.3 Análise Demográfica

```python
def get_demographic_stats(self) -> Dict:
    # Distribuição por gênero
    cursor.execute("""
        SELECT
            sex,
            COUNT(*) as count,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM srag_cases)), 2) as percentage
        FROM srag_cases
        WHERE sex IS NOT NULL
        GROUP BY sex
    """)
    gender_dist = [dict(row) for row in cursor.fetchall()]

    # Distribuição por faixa etária
    cursor.execute("""
        SELECT
            CASE
                WHEN age < 18 THEN 'Under 18'
                WHEN age BETWEEN 18 AND 59 THEN '18-59'
                WHEN age >= 60 THEN '60+'
            END as age_group,
            COUNT(*) as count
        FROM srag_cases
        GROUP BY age_group
    """)
    age_dist = [dict(row) for row in cursor.fetchall()]

    return {"gender_distribution": gender_dist, "age_distribution": age_dist}
```

---

## 7. Tools e Ferramentas

### 7.1 DatabaseTool

Interface de alto nível para consultas ao banco com auditoria integrada.

```python
class SRAGDatabaseTool:
    def __init__(self, db_path="src/data/srag_database.db"):
        self.db_path = db_path
        self._audit_manager = None  # Lazy initialization

    @property
    def audit_manager(self):
        """Lazy init do audit manager"""
        if self._audit_manager is None:
            from audit.audit_trail_manager import create_audit_trail_manager
            self._audit_manager = create_audit_trail_manager()
        return self._audit_manager

    def run(self, query_type: str, **kwargs) -> Dict[str, Any]:
        start_time = time.time()

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        # Executar query apropriada
        if query_type == "get_key_metrics":
            result = self._get_key_metrics(conn)
        elif query_type == "get_daily_cases":
            result = self._get_daily_cases(conn, kwargs.get('days', 30))
        elif query_type == "get_growth_rate":
            result = self._get_growth_rate(conn, kwargs.get('period_days', 30))
        # ... outras queries

        conn.close()

        # AUDITORIA AUTOMÁTICA
        execution_time = (time.time() - start_time) * 1000
        if self.audit_manager and result.get("status") == "success":
            try:
                self.audit_manager.audit_database_query(
                    query_type=query_type,
                    sql_query=f"Database operation: {query_type}",
                    results_count=len(result.get("data", {})),
                    execution_time_ms=execution_time,
                    user_role="data_analyst"
                )
            except Exception as audit_error:
                logger.warning(f"Audit failed: {audit_error}")

        return result
```

**Queries Disponíveis**:
- `get_key_metrics`: Estatísticas gerais (UTI, mortalidade, vacinação)
- `get_daily_cases`: Casos diários para período especificado
- `get_monthly_cases`: Casos mensais para período especificado
- `get_growth_rate`: Análise de taxa de crescimento
- `get_demographic_stats`: Distribuição de idade e gênero
- `get_vaccination_analysis`: Análise de status de vacinação
- `custom_query`: Query SQL personalizada (apenas SELECT)

### 7.2 NewsTool

Ferramenta para coleta de informações contextuais de fontes externas.

```python
class SRAGNewsTool:
    def __init__(self):
        self.name = "srag_news_search"
        self.description = "Busca notícias e informações sobre SRAG"
        self.sources = [
            "https://news.google.com/rss/search?q=SRAG",
            "https://www.gov.br/saude/pt-br"
        ]

    def run(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Busca notícias relacionadas ao query"""
        articles = []

        try:
            # Buscar via RSS feeds
            for source in self.sources:
                feed = feedparser.parse(source)
                for entry in feed.entries[:max_results]:
                    articles.append({
                        "title": entry.title,
                        "source": entry.source.title if hasattr(entry, 'source') else "Unknown",
                        "date": entry.published,
                        "content": entry.summary,
                        "link": entry.link
                    })

            return {
                "status": "success",
                "articles": articles,
                "total_found": len(articles)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_recent_trends(self, days: int = 30) -> Dict[str, Any]:
        """Analisa tendências recentes em notícias"""
        # Implementação de análise de tendências
        pass
```

### 7.3 ChartGenerator

Gerador de visualizações interativas usando Plotly.

```python
class SRAGChartGenerator:
    def __init__(self):
        self.db_tool = SRAGDatabaseTool()
        self.output_dir = "reports/charts"

    def generate_daily_cases_chart(self, days=30) -> Dict[str, Any]:
        """Gera gráfico de casos diários"""
        data = self.db_tool.run("get_daily_cases", days=days)

        if data.get("status") != "success":
            return {"status": "error", "message": "Failed to get data"}

        daily_cases = data["data"]["daily_cases"]

        # Criar gráfico Plotly
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=[d['date'] for d in daily_cases],
            y=[d['cases'] for d in daily_cases],
            mode='lines+markers',
            name='Casos Totais',
            line=dict(color='#1f77b4', width=2)
        ))

        fig.add_trace(go.Scatter(
            x=[d['date'] for d in daily_cases],
            y=[d['deaths'] for d in daily_cases],
            mode='lines+markers',
            name='Óbitos',
            line=dict(color='#d62728', width=2)
        ))

        fig.update_layout(
            title='Casos Diários de SRAG',
            xaxis_title='Data',
            yaxis_title='Número de Casos',
            hovermode='x unified'
        )

        # Salvar gráfico
        output_path = f"{self.output_dir}/daily_cases.html"
        fig.write_html(output_path)

        return {
            "status": "success",
            "path": output_path,
            "chart_type": "daily_cases"
        }

    def generate_all_charts(self) -> Dict[str, Any]:
        """Gera todos os gráficos"""
        results = {}

        results["daily_cases"] = self.generate_daily_cases_chart()
        results["monthly_cases"] = self.generate_monthly_cases_chart()
        results["demographics"] = self.generate_demographics_chart()

        return results
```

### 7.4 ReportGenerator

Gerador de relatórios HTML com templates customizáveis.

```python
class SRAGReportGenerator:
    def __init__(self):
        self.db_tool = SRAGDatabaseTool()
        self.chart_generator = SRAGChartGenerator()
        self.agent = SRAGAgent()

    def generate_full_report(self) -> Dict[str, Any]:
        """Gera relatório completo"""
        # 1. Gerar análise via agente
        analysis = self.agent.generate_report()

        # 2. Gerar gráficos
        charts = self.chart_generator.generate_all_charts()

        # 3. Compilar HTML
        html_content = self._build_html_report(analysis, charts)

        # 4. Salvar arquivos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_path = f"reports/srag_report_{timestamp}.html"
        json_path = f"reports/srag_report_{timestamp}.json"

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        return {
            "status": "success",
            "html_report": html_path,
            "json_report": json_path,
            "charts": charts
        }

    def _build_html_report(self, analysis, charts) -> str:
        """Constrói relatório HTML"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório SRAG</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .metric {{ background: #f0f0f0; padding: 20px; margin: 10px 0; }}
                .critical {{ border-left: 5px solid #d62728; }}
            </style>
        </head>
        <body>
            <h1>{analysis['title']}</h1>
            <p><strong>Data:</strong> {analysis['timestamp']}</p>

            <h2>Resumo Executivo</h2>
            <p>{analysis['executive_summary']}</p>

            <h2>Métricas Principais</h2>
            {self._render_metrics(analysis['key_metrics'])}

            <h2>Visualizações</h2>
            {self._embed_charts(charts)}

            <h2>Recomendações</h2>
            {self._render_recommendations(analysis['insights']['recommendations'])}
        </body>
        </html>
        """
        return html
```

---

## 8. MCP (Model Context Protocol)

### 8.1 HealthcareContextProvider

Provider especializado em contexto clínico e epidemiológico.

```python
class HealthcareContextProvider:
    """
    MCP Provider para contexto de saúde especializado
    """

    def __init__(self):
        self.name = "healthcare_context_provider"
        self.version = "1.0.0"

        # Thresholds clínicos baseados em evidências
        self.clinical_thresholds = {
            "mortality_rate": {
                "excellent": {"max": 2.0, "interpretation": "Taxa excelente"},
                "good": {"max": 5.0, "interpretation": "Taxa boa"},
                "acceptable": {"max": 10.0, "interpretation": "Taxa aceitável"},
                "concerning": {"max": 20.0, "interpretation": "Preocupante"},
                "critical": {"max": float('inf'), "interpretation": "Crítico"}
            },
            "uti_rate": {...},
            "vaccination_coverage": {...}
        }

        # Recomendações clínicas pré-definidas
        self.clinical_recommendations = {
            "high_mortality": [
                "Revisar protocolos de triagem",
                "Avaliar recursos de UTI",
                "Implementar cuidados paliativos",
                "Fortalecer capacitação de equipes",
                "Considerar transferências"
            ],
            "high_uti_demand": [...],
            "low_vaccination": [...],
            "rapid_growth": [...]
        }
```

### 8.2 Interpretação Clínica

```python
def get_clinical_interpretation(
    self,
    metric_type: str,
    value: float
) -> Dict[str, Any]:
    """Fornece interpretação clínica de uma métrica"""

    if metric_type not in self.clinical_thresholds:
        return {"interpretation": "Métrica não reconhecida", "severity": "unknown"}

    thresholds = self.clinical_thresholds[metric_type]

    for level, threshold_data in thresholds.items():
        if value <= threshold_data["max"]:
            return {
                "level": level,
                "interpretation": threshold_data["interpretation"],
                "severity": self._get_severity(level),
                "clinical_significance": self._get_clinical_significance(
                    metric_type, level
                )
            }

    return {"interpretation": "Valor fora dos padrões", "severity": "unknown"}
```

**Exemplo de Uso**:
```python
provider = HealthcareContextProvider()

interp = provider.get_clinical_interpretation("mortality_rate", 22.5)

# Output:
# {
#     "level": "critical",
#     "interpretation": "Taxa de mortalidade crítica, requer intervenção imediata",
#     "severity": "critical",
#     "clinical_significance": "Intervenção imediata, auditoria de óbitos, revisão sistêmica"
# }
```

### 8.3 Recomendações Contextualizadas

```python
def get_contextualized_recommendations(
    self,
    metrics: Dict[str, float]
) -> List[str]:
    """Gera recomendações baseadas em múltiplas métricas"""

    recommendations = []

    # Analisar mortalidade
    if metrics.get("mortality_rate", 0) > 15:
        recommendations.extend(self.clinical_recommendations["high_mortality"])

    # Analisar UTI
    if metrics.get("uti_rate", 0) > 25:
        recommendations.extend(self.clinical_recommendations["high_uti_demand"])

    # Analisar vacinação
    if metrics.get("vaccination_rate", 0) < 60:
        recommendations.extend(self.clinical_recommendations["low_vaccination"])

    # Analisar crescimento
    if metrics.get("growth_rate", 0) > 20:
        recommendations.extend(self.clinical_recommendations["rapid_growth"])

    # Contexto sazonal
    current_month = datetime.now().month
    if current_month in [6, 7, 8]:  # Inverno no Brasil
        recommendations.append("Monitorar padrão sazonal de inverno")
        recommendations.append("Preparar recursos para pico sazonal")

    # Remover duplicatas preservando ordem
    seen = set()
    unique_recommendations = []
    for rec in recommendations:
        if rec not in seen:
            seen.add(rec)
            unique_recommendations.append(rec)

    return unique_recommendations[:8]  # Top 8 recomendações
```

### 8.4 Avaliação de Risco

```python
def get_risk_assessment(self, metrics: Dict[str, float]) -> Dict[str, Any]:
    """Avaliação abrangente de risco"""

    risk_factors = []
    risk_score = 0

    # Risco de mortalidade
    mortality_rate = metrics.get("mortality_rate", 0)
    if mortality_rate > 20:
        risk_factors.append("Taxa de mortalidade crítica")
        risk_score += 3
    elif mortality_rate > 10:
        risk_factors.append("Taxa de mortalidade elevada")
        risk_score += 2

    # Risco de capacidade do sistema
    uti_rate = metrics.get("uti_rate", 0)
    if uti_rate > 30:
        risk_factors.append("Sobrecarga crítica de UTI")
        risk_score += 3
    elif uti_rate > 20:
        risk_factors.append("Pressão elevada em UTI")
        risk_score += 2

    # Vulnerabilidade populacional
    vaccination_rate = metrics.get("vaccination_rate", 0)
    if vaccination_rate < 50:
        risk_factors.append("Baixa proteção vacinal")
        risk_score += 2
    elif vaccination_rate < 70:
        risk_factors.append("Proteção vacinal moderada")
        risk_score += 1

    # Risco epidêmico
    growth_rate = metrics.get("growth_rate", 0)
    if growth_rate > 25:
        risk_factors.append("Crescimento epidêmico acelerado")
        risk_score += 3
    elif growth_rate > 15:
        risk_factors.append("Crescimento epidêmico moderado")
        risk_score += 2

    # Classificação de risco
    if risk_score >= 7:
        risk_level = "CRÍTICO"
        risk_description = "Emergência sanitária, ação imediata necessária"
    elif risk_score >= 5:
        risk_level = "ALTO"
        risk_description = "Alerta, monitoramento intensivo necessário"
    elif risk_score >= 3:
        risk_level = "MODERADO"
        risk_description = "Situação controlada com pontos de atenção"
    else:
        risk_level = "BAIXO"
        risk_description = "Situação estável"

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "risk_description": risk_description,
        "risk_factors": risk_factors,
        "monitoring_priority": "ALTA" if risk_score >= 5 else "MÉDIA" if risk_score >= 3 else "ROTINA"
    }
```

**Exemplo**:
```python
test_metrics = {
    "mortality_rate": 22.5,
    "uti_rate": 18.3,
    "vaccination_rate": 65.2,
    "growth_rate": 8.1
}

risk = provider.get_risk_assessment(test_metrics)

# Output:
# {
#     "risk_level": "ALTO",
#     "risk_score": 5,
#     "risk_description": "Alerta, monitoramento intensivo necessário",
#     "risk_factors": [
#         "Taxa de mortalidade crítica",
#         "Proteção vacinal moderada"
#     ],
#     "monitoring_priority": "ALTA"
# }
```

---

## 9. Fluxo de Dados

### 9.1 Pipeline Completo

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. INGESTÃO DE DADOS                                            │
│    - Arquivo INFLUD19 CSV (DATASUS)                             │
│    - Data Downloader (fontes externas)                          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. PROCESSAMENTO E VALIDAÇÃO                                    │
│    - DataProcessor: limpeza, normalização                       │
│    - Guardrails: validação de ranges médicos                    │
│    - Audit: logging de processamento                            │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. PERSISTÊNCIA                                                 │
│    - DatabaseManager: carga no SQLite                           │
│    - Geração de índices                                         │
│    - Agregações (daily_metrics)                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. ANÁLISE E INTERPRETAÇÃO                                      │
│    - SRAGAgent: orquestração                                    │
│    - DatabaseTool: consultas auditadas                          │
│    - MCP: interpretação clínica                                 │
│    - NewsTool: contexto externo                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. VALIDAÇÃO E AUDITORIA                                        │
│    - MedicalGuardrails: validação de métricas                   │
│    - AuditTrailManager: logging de decisões                     │
│    - DecisionLogger: persistência de auditoria                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. GERAÇÃO DE VISUALIZAÇÕES                                     │
│    - ChartGenerator: gráficos Plotly                            │
│    - Casos diários, mensais, demográficos                       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 7. COMPILAÇÃO DE RELATÓRIOS                                     │
│    - ReportGenerator: HTML + JSON                               │
│    - Métricas, insights, recomendações                          │
│    - Embed de visualizações                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Fluxo de Auditoria

```
┌──────────────────┐
│ Operação Iniciada│
└──────────────────┘
        ↓
┌──────────────────────────┐
│ 1. Guardrails (Pré-exec) │
│    - Validar permissões  │
│    - Verificar rate limit│
│    - Sanitizar inputs    │
└──────────────────────────┘
        ↓
    [VÁLIDO?] ──NO──→ [Log Rejeição] ──→ [Raise Exception]
        ↓
       YES
        ↓
┌──────────────────────────┐
│ 2. Execução da Operação  │
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│ 3. Guardrails (Pós-exec) │
│    - Validar ranges      │
│    - Verificar thresholds│
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│ 4. Logging de Decisão    │
│    - Decision ID (UUID)  │
│    - Input/Output data   │
│    - Reasoning           │
│    - Confidence score    │
│    - Data hash (SHA256)  │
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│ 5. Logging de Métricas   │
│    - Metric name/value   │
│    - Threshold used      │
│    - Validation result   │
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│ 6. Logging de Validações │
│    - Validation type     │
│    - Result (PASS/FAIL)  │
│    - Guardrail triggered │
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│ 7. Retorno ao Chamador   │
│    - Decision ID anexado │
│    - Resultado completo  │
└──────────────────────────┘
```

### 9.3 Exemplo Completo de Fluxo

```python
# 1. Usuário executa: python main.py --all

# 2. Setup do sistema
setup_system()
    ├─> SimpleSRAGDataGenerator.generate_sample_data()  # Se necessário
    ├─> SRAGDataProcessor.process_data()
    │   └─> Audit: audit_data_processing(...)
    └─> SRAGDatabaseManager.load_processed_data()
        └─> _generate_daily_metrics()

# 3. Geração de relatório
generate_report()
    └─> SRAGReportGenerator.generate_full_report()
        ├─> SRAGAgent.generate_report()
        │   ├─> _gather_metrics()
        │   │   └─> DatabaseTool.run("get_key_metrics")
        │   │       └─> Audit: audit_database_query(...)
        │   │
        │   ├─> _gather_news_context()
        │   │   └─> NewsTool.run("SRAG")
        │   │
        │   ├─> _calculate_required_metrics()
        │   │   ├─> DatabaseTool.run("get_growth_rate")
        │   │   ├─> HealthcareContextProvider.get_clinical_interpretation()
        │   │   └─> AuditTrailManager.audit_clinical_interpretation()
        │   │       ├─> MedicalGuardrails.validate_medical_data()
        │   │       │   ├─> InputSanitizer.sanitize_input()
        │   │       │   ├─> MedicalRangeValidator.validate_medical_value()
        │   │       │   ├─> RateLimiter.check_rate_limit()
        │   │       │   └─> AccessController.check_permission()
        │   │       ├─> DecisionLogger.log_decision()
        │   │       ├─> DecisionLogger.log_metric_decision()
        │   │       └─> DecisionLogger.log_validation()
        │   │
        │   ├─> _generate_insights()
        │   │   ├─> HealthcareContextProvider.get_risk_assessment()
        │   │   └─> HealthcareContextProvider.get_contextualized_recommendations()
        │   │
        │   ├─> _prepare_chart_data()
        │   └─> _compile_report()
        │
        ├─> ChartGenerator.generate_all_charts()
        │   ├─> generate_daily_cases_chart()
        │   ├─> generate_monthly_cases_chart()
        │   └─> generate_demographics_chart()
        │
        └─> _build_html_report()

# 4. Resultado
# - reports/srag_report_YYYYMMDD_HHMMSS.html
# - reports/srag_report_YYYYMMDD_HHMMSS.json
# - reports/charts/*.html
# - src/data/decisions_audit.db (auditoria completa)
```

---

## 10. Segurança e Compliance

### 10.1 Camadas de Segurança

```
┌─────────────────────────────────────────────────────────┐
│ Camada 1: Input Validation                              │
│ - InputSanitizer (SQL injection, XSS)                   │
│ - Pattern matching                                      │
│ - Length validation                                     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Camada 2: Access Control                                │
│ - Role-based permissions                                │
│ - Sensitive operation detection                         │
│ - Permission auditing                                   │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Camada 3: Medical Range Validation                      │
│ - Clinically acceptable ranges                          │
│ - Critical threshold detection                          │
│ - Evidence-based validation                             │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Camada 4: Rate Limiting                                 │
│ - Per-operation limits                                  │
│ - Time-window controls                                  │
│ - Overload prevention                                   │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Camada 5: Audit Trail                                   │
│ - Complete decision logging                             │
│ - Tamper detection (SHA256)                             │
│ - Compliance reporting                                  │
└─────────────────────────────────────────────────────────┘
```

### 10.2 Conformidade LGPD/HIPAA

**Princípios Implementados**:

1. **Rastreabilidade**: Todas as operações são auditadas com timestamps e decision IDs
2. **Integridade**: Hashes SHA256 garantem detecção de alterações
3. **Minimização**: Apenas dados necessários são coletados e processados
4. **Segurança**: Múltiplas camadas de validação e sanitização
5. **Transparência**: Logs detalhados de reasoning e confidence scores

### 10.3 Guardrails Críticos

**SQL Injection Prevention**:
```python
# BLOQUEADO
input_value = "SELECT * FROM users; DROP TABLE users;--"
result = sanitizer.sanitize_input(input_value, "alphanumeric")
# ValidationResult(is_valid=False, guardrail_triggered="SQL_INJECTION_ATTEMPT")
```

**Medical Range Violations**:
```python
# BLOQUEADO
mortality_rate = 150.0  # Impossível > 100%
result = validator.validate_medical_value("mortality_rate", 150.0)
# ValidationResult(is_valid=False, level=CRITICAL, guardrail_triggered="MEDICAL_RANGE_VIOLATION")
```

**Rate Limiting**:
```python
# 101ª consulta em 10 minutos - BLOQUEADA
result = limiter.check_rate_limit("database_query")
# ValidationResult(is_valid=False, guardrail_triggered="RATE_LIMIT_EXCEEDED")
```

**Unauthorized Access**:
```python
# Usuário data_reader tentando modificar banco - BLOQUEADO
result = access_controller.check_permission("data_reader", "modify_database")
# ValidationResult(is_valid=False, guardrail_triggered="ACCESS_DENIED")
```

### 10.4 Trilha de Auditoria Completa

Cada decisão clínica gera registro completo:

```json
{
  "decision_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2025-02-01T14:30:45.123Z",
  "decision_type": "clinical_interpretation",
  "component": "health_context_provider",
  "input_data": {
    "metric_type": "mortality_rate",
    "metric_value": 22.5,
    "threshold_used": 5.0,
    "user_role": "data_analyst"
  },
  "output_data": {
    "interpretation": "Taxa de mortalidade crítica",
    "severity": "critical",
    "clinical_significance": "Intervenção imediata necessária",
    "validation_results": [
      {
        "field": "mortality_rate",
        "level": "critical",
        "message": "Threshold crítico excedido",
        "is_valid": true
      }
    ]
  },
  "reasoning": "Interpretação clínica baseada em threshold de 5.0 para métrica mortality_rate",
  "confidence_score": 0.95,
  "user_context": "data_analyst",
  "data_hash": "7f9a3b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0",
  "version": "1.0"
}
```

### 10.5 Consulta de Auditoria

```python
# Obter resumo de auditoria das últimas 24 horas
audit_manager = create_audit_trail_manager()
summary = audit_manager.get_audit_summary(hours=24)

# Output:
{
    "audit_period_hours": 24,
    "total_decisions": 156,
    "error_rate": 2.56,
    "decisions_by_type": {
        "clinical_interpretation": 48,
        "database_query": 92,
        "data_processing": 12,
        "report_generation": 4
    },
    "decisions_by_component": {
        "health_context_provider": 48,
        "database_tool": 92,
        "data_processor": 12,
        "report_generator": 4
    },
    "error_count": 4,
    "recent_decisions": [...]
}
```

---

## Conclusão

O **SRAG AI Reporter** implementa uma arquitetura robusta e auditável para análise epidemiológica automatizada, combinando:

- **Agentes Inteligentes** para orquestração de análise
- **Guardrails Médicos** para validação rigorosa
- **Sistema de Auditoria Completa** para rastreabilidade
- **MCP Especializado** para contexto clínico
- **Tools Auditáveis** para operações seguras

Esta arquitetura garante que todas as decisões do sistema sejam:
- **Rastreáveis**: Audit trail completa
- **Válidas**: Múltiplas camadas de validação
- **Seguras**: Proteção contra ataques e erros
- **Contextualizadas**: Interpretação clínica especializada
- **Auditáveis**: Compliance com regulações de saúde

O sistema está pronto para uso em ambientes de produção que requerem conformidade regulatória e alta confiabilidade em análise de dados de saúde.
