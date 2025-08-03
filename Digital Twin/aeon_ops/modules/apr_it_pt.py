import json
from datetime import datetime
from uuid import uuid4

def compute_sha256(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()

def generate_document(task_id: str, location: str, prepared_by: dict, supervisor: dict = None):
    doc = {
        "document_id": f"aeonops-{uuid4().hex}",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "task_id": task_id,
        "location": location,
        "apr": {
            "prepared_by": prepared_by,
            "risk_category": "Alta (Fiação e ambiente com tensão)",
            "identified_hazards": [
                "Contato acidental com circuito energizado",
                "Ferramenta solta causando arco"
            ],
            "control_measures": [
                "Uso obrigatório de luva isolante + gorro resistente a arco",
                "Bloqueio prévio: desligamento e abertura de dispositivos"
            ]
        },
        "it": {
            "steps": [
                "1. Informar à operação que vai iniciar sequência de seccionamento",
                "2. Pirômetro: resistência de contato abaixo de 300mΩ",
                "3. Verificação de tensão = 0V antes de iniciar o trabalho",
                "4. Instalação de sinalizador próximo",
                "5. Realização de teste funcional p/ marcha de carga"
            ]
        },
        "pt": {
            "permit_approval": supervisor or {},
            "validity": {
                "start": datetime.utcnow().isoformat() + "Z",
                "end": datetime.utcnow().replace(hour=17, minute=30).isoformat() + "Z"
            }
        }
    }
    doc_bytes = json.dumps(doc, sort_keys=True).encode('utf-8')
    doc_hash = compute_sha256(doc_bytes)
    doc["hash"] = doc_hash
    return doc
