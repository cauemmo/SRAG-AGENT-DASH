#!/usr/bin/env python3
"""
SRAG AI Reporter - Sistema Principal
Sistema de Inteligência Artificial Generativa para análise de SRAG

Uso:
    python main.py --setup    # Configuração inicial
    python main.py --report   # Gerar relatório
    python main.py --charts   # Gerar apenas gráficos
    python main.py --all      # Executar pipeline completo
"""

import argparse
import os
import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def setup_system():
    """Configuração inicial do sistema"""
    print("=" * 60)
    print("SRAG AI REPORTER - Configuracao Inicial")
    print("=" * 60)
    print()
    
    try:
        # 1. Verificar se arquivo INFLUD19 existe, senão gerar dados de amostra
        influd_path = "C:/Users/Usuário/Downloads/INFLUD19-26-06-2025.csv"
        if os.path.exists(influd_path):
            print("1. Arquivo INFLUD19 encontrado, pulando geração de dados sintéticos...")
            print("   [OK] Usando dados reais do INFLUD19")
        else:
            print("1. Arquivo INFLUD19 não encontrado, gerando dados de amostra...")
            from src.utils.simple_data_generator import SimpleSRAGDataGenerator
            generator = SimpleSRAGDataGenerator()
            generator.generate_sample_data()
            print("   [OK] Dados de amostra gerados")
        
        # 2. Processar dados
        print("2. Processando e limpando dados...")
        from src.utils.data_processor import SRAGDataProcessor
        processor = SRAGDataProcessor()
        processor.process_data()
        print("   [OK] Dados processados")
        
        # 3. Criar banco de dados
        print("3. Criando banco de dados...")
        from src.utils.database_manager import SRAGDatabaseManager
        db_manager = SRAGDatabaseManager()
        if db_manager.connect():
            if db_manager.create_tables():
                if db_manager.load_processed_data():
                    print("   [OK] Banco de dados configurado")
                else:
                    print("   [ERRO] Falha ao carregar dados")
                    return False
            else:
                print("   [ERRO] Falha ao criar tabelas")
                return False
            db_manager.disconnect()
        else:
            print("   [ERRO] Falha na conexao com banco")
            return False
        
        print()
        print("[OK] Sistema configurado com sucesso!")
        print("Execute 'python main.py --report' para gerar um relatorio")
        return True
        
    except Exception as e:
        print(f"[ERRO] Falha na configuracao: {e}")
        return False

def generate_charts():
    """Gerar apenas gráficos"""
    print("=" * 60)
    print("SRAG AI REPORTER - Geracao de Graficos")
    print("=" * 60)
    print()
    
    try:
        from src.visualizations.chart_generator import SRAGChartGenerator
        generator = SRAGChartGenerator()
        
        print("Gerando graficos...")
        results = generator.generate_all_charts()
        
        success_count = 0
        for chart_type, result in results.items():
            if result.get("status") == "success":
                print(f"[OK] {chart_type}: {result['path']}")
                success_count += 1
            else:
                print(f"[ERRO] {chart_type}: {result.get('message', 'Erro desconhecido')}")
        
        print()
        print(f"Graficos gerados: {success_count}/{len(results)}")
        return success_count > 0
        
    except Exception as e:
        print(f"[ERRO] Falha na geracao de graficos: {e}")
        return False

def generate_report():
    """Gerar relatório completo"""
    print("=" * 60)
    print("SRAG AI REPORTER -")
    print("=" * 60)
    print()
    
    try:
        from src.reports.report_generator import SRAGReportGenerator
        generator = SRAGReportGenerator()
        
        print("Gerando relatorio completo...")
        result = generator.generate_full_report()
        
        if result.get("status") == "success":
            print("[OK] Relatorio gerado")
            print()
            print(f"Relatorio HTML: {result['html_report']}")
            print(f"Dados JSON: {result['json_report']}")
            print()
            print("Graficos:")
            for chart_type, chart_result in result["charts"].items():
                if chart_result.get("status") == "success":
                    print(f"  - {chart_type}: {chart_result['path']}")
            print()
            print("Abra o arquivo HTML em seu navegador para visualizar.")
            return True
        else:
            print(f"[ERRO] Falha na geracao: {result.get('error', 'Erro desconhecido')}")
            return False
            
    except Exception as e:
        print(f"[ERRO] Falha na geracao de relatorio: {e}")
        return False

def run_agent():
    """Executar agente principal"""
    print("=" * 60)
    print("SRAG AI REPORTER - Agente Principal")
    print("=" * 60)
    print()
    
    try:
        from src.agents.srag_agent import SRAGAgent
        agent = SRAGAgent()
        
        print("Executando agente SRAG...")
        report = agent.generate_report()
        
        if report.get("status") == "completed":
            print("[OK] Analise concluida!")
            print()
            print("RESUMO:")
            print("-" * 40)
            print(report.get("executive_summary", "Não disponível"))
            print()
            
            print("METRICAS PRINCIPAIS:")
            print("-" * 40)
            for metric_name, metric_data in report.get("key_metrics", {}).items():
                if isinstance(metric_data, dict) and "value" in metric_data:
                    print(f"{metric_data['description']}: {metric_data['value']}{metric_data.get('unit', '')}")
            
            return True
        else:
            print(f"[ERRO] Falha na analise: {report.get('error', 'Erro desconhecido')}")
            return False
            
    except Exception as e:
        print(f"[ERRO] Falha na execucao do agente: {e}")
        return False

def run_full_pipeline():
    """Executar pipeline completo"""
    print("=" * 60)
    print("SRAG AI REPORTER - Pipeline Completo")
    print("=" * 60)
    print()
    
    # Verificar se sistema está configurado
    if not os.path.exists("src/data/srag_database.db"):
        print("Sistema nao configurado. Executando configuracao inicial...")
        if not setup_system():
            return False
        print()
    
    # Gerar relatório completo
    success = generate_report()
    
    if success:
        print()
        print("=" * 60)
        print("PIPELINE CONCLUIDO COM SUCESSO!")
        print("=" * 60)
        print()
        print("Próximos passos:")
        print("1. Abra o arquivo HTML gerado para visualizar o relatório")
        print("2. Revise as métricas e recomendações")
        print("3. Compartilhe com stakeholders relevantes")
        print("4. Configure execução automática se necessário")
    
    return success

def show_status():
    """Mostrar status do sistema"""
    print("=" * 60)
    print("SRAG AI REPORTER - Status do Sistema")
    print("=" * 60)
    print()
    
    # Verificar componentes
    components = {
        "Dados de amostra": "src/data/raw/srag_2023_sample.csv",
        "Dados processados": "src/data/processed/srag_processed.csv",
        "Banco de dados": "src/data/srag_database.db",
        "Estatísticas": "src/data/processed/summary_stats.txt"
    }
    
    all_ok = True
    for component, path in components.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"[OK] {component}: {path} ({size:,} bytes)")
        else:
            print(f"[FALTA] {component}: {path}")
            all_ok = False
    
    # Verificar relatórios
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        reports = [f for f in os.listdir(reports_dir) if f.endswith('.html')]
        print(f"\nRelatórios disponíveis: {len(reports)}")
        for report in sorted(reports)[-3:]:  # Últimos 3
            print(f"  - {report}")
    else:
        print("\n[FALTA] Diretório de relatórios")
        all_ok = False
    
    print()
    if all_ok:
        print("[OK] Sistema operacional!")
    else:
        print("[ATENÇÃO] Sistema precisa de configuração")
        print("Execute: python main.py --setup")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="SRAG AI Reporter - Sistema de IA Generativa para análise de SRAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --setup     # Configuração inicial
  python main.py --report    # Gerar relatório completo
  python main.py --charts    # Gerar apenas gráficos
  python main.py --agent     # Executar agente principal
  python main.py --all       # Pipeline completo
  python main.py --status    # Verificar status
        """
    )
    
    parser.add_argument("--setup", action="store_true", help="Configuração inicial do sistema")
    parser.add_argument("--report", action="store_true", help="Gerar relatório completo")
    parser.add_argument("--charts", action="store_true", help="Gerar apenas gráficos")
    parser.add_argument("--agent", action="store_true", help="Executar agente principal")
    parser.add_argument("--all", action="store_true", help="Executar pipeline completo")
    parser.add_argument("--status", action="store_true", help="Verificar status do sistema")
    
    args = parser.parse_args()
    
    # Se nenhum argumento foi fornecido, mostrar ajuda
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Executar comando solicitado
    success = True
    
    if args.status:
        show_status()
    elif args.setup:
        success = setup_system()
    elif args.charts:
        success = generate_charts()
    elif args.agent:
        success = run_agent()
    elif args.report:
        success = generate_report()
    elif args.all:
        success = run_full_pipeline()
    
    # Exit code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()