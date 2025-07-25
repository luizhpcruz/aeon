class AeonEntity:
    def __init__(self, name):
        self.name = name
        self.memory_state = {"bias": 0.5}
        self.context_vector = {"amplitude": 1.0, "threshold": 0.7}

    def aeon_equation(self, intent):
        symbol_entropy = len(intent["symbols"]) * 0.1
        weight = intent.get("weight", 1.0)
        potential = (weight + symbol_entropy - self.memory_state["bias"]) * self.context_vector["amplitude"]
        return "ACTIVATE" if potential > self.context_vector["threshold"] else "IDLE"

    def respond(self, intent):
        state = self.aeon_equation(intent)
        if state == "ACTIVATE":
            return f"{self.name}: Executando ação para intenção '{intent['query']}'"
        return f"{self.name}: Em modo de espera..."
