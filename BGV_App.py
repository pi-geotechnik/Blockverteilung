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
def speichere_werte(dateiname, werte, speicherpfad="."):
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
def berechne_perzentile(längen, perzentile):
    return np.percentile(längen, perzentile)
    

# Streamlit App

# Zeige das Logo zu Beginn der App
logo = Image.open("pi-geotechnik-1-RGB-192-30-65.png")  # Lade das Bild
st.image(logo, caption="ZT GmbH by A Preh & M Illeditsch", use_container_width=True)  # Zeige das Logo an

st.title("Willkommen bei pi!")
st.header("Blockgrößenverteilung")

# Auswahl der Einheit
einheit = st.selectbox("Wählen Sie die Einheit der Eingabedaten:", ["Volumen in m³", "Masse in t (Dichte erforderlich)", "Achsen beliebig vieler Blöcke in cm eingeben"])

if einheit == "Volumen in m³":
    st.subheader("Wählen Sie eine Datei mit Blockvolumina aus")
    uploaded_file_m3 = st.file_uploader("Wählen Sie eine Textdatei mit m³-Werten aus", type=["txt"])
    
    if uploaded_file_m3 is not None:
        # Datei auslesen
        text_m3 = uploaded_file_m3.read().decode("utf-8")
        # Inhalt anzeigen
        st.text_area("Inhalt der Datei:", text_m3, height=300)
        
        try:
            # Text in Zahlen (m³) umwandeln
            m3_werte = [float(val.strip()) for val in text_m3.splitlines() if val.strip().replace(".", "", 1).isdigit()]
            st.write("Die m³-Werte in der Datei:")
            st.write(m3_werte)
            
            # Speicherpfad ermitteln
            original_filename = uploaded_file_m3.name  # Ursprünglicher Dateiname
            original_folder = os.path.dirname(original_filename)  # Verzeichnis extrahieren

            if not original_folder:  
                original_folder = os.getcwd()  # Falls kein Pfad ermittelt werden kann, Standardverzeichnis verwenden

            speicherpfad_m3 = os.path.join(original_folder, "m3_werte.txt")

            # Datei m3_werte.txt speichern
            with open(speicherpfad_m3, "w") as f:
                for wert in m3_werte:
                    f.write(f"{wert}\n")
            
            # Berechnung der dritten Wurzel (Längen in Metern)
            m_längen = [berechne_dritte_wurzel(val) for val in m3_werte]
            st.write("Die Längen in Metern (dritte Wurzel der m³-Werte):")
            st.write(m_längen)
            
            # Datei m_werte.txt speichern
            with open(speicherpfad_m, "w") as f:
                for wert in m_längen:
                    f.write(f"{wert}\n")
            st.success(f"Die m-Werte wurden in der Datei '{speicherpfad_m}' gespeichert.")

            # Visualisierung der Histogramme nebeneinander
            visualisiere_histogramm_m3_und_m(m_längen, m3_werte)
            
            # Berechnung und Anzeige der 95., 96., 97. und 98. Perzentile
            perzentile = [95, 96, 97, 98]
            perzentile_werte = berechne_perzentile(m_längen, perzentile)
            for p, perzentil in zip(perzentile, perzentile_werte):
                st.write(f"{p} Perzentil der Blockverteilung: {perzentil:.2f} m³")
        
        except Exception as e:
            st.error(f"Fehler bei der Verarbeitung der Daten: {e}")

elif einheit == "Masse in t (Dichte erforderlich)":
    st.subheader("Wählen Sie eine Datei mit Blockmassen aus")
    uploaded_file_tonnen = st.file_uploader("Wählen Sie eine Textdatei mit t-Werten aus", type=["txt"])
    
    if uploaded_file_tonnen is not None:
        # Datei auslesen
        text_tonnen = uploaded_file_tonnen.read().decode("utf-8")
        # Inhalt anzeigen
        st.text_area("Inhalt der Datei:", text_tonnen, height=300)
        
        # Eingabe der Dichte in kg/m³ (Standardwert: 2650)
        dichte_kg_m3 = st.number_input("Geben Sie die Dichte in kg/m³ ein:", min_value=0, value=2650, step=10)
        
        if dichte_kg_m3 > 0:
            try:
                # Text in Zahlen (Tonnen) umwandeln und in m³ umrechnen
                tonnen_werte = [float(val.strip()) for val in text_tonnen.splitlines() if val.strip().replace(".", "", 1).isdigit()]
                m3_werte = [val * 1000 / dichte_kg_m3 for val in tonnen_werte]
                
                st.write("Berechnete m³-Werte aus Tonnen:")
                st.write(m3_werte)
                
                # Speicherpfad ermitteln
                original_filename = uploaded_file_tonnen.name  # Ursprünglicher Dateiname
                original_folder = os.path.dirname(original_filename)  # Verzeichnis extrahieren

                if not original_folder:
                    original_folder = os.getcwd()  # Falls kein Pfad ermittelt werden kann, Standardverzeichnis verwenden

                # Speicherpfade für beide Dateien
                speicherpfad_m3 = os.path.join(original_folder, "m3_werte.txt")
                speicherpfad_m = os.path.join(original_folder, "m_werte.txt")

                # Datei m3_werte.txt speichern
                with open(speicherpfad_m3, "w") as f:
                    for wert in m3_werte:
                        f.write(f"{wert}\n")
                st.success(f"Die m³-Werte wurden in der Datei '{speicherpfad_m3}' gespeichert.")

                # Berechnung der dritten Wurzel (Längen in Metern)
                m_längen = [berechne_dritte_wurzel(val) for val in m3_werte]
                st.write("Die Längen in Metern (dritte Wurzel der m³-Werte):")
                st.write(m_längen)

                # Datei m_werte.txt speichern
                with open(speicherpfad_m, "w") as f:
                    for wert in m_längen:
                        f.write(f"{wert}\n")
                st.success(f"Die m-Werte wurden in der Datei '{speicherpfad_m}' gespeichert.")
                
                # Visualisierung der Histogramme nebeneinander
                visualisiere_histogramm_m3_und_m(m_längen, m3_werte)
            
                # Berechnung und Anzeige der 95., 96., 97. und 98. Perzentile
                perzentile = [95, 96, 97, 98]
                perzentile_werte = berechne_perzentile(m_längen, perzentile)
                for p, perzentil in zip(perzentile, perzentile_werte):
                    st.write(f"{p} Perzentil der Blockverteilung: {perzentil:.2f} m³")
                
            except Exception as e:
                st.error(f"Fehler bei der Verarbeitung der Daten: {e}")


elif einheit == "Achsen beliebig vieler Blöcke in cm eingeben":
    st.subheader("Blockdichte eingeben")
    dichte_kg_m3 = st.number_input("Geben Sie die Dichte in kg/m³ ein:", min_value=0, value=2650, step=10)
    
    st.subheader("Blockachsen eingeben")

    # Initialisierung von session_state-Variablen
    if "block_werte_m3" not in st.session_state:
        st.session_state.block_werte_m3 = []  # Liste zur Speicherung der m³-Werte jedes Blocks
    if "block_counter" not in st.session_state:
        st.session_state.block_counter = 1  # Startet bei 1
    if "input_round" not in st.session_state:
        st.session_state.input_round = 0  # Rundenzähler für Eingabegruppen

    # Anzahl der Blöcke pro Runde
    max_blocks_per_input = 5
    aktuelle_runde_start = st.session_state.input_round * max_blocks_per_input + 1
    aktuelle_runde_ende = aktuelle_runde_start + max_blocks_per_input

    # Schleife für genau 5 Blockeingaben
    for i in range(aktuelle_runde_start, aktuelle_runde_ende):
        st.write(f"### Block {i}")
        
        länge_cm = st.number_input(f"Länge (cm) von Block {i}:", min_value=1, value=10, step=1, key=f"länge_cm_{i}")
        breite_cm = st.number_input(f"Breite (cm) von Block {i}:", min_value=1, value=10, step=1, key=f"breite_cm_{i}")
        höhe_cm = st.number_input(f"Höhe (cm) von Block {i}:", min_value=1, value=10, step=1, key=f"höhe_cm_{i}")

        if länge_cm > 0 and breite_cm > 0 and höhe_cm > 0:
            länge_m = länge_cm / 100
            breite_m = breite_cm / 100
            höhe_m = höhe_cm / 100
            volumen_m3 = länge_m * breite_m * höhe_m
            st.session_state.block_werte_m3.append(volumen_m3)
            st.write(f"➡ Das Volumen von Block {i} beträgt **{volumen_m3:.2f} m³**.")
    
        st.write("### Volumina der eingegebenen Blöcke:")
        st.write(st.session_state.block_werte_m3)
    
        speicherpfad = st.text_input("Geben Sie den Pfad an, in dem die Dateien gespeichert werden sollen:")

        if speicherpfad:
            if not os.path.exists(speicherpfad):
                st.error("Der angegebene Pfad existiert nicht. Bitte prüfen Sie die Eingabe.")
            else:
                if st.session_state.block_werte_m3:
                    dateiname = speichere_werte("block_volumen.txt", st.session_state.block_werte_m3, speicherpfad)
                    st.success(f"Die m³-Werte der Blöcke wurden in der Datei '{dateiname}' gespeichert.")
                    m_längen = [wert ** (1/3) for wert in st.session_state.block_werte_m3]
                    st.write("### Längen in Metern (dritte Wurzel der m³-Werte):")
                    st.write(m_längen)
                    dateiname = speichere_werte("block_längen.txt", m_längen, speicherpfad)
                    st.success(f"Die m-Werte der Blöcke wurden in der Datei '{dateiname}' gespeichert.")
                    visualisiere_histogramm_m3_und_m(m_längen, st.session_state.block_werte_m3)
                    perzentile = berechne_perzentile(m_längen, [95, 96, 97, 98])
                    for p, perzentil in zip([95, 96, 97, 98], perzentile):
                        st.write(f"{p} Perzentil der Blockverteilung: {perzentil:.2f} m")
    
        if st.button("Weitere 5 Blöcke eingeben"):
            st.session_state.input_round += 1
            st.rerun()



# Anpassung einer Wahrscheinlichkeitsfunktion






