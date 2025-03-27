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
from scipy import stats
from scipy.stats import lognorm
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
    
# Funktion zur Berechnung der Perzentile und Visualisierung
def berechne_perzentile_und_visualisierung(m_achsen):
    steps = np.linspace(0.01, 1.00, num=100)

    Perc_steps = ['0','5','10','15','20','25','30','35','40','45','50','55','60','65','70','75','80','85','90','95','96','97','98','99','100']

    # Berechnung der Perzentile
    percentiles_m_achsen = np.quantile(m_achsen, steps)
    Perc_m_achsen = percentiles_m_achsen[0], percentiles_m_achsen[4], percentiles_m_achsen[9], \
                        percentiles_m_achsen[14], percentiles_m_achsen[19], percentiles_m_achsen[24], \
                        percentiles_m_achsen[29], percentiles_m_achsen[34], percentiles_m_achsen[39], \
                        percentiles_m_achsen[44], percentiles_m_achsen[49], percentiles_m_achsen[54], \
                        percentiles_m_achsen[59], percentiles_m_achsen[64], percentiles_m_achsen[69], \
                        percentiles_m_achsen[74], percentiles_m_achsen[79], percentiles_m_achsen[84], \
                        percentiles_m_achsen[89], percentiles_m_achsen[94], percentiles_m_achsen[95], \
                        percentiles_m_achsen[96], percentiles_m_achsen[97], percentiles_m_achsen[98], \
                        percentiles_m_achsen[99]


    # Visualisierung der Ergebnisse
    fig1, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(18, 4))

    # Histogramm der Wahrscheinlichkeitsdichte
    ax1.hist(m_achsen, density=True, bins='auto', histtype='stepfilled', color='tab:blue', alpha=0.3, label='sample pdf')
    
    # CDF auf normaler Skala
    ax2.plot(percentiles_m_achsen, steps, lw=2.0, color='tab:blue', alpha=0.7, label='sample cdf')
    
    # CDF auf Log-Skala
    ax3.plot(percentiles_m_achsen, steps, lw=2.0, color='tab:blue', alpha=0.7, label='sample cdf')

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
    st.pyplot(fig1)
    
# Funktion zur Anpassung der Verteilungen und Visualisierung
def passe_verteilungen_an_und_visualisiere(m_achsen, ausgewählte_verteilungen):
    fig2, (ax4, ax5) = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))

    # Histogramm der m_achsen
    ax4.hist(m_achsen, color='tab:blue', density=True, bins='auto', histtype='stepfilled', alpha=0.3, 
             label='Sample pdf')

    # Kumulative Verteilungen und CDF Berechnungen
    if 'genexpon' in ausgewählte_verteilungen:
        a1, b1, c1, loc1, scale1 = stats.genexpon.fit(m_achsen)
        X1 = np.linspace(stats.genexpon.ppf(0.001, a1, b1, c1, loc=loc1, scale=scale1), 
                         stats.genexpon.ppf(0.999, a1, b1, c1, loc=loc1, scale=scale1), len(m_achsen))
        ax4.plot(X1, stats.genexpon.pdf(X1, a1, b1, c1, loc=loc1, scale=scale1), '#800020', lw=1.0, alpha=0.7, label='genexpon pdf')
        ax5.plot(X1, stats.genexpon.cdf(X1, a1, b1, c1, loc=loc1, scale=scale1), '#800020', lw=1.0, alpha=0.7, label='genexpon cdf')

    if 'lognorm' in ausgewählte_verteilungen:
        shape1, loc1, scale1 = stats.lognorm.fit(m_achsen, floc=0)
        X2 = np.linspace(stats.lognorm.ppf(0.001, shape1, loc=loc1, scale=scale1), 
                         stats.lognorm.ppf(0.999, shape1, loc=loc1, scale=scale1), len(m_achsen))
        ax4.plot(X2, stats.lognorm.pdf(X2, shape1, loc=loc1, scale=scale1), '#00008B', lw=1.0, alpha=0.7, label='lognorm pdf')
        ax5.plot(X2, stats.lognorm.cdf(X2, shape1, loc=loc1, scale=scale1), '#00008B', lw=1.0, alpha=0.7, label='lognorm cdf')

    if 'expon' in ausgewählte_verteilungen:
        loc2, scale2 = stats.expon.fit(m_achsen)
        X3 = np.linspace(stats.expon.ppf(0.001, loc=loc2, scale=scale2), 
                         stats.expon.ppf(0.999, loc=loc2, scale=scale2), len(m_achsen))
        ax4.plot(X3, stats.expon.pdf(X3, loc=loc2, scale=scale2), '#333333', lw=1.0, alpha=0.7, label='expon pdf')
        ax5.plot(X3, stats.expon.cdf(X3, loc=loc2, scale=scale2), '#333333', lw=1.0, alpha=0.7, label='expon cdf')

    if 'powerlaw' in ausgewählte_verteilungen:
        a3, loc3, scale3 = stats.powerlaw.fit(m_achsen)
        X4 = np.linspace(stats.powerlaw.ppf(0.001, a3, loc=loc3, scale=scale3), 
                         stats.powerlaw.ppf(0.999, a3, loc=loc3, scale=scale3), len(m_achsen))
        ax4.plot(X4, stats.powerlaw.pdf(X4, a3, loc=loc3, scale=scale3), '#006400', lw=1.0, alpha=0.7, label='powerlaw pdf')
        ax5.plot(X4, stats.powerlaw.cdf(X4, a3, loc=loc3, scale=scale3), '#006400', lw=1.0, alpha=0.7, label='powerlaw cdf')

    # CDF für m_achsen (kumulative Verteilung)
    steps = np.linspace(0.01, 1.00, num=100)
    percentiles_m_achsen = np.quantile(m_achsen, steps)
    ax5.plot(percentiles_m_achsen, steps, lw=8.0, color='tab:blue', alpha=0.3, label='sample cdf')

    # Achsen für das Diagramm
    ax4.legend(loc='best', frameon=False)
    ax4.set_xlabel('Block size a [m]', fontsize=12)
    ax4.set_ylabel('Probability density f(a)', fontsize=12)
    
    ax5.legend(loc='best', frameon=False)
    ax5.set_xscale('log')
    ax5.set_xlabel('Block size a [m] (log scale)', fontsize=12)
    ax5.set_ylabel('Cumulative probability F(a) [%]', fontsize=12)

    # Diagramm anzeigen
    st.pyplot(fig2)
    
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
st.subheader("Visualisierung der Wahrscheinlichkeitsdichte und der kumulativen Wahrscheinlichkeit")

# Button zur Berechnung und Visualisierung
if st.button('Visualisieren'):
    # Platzhalter für fig1
    fig1_placeholder = st.empty()
    # Aufruf der Funktion zur Berechnung und Visualisierung
    berechne_perzentile_und_visualisierung(m_achsen)
    fig1_placeholder.pyplot(fig1)  # Plot für fig1


# Anpassung einer Wahrscheinlichkeitsfunktion

st.subheader("Anpassung und Visualisierung von Wahrscheinlichkeitsfunktionen")

# Auswahl der Verteilungen durch Checkboxen
verteilungen = ['genexpon', 'lognorm', 'expon', 'powerlaw']
ausgewählte_verteilungen = st.multiselect("Wählen Sie die Verteilungen zur Anpassung aus (mehrere möglich):", verteilungen)

# Button zur Berechnung und Visualisierung
if st.button('Anpassen'):
    # Platzhalter für fig2
    fig2_placeholder = st.empty()
    if ausgewählte_verteilungen:
        # Aufruf der Funktion zur Berechnung und Visualisierung mit den gewählten Verteilungen
        passe_verteilungen_an_und_visualisiere(m_achsen, ausgewählte_verteilungen)
        fig2_placeholder.pyplot(fig2)  # Plot für fig2
    else:
        st.warning("Bitte wählen Sie mindestens eine Verteilung aus.")


# asdf
