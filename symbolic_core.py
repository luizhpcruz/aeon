
class SymbolicCore:
    def __init__(self, emotion_mode="on"):
        self.emotion_mode = emotion_mode
        self.symbol_map = {}

    def process_symbol(self, symbol, context):
        if self.emotion_mode == "off":
            return self.logic_only(symbol, context)
        else:
            return self.affective_symbolism(symbol, context)

    def logic_only(self, symbol, context):
        # apenas relações causais, não afetivas
        return f"Lógica de '{symbol}' processada no contexto {context}"

    def affective_symbolism(self, symbol, context):
        # analisa emoção, valência, memória afetiva
        return f"'{symbol}' possui carga afetiva em {context}"
