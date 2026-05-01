import numpy as np
from janus.core.engine import JanusEngine

np.random.seed(42)

series = list(np.random.normal(0, 1, 200)) + list(np.random.normal(3, 1, 200))

engine = JanusEngine()

for i, v in enumerate(series):
    out = engine.ingest(float(v))
    if out.event:
        print(f"{i:03d} | EVENT={out.event} | score={out.score}")
