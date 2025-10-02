"""
Script de demonstração do sistema de auditoria e guardrails
Mostra as funcionalidades implementadas
"""

import sys
import os
sys.path.append('src')

from audit.audit_trail_manager import create_audit_trail_manager
from audit.medical_guardrails import create_medical_guardrails
from audit.decision_logger import create_decision_logger

def demonstrate_audit_system():
    """Demonstra o sistema de auditoria completo"""
    print("="*60)
    print("DEMONSTRAÇÃO: Sistema de Auditoria e Guardrails Médicos")
    print("="*60)
    print()
    
    # Inicializar componentes
    audit_manager = create_audit_trail_manager()
    guardrails = create_medical_guardrails()
    decision_logger = create_decision_logger()
    
    print("✅ Componentes inicializados:")
    print("  - Audit Trail Manager")
    print("  - Medical Guardrails")
    print("  - Decision Logger")
    print()
    
    # 1. Demonstrar validações médicas
    print("1. VALIDAÇÕES MÉDICAS:")
    print("-" * 30)
    
    test_data = {
        "mortality_rate": 15.5,
        "uti_rate": 25.0,
        "age": 65,
        "vaccination_rate": 85.0
    }
    
    print(f"Testando dados: {test_data}")
    validation_results = guardrails.validate_medical_data(test_data, "data_analyst")
    
    for result in validation_results:
        status = "✅ PASSOU" if result.is_valid else "❌ FALHOU"
        print(f"  {status} {result.field}: {result.message}")
        if result.guardrail_triggered:
            print(f"    🚨 Guardrail: {result.guardrail_triggered}")
    print()
    
    # 2. Demonstrar auditoria de interpretação clínica
    print("2. AUDITORIA DE INTERPRETAÇÃO CLÍNICA:")
    print("-" * 40)
    
    try:
        decision_id = audit_manager.audit_clinical_interpretation(
            metric_type="mortality_rate",
            metric_value=15.5,
            threshold_used=10.0,
            interpretation="Taxa de mortalidade preocupante, requer monitoramento",
            confidence_score=0.9,
            user_role="data_analyst"
        )
        print(f"✅ Interpretação auditada - Decision ID: {decision_id}")
        
        # Mostrar detalhes da decisão
        decisions = decision_logger.get_decision_history(limit=1)
        if decisions:
            decision = decisions[0]
            print(f"  📊 Tipo: {decision['decision_type']}")
            print(f"  📅 Data: {decision['timestamp']}")
            print(f"  🎯 Confiança: {decision['confidence_score']}")
    except Exception as e:
        print(f"❌ Erro na auditoria: {e}")
    print()
    
    # 3. Demonstrar validações de entrada perigosas
    print("3. PROTEÇÃO CONTRA ENTRADAS MALICIOSAS:")
    print("-" * 42)
    
    dangerous_inputs = [
        "SELECT * FROM users; DROP TABLE users;",
        "<script>alert('XSS')</script>",
        "'; DELETE FROM srag_cases; --",
        "Normal input text"
    ]
    
    for dangerous_input in dangerous_inputs:
        result = guardrails.input_sanitizer.sanitize_input(dangerous_input, "alphanumeric")
        status = "✅ SEGURO" if result.is_valid else "🚨 BLOQUEADO"
        print(f"  {status} '{dangerous_input[:30]}...'")
        if result.guardrail_triggered:
            print(f"    Motivo: {result.guardrail_triggered}")
    print()
    
    # 4. Demonstrar controle de acesso
    print("4. CONTROLE DE ACESSO:")
    print("-" * 25)
    
    operations = ["read_database", "generate_reports", "process_data", "modify_database"]
    roles = ["data_reader", "data_analyst", "admin"]
    
    for role in roles:
        print(f"  Usuário {role}:")
        for operation in operations:
            access_result = guardrails.access_controller.check_permission(role, operation)
            status = "✅ PERMITIDO" if access_result.is_valid else "❌ NEGADO"
            print(f"    {status} {operation}")
    print()
    
    # 5. Demonstrar rate limiting
    print("5. RATE LIMITING:")
    print("-" * 18)
    
    print("  Testando múltiplas consultas de banco:")
    for i in range(5):
        rate_result = guardrails.rate_limiter.check_rate_limit("database_query", "test_user")
        status = "✅ PERMITIDO" if rate_result.is_valid else "🚫 BLOQUEADO"
        print(f"    Consulta {i+1}: {status}")
    print()
    
    # 6. Resumo de auditoria
    print("6. RESUMO DE AUDITORIA (últimas 24h):")
    print("-" * 35)
    
    audit_summary = audit_manager.get_audit_summary(hours=24)
    print(f"  📊 Total de decisões: {audit_summary['total_decisions']}")
    print(f"  ❌ Taxa de erro: {audit_summary['error_rate']:.1f}%")
    print(f"  🔍 Tipos de decisão:")
    for decision_type, count in audit_summary['decisions_by_type'].items():
        print(f"    - {decision_type}: {count}")
    print()
    
    print("="*60)
    print("DEMONSTRAÇÃO CONCLUÍDA")
    print("="*60)
    print()
    print("🗃️  Banco de auditoria criado em: src/data/decisions_audit.db")
    print("📝 Logs detalhados disponíveis no terminal")
    print("🔍 Use as APIs de auditoria para análise detalhada")

if __name__ == "__main__":
    demonstrate_audit_system()