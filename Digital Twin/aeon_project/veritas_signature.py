"""
VERITAS - Módulo de Assinatura Digital Gov.br
Integração com certificados A3 e validação gov.br
"""

import hashlib
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import uuid

class GovBrSignature:
    """Simulação de integração com Gov.br para assinatura digital"""
    
    def __init__(self):
        self.certificates = {
            "000.000.000-00": {
                "name": "João Silva",
                "role": "Eletricista Senior",
                "cert_type": "A3",
                "valid_until": "2025-12-31",
                "issuer": "AC SERASA RFB v5"
            },
            "111.111.111-11": {
                "name": "Maria Santos",
                "role": "Supervisor de Segurança",
                "cert_type": "A3",
                "valid_until": "2025-12-31",
                "issuer": "AC SERASA RFB v5"
            }
        }
    
    def validate_cpf(self, cpf: str) -> bool:
        """Valida formato do CPF (simulação)"""
        cpf_clean = cpf.replace(".", "").replace("-", "")
        return len(cpf_clean) == 11 and cpf_clean.isdigit()
    
    def get_certificate_info(self, cpf: str) -> dict:
        """Obtém informações do certificado (simulação gov.br)"""
        if cpf in self.certificates:
            return {
                "valid": True,
                "certificate": self.certificates[cpf],
                "status": "ATIVO"
            }
        else:
            return {
                "valid": False,
                "error": "CPF não encontrado na base gov.br",
                "status": "INVÁLIDO"
            }
    
    def generate_digital_signature(self, document_hash: str, cpf: str) -> dict:
        """Gera assinatura digital para o documento"""
        if not self.validate_cpf(cpf):
            return {"success": False, "error": "CPF inválido"}
        
        cert_info = self.get_certificate_info(cpf)
        if not cert_info["valid"]:
            return {"success": False, "error": cert_info["error"]}
        
        # Gerar chave privada (em produção seria do certificado A3)
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Assinar o hash do documento
        signature = private_key.sign(
            document_hash.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        
        signature_data = {
            "signature_id": str(uuid.uuid4()),
            "signature": signature.hex(),
            "signer_cpf": cpf,
            "signer_name": cert_info["certificate"]["name"],
            "signer_role": cert_info["certificate"]["role"],
            "certificate_type": cert_info["certificate"]["cert_type"],
            "certificate_issuer": cert_info["certificate"]["issuer"],
            "timestamp": datetime.now().isoformat(),
            "document_hash": document_hash,
            "validation_url": f"https://govbr.veritas.com/validate/{signature_data.get('signature_id', 'unknown')}"
        }
        
        return {
            "success": True,
            "signature": signature_data
        }
    
    def verify_signature(self, signature_data: dict, document_hash: str) -> dict:
        """Verifica assinatura digital"""
        try:
            # Verificar se o hash confere
            if signature_data.get("document_hash") != document_hash:
                return {
                    "valid": False,
                    "error": "Hash do documento não confere",
                    "status": "COMPROMETIDO"
                }
            
            # Verificar certificado
            cpf = signature_data.get("signer_cpf")
            cert_info = self.get_certificate_info(cpf)
            
            if not cert_info["valid"]:
                return {
                    "valid": False,
                    "error": "Certificado inválido ou revogado",
                    "status": "INVÁLIDO"
                }
            
            return {
                "valid": True,
                "signer": cert_info["certificate"]["name"],
                "timestamp": signature_data.get("timestamp"),
                "status": "VÁLIDA"
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"Erro na verificação: {str(e)}",
                "status": "ERRO"
            }

class VeritasAdvancedDocument:
    """Documento VERITAS com assinatura digital e blockchain"""
    
    def __init__(self):
        self.gov_signature = GovBrSignature()
        self.blockchain = []
    
    def create_signed_document(self, task_data: dict, signer_cpf: str, supervisor_cpf: str = None) -> dict:
        """Cria documento com assinatura digital"""
        from veritas_core import create_veritas_document
        
        # Criar documento base
        document = create_veritas_document(task_data)
        
        # Assinar documento
        primary_signature = self.gov_signature.generate_digital_signature(
            document["hash"], signer_cpf
        )
        
        if not primary_signature["success"]:
            return {
                "success": False,
                "error": f"Erro na assinatura principal: {primary_signature['error']}"
            }
        
        document["primary_signature"] = primary_signature["signature"]
        
        # Assinatura do supervisor (se fornecida)
        if supervisor_cpf:
            supervisor_signature = self.gov_signature.generate_digital_signature(
                document["hash"], supervisor_cpf
            )
            
            if supervisor_signature["success"]:
                document["supervisor_signature"] = supervisor_signature["signature"]
        
        # Registrar na blockchain
        self.add_to_blockchain(document, "CREATE_SIGNED")
        
        return {
            "success": True,
            "document": document
        }
    
    def validate_signed_document(self, document: dict) -> dict:
        """Valida todas as assinaturas do documento"""
        validations = []
        
        # Validar assinatura principal
        if "primary_signature" in document:
            primary_validation = self.gov_signature.verify_signature(
                document["primary_signature"], document["hash"]
            )
            validations.append({
                "type": "primary",
                "validation": primary_validation
            })
        
        # Validar assinatura do supervisor
        if "supervisor_signature" in document:
            supervisor_validation = self.gov_signature.verify_signature(
                document["supervisor_signature"], document["hash"]
            )
            validations.append({
                "type": "supervisor",
                "validation": supervisor_validation
            })
        
        all_valid = all(v["validation"]["valid"] for v in validations)
        
        return {
            "document_valid": all_valid,
            "validations": validations,
            "validation_timestamp": datetime.now().isoformat()
        }
    
    def add_to_blockchain(self, document: dict, action: str) -> dict:
        """Adiciona evento à blockchain"""
        previous_hash = self.blockchain[-1]["hash"] if self.blockchain else "0"
        
        block = {
            "index": len(self.blockchain),
            "timestamp": datetime.now().isoformat(),
            "document_id": document["document_id"],
            "action": action,
            "document_hash": document["hash"],
            "previous_hash": previous_hash,
            "signatures": {
                "primary": document.get("primary_signature", {}).get("signer_cpf"),
                "supervisor": document.get("supervisor_signature", {}).get("signer_cpf")
            }
        }
        
        # Hash do bloco
        block_data = json.dumps(block, sort_keys=True)
        block["hash"] = hashlib.sha256(block_data.encode()).hexdigest()
        
        self.blockchain.append(block)
        return block
    
    def get_document_audit_trail(self, document_id: str) -> list:
        """Retorna trilha completa de auditoria"""
        return [block for block in self.blockchain if block["document_id"] == document_id]
    
    def export_pdf_report(self, document: dict) -> dict:
        """Gera relatório PDF do documento (simulação)"""
        return {
            "pdf_generated": True,
            "file_path": f"reports/{document['document_id']}.pdf",
            "file_size": "2.3 MB",
            "pages": 4,
            "includes_qr": True,
            "includes_signatures": True,
            "timestamp": datetime.now().isoformat()
        }

# Funções de conveniência
def create_fully_signed_document(task_data: dict, signer_cpf: str, supervisor_cpf: str = None):
    """Função principal para criar documento completo com assinaturas"""
    veritas_doc = VeritasAdvancedDocument()
    return veritas_doc.create_signed_document(task_data, signer_cpf, supervisor_cpf)

def validate_document_signatures(document: dict):
    """Função para validar todas as assinaturas de um documento"""
    veritas_doc = VeritasAdvancedDocument()
    return veritas_doc.validate_signed_document(document)
