#!/usr/bin/env python
# coding: utf-8

# App zur Darstellung einer Blockgrößenverteilung und Anpassung einer Wahrscheinlichkeitsfunktion
# by Mariella Illeditsch

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import scipy as sp
from scipy.stats import expon
from scipy.stats import genexpon
from scipy.stats import powerlaw
from PIL import Image # für das Logo

# Funktion zur Berechnung der Masse in Tonnen aus m³ und Dichte
def berechne_masse_in_tonnen(volumen_m3, dichte_kg_m3):
    return (volumen_m3 * dichte_kg_m3) / 1000

# Funktion zur Berechnung der dritten Wurzel von m³
def berechne_dritte_wurzel(v):
    return round(v ** (1/3), 2)

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
st.image(logo, caption="by A Preh & M Illeditsch", use_container_width=True)  # Zeige das Logo an

st.title("Willkommen bei pi!")
st.header("Blockgrößenverteilung")

# Auswahl der Einheit
einheit = st.selectbox("Wählen Sie die Einheit der Eingabedaten:", ["Volumen in m³", "Masse in t (Dichte erforderlich)"])

if einheit == "Volumen in m³":
    uploaded_file = st.file_uploader("Wählen Sie eine Textdatei mit m³-Werten aus", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("Inhalt der Datei:", text, height=300)

        try:
            # Text in Zahlen (m³) umwandeln
            werte = [float(val.strip()) for val in text.splitlines() if val.strip().replace(".", "", 1).isdigit()]
            st.write("Die m³-Werte in der Datei:")
            st.write(werte)

            # Berechnung der dritten Wurzel (Achsen in Metern)
            m_achsen = [berechne_dritte_wurzel(val) for val in werte]
            st.write("Achsen in Metern:")
            st.write(m_achsen)

            # Visualisierung der Histogramme
            visualisiere_histogramm_m3_und_m(m_achsen, werte)
            perzentile = berechne_perzentile(m_achsen, [95, 96, 97, 98])
            for p, perzentil in zip([95, 96, 97, 98], perzentile):
                st.write(f"{p}. Perzentil der Blockverteilung: {perzentil:.2f} m")

        except Exception as e:
            st.error(f"Fehler bei der Verarbeitung der Daten: {e}")


# Datei-Upload für Masse in t (Dichte erforderlich)
if einheit == "Masse in t (Dichte erforderlich)":
    uploaded_file = st.file_uploader("Wählen Sie eine Textdatei mit t-Werten aus", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("Inhalt der Datei:", text, height=300)

        try:
            # Text in Zahlen (Tonnen) umwandeln
            werte = [float(val.strip()) for val in text.splitlines() if val.strip().replace(".", "", 1).isdigit()]
            st.write("Die Tonnen-Werte in der Datei:")
            st.write(werte)

            # Eingabe der Dichte in kg/m³
            dichte_kg_m3 = st.number_input("Geben Sie die Dichte in kg/m³ ein:", min_value=0, value=2650, step=10)
            # Umrechnung von Tonnen in m³
            werte_m3 = [val * 1000 / dichte_kg_m3 for val in werte]
            st.write("Berechnete m³-Werte aus Tonnen:")
            st.write(werte_m3)

            # Berechnung der dritten Wurzel (Achsen in Metern)
            m_achsen = [berechne_dritte_wurzel(val) for val in werte_m3]
            st.write("Achsen in Metern:")
            st.write(m_achsen)

            # Visualisierung der Histogramme
            visualisiere_histogramm_m3_und_m(m_achsen, werte_m3)
            perzentile = berechne_perzentile(m_achsen, [95, 96, 97, 98])
            for p, perzentil in zip([95, 96, 97, 98], perzentile):
                st.write(f"{p}. Perzentil der Blockverteilung: {perzentil:.2f} m")

        except Exception as e:
            st.error(f"Fehler bei der Verarbeitung der Daten: {e}")  


# Darstellung

# Funktion zur Berechnung der Perzentile und Anpassung der Wahrscheinlichkeitsfunktion
def berechne_perzentile_und_visualisierung(m_achsen):
    steps = np.linspace(0.01, 1.00, num=100)

    Perc_steps = ['0','5','10','15','20','25','30','35','40','45','50','55','60','65','70','75','80','85','90','95','96','97','98','99','100']

    # Berechnung der Perzentile
    percentiles_sample_seite = np.quantile(m_achsen, steps)
    Perc_sample_seite = percentiles_sample_seite[0], percentiles_sample_seite[4], percentiles_sample_seite[9], \
                        percentiles_sample_seite[14], percentiles_sample_seite[19], percentiles_sample_seite[24], \
                        percentiles_sample_seite[29], percentiles_sample_seite[34], percentiles_sample_seite[39], \
                        percentiles_sample_seite[44], percentiles_sample_seite[49], percentiles_sample_seite[54], \
                        percentiles_sample_seite[59], percentiles_sample_seite[64], percentiles_sample_seite[69], \
                        percentiles_sample_seite[74], percentiles_sample_seite[79], percentiles_sample_seite[84], \
                        percentiles_sample_seite[89], percentiles_sample_seite[94], percentiles_sample_seite[95], \
                        percentiles_sample_seite[96], percentiles_sample_seite[97], percentiles_sample_seite[98], \
                        percentiles_sample_seite[99]


    # Visualisierung der Ergebnisse
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(18, 4))

    # Histogramm der Wahrscheinlichkeitsdichte
    ax1.hist(m_achsen, density=True, bins='auto', histtype='stepfilled', color='tab:blue', alpha=0.3, label='sample pdf')
    
    # CDF auf normaler Skala
    ax2.plot(percentiles_sample_seite, steps, lw=2.0, color='tab:blue', alpha=0.7, label='sample cdf')
    
    # CDF auf Log-Skala
    ax3.plot(percentiles_sample_seite, steps, lw=2.0, color='tab:blue', alpha=0.7, label='sample cdf')

    # Achsenbeschriftungen
    ax1.set_xlim(left=-0.2, right=None)
    ax1.set_xlabel('Blockgröße a [m]', fontsize=14)
    ax1.set_ylabel('Wahrscheinlichkeitsdichte f(a)', fontsize=14)

    ax2.set_xlim(left=-0.2, right=None)
    ax2.set_xlabel('Blockgröße a [m]', fontsize=14)
    ax2.set_ylabel('Kumulative Wahrscheinlichkeit F(a)', fontsize=14)

    ax3.set_xscale('log')
    ax3.set_xlabel('Blockgröße a [m] (log Skala)', fontsize=14)
    ax3.set_ylabel('Kumulative Wahrscheinlichkeit F(a)', fontsize=14)

    # Legenden
    ax1.legend(loc='best', frameon=False)
    ax2.legend(loc='best', frameon=False)
    ax3.legend(loc='best', frameon=False)

    # Diagramm anzeigen
    st.pyplot(fig)

# Streamlit App
st.header("Blockgrößenverteilung")
st.subheader("Visualisierung der Wahrscheinlichkeitsdichte und kumulativen Wahrscheinlichkeit")

# Beispielhafte Eingabedaten
m_achsen = np.random.lognormal(mean=0, sigma=1, size=1000)  # Beispielhafte Daten für die Blockgrößen

# Aufruf der Funktion zur Berechnung und Visualisierung
berechne_perzentile_und_visualisierung(m_achsen)



# Anpassung einer Wahrscheinlichkeitsfunktion

