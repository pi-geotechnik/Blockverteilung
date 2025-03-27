#!/usr/bin/env python
# coding: utf-8

# App zur Darstellung einer Blockgrößenverteilung und Anpassung einer Wahrscheinlichkeitsfunktion

# by Mariella Illeditsch


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import os
from PIL import Image

# Funktion zur Berechnung der Masse in Tonnen aus m³ und Dichte
def berechne_masse_in_tonnen(volumen_m3, dichte_kg_m3):
    return (volumen_m3 * dichte_kg_m3) / 1000

# Funktion zur Berechnung der dritten Wurzel von m³
def berechne_dritte_wurzel(v):
    return round(v ** (1/3), 2)

# Funktion zum Speichern von Werten in einer Datei
def speichere_werte(dateiname, werte, speicherpfad):
    pfad = os.path.join(speicherpfad, dateiname)
    with open(pfad, "w") as f:
        for wert in werte:
            f.write(f"{wert}\n")
    return pfad

# Funktion zur Visualisierung von Histogrammen
def visualisiere_histogramm_m3_und_m(m_werte, m3_werte):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.hist(m3_werte, bins=20, color='lightgreen', edgecolor='black')
    ax1.set_title("Histogramm der Volumina (m³)")
    ax1.set_xlabel("Blockvolumen (m³)")
    ax1.set_ylabel("Häufigkeit")
    
    ax2.hist(m_werte, bins=20, color='skyblue', edgecolor='black')
    ax2.set_title("Histogramm der Achsen (m)")
    ax2.set_xlabel("Blockachse (m)")
    ax2.set_ylabel("Häufigkeit")
    
    plt.tight_layout()
    st.pyplot(fig)

# Funktion zur Berechnung der Perzentile
def berechne_perzentile(Achsen, perzentile):
    return np.percentile(Achsen, perzentile)
    

# Streamlit App

# Zeige das Logo zu Beginn der App
logo = Image.open("pi-geotechnik-1-RGB-192-30-65.png")  # Lade das Bild
st.image(logo, caption="ZT GmbH by A Preh & M Illeditsch", use_container_width=True)  # Zeige das Logo an

st.title("Willkommen bei pi!")
st.header("Blockgrößenverteilung")

# Auswahl der Einheit
einheit = st.selectbox("Wählen Sie die Einheit der Eingabedaten:", ["Volumen in m³", "Masse in t (Dichte erforderlich)", "Achsen beliebig vieler Blöcke in cm eingeben"])

# Datei-Upload für m³ oder t
if einheit in ["Volumen in m³", "Masse in t (Dichte erforderlich)"]:
    uploaded_file = st.file_uploader("Wählen Sie eine Textdatei aus", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("Inhalt der Datei:", text, height=300)
        
        # Nutzung des temporären Speicherorts von Streamlit-Dateien
        speicherpfad = os.getcwd()  # Standardmäßig aktuelles Arbeitsverzeichnis
        temp_speicherort = tempfile.NamedTemporaryFile(delete=False)
        speicherpfad = os.path.dirname(temp_speicherort.name)
        
        try:
            werte = [float(val.strip()) for val in text.splitlines() if val.strip().replace(".", "", 1).isdigit()]
            st.write("Die Werte in der Datei:")
            st.write(werte)
            
            if einheit == "Masse in t (Dichte erforderlich)":
                dichte_kg_m3 = st.number_input("Geben Sie die Dichte in kg/m³ ein:", min_value=0, value=2650, step=10)
                werte = [val * 1000 / dichte_kg_m3 for val in werte]  # Umrechnung t → m³
                st.write("Berechnete m³-Werte:")
                st.write(werte)
            
            m_achsen = [berechne_dritte_wurzel(val) for val in werte]
            st.write("Achsen in Metern:")
            st.write(m_achsen)
            
            speichere_werte("m3_werte.txt", werte, speicherpfad)
            speichere_werte("m_werte.txt", m_achsen, speicherpfad)
            st.success(f"Dateien gespeichert in '{speicherpfad}'")
            
            visualisiere_histogramm_m3_und_m(m_achsen, werte)
            perzentile = berechne_perzentile(m_achsen, [95, 96, 97, 98])
            for p, perzentil in zip([95, 96, 97, 98], perzentile):
                st.write(f"{p}. Perzentil der Blockverteilung: {perzentil:.2f} m")
        except Exception as e:
            st.error(f"Fehler bei der Verarbeitung der Daten: {e}")

# Manuelle Eingabe von Blockachsen
elif einheit == "Achsen beliebig vieler Blöcke in cm eingeben":
    speicherpfad = st.text_input("Geben Sie den Speicherpfad für die Dateien an:", value=os.getcwd())
    
    st.subheader("Blockdichte eingeben")
    dichte_kg_m3 = st.number_input("Geben Sie die Dichte in kg/m³ ein:", min_value=0, value=2650, step=10)
    
    st.subheader("Blockachsen eingeben")

    # Initialisierung von Session-State-Variablen, falls sie noch nicht existieren
    if "block_werte_m3" not in st.session_state:
        st.session_state.block_werte_m3 = []  # Liste zur Speicherung der Blockvolumina
    if "block_counter" not in st.session_state:
        st.session_state.block_counter = 1  # Zählt die eingegebenen Blöcke

    # Eingabe der drei Achsen (Länge, Breite, Höhe) in cm
    länge_cm = st.number_input("Länge (cm):", min_value=1, value=10, step=1)
    breite_cm = st.number_input("Breite (cm):", min_value=1, value=10, step=1)
    höhe_cm = st.number_input("Höhe (cm):", min_value=1, value=10, step=1)
    
    # Button zum Speichern der Blockgröße
    if st.button("Block speichern"):
        länge_m = länge_cm / 100  # Umrechnung von cm in m
        breite_m = breite_cm / 100
        höhe_m = höhe_cm / 100
        volumen_m3 = länge_m * breite_m * höhe_m  # Berechnung des Volumens in m³
        st.session_state.block_werte_m3.append(volumen_m3)  # Speicherung in der Liste
        st.session_state.block_counter += 1  # Erhöhe den Zähler
        st.success(f"Block {st.session_state.block_counter - 1} gespeichert: {volumen_m3:.2f} m³")
        st.rerun()  # Aktualisiere die App
    
    # Anzeige der eingegebenen Blockvolumina
    st.write("### Eingegebene Blockvolumina:")
    st.write(st.session_state.block_werte_m3)
    
    # Abschließen der Eingabe und Daten speichern
    if len(st.session_state.block_werte_m3) > 0 and st.button("Eingabe abschließen und speichern"):
        # Speichern der Volumendaten
        speichere_werte("block_volumen.txt", st.session_state.block_werte_m3, speicherpfad)
        st.success(f"Die m3-Werte wurden in '{speicherpfad}' gespeichert.")
        
        # Berechnung der dritten Wurzel (Achsen in Metern)
        m_achsen = [wert ** (1/3) for wert in st.session_state.block_werte_m3]
        st.write("### Achsen in Metern (dritte Wurzel der m³-Werte):")
        st.write(m_achsen)
            
        # Speichern der Achsendaten
        speichere_werte("block_achsen.txt", m_achsen, speicherpfad)
        st.success(f"Die m-Werte wurden in '{speicherpfad}' gespeichert.")
            
        # Visualisierung der Histogramme
        visualisiere_histogramm_m3_und_m(m_achsen, st.session_state.block_werte_m3)
            
        # Berechnung und Ausgabe der Perzentile
        perzentile = berechne_perzentile(m_achsen, [95, 96, 97, 98])
        for p, perzentil in zip([95, 96, 97, 98], perzentile):
            st.write(f"{p}. Perzentil der Blockverteilung: {perzentil:.2f} m")


# Anpassung einer Wahrscheinlichkeitsfunktion






