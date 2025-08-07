"""
VERITAS - Sistema Inteligente de Validação de Riscos e Tarefas Autônomas com Segurança
Módulo de Geração de QR Code e Verificação de Integridade
"""

import qrcode
import hashlib
import json
from datetime import datetime
from io import BytesIO
import base64

class VeritasDocumentValidator:
    def __init__(self):
        self.blockchain = []  # Simula blockchain local
        
    def generate_document_hash(self, document_data: dict) -> str:
        """Gera hash SHA256 do documento"""
        doc_string = json.dumps(document_data, sort_keys=True)
        return hashlib.sha256(doc_string.encode()).hexdigest()
    
    def create_qr_code(self, document_hash: str, document_id: str) -> str:
        """Cria QR Code com hash do documento para verificação"""
        qr_data = {
            "document_id": document_id,
            "hash": document_hash,
            "timestamp": datetime.now().isoformat(),
            "veritas_version": "1.0",
            "validation_url": f"https://veritas.aeon.com/verify/{document_id}"
        }
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str
    
    def validate_document_integrity(self, document_data: dict, provided_hash: str) -> dict:
        """Valida integridade do documento comparando hashes"""
        calculated_hash = self.generate_document_hash(document_data)
        is_valid = calculated_hash == provided_hash
        
        return {
            "is_valid": is_valid,
            "calculated_hash": calculated_hash,
            "provided_hash": provided_hash,
            "validation_timestamp": datetime.now().isoformat(),
            "status": "ÍNTEGRO" if is_valid else "COMPROMETIDO"
        }
    
    def add_to_blockchain(self, document_data: dict) -> dict:
        """Adiciona documento à blockchain local para auditoria"""
        previous_hash = self.blockchain[-1]["hash"] if self.blockchain else "0"
        
        block = {
            "index": len(self.blockchain),
            "timestamp": datetime.now().isoformat(),
            "document_id": document_data.get("document_id"),
            "document_hash": self.generate_document_hash(document_data),
            "previous_hash": previous_hash,
            "action": "CREATE",
            "user": document_data.get("user", "system")
        }
        
        block["hash"] = self.generate_document_hash(block)
        self.blockchain.append(block)
        
        return block
    
    def get_audit_trail(self, document_id: str) -> list:
        """Retorna trilha de auditoria do documento"""
        return [block for block in self.blockchain if block.get("document_id") == document_id]

class VeritasRiskAnalyzer:
    """IA Simbólica para Análise de Riscos"""
    
    def __init__(self):
        self.risk_patterns = {
            "electrical": {
                "keywords": ["tensão", "eletricidade", "circuito", "energizado", "choque"],
                "required_epi": ["luva isolante", "capacete", "óculos de proteção"],
                "risk_level": "ALTO"
            },
            "height": {
                "keywords": ["altura", "escada", "andaime", "queda", "elevado"],
                "required_epi": ["cinto de segurança", "capacete", "trava-quedas"],
                "risk_level": "ALTO"
            },
            "chemical": {
                "keywords": ["químico", "ácido", "solvente", "tóxico", "corrosivo"],
                "required_epi": ["máscara", "luvas químicas", "avental", "óculos"],
                "risk_level": "MÉDIO"
            },
            "mechanical": {
                "keywords": ["máquina", "motor", "rotativo", "prensa", "corte"],
                "required_epi": ["luvas mecânicas", "protetor auricular", "óculos"],
                "risk_level": "MÉDIO"
            }
        }
    
    def analyze_task_risks(self, task_description: str) -> dict:
        """Analisa descrição da tarefa e identifica riscos"""
        task_lower = task_description.lower()
        identified_risks = []
        suggested_epi = set()
        max_risk_level = "BAIXO"
        
        for risk_type, pattern in self.risk_patterns.items():
            if any(keyword in task_lower for keyword in pattern["keywords"]):
                identified_risks.append({
                    "type": risk_type,
                    "level": pattern["risk_level"],
                    "description": f"Risco {risk_type} identificado"
                })
                suggested_epi.update(pattern["required_epi"])
                
                if pattern["risk_level"] == "ALTO":
                    max_risk_level = "ALTO"
                elif pattern["risk_level"] == "MÉDIO" and max_risk_level != "ALTO":
                    max_risk_level = "MÉDIO"
        
        return {
            "overall_risk_level": max_risk_level,
            "identified_risks": identified_risks,
            "suggested_epi": list(suggested_epi),
            "safety_questions": self.generate_safety_questions(identified_risks),
            "ai_recommendation": self.generate_ai_recommendation(max_risk_level, identified_risks)
        }
    
    def generate_safety_questions(self, risks: list) -> list:
        """Gera perguntas de segurança baseadas nos riscos"""
        questions = []
        
        for risk in risks:
            if risk["type"] == "electrical":
                questions.append("O circuito foi desenergizado e bloqueado?")
                questions.append("A tensão foi medida e confirmada como zero?")
            elif risk["type"] == "height":
                questions.append("O sistema de proteção contra quedas foi inspecionado?")
                questions.append("A área inferior foi sinalizada e isolada?")
            elif risk["type"] == "chemical":
                questions.append("A FISPQ do produto foi consultada?")
                questions.append("O sistema de ventilação é adequado?")
            elif risk["type"] == "mechanical":
                questions.append("A máquina foi completamente parada?")
                questions.append("Os dispositivos de segurança estão funcionando?")
        
        return list(set(questions))  # Remove duplicatas
    
    def generate_ai_recommendation(self, risk_level: str, risks: list) -> str:
        """Gera recomendação inteligente da IA"""
        if risk_level == "ALTO":
            return "🚨 ATENÇÃO: Esta tarefa apresenta riscos ALTOS. Recomendo revisão detalhada dos procedimentos e supervisão constante. Considere dividir a tarefa em etapas menores."
        elif risk_level == "MÉDIO":
            return "⚠️ CUIDADO: Riscos moderados identificados. Certifique-se de que todos os EPIs estão disponíveis e em bom estado. Faça uma reunião de segurança antes do início."
        else:
            return "✅ SEGURO: Tarefa de baixo risco. Mantenha os procedimentos padrão de segurança e EPIs básicos."
    
    def validate_document_logic(self, document_data: dict) -> dict:
        """Valida lógica do documento APR/IT"""
        errors = []
        warnings = []
        
        # Verificar se EPIs sugeridos estão listados
        task_desc = document_data.get("task_description", "")
        risk_analysis = self.analyze_task_risks(task_desc)
        listed_epi = document_data.get("required_epi", [])
        
        for suggested_epi in risk_analysis["suggested_epi"]:
            if not any(suggested_epi.lower() in epi.lower() for epi in listed_epi):
                warnings.append(f"EPI recomendado não listado: {suggested_epi}")
        
        # Verificar coerência entre risco e medidas
        if risk_analysis["overall_risk_level"] == "ALTO" and len(document_data.get("control_measures", [])) < 3:
            errors.append("Tarefa de alto risco deve ter pelo menos 3 medidas de controle")
        
        # Verificar preenchimento obrigatório
        required_fields = ["task_description", "location", "responsible_person", "required_epi"]
        for field in required_fields:
            if not document_data.get(field):
                errors.append(f"Campo obrigatório não preenchido: {field}")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "risk_analysis": risk_analysis
        }

# Funções auxiliares para integração
def create_veritas_document(task_data: dict) -> dict:
    """Cria documento VERITAS completo com validações"""
    validator = VeritasDocumentValidator()
    risk_analyzer = VeritasRiskAnalyzer()
    
    # Análise de riscos
    risk_analysis = risk_analyzer.analyze_task_risks(task_data.get("task_description", ""))
    
    # Validação lógica
    logic_validation = risk_analyzer.validate_document_logic(task_data)
    
    # Criar documento
    document = {
        "document_id": f"veritas-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "created_at": datetime.now().isoformat(),
        "document_type": "APR-IT-PT",
        "task_data": task_data,
        "risk_analysis": risk_analysis,
        "validation": logic_validation,
        "veritas_version": "1.0"
    }
    
    # Gerar hash e QR code
    document_hash = validator.generate_document_hash(document)
    qr_code = validator.create_qr_code(document_hash, document["document_id"])
    
    document["hash"] = document_hash
    document["qr_code"] = qr_code
    
    # Adicionar à blockchain
    blockchain_entry = validator.add_to_blockchain(document)
    document["blockchain_index"] = blockchain_entry["index"]
    
    return document

def verify_veritas_document(document_data: dict, provided_hash: str) -> dict:
    """Verifica integridade de documento VERITAS"""
    validator = VeritasDocumentValidator()
    return validator.validate_document_integrity(document_data, provided_hash)
