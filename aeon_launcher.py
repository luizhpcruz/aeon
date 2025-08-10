#!/usr/bin/env python3
"""
🚀 AEON LAUNCHER - Sistema Integrado de Execução
Executa todos os sistemas AEON em sequência automatizada
"""

import subprocess
import time
import sys
from datetime import datetime
import os
import json
import logging
import argparse


def executar_sistema(nome, arquivo, descricao, timeout, retries, logger):
    """Executa um sistema AEON com robustez (retries, timeout, logs)"""
    print(f"\n🔄 EXECUTANDO: {nome}")
    print(f"📄 Arquivo: {arquivo}")
    print(f"📋 Descrição: {descricao}")
    print("=" * 60)

    if not os.path.exists(arquivo):
        msg = f"Arquivo não encontrado: {arquivo}"
        print(f"❌ {nome} - {msg}")
        logger.error(msg)
        return False, 0.0, 0, "", msg

    attempts = 0
    last_err = ""
    while attempts <= retries:
        attempts += 1
        try:
            inicio = time.time()
            result = subprocess.run(
                [sys.executable, arquivo],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            duracao = time.time() - inicio

            if result.returncode == 0:
                print(f"✅ {nome} - SUCESSO ({duracao:.1f}s) [tentativa {attempts}]")
                logger.info(f"{nome} OK em {duracao:.1f}s")
                return True, duracao, attempts, result.stdout, ""
            else:
                last_err = (result.stderr or result.stdout or "").strip()
                print(f"❌ {nome} - ERRO (tentativa {attempts}): {last_err[:200]}")
                logger.warning(f"{nome} falhou (tentativa {attempts}): {last_err[:200]}")
        except subprocess.TimeoutExpired:
            last_err = f"Timeout >{timeout}s"
            print(f"⏰ {nome} - TIMEOUT (>{timeout}s) [tentativa {attempts}]")
            logger.warning(f"{nome} timeout (tentativa {attempts})")
        except Exception as e:
            last_err = str(e)
            print(f"💥 {nome} - EXCEÇÃO: {last_err}")
            logger.error(f"{nome} exceção (tentativa {attempts}): {last_err}")

        if attempts <= retries:
            time.sleep(1)  # pequeno intervalo entre tentativas

    return False, 0.0, attempts, "", last_err


def _setup_logger(log_path: str) -> logging.Logger:
    logger = logging.getLogger("aeon_launcher")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if log_path:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def _carregar_sistemas(config_path: str | None):
    # Padrão (fallback) preserva a lista existente
    padrao = [
        ("🧠 V.E.R.N.A.", "teste_simples.py", "Consciência emergente"),
        ("🌌 Cosmológico", "teste_cosmologia.py", "Análise do universo"),
        ("🔬 Entropia", "teste_entropia.py", "Evolução informacional"),
        ("🤖 AEON Cosma", "teste_aeon_cosma.py", "Motor de consciência"),
    ]
    if not config_path:
        return padrao

    try:
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            sistemas = []
            for item in data:
                sistemas.append((
                    item.get("nome") or item.get("name"),
                    item.get("arquivo") or item.get("file"),
                    item.get("descricao") or item.get("description", ""),
                ))
            return sistemas or padrao
    except Exception:
        # Em caso de erro, volta ao padrão
        return padrao
    return padrao


def main():
    """Launcher principal do ecossistema AEON"""
    parser = argparse.ArgumentParser(description="AEON Integrated Launcher")
    parser.add_argument("--timeout", type=int, default=30, help="Tempo limite por sistema (s)")
    parser.add_argument("--pause", type=float, default=2, help="Pausa entre execuções (s)")
    parser.add_argument("--retries", type=int, default=0, help="Repetições em caso de falha")
    parser.add_argument("--log", type=str, default="aeon_launcher.log", help="Arquivo de log")
    parser.add_argument("--report", type=str, default="aeon_report.json", help="Relatório JSON")
    parser.add_argument("--config", type=str, help="JSON com lista de sistemas")
    args = parser.parse_args()

    logger = _setup_logger(args.log)

    print("🌟 AEON INTEGRATED LAUNCHER")
    print(f"⏰ Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Sistemas para executar (pode vir de um JSON)
    sistemas = _carregar_sistemas(args.config)

    resultados = []
    relatorio = []

    # Executar cada sistema
    for nome, arquivo, descricao in sistemas:
        sucesso, duracao, tentativas, stdout, err = executar_sistema(
            nome, arquivo, descricao, timeout=args.timeout, retries=args.retries, logger=logger
        )
        resultados.append((nome, sucesso))
        relatorio.append({
            "nome": nome,
            "arquivo": arquivo,
            "descricao": descricao,
            "sucesso": sucesso,
            "duracao_s": round(duracao, 3),
            "tentativas": tentativas,
            "erro": (err or "")[:1000],
        })
        time.sleep(args.pause)

    # Relatório final
    print("\n" + "=" * 70)
    print("🎯 RELATÓRIO FINAL DE EXECUÇÃO")
    print("=" * 70)

    sucessos = 0
    for nome, sucesso in resultados:
        status = "✅ SUCESSO" if sucesso else "❌ FALHA"
        print(f"{nome}: {status}")
        if sucesso:
            sucessos += 1

    taxa_sucesso = (sucessos / len(sistemas)) * 100
    print(f"\n📊 Taxa de Sucesso: {sucessos}/{len(sistemas)} ({taxa_sucesso:.1f}%)")

    if taxa_sucesso >= 75:
        print("🎉 ECOSSISTEMA AEON: OPERACIONAL")
        print("✓ Sistemas principais funcionando")
        print("✓ Pronto para próxima fase")
    else:
        print("🔧 ECOSSISTEMA AEON: REQUER AJUSTES")
        print("⚠️ Alguns sistemas precisam correção")

    # Salva relatório estruturado (para CI/observabilidade)
    try:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(
                {"executado_em": datetime.now().isoformat(), "resultados": relatorio},
                f, ensure_ascii=False, indent=2
            )
        print(f"\n📝 Relatório salvo em: {args.report}")
    except Exception as e:
        logger.warning(f"Falha ao salvar relatório: {e}")

    print(f"\n🏁 Execução concluída em: {datetime.now().strftime('%H:%M:%S')}")
    # Código de saída: 0 se todos sucesso; 1 se houve falhas
    return 0 if sucessos == len(sistemas) else 1


if __name__ == "__main__":
    sys.exit(main())
