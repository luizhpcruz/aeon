import math
import hashlib
import os
import time
from datetime import datetime

class AEONBlockchain:
    """
    🔗 Módulo de Blockchain e Atomic Swap do AEON.
    Integra persistência criptográfica e troca de ativos cross-chain.
    """
    def __init__(self, carteira="0x0", wif="WIF_PADRAO"):
        self.carteira = carteira
        self.wif = wif
        self.arquivo_log = "config/blockchain.log"
        # Garantir que o diretório config existe
        os.makedirs(os.path.dirname(self.arquivo_log), exist_ok=True)
        
    def quebrar_bloco_bitwise(self, valor):
        """Usa deslocamento de bits para processamento de baixo nível."""
        return valor >> 1

    def obter_ultimo_hash(self):
        """Recupera o último hash da corrente para manter a integridade."""
        if not os.path.exists(self.arquivo_log) or os.stat(self.arquivo_log).st_size == 0:
            return "0" * 64  # Bloco Gênese
        
        try:
            with open(self.arquivo_log, "r", encoding="utf-8") as f:
                linhas = f.readlines()
                if linhas:
                    ultima_linha = linhas[-1].strip()
                    if "HASH: " in ultima_linha:
                        return ultima_linha.split("HASH: ")[1]
        except Exception:
            pass
        return "0" * 64

    def processar_e_salvar_bloco(self, sinal, peso):
        """Calcula ativação, assina e persiste o bloco na corrente."""
        hash_anterior = self.obter_ultimo_hash()
        
        soma = sinal * peso
        try:
            ativacao = math.tanh(soma)
        except OverflowError:
            ativacao = 1.0 if soma > 0 else -1.0
            
        dados_combustao = f"{ativacao:.6f}_{self.carteira}_{self.wif}_{hash_anterior}".encode('utf-8')
        novo_hash = hashlib.sha256(dados_combustao).hexdigest()
        
        if ativacao >= 0.99:
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            linha_registro = f"[{agora}] ATIVACAO: {ativacao:.6f} | ANTERIOR: {hash_anterior[:8]}... | HASH: {novo_hash}\n"
            
            with open(self.arquivo_log, "a", encoding="utf-8") as f:
                f.write(linha_registro)
            return novo_hash
        return None

    def criar_swap_cross_chain(self, segredo_secreto, tempo_validade_segundos=3600):
        """Cria uma trava criptográfica para Atomic Swap."""
        hash_trava = hashlib.sha256(segredo_secreto.encode('utf-8')).hexdigest()
        tempo_limite = time.time() + tempo_validade_segundos
        return {"hash_trava": hash_trava, "tempo_limite": tempo_limite, "segredo_original": segredo_secreto}

    def executar_swap_cross_chain(self, contrato, segredo_apresentado, carteira_destino):
        """Valida o segredo e o tempo para liberar o swap."""
        if time.time() > contrato["tempo_limite"]:
            return False
            
        hash_teste = hashlib.sha256(segredo_apresentado.encode('utf-8')).hexdigest()
        if hash_teste == contrato["hash_trava"]:
            return True
        return False
