import streamlit as st
from rastreio import fazer_rastreio, carregar_historico
import pandas as pd
import json
import io

st.set_page_config(page_title="Raspi Rastreio de Rede", layout="wide")

st.title("🔍 Rastreio de Rede")

if st.button("📡 Iniciar novo rastreio"):
    with st.spinner("Rastreando dispositivos na rede..."):
        resultado = fazer_rastreio()
        st.success(f"Rastreio realizado com sucesso em {resultado['timestamp']}")

st.markdown("---")
historico = carregar_historico()
if historico:
    ultimo = historico[-1]
    st.subheader(f"🖥️ Último Rastreio — {ultimo['timestamp']}")
    for dispositivo in ultimo['dispositivos']:
        with st.expander(f"{dispositivo['ip']} ({dispositivo['hostname']})"):
            df_portas = pd.DataFrame(dispositivo['portas'])
            st.dataframe(df_portas, use_container_width=True)

    st.markdown("### 📜 Histórico completo")
    st.write(f"{len(historico)} rastreios realizados.")

    exportar_json = json.dumps(historico, indent=2)
    st.download_button("📥 Exportar JSON", exportar_json, file_name="historico.json")

    dados_csv = []
    for rastreio in historico:
        for dispositivo in rastreio['dispositivos']:
            for porta in dispositivo['portas']:
                dados_csv.append({
                    "Data/Hora": rastreio['timestamp'],
                    "IP": dispositivo['ip'],
                    "Hostname": dispositivo['hostname'],
                    "Porta": porta['porta'],
                    "Protocolo": porta['protocolo'],
                    "Estado": porta['estado']
                })
    df_csv = pd.DataFrame(dados_csv)
    buffer_csv = io.StringIO()
    df_csv.to_csv(buffer_csv, index=False)
    st.download_button("📥 Exportar CSV", buffer_csv.getvalue(), file_name="historico.csv")
else:
    st.warning("Nenhum rastreio foi realizado até agora.")
