from core.aeon_entity import AeonEntity
from core.aeon_tutor import AeonTutor

aeon = AeonEntity()
tutor = AeonTutor(aeon)

# Ensina um conceito básico:
tutor.teach(
    "loop_for",
    "def loop_for():\n    for i in range(3):\n        print(f'AEON pensa: passo {i}')",
    "Loop simples que imprime três passos."
)

# Salva o progresso e compila
tutor.save_knowledge()
tutor.compile_brain()

# AEON executa o que aprendeu
aeon.show_self()
aeon.self_learn()

# Atualiza o escopo global com a base de conhecimento do AEON
globals().update(aeon.knowledge_base)

# Depuração: Verificar o conteúdo da base de conhecimento do AEON
print("Base de conhecimento do AEON:", aeon.knowledge_base)
if 'loop_for' in aeon.knowledge_base:
else:
    print("Erro: A função 'loop_for' não foi carregada corretamente.")
