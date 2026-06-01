import streamlit as st
import pandas as pd
import requests

st.title("AEON‑AI Dashboard Operacional")

if st.button("🚀 Simular Cosma"):
    res = requests.post("http://localhost:8000/cosma/simulate")
    st.write(res.json())

if st.button("📡 Broadcast bloco"):
    block = {"data": "eventoX"}
    res = requests.post("http://localhost:8000/chain/broadcast", json=block)
    st.write(res.status_code, res.json())

st.header("UHE Twin Simulation")
inflow = pd.DataFrame({"date": pd.date_range("2025-08-01", periods=7), "inflow_m3_s": st.slider("Vazão diária (m³/s)", 10, 1000, (100, 500), step=10)})
res = requests.post("http://localhost:8000/ops/simulate", json=inflow.to_dict(orient="records"))
st.write(pd.DataFrame(res.json()))

if st.button("🖊️ Gerar e Assinar Documento"):
    payload = {"task_id": "OS-45"}
    res = requests.post("http://localhost:8000/ops/generate_and_sign", json=payload)
    st.json(res.json())
