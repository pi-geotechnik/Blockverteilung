#!/usr/bin/env python
# coding: utf-8

# # App zur Darstellung einer Blockgrößenverteilung und Anpassung einer Wahrscheinlichkeitsfunktion

# Mariella Illeditsch


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import os
from PIL import Image

# Funktion zur Berechnung der Masse in Tonnen aus m³ und Dichte
def berechne_masse_in_tonnen(volumen_m3, dichte_kg_m3):
    # Masse in kg
    masse_kg = volumen_m3 * dichte_kg_m3
    # Umrechnung in Tonnen
    masse_tonnen = masse_kg / 1000
    return masse_tonnen

# Funktion zum Speichern der berechneten m³-Werte in einer .txt-Datei
def speichere_m3_werte(m3_werte):
    # Dateiname mit dem aktuellen Datum und Uhrzeit
    dateiname = "berechnete_m3_werte.txt"
    
    with open(dateiname, "w") as f:
        for wert in m3_werte:
            f.write(f"{wert:.2f}\n")  # Nur die m³-Werte, mit 2 Nachkommastellen
    return dateiname

# Funktion zur Berechnung der dritten Wurzel von m³ (Umrechnung zu m)
def berechne_dritte_wurzel(v):
    return round(v ** (1/3), 2)

# Funktion zum Speichern der m³-Werte in einer Datei
def speichere_m3_werte(m3_werte):
    dateiname = "m3_werte.txt"
    with open(dateiname, 'w') as f:
        for wert in m3_werte:
            f.write(f"{wert}\n")
    return dateiname

# Funktion zum Speichern der m-Werte in einer Datei
def speichere_m_werte(m_werte):
    dateiname = "m_werte.txt"
    with open(dateiname, 'w') as f:
        for wert in m_werte:
            f.write(f"{wert}\n")
    return dateiname

def visualisiere_histogramm_m3_und_m(m_werte, m3_werte):
    # Erstellen der Subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    # Histogramm für Volumen (m³)
    ax1.hist(m3_werte, bins=20, color='lightgreen', edgecolor='black')
    ax1.set_title("Histogramm der Volumina (m³)")
    ax1.set_xlabel("Blockvolumen (m³)")
    ax1.set_ylabel("Häufigkeit")
    # Histogramm für Achsen (m)
    ax2.hist(m_werte, bins=20, color='skyblue', edgecolor='black')
    ax2.set_title("Histogramm der Achsen (m)")
    ax2.set_xlabel("Blockachse (m)")
    ax2.set_ylabel("Häufigkeit")
    # Layout anpassen und anzeigen
    plt.tight_layout()
    st.pyplot(fig)

def berechne_perzentile(längen, perzentile):
    # Zuerst die Längen in m³ umrechnen, indem wir sie hoch drei nehmen
    m3_werte = [länge ** 3 for länge in längen]  # Umrechnung jedes einzelnen Längenwerts in m³
    # Berechnung der Perzentile der Volumina (m³)
    return np.percentile(m3_werte, perzentile)



# Streamlit App

# Zeige das Logo zu Beginn der App
logo = Image.open("pi-geotechnik-1-RGB-192-30-65.png")  # Lade das Bild
st.image(logo, caption="ZT GmbH", use_column_width=True)  # Zeige das Logo an

st.title("Willkommen bei pi!")
st.header("Blockgrößenverteilung")

# Auswahl der Einheit
einheit = st.selectbox("Wählen Sie die Einheit der Eingabedaten:", ["Volumen in m³", "Masse in t (Dichte erforderlich)", "Achsen beliebig vieler Blöcke in cm eingeben"])

if einheit == "Volumen in m³":
    st.header("Wählen Sie eine Datei mit Blockvolumina aus")
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
            
            # Speichern der m³-Werte in einer Datei
            dateiname = speichere_m3_werte(m3_werte)
            st.success(f"Die m³-Werte wurden in der Datei '{dateiname}' gespeichert.")
            
            # Berechnung der dritten Wurzel (Längen in Metern)
            m_längen = [berechne_dritte_wurzel(val) for val in m3_werte]
            st.write("Die Längen in Metern (dritte Wurzel der m³-Werte):")
            st.write(m_längen)
            
            # Speichern der m-Werte in einer Datei
            dateiname = speichere_m_werte(m_längen)
            st.success(f"Die m-Werte wurden in der Datei '{dateiname}' gespeichert.")

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
    st.header("Wählen Sie eine Datei mit Blockmassen aus")
    uploaded_file_tonnen = st.file_uploader("Wählen Sie eine Textdatei mit t-Werten aus", type=["txt"])
    
    if uploaded_file_tonnen is not None:
        # Datei auslesen
        text_tonnen = uploaded_file_tonnen.read().decode("utf-8")
        # Inhalt anzeigen
        st.text_area("Inhalt der Datei:", text_tonnen, height=300)
        
        # Eingabe der Dichte in kg/m³ (Standardwert: 2700)
        dichte_kg_m3 = st.number_input("Geben Sie die Dichte in kg/m³ ein:", min_value=0.0, value=2700.0)
        
        if dichte_kg_m3 > 0:
            try:
                # Text in Zahlen (Tonnen) umwandeln und in m³ umrechnen
                tonnen_werte = [float(val.strip()) for val in text_tonnen.splitlines() if val.strip().replace(".", "", 1).isdigit()]
                m3_werte = [val * 1000 / dichte_kg_m3 for val in tonnen_werte]
                
                st.write("Berechnete m³-Werte aus Tonnen:")
                st.write(m3_werte)
                
                # Speichern der berechneten m³-Werte in einer Datei
                dateiname = speichere_m3_werte(m3_werte)
                st.success(f"Die m³-Werte wurden in der Datei '{dateiname}' gespeichert.")

                # Berechnung der dritten Wurzel (Längen in Metern)
                m_längen = [berechne_dritte_wurzel(val) for val in m3_werte]
                st.write("Die Längen in Metern (dritte Wurzel der m³-Werte):")
                st.write(m_längen)

                # Speichern der berechneten m-Werte in einer Datei
                dateiname = speichere_m_werte(m_längen)
                st.success(f"Die m-Werte wurden in der Datei '{dateiname}' gespeichert.")
                
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
    # Eingabe der Dichte (für alle Blöcke gleich)
    
    st.header("Blockdichte eingeben")
    dichte_kg_m3 = st.number_input("Geben Sie die Dichte in kg/m³ ein:", min_value=0.0, value=2700.0)
    
    st.header("Blockachsen eingeben")
    block_werte_m3 = []  # Liste zur Speicherung der m³-Werte jedes Blocks
    
    # Schleife, um mehrere Blockgrößen zu ermöglichen
    block_counter = 0  # Zähler für die Blöcke
    while block_counter <= max_blocks:  # Zähler für den Block erhöhen
        
        # Eingabe der Blockmaße in cm mit eindeutigen keys
        länge_cm = st.number_input(f"Geben Sie die Länge des Blocks {block_counter} in cm ein:", min_value=0.0, key=f"länge_cm_{block_counter}")
        breite_cm = st.number_input(f"Geben Sie die Breite des Blocks {block_counter} in cm ein:", min_value=0.0, key=f"breite_cm_{block_counter}")
        höhe_cm = st.number_input(f"Geben Sie die Höhe des Blocks {block_counter} in cm ein:", min_value=0.0, key=f"höhe_cm_{block_counter}")
        
        if länge_cm > 0 and breite_cm > 0 and höhe_cm > 0:
            # Berechnung des Volumens in m³ des Blocks
            länge_m = länge_cm / 100
            breite_m = breite_cm / 100
            höhe_m = höhe_cm / 100
            volumen_m3 = länge_m * breite_m * höhe_m
            block_werte_m3.append(volumen_m3)
            st.write(f"Das Volumen des Blocks {block_counter} beträgt {volumen_m3:.2f} m³.")
        
        # Option für den Benutzer, einen weiteren Block hinzuzufügen oder abzuschließen
        if block_counter < max_blocks:
            weiter_block = st.radio(Möchten Sie einen weiteren Block eingeben?", ("Ja", "Nein, ich bin fertig"), key=f"weiter_block_{block_counter}")
            
            if weiter_block == "Nein, ich bin fertig":
                break
                
    st.write("Alle Blöcke wurden erfolgreich eingegeben!")
    st.write(f"Die Volumina der eingegebenen Blöcke: {block_werte_m3}")
    
    # Wenn es berechnete m³-Werte gibt, speichere sie in einer Datei
    if block_werte_m3:
        # Speichern der m³-Werte in einer Datei
        dateiname = speichere_m3_werte(block_werte_m3)
        st.success(f"Die m³-Werte der Blöcke wurden in der Datei '{dateiname}' gespeichert.")
        
        # Berechnung der dritten Wurzel (Längen in Metern)
        m_längen = [berechne_dritte_wurzel(val) for val in block_werte_m3]
        st.write("Die Längen in Metern (dritte Wurzel der m³-Werte):")
        st.write(m_längen)
        
        # Speichern der m-Werte in einer Datei
        dateiname = speichere_m_werte(m_längen)
        st.success(f"Die m-Werte der Blöcke wurden in der Datei '{dateiname}' gespeichert.")

        # Visualisierung der Histogramme nebeneinander
        visualisiere_histogramm_m3_und_m(m_längen, block_werte_m3)

        # Berechnung und Anzeige der 95., 96., 97. und 98. Perzentile
        perzentile = [95, 96, 97, 98]
        perzentile_werte = berechne_perzentile(m_längen, perzentile)
        for p, perzentil in zip(perzentile, perzentile_werte):
            st.write(f"{p} Perzentil der Blockverteilung: {perzentil:.2f} m³")


# Anpassung einer Wahrscheinlichkeitsfunktion






