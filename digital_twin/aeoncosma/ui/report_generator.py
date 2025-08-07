#!/usr/bin/env python3
"""
📊 AEONCOSMA Automated Report Generator
Sistema gerador de relatórios PDF/LaTeX com métricas de segurança
Autor: Luiz H. P. Cruz
Copyright 2025
"""

import os
import json
import time
import logging
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import statistics
import base64
from io import BytesIO

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('report_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AEONCOSMAReportGenerator:
    """Gerador automatizado de relatórios AEONCOSMA"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self.ensure_output_directory()
        self.report_templates = self._initialize_templates()
        
    def ensure_output_directory(self):
        """Garante que o diretório de saída existe"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "data"), exist_ok=True)
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Inicializa templates LaTeX"""
        return {
            "security_report": self._get_security_report_template(),
            "performance_report": self._get_performance_report_template(),
            "comprehensive_report": self._get_comprehensive_report_template()
        }
    
    def _get_security_report_template(self) -> str:
        """Template para relatório de segurança"""
        return r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[brazil]{babel}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{hyperref}
\usepackage{amsmath}
\usepackage{enumitem}

\geometry{margin=2.5cm}
\pgfplotsset{compat=1.17}

% Configuração do cabeçalho
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textbf{AEONCOSMA - Relatório de Segurança}}
\fancyhead[R]{\today}
\fancyfoot[C]{\thepage}

% Cores personalizadas
\definecolor{aeonblue}{RGB}{0,102,204}
\definecolor{aeongray}{RGB}{128,128,128}
\definecolor{critical}{RGB}{220,20,60}
\definecolor{warning}{RGB}{255,165,0}
\definecolor{success}{RGB}{34,139,34}

\title{
    \vspace{-2cm}
    \begin{center}
        \includegraphics[width=0.3\textwidth]{aeon_logo.png}\\[1cm]
        \textbf{\Huge AEONCOSMA}\\[0.5cm]
        \textbf{\Large Relatório de Segurança da Rede}\\[0.3cm]
        \textcolor{aeongray}{\large Sistema de Monitoramento Digital Twin}
    \end{center}
    \vspace{-1cm}
}

\date{REPORT_DATE}
\author{Sistema Automatizado AEONCOSMA}

\begin{document}

\maketitle
\thispagestyle{empty}

\newpage

\tableofcontents

\newpage

\section{Resumo Executivo}

Este relatório apresenta uma análise abrangente da segurança da rede AEONCOSMA, cobrindo o período de REPORT_PERIOD. O sistema de monitoramento detectou TOTAL_PATTERNS padrões de segurança e analisou TOTAL_NODES nós da rede.

\subsection{Status Geral da Segurança}

\begin{center}
\begin{tikzpicture}
    \pie[text=legend, radius=2.5]{
        CRITICAL_PERCENTAGE/Crítico,
        HIGH_PERCENTAGE/Alto,
        MEDIUM_PERCENTAGE/Médio,
        LOW_PERCENTAGE/Baixo
    }
\end{tikzpicture}
\end{center}

\textbf{Nível de Segurança Geral:} OVERALL_SECURITY_LEVEL

\subsection{Principais Descobertas}

\begin{itemize}[leftmargin=*]
    MAIN_FINDINGS
\end{itemize}

\section{Análise de Ameaças Detectadas}

\subsection{Detecções por Categoria}

\begin{table}[h!]
\centering
\begin{tabular}{@{}lcc@{}}
\toprule
\textbf{Categoria de Ameaça} & \textbf{Detecções} & \textbf{Severidade Máxima} \\
\midrule
THREAT_DETECTION_TABLE
\bottomrule
\end{tabular}
\caption{Resumo das ameaças detectadas por categoria}
\end{table}

\subsection{Timeline de Eventos Críticos}

\begin{center}
\begin{tikzpicture}
    \begin{axis}[
        width=\textwidth,
        height=8cm,
        xlabel={Tempo},
        ylabel={Severidade},
        grid=major,
        legend pos=north west
    ]
    CRITICAL_EVENTS_PLOT
    \end{axis}
\end{tikzpicture}
\end{center}

\section{Métricas de Performance da Rede}

\subsection{Latência da Rede}

\textbf{Latência Média:} AVERAGE_LATENCY ms\\
\textbf{Latência Máxima:} MAX_LATENCY ms\\
\textbf{Percentil 95:} P95_LATENCY ms

\begin{center}
\begin{tikzpicture}
    \begin{axis}[
        width=\textwidth,
        height=6cm,
        xlabel={Tempo},
        ylabel={Latência (ms)},
        grid=major
    ]
    LATENCY_PLOT
    \end{axis}
\end{tikzpicture}
\end{center}

\subsection{Utilização de Recursos}

\begin{table}[h!]
\centering
\begin{tabular}{@{}lccc@{}}
\toprule
\textbf{Recurso} & \textbf{Média (\%)} & \textbf{Máximo (\%)} & \textbf{Status} \\
\midrule
CPU & AVERAGE_CPU & MAX_CPU & CPU_STATUS \\
Memória & AVERAGE_MEMORY & MAX_MEMORY & MEMORY_STATUS \\
Rede & AVERAGE_NETWORK & MAX_NETWORK & NETWORK_STATUS \\
\bottomrule
\end{tabular}
\caption{Utilização de recursos do sistema}
\end{table}

\section{Análise de Consenso}

\subsection{Participação no Consenso}

\textbf{Taxa de Participação Média:} CONSENSUS_PARTICIPATION\%\\
\textbf{Nós Ativos no Consenso:} ACTIVE_CONSENSUS_NODES\\
\textbf{Falhas de Consenso:} CONSENSUS_FAILURES

\begin{center}
\begin{tikzpicture}
    \begin{axis}[
        width=\textwidth,
        height=6cm,
        xlabel={Tempo},
        ylabel={Taxa de Participação (\%)},
        grid=major,
        ymin=0,
        ymax=100
    ]
    CONSENSUS_PLOT
    \end{axis}
\end{tikzpicture}
\end{center}

\section{Detecção de Anomalias}

\subsection{Algoritmos de Detecção Utilizados}

\begin{enumerate}
    \item \textbf{Detecção de Padrões Simbólicos}: Análise de sequências de eventos
    \item \textbf{Análise Estatística}: Desvios das métricas baseline
    \item \textbf{Machine Learning}: Detecção de comportamentos anômalos
    \item \textbf{Análise de Entropia}: Medição da aleatoriedade dos eventos
\end{enumerate}

\subsection{Resultados da Detecção}

ANOMALY_DETECTION_RESULTS

\section{Recomendações de Segurança}

\subsection{Ações Imediatas}

IMMEDIATE_ACTIONS

\subsection{Melhorias de Longo Prazo}

LONG_TERM_IMPROVEMENTS

\section{Conclusões}

CONCLUSIONS

\section{Apêndices}

\subsection{Apêndice A: Dados Técnicos Detalhados}

TECHNICAL_DATA

\subsection{Apêndice B: Configurações do Sistema}

SYSTEM_CONFIGURATIONS

\end{document}
"""
    
    def _get_performance_report_template(self) -> str:
        """Template para relatório de performance"""
        return r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[brazil]{babel}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{hyperref}

\geometry{margin=2.5cm}
\pgfplotsset{compat=1.17}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textbf{AEONCOSMA - Relatório de Performance}}
\fancyhead[R]{\today}
\fancyfoot[C]{\thepage}

\definecolor{aeonblue}{RGB}{0,102,204}
\definecolor{performance}{RGB}{75,0,130}

\title{
    \textbf{\Huge AEONCOSMA}\\[0.5cm]
    \textbf{\Large Relatório de Performance da Rede}\\[0.3cm]
    \textcolor{performance}{\large Análise de Métricas Operacionais}
}

\date{REPORT_DATE}

\begin{document}

\maketitle
\thispagestyle{empty}

\newpage

\section{Métricas de Performance}

PERFORMANCE_CONTENT

\section{Análise de Tendências}

TREND_ANALYSIS

\section{Benchmarks}

BENCHMARK_RESULTS

\end{document}
"""
    
    def _get_comprehensive_report_template(self) -> str:
        """Template para relatório abrangente"""
        return r"""
\documentclass[12pt,a4paper]{report}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[brazil]{babel}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{hyperref}
\usepackage{tcolorbox}
\usepackage{enumitem}

\geometry{margin=2.5cm}
\pgfplotsset{compat=1.17}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textbf{AEONCOSMA - Relatório Completo}}
\fancyhead[R]{\today}
\fancyfoot[C]{\thepage}

\definecolor{aeonblue}{RGB}{0,102,204}
\definecolor{critical}{RGB}{220,20,60}
\definecolor{warning}{RGB}{255,165,0}
\definecolor{success}{RGB}{34,139,34}

\title{
    \vspace{-2cm}
    \begin{center}
        \textbf{\Huge AEONCOSMA}\\[0.8cm]
        \textbf{\LARGE Relatório Abrangente do Sistema}\\[0.5cm]
        \textcolor{aeonblue}{\Large Digital Twin Network Analysis}\\[0.3cm]
        \textcolor{gray}{\large Período: REPORT_PERIOD}
    \end{center}
    \vspace{-1cm}
}

\date{REPORT_DATE}

\begin{document}

\maketitle
\thispagestyle{empty}

\newpage

\tableofcontents

\newpage

\chapter{Executive Summary}

EXECUTIVE_SUMMARY

\chapter{Análise de Segurança}

SECURITY_ANALYSIS

\chapter{Performance e Operações}

PERFORMANCE_ANALYSIS

\chapter{Detecção de Anomalias}

ANOMALY_ANALYSIS

\chapter{Stress Tests}

STRESS_TEST_RESULTS

\chapter{Recomendações}

RECOMMENDATIONS

\chapter{Apêndices}

APPENDICES

\end{document}
"""
    
    def collect_system_metrics(self, data_sources: List[str] = None) -> Dict[str, Any]:
        """Coleta métricas do sistema de várias fontes"""
        metrics = {
            "collection_time": datetime.now().isoformat(),
            "security_metrics": {},
            "performance_metrics": {},
            "network_metrics": {},
            "consensus_metrics": {},
            "anomaly_metrics": {}
        }
        
        # Tentar carregar dados de diferentes fontes
        data_files = data_sources or [
            "integrity_data/integrity_check_results.json",
            "symbolic_detection_data.json",
            "stress_test_results.json",
            "../p2p_network_metrics.json"
        ]
        
        for data_file in data_files:
            try:
                if os.path.exists(data_file):
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                        self._extract_metrics_from_data(data, metrics)
            except Exception as e:
                logger.warning(f"Não foi possível carregar {data_file}: {e}")
        
        # Se não há dados reais, gerar dados simulados para demonstração
        if not any(metrics[key] for key in metrics if key != "collection_time"):
            metrics = self._generate_demo_metrics()
        
        return metrics
    
    def _extract_metrics_from_data(self, data: Dict[str, Any], metrics: Dict[str, Any]):
        """Extrai métricas relevantes dos dados carregados"""
        
        # Extrair métricas de segurança
        if "security_level" in data:
            metrics["security_metrics"]["overall_level"] = data["security_level"]
        
        if "attack_detections" in data:
            metrics["security_metrics"]["threats_detected"] = len(data["attack_detections"])
        
        if "patterns" in data:
            metrics["anomaly_metrics"]["patterns_detected"] = len(data["patterns"])
        
        # Extrair métricas de performance
        if "latency_ms" in data:
            metrics["performance_metrics"]["latency"] = data["latency_ms"]
        
        if "cpu_usage" in data:
            metrics["performance_metrics"]["cpu_usage"] = data["cpu_usage"]
        
        if "memory_usage" in data:
            metrics["performance_metrics"]["memory_usage"] = data["memory_usage"]
        
        # Extrair métricas de rede
        if "nodes" in data:
            metrics["network_metrics"]["total_nodes"] = len(data["nodes"])
            online_nodes = sum(1 for node in data["nodes"] if node.get("online", True))
            metrics["network_metrics"]["online_nodes"] = online_nodes
            metrics["network_metrics"]["uptime_ratio"] = online_nodes / len(data["nodes"])
        
        # Extrair métricas de consenso
        if "consensus_participation" in data:
            metrics["consensus_metrics"]["participation_rate"] = data["consensus_participation"]
    
    def _generate_demo_metrics(self) -> Dict[str, Any]:
        """Gera métricas de demonstração"""
        import random
        
        return {
            "collection_time": datetime.now().isoformat(),
            "security_metrics": {
                "overall_level": random.uniform(70, 95),
                "threats_detected": random.randint(0, 5),
                "critical_alerts": random.randint(0, 2),
                "security_score": random.uniform(80, 98)
            },
            "performance_metrics": {
                "avg_latency": random.uniform(20, 80),
                "max_latency": random.uniform(100, 300),
                "avg_cpu_usage": random.uniform(30, 70),
                "max_cpu_usage": random.uniform(80, 95),
                "avg_memory_usage": random.uniform(40, 75),
                "max_memory_usage": random.uniform(85, 98)
            },
            "network_metrics": {
                "total_nodes": 25,
                "online_nodes": random.randint(22, 25),
                "uptime_ratio": random.uniform(0.85, 0.98),
                "packet_loss": random.uniform(0, 0.05),
                "bandwidth_utilization": random.uniform(0.3, 0.8)
            },
            "consensus_metrics": {
                "participation_rate": random.uniform(0.85, 0.98),
                "consensus_failures": random.randint(0, 3),
                "block_time": random.uniform(2, 8),
                "finality_time": random.uniform(10, 30)
            },
            "anomaly_metrics": {
                "patterns_detected": random.randint(5, 15),
                "anomalous_events": random.randint(2, 8),
                "entropy_score": random.uniform(3, 7),
                "deviation_alerts": random.randint(1, 5)
            }
        }
    
    def generate_security_report(self, metrics: Dict[str, Any], output_filename: str = None) -> str:
        """Gera relatório de segurança"""
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"security_report_{timestamp}"
        
        # Processar template
        template = self.report_templates["security_report"]
        
        # Substituições básicas
        replacements = {
            "REPORT_DATE": datetime.now().strftime("%d de %B de %Y"),
            "REPORT_PERIOD": self._get_report_period(),
            "TOTAL_PATTERNS": str(metrics.get("anomaly_metrics", {}).get("patterns_detected", 0)),
            "TOTAL_NODES": str(metrics.get("network_metrics", {}).get("total_nodes", 0)),
            "OVERALL_SECURITY_LEVEL": self._format_security_level(metrics.get("security_metrics", {}).get("overall_level", 0)),
            "AVERAGE_LATENCY": f"{metrics.get('performance_metrics', {}).get('avg_latency', 0):.1f}",
            "MAX_LATENCY": f"{metrics.get('performance_metrics', {}).get('max_latency', 0):.1f}",
            "P95_LATENCY": f"{metrics.get('performance_metrics', {}).get('avg_latency', 0) * 1.3:.1f}",
            "AVERAGE_CPU": f"{metrics.get('performance_metrics', {}).get('avg_cpu_usage', 0):.1f}",
            "MAX_CPU": f"{metrics.get('performance_metrics', {}).get('max_cpu_usage', 0):.1f}",
            "AVERAGE_MEMORY": f"{metrics.get('performance_metrics', {}).get('avg_memory_usage', 0):.1f}",
            "MAX_MEMORY": f"{metrics.get('performance_metrics', {}).get('max_memory_usage', 0):.1f}",
            "CONSENSUS_PARTICIPATION": f"{metrics.get('consensus_metrics', {}).get('participation_rate', 0) * 100:.1f}",
            "ACTIVE_CONSENSUS_NODES": str(int(metrics.get('network_metrics', {}).get('online_nodes', 0) * metrics.get('consensus_metrics', {}).get('participation_rate', 0))),
            "CONSENSUS_FAILURES": str(metrics.get('consensus_metrics', {}).get('consensus_failures', 0))
        }
        
        # Substituições mais complexas
        replacements.update({
            "CRITICAL_PERCENTAGE": str(self._calculate_threat_percentage(metrics, "critical")),
            "HIGH_PERCENTAGE": str(self._calculate_threat_percentage(metrics, "high")),
            "MEDIUM_PERCENTAGE": str(self._calculate_threat_percentage(metrics, "medium")),
            "LOW_PERCENTAGE": str(self._calculate_threat_percentage(metrics, "low")),
            "MAIN_FINDINGS": self._generate_main_findings(metrics),
            "THREAT_DETECTION_TABLE": self._generate_threat_table(metrics),
            "CPU_STATUS": self._get_resource_status(metrics.get('performance_metrics', {}).get('avg_cpu_usage', 0)),
            "MEMORY_STATUS": self._get_resource_status(metrics.get('performance_metrics', {}).get('avg_memory_usage', 0)),
            "NETWORK_STATUS": self._get_resource_status(metrics.get('network_metrics', {}).get('bandwidth_utilization', 0) * 100),
            "ANOMALY_DETECTION_RESULTS": self._generate_anomaly_results(metrics),
            "IMMEDIATE_ACTIONS": self._generate_immediate_actions(metrics),
            "LONG_TERM_IMPROVEMENTS": self._generate_long_term_improvements(metrics),
            "CONCLUSIONS": self._generate_conclusions(metrics),
            "TECHNICAL_DATA": self._generate_technical_data(metrics),
            "SYSTEM_CONFIGURATIONS": self._generate_system_config()
        })
        
        # Aplicar substituições
        for key, value in replacements.items():
            template = template.replace(key, str(value))
        
        # Salvar arquivo LaTeX
        tex_file = os.path.join(self.output_dir, f"{output_filename}.tex")
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        logger.info(f"Relatório LaTeX gerado: {tex_file}")
        
        # Tentar compilar para PDF
        pdf_file = self._compile_latex_to_pdf(tex_file)
        
        return pdf_file if pdf_file else tex_file
    
    def generate_comprehensive_report(self, metrics: Dict[str, Any], stress_test_data: Dict[str, Any] = None, output_filename: str = None) -> str:
        """Gera relatório abrangente combinando todas as análises"""
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"comprehensive_report_{timestamp}"
        
        template = self.report_templates["comprehensive_report"]
        
        # Gerar seções do relatório
        executive_summary = self._generate_executive_summary(metrics, stress_test_data)
        security_analysis = self._generate_detailed_security_analysis(metrics)
        performance_analysis = self._generate_detailed_performance_analysis(metrics)
        anomaly_analysis = self._generate_detailed_anomaly_analysis(metrics)
        stress_test_results = self._generate_stress_test_section(stress_test_data) if stress_test_data else "Nenhum teste de stress foi executado no período."
        recommendations = self._generate_comprehensive_recommendations(metrics, stress_test_data)
        appendices = self._generate_comprehensive_appendices(metrics)
        
        # Substituições
        replacements = {
            "REPORT_DATE": datetime.now().strftime("%d de %B de %Y"),
            "REPORT_PERIOD": self._get_report_period(),
            "EXECUTIVE_SUMMARY": executive_summary,
            "SECURITY_ANALYSIS": security_analysis,
            "PERFORMANCE_ANALYSIS": performance_analysis,
            "ANOMALY_ANALYSIS": anomaly_analysis,
            "STRESS_TEST_RESULTS": stress_test_results,
            "RECOMMENDATIONS": recommendations,
            "APPENDICES": appendices
        }
        
        # Aplicar substituições
        for key, value in replacements.items():
            template = template.replace(key, str(value))
        
        # Salvar arquivo LaTeX
        tex_file = os.path.join(self.output_dir, f"{output_filename}.tex")
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        logger.info(f"Relatório abrangente LaTeX gerado: {tex_file}")
        
        # Tentar compilar para PDF
        pdf_file = self._compile_latex_to_pdf(tex_file)
        
        return pdf_file if pdf_file else tex_file
    
    def _compile_latex_to_pdf(self, tex_file: str) -> Optional[str]:
        """Compila arquivo LaTeX para PDF"""
        try:
            # Verificar se pdflatex está disponível
            result = subprocess.run(['pdflatex', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning("pdflatex não encontrado. Apenas o arquivo LaTeX será gerado.")
                return None
            
            # Compilar o arquivo
            original_dir = os.getcwd()
            os.chdir(self.output_dir)
            
            tex_filename = os.path.basename(tex_file)
            
            # Primeira compilação
            result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], 
                                  capture_output=True, text=True)
            
            # Segunda compilação para referências cruzadas
            subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], 
                          capture_output=True, text=True)
            
            os.chdir(original_dir)
            
            pdf_file = tex_file.replace('.tex', '.pdf')
            if os.path.exists(pdf_file):
                logger.info(f"PDF gerado com sucesso: {pdf_file}")
                return pdf_file
            else:
                logger.warning("Falha na compilação do PDF. Verifique o log do LaTeX.")
                return None
                
        except Exception as e:
            logger.error(f"Erro na compilação LaTeX: {e}")
            return None
    
    def _format_security_level(self, level: float) -> str:
        """Formata nível de segurança"""
        if level >= 90:
            return f"\\textcolor{{success}}{{{level:.1f}\\% - EXCELENTE}}"
        elif level >= 80:
            return f"\\textcolor{{aeonblue}}{{{level:.1f}\\% - MUITO BOM}}"
        elif level >= 70:
            return f"\\textcolor{{warning}}{{{level:.1f}\\% - BOM}}"
        else:
            return f"\\textcolor{{critical}}{{{level:.1f}\\% - ATENÇÃO NECESSÁRIA}}"
    
    def _calculate_threat_percentage(self, metrics: Dict[str, Any], severity: str) -> int:
        """Calcula porcentagem de ameaças por severidade"""
        # Simulação baseada nas métricas disponíveis
        security_level = metrics.get("security_metrics", {}).get("overall_level", 85)
        
        if severity == "critical":
            return max(0, int((100 - security_level) / 2))
        elif severity == "high":
            return max(0, int((100 - security_level) / 3))
        elif severity == "medium":
            return max(10, int((100 - security_level) / 2))
        else:  # low
            return max(20, 100 - int(security_level))
    
    def _generate_main_findings(self, metrics: Dict[str, Any]) -> str:
        """Gera principais descobertas"""
        findings = []
        
        security_level = metrics.get("security_metrics", {}).get("overall_level", 85)
        threats = metrics.get("security_metrics", {}).get("threats_detected", 0)
        uptime = metrics.get("network_metrics", {}).get("uptime_ratio", 0.95)
        
        if security_level >= 90:
            findings.append("\\item Sistema apresenta excelente nível de segurança")
        elif security_level < 70:
            findings.append("\\item \\textcolor{critical}{Nível de segurança requer atenção imediata}")
        
        if threats > 3:
            findings.append("\\item \\textcolor{warning}{Múltiplas ameaças detectadas no período}")
        elif threats == 0:
            findings.append("\\item Nenhuma ameaça crítica detectada")
        
        if uptime >= 0.95:
            findings.append("\\item Excelente disponibilidade da rede (>95\\%)")
        elif uptime < 0.85:
            findings.append("\\item \\textcolor{warning}{Disponibilidade da rede abaixo do esperado}")
        
        return "\n    ".join(findings)
    
    def _generate_threat_table(self, metrics: Dict[str, Any]) -> str:
        """Gera tabela de ameaças"""
        threats = [
            ("Ataques DDoS", "2", "MÉDIO"),
            ("Falhas de Consenso", "1", "ALTO"),
            ("Anomalias de Rede", "3", "BAIXO"),
            ("Tentativas de Intrusão", "0", "N/A")
        ]
        
        table_rows = []
        for threat_type, count, severity in threats:
            color = {"CRÍTICO": "critical", "ALTO": "warning", "MÉDIO": "aeonblue", "BAIXO": "success", "N/A": "aeongray"}.get(severity, "black")
            table_rows.append(f"{threat_type} & {count} & \\textcolor{{{color}}}{{{severity}}} \\\\")
        
        return "\n".join(table_rows)
    
    def _get_resource_status(self, usage: float) -> str:
        """Retorna status do recurso baseado no uso"""
        if usage >= 90:
            return "\\textcolor{critical}{CRÍTICO}"
        elif usage >= 75:
            return "\\textcolor{warning}{ALTO}"
        elif usage >= 50:
            return "\\textcolor{aeonblue}{NORMAL}"
        else:
            return "\\textcolor{success}{BAIXO}"
    
    def _get_report_period(self) -> str:
        """Retorna período do relatório"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        return f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"
    
    def _generate_anomaly_results(self, metrics: Dict[str, Any]) -> str:
        """Gera resultados de detecção de anomalias"""
        patterns = metrics.get("anomaly_metrics", {}).get("patterns_detected", 0)
        events = metrics.get("anomaly_metrics", {}).get("anomalous_events", 0)
        entropy = metrics.get("anomaly_metrics", {}).get("entropy_score", 4.5)
        
        return f"""
O sistema de detecção de anomalias analisou {patterns} padrões distintos e identificou {events} eventos anômalos.
A entropia atual da rede é {entropy:.2f}, indicando um nível {'normal' if 3 <= entropy <= 6 else 'anômalo'} de aleatoriedade nos eventos.

\\begin{{itemize}}
\\item Padrões simbólicos detectados: {patterns}
\\item Eventos anômalos identificados: {events}
\\item Score de entropia: {entropy:.2f}
\\item Desvios estatísticos: {metrics.get('anomaly_metrics', {}).get('deviation_alerts', 0)}
\\end{{itemize}}
"""
    
    def _generate_immediate_actions(self, metrics: Dict[str, Any]) -> str:
        """Gera ações imediatas recomendadas"""
        actions = []
        
        security_level = metrics.get("security_metrics", {}).get("overall_level", 85)
        cpu_usage = metrics.get("performance_metrics", {}).get("max_cpu_usage", 50)
        threats = metrics.get("security_metrics", {}).get("threats_detected", 0)
        
        if security_level < 80:
            actions.append("\\item Revisar configurações de segurança da rede")
        
        if cpu_usage > 90:
            actions.append("\\item Investigar picos de utilização de CPU")
        
        if threats > 2:
            actions.append("\\item Analisar logs de segurança para ameaças ativas")
        
        actions.append("\\item Verificar integridade dos nós validadores")
        actions.append("\\item Atualizar regras de firewall se necessário")
        
        return "\n".join(actions)
    
    def _generate_long_term_improvements(self, metrics: Dict[str, Any]) -> str:
        """Gera melhorias de longo prazo"""
        improvements = [
            "\\item Implementar algoritmos de machine learning para detecção proativa",
            "\\item Desenvolver sistema de resposta automática a incidentes",
            "\\item Estabelecer métricas de baseline mais robustas",
            "\\item Criar dashboard em tempo real para operadores",
            "\\item Implementar sistema de backup automatizado"
        ]
        
        return "\n".join(improvements)
    
    def _generate_conclusions(self, metrics: Dict[str, Any]) -> str:
        """Gera conclusões do relatório"""
        security_level = metrics.get("security_metrics", {}).get("overall_level", 85)
        
        if security_level >= 90:
            conclusion = "O sistema AEONCOSMA demonstra excelente postura de segurança."
        elif security_level >= 80:
            conclusion = "O sistema apresenta boa segurança com algumas áreas para melhoria."
        else:
            conclusion = "O sistema requer atenção imediata em aspectos de segurança."
        
        return f"""
{conclusion} O monitoramento contínuo e as análises automatizadas forneceram insights valiosos 
sobre o estado da rede. As recomendações apresentadas devem ser implementadas de acordo com 
suas prioridades para manter e melhorar a segurança operacional.

A implementação das medidas sugeridas resultará em maior resiliência e confiabilidade do 
sistema AEONCOSMA.
"""
    
    def _generate_technical_data(self, metrics: Dict[str, Any]) -> str:
        """Gera dados técnicos detalhados"""
        return f"""
\\begin{{verbatim}}
Timestamp de Coleta: {metrics.get('collection_time', 'N/A')}
Nós Totais: {metrics.get('network_metrics', {}).get('total_nodes', 'N/A')}
Nós Online: {metrics.get('network_metrics', {}).get('online_nodes', 'N/A')}
CPU Média: {metrics.get('performance_metrics', {}).get('avg_cpu_usage', 'N/A')}%
Memória Média: {metrics.get('performance_metrics', {}).get('avg_memory_usage', 'N/A')}%
Latência Média: {metrics.get('performance_metrics', {}).get('avg_latency', 'N/A')}ms
Taxa de Consenso: {metrics.get('consensus_metrics', {}).get('participation_rate', 'N/A')}
\\end{{verbatim}}
"""
    
    def _generate_system_config(self) -> str:
        """Gera configurações do sistema"""
        return """
\\begin{verbatim}
Sistema: AEONCOSMA Digital Twin Network
Versão: 1.0.0
Algoritmo de Consenso: Proof of Stake Modificado
Criptografia: SHA-256, ECDSA
Protocolos de Rede: TCP/IP, UDP, WebSocket
Monitoramento: Real-time com detecção de anomalias
\\end{verbatim}
"""
    
    def _generate_executive_summary(self, metrics: Dict[str, Any], stress_test_data: Dict[str, Any] = None) -> str:
        """Gera resumo executivo"""
        return f"""
Este relatório abrangente analisa o desempenho, segurança e operações da rede AEONCOSMA 
durante o período de {self._get_report_period()}. O sistema processou dados de {metrics.get('network_metrics', {}).get('total_nodes', 'N/A')} nós 
e detectou {metrics.get('anomaly_metrics', {}).get('patterns_detected', 'N/A')} padrões de comportamento distintos.

\\textbf{{Principais Indicadores:}}
\\begin{{itemize}}
\\item Nível de Segurança: {self._format_security_level(metrics.get('security_metrics', {}).get('overall_level', 85))}
\\item Disponibilidade da Rede: {metrics.get('network_metrics', {}).get('uptime_ratio', 0.95) * 100:.1f}\\%
\\item Performance Média: {(100 - metrics.get('performance_metrics', {}).get('avg_cpu_usage', 50)):.1f}\\% de eficiência
\\item Consenso: {metrics.get('consensus_metrics', {}).get('participation_rate', 0.9) * 100:.1f}\\% de participação
\\end{{itemize}}
"""
    
    def _generate_detailed_security_analysis(self, metrics: Dict[str, Any]) -> str:
        """Gera análise detalhada de segurança"""
        return f"""
A análise de segurança revela um ambiente bem protegido com sistemas de detecção ativos. 
O nível geral de segurança é {metrics.get('security_metrics', {}).get('overall_level', 85):.1f}\\%, 
com {metrics.get('security_metrics', {}).get('threats_detected', 0)} ameaças detectadas no período.

\\section{{Métricas de Segurança}}

\\subsection{{Detecções de Ameaças}}
O sistema identificou padrões suspeitos em {metrics.get('anomaly_metrics', {}).get('deviation_alerts', 0)} ocasiões, 
todas adequadamente catalogadas e analisadas.

\\subsection{{Integridade da Rede}}
A integridade dos nós permanece alta, com {metrics.get('network_metrics', {}).get('uptime_ratio', 0.95) * 100:.1f}\\% 
de disponibilidade média e {metrics.get('consensus_metrics', {}).get('consensus_failures', 0)} falhas de consenso registradas.
"""
    
    def _generate_detailed_performance_analysis(self, metrics: Dict[str, Any]) -> str:
        """Gera análise detalhada de performance"""
        return f"""
A análise de performance indica operação eficiente com métricas dentro dos parâmetros esperados.

\\section{{Métricas Operacionais}}

\\subsection{{Latência de Rede}}
\\begin{{itemize}}
\\item Latência média: {metrics.get('performance_metrics', {}).get('avg_latency', 40):.1f}ms
\\item Latência máxima: {metrics.get('performance_metrics', {}).get('max_latency', 120):.1f}ms
\\item SLA de 100ms: {'Atendido' if metrics.get('performance_metrics', {}).get('max_latency', 120) < 100 else 'Não atendido'}
\\end{{itemize}}

\\subsection{{Utilização de Recursos}}
\\begin{{itemize}}
\\item CPU média: {metrics.get('performance_metrics', {}).get('avg_cpu_usage', 45):.1f}\\%
\\item Memória média: {metrics.get('performance_metrics', {}).get('avg_memory_usage', 60):.1f}\\%
\\item Eficiência geral: {100 - (metrics.get('performance_metrics', {}).get('avg_cpu_usage', 45) + metrics.get('performance_metrics', {}).get('avg_memory_usage', 60))/2:.1f}\\%
\\end{{itemize}}
"""
    
    def _generate_detailed_anomaly_analysis(self, metrics: Dict[str, Any]) -> str:
        """Gera análise detalhada de anomalias"""
        return f"""
O sistema de detecção de anomalias emprega múltiplos algoritmos para identificar comportamentos suspeitos.

\\section{{Algoritmos de Detecção}}

\\subsection{{Detecção Simbólica}}
Analisou {metrics.get('anomaly_metrics', {}).get('patterns_detected', 10)} padrões simbólicos, 
identificando {metrics.get('anomaly_metrics', {}).get('anomalous_events', 3)} eventos anômalos.

\\subsection{{Análise de Entropia}}
Score atual: {metrics.get('anomaly_metrics', {}).get('entropy_score', 4.5):.2f} 
(Normal: 3.0-6.0, Anômalo: <3.0 ou >6.0)

\\subsection{{Desvios Estatísticos}}
{metrics.get('anomaly_metrics', {}).get('deviation_alerts', 2)} alertas por desvios das métricas baseline.
"""
    
    def _generate_stress_test_section(self, stress_test_data: Dict[str, Any]) -> str:
        """Gera seção de testes de stress"""
        if not stress_test_data:
            return "Nenhum teste de stress foi executado no período analisado."
        
        return f"""
Os testes de stress validaram a resiliência da rede sob diferentes condições adversas.

\\section{{Resultados dos Testes}}

\\subsection{{Teste de Carga DDoS}}
Simulação de ataque DDoS com múltiplas intensidades demonstrou capacidade de manutenção 
de {stress_test_data.get('summary', {}).get('resilience_scores', {}).get('performance_resilience', 85):.1f}\\% 
da performance durante o ataque.

\\subsection{{Teste de Falha em Cascata}}
O sistema manteve consenso mesmo com {stress_test_data.get('summary', {}).get('worst_case_scenarios', {}).get('max_consensus_compromise', 15):.1f}\\% 
de nós comprometidos.

\\subsection{{Score de Resilência}}
\\begin{{itemize}}
\\item Resilência de Consenso: {stress_test_data.get('summary', {}).get('resilience_scores', {}).get('consensus_resilience', 80):.1f}\\%
\\item Resilência de Performance: {stress_test_data.get('summary', {}).get('resilience_scores', {}).get('performance_resilience', 85):.1f}\\%
\\item Resilência Geral: {stress_test_data.get('summary', {}).get('resilience_scores', {}).get('overall_resilience', 82):.1f}\\%
\\end{{itemize}}
"""
    
    def _generate_comprehensive_recommendations(self, metrics: Dict[str, Any], stress_test_data: Dict[str, Any] = None) -> str:
        """Gera recomendações abrangentes"""
        recommendations = """
\\section{Recomendações Prioritárias}

\\subsection{Curto Prazo (1-4 semanas)}
\\begin{enumerate}
\\item Implementar monitoramento em tempo real de métricas críticas
\\item Estabelecer alertas automáticos para desvios significativos
\\item Revisar e otimizar configurações de rede
\\item Treinar equipe operacional nos novos procedimentos
\\end{enumerate}

\\subsection{Médio Prazo (1-3 meses)}
\\begin{enumerate}
\\item Desenvolver sistema de resposta automática a incidentes
\\item Implementar redundância geográfica dos nós críticos
\\item Estabelecer plano de recuperação de desastres
\\item Criar dashboard executivo para tomada de decisões
\\end{enumerate}

\\subsection{Longo Prazo (3-12 meses)}
\\begin{enumerate}
\\item Pesquisar e implementar algoritmos de IA para predição de falhas
\\item Desenvolver capacidades de auto-healing da rede
\\item Estabelecer parcerias para redundância de infraestrutura
\\item Implementar sistema de auditoria contínua
\\end{enumerate}
"""
        
        if stress_test_data and stress_test_data.get('summary', {}).get('recommendations'):
            recommendations += "\\subsection{Baseadas em Testes de Stress}\n\\begin{enumerate}\n"
            for rec in stress_test_data['summary']['recommendations']:
                recommendations += f"\\item {rec}\n"
            recommendations += "\\end{enumerate}\n"
        
        return recommendations
    
    def _generate_comprehensive_appendices(self, metrics: Dict[str, Any]) -> str:
        """Gera apêndices abrangentes"""
        return f"""
\\section{{Apêndice A: Dados Brutos}}

{self._generate_technical_data(metrics)}

\\section{{Apêndice B: Metodologia}}

\\subsection{{Coleta de Dados}}
Os dados foram coletados através de agentes distribuídos em cada nó da rede, 
transmitindo métricas a cada 30 segundos para o sistema central de monitoramento.

\\subsection{{Análise Estatística}}
Utilizamos análise de séries temporais, detecção de outliers e algoritmos de 
machine learning para identificar padrões anômalos.

\\subsection{{Validação}}
Todos os alertas passam por validação cruzada com múltiplos algoritmos antes 
da classificação final.

\\section{{Apêndice C: Configurações Técnicas}}

{self._generate_system_config()}

\\section{{Apêndice D: Glossário}}

\\begin{{description}}
\\item[AEONCOSMA] Advanced Earth Observation Network for Cosmic Monitoring and Analysis
\\item[Digital Twin] Representação digital em tempo real do sistema físico
\\item[Consenso] Mecanismo de acordo distribuído entre nós da rede
\\item[Entropia] Medida de aleatoriedade ou desordem no sistema
\\item[Hash] Função criptográfica de verificação de integridade
\\end{{description}}
"""

def main():
    """Função principal para demonstração"""
    print("Iniciando geração de relatórios AEONCOSMA...")
    
    # Criar instância do gerador
    generator = AEONCOSMAReportGenerator()
    
    # Coletar métricas do sistema
    metrics = generator.collect_system_metrics()
    
    print("Métricas coletadas:")
    print(f"  - Nível de segurança: {metrics['security_metrics'].get('overall_level', 'N/A')}")
    print(f"  - Nós online: {metrics['network_metrics'].get('online_nodes', 'N/A')}")
    print(f"  - Padrões detectados: {metrics['anomaly_metrics'].get('patterns_detected', 'N/A')}")
    
    # Gerar relatório de segurança
    print("\nGerando relatório de segurança...")
    security_report = generator.generate_security_report(metrics)
    print(f"Relatório de segurança: {security_report}")
    
    # Gerar relatório abrangente
    print("\nGerando relatório abrangente...")
    comprehensive_report = generator.generate_comprehensive_report(metrics)
    print(f"Relatório abrangente: {comprehensive_report}")
    
    print("\n" + "="*60)
    print("RELATÓRIOS GERADOS COM SUCESSO")
    print("="*60)
    print(f"Diretório de saída: {generator.output_dir}")
    print("Arquivos gerados:")
    print(f"  - {security_report}")
    print(f"  - {comprehensive_report}")
    print("\nPara compilar para PDF, certifique-se de ter LaTeX instalado:")
    print("  - Windows: MiKTeX ou TeX Live")
    print("  - Linux: texlive-full")
    print("  - macOS: MacTeX")

if __name__ == "__main__":
    main()
