#!/usr/bin/env python
# coding: utf-8

# App zur Darstellung einer Blockgrößenverteilung und Anpassung einer Wahrscheinlichkeitsfunktion
# by Mariella Illeditsch

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import io
from io import BytesIO
from scipy import stats
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
    ax1.set_xlabel("Blockvolumen [m³]")
    ax1.set_ylabel("Häufigkeit")
    
    ax2.hist(m_werte, bins=20, color='skyblue', edgecolor='black')
    ax2.set_title("Histogramm der Achsen [m]")
    ax2.set_xlabel("Blockachse [m]")
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
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(18, 4))

    # Histogramm der Wahrscheinlichkeitsdichte
    ax1.hist(m_achsen, density=True, bins='auto', histtype='stepfilled', color='tab:blue', alpha=0.3, label='upload pdf')
    
    # CDF auf normaler Skala
    ax2.plot(percentiles_m_achsen, steps, lw=2.0, color='tab:blue', alpha=0.7, label='upload cdf')
    
    # CDF auf Log-Skala
    ax3.plot(percentiles_m_achsen, steps, lw=2.0, color='tab:blue', alpha=0.7, label='upload cdf')

    # Achsenbeschriftungen
    ax1.set_xlim(left=None, right=None)
    ax1.set_xlabel('Blockachse a [m]', fontsize=14)
    ax1.set_ylabel('Wahrscheinlichkeitsdichte f(a)', fontsize=14)

    ax2.set_xlim(left=None, right=None)
    ax2.set_xlabel('Blockachse a [m]', fontsize=14)
    ax2.set_ylabel('Kumulative Wahrscheinlichkeit F(a)', fontsize=14)

    ax3.set_xscale('log')
    ax3.set_xlabel('Blockachse a [m] (log)', fontsize=14)
    ax3.set_ylabel('Kumulative Wahrscheinlichkeit F(a)', fontsize=14)

    # Legenden
    ax1.legend(loc='best', frameon=False)
    ax2.legend(loc='best', frameon=False)
    ax3.legend(loc='best', frameon=False)

    # Diagramm übergeben
    return(fig)
    
# Funktion zur Anpassung der Verteilungen und Visualisierung
def passe_verteilungen_an_und_visualisiere(m_achsen, ausgewählte_verteilungen):
    fig, (ax4, ax5) = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))

    # Histogramm der m_achsen
    ax4.hist(m_achsen, color='tab:blue', density=True, bins='auto', histtype='stepfilled', alpha=0.3, 
             label='upload pdf')
        
    # CDF für m_achsen (kumulative Verteilung)
    steps = np.linspace(0.01, 1.00, num=100)
    percentiles_m_achsen = np.quantile(m_achsen, steps)
    ax5.plot(percentiles_m_achsen, steps, lw=8.0, color='tab:blue', alpha=0.3, label='upload cdf')
    
    # Kumulative Verteilungen und CDF Berechnungen
        
    if 'expon' in ausgewählte_verteilungen:
        loc3, scale3 = stats.expon.fit(m_achsen)
        X3 = np.linspace(stats.expon.ppf(0.001, loc=loc3, scale=scale3), 
                         stats.expon.ppf(0.999, loc=loc3, scale=scale3), len(m_achsen))
        ax4.plot(X3, stats.expon.pdf(X3, loc=loc3, scale=scale3), '#333333', lw=1.0, alpha=0.7, label='expon pdf')
        ax5.plot(X3, stats.expon.cdf(X3, loc=loc3, scale=scale3), '#333333', lw=1.0, alpha=0.7, label='expon cdf')
        
        # Speichern der Parameter in session_state
        st.session_state.loc3 = loc3
        st.session_state.scale3 = scale3

    if 'genexpon' in ausgewählte_verteilungen:
        a1, b1, c1, loc1, scale1 = stats.genexpon.fit(m_achsen)
        X1 = np.linspace(stats.genexpon.ppf(0.001, a1, b1, c1, loc=loc1, scale=scale1), 
                         stats.genexpon.ppf(0.999, a1, b1, c1, loc=loc1, scale=scale1), len(m_achsen))
        ax4.plot(X1, stats.genexpon.pdf(X1, a1, b1, c1, loc=loc1, scale=scale1), '#800020', lw=1.0, alpha=0.7, label='genexpon pdf')
        ax5.plot(X1, stats.genexpon.cdf(X1, a1, b1, c1, loc=loc1, scale=scale1), '#800020', lw=1.0, alpha=0.7, label='genexpon cdf')

        # Speichern der Parameter in session_state
        st.session_state.a1 = a1
        st.session_state.b1 = b1
        st.session_state.c1 = c1
        st.session_state.loc1 = loc1
        st.session_state.scale1 = scale1
                
    #if 'lognorm' in ausgewählte_verteilungen:
    #    shape2, loc2, scale2 = stats.lognorm.fit(m_achsen, floc=0)
    #    X2 = np.linspace(stats.lognorm.ppf(0.001, shape2, loc=loc2, scale=scale2), 
    #                     stats.lognorm.ppf(0.999, shape2, loc=loc2, scale=scale2), len(m_achsen))
    #    ax4.plot(X2, stats.lognorm.pdf(X2, shape2, loc=loc2, scale=scale2), '#00008B', lw=1.0, alpha=0.7, label='lognorm pdf')
    #    ax5.plot(X2, stats.lognorm.cdf(X2, shape2, loc=loc2, scale=scale2), '#00008B', lw=1.0, alpha=0.7, label='lognorm cdf')

        # Speichern der Parameter in session_state
    #    st.session_state.shape2 = shape2
    #    st.session_state.loc2 = loc2
    #    st.session_state.scale2 = scale2
        
    if 'powerlaw' in ausgewählte_verteilungen:
        a4, loc4, scale4 = stats.powerlaw.fit(m_achsen)
        X4 = np.linspace(stats.powerlaw.ppf(0.001, a4, loc=loc4, scale=scale4), 
                         stats.powerlaw.ppf(0.999, a4, loc=loc4, scale=scale4), len(m_achsen))
        ax4.plot(X4, stats.powerlaw.pdf(X4, a4, loc=loc4, scale=scale4), '#006400', lw=1.0, alpha=0.7, label='powerlaw pdf')
        ax5.plot(X4, stats.powerlaw.cdf(X4, a4, loc=loc4, scale=scale4), '#006400', lw=1.0, alpha=0.7, label='powerlaw cdf')

        # Speichern der Parameter in session_state
        st.session_state.a4 = a4
        st.session_state.loc4 = loc4
        st.session_state.scale4 = scale4
    
    # Berechne das Histogramm (counts und bins)
    counts, bins = np.histogram(m_achsen, bins='auto', density=True)
        # Finde den maximalen Wert des Histogramms
    max_y_value = max(counts)

    # Achsen für das Diagramm
    ax4.legend(loc='best', frameon=False)
    ax4.set_ylim(0, max_y_value * 1.1)
    ax4.set_xlabel('Blockachse a [m]', fontsize=12)
    ax4.set_ylabel('Wahrscheinlichkeitsdichte f(a)', fontsize=12)
    
    ax5.legend(loc='best', frameon=False)
    ax5.set_xscale('log')
    ax5.set_xlabel('Blockachse a [m] (log)', fontsize=12)
    ax5.set_ylabel('Kumulative Wahrscheinlichkeit F(a)', fontsize=12)
    
    # Parameter und Diagramm übergeben
    return fig
    
# Function to calculate percentiles for a distribution
def calculate_percentiles(distribution, percentiles, *params):
    return [distribution.ppf(p / 100, *params) for p in percentiles]

# Streamlit App

# Zeige das Logo zu Beginn der App
logo = Image.open("pi-geotechnik-1-RGB-192-30-65.png")  # Lade das Bild
st.image(logo, caption="https://pi-geo.at/", use_container_width=True)  # Zeige das Logo an

st.title("Willkommen bei pi!")
st.header("Blockgrößenverteilung")

# URL der Beispiel-Datei auf GitHub
example_file_url = "https://github.com/pi-geotechnik/Blockverteilung/raw/main/Bloecke_Dachsteinkalk.txt" 

# Auswahl der Einheit
einheit = st.selectbox("Wählen Sie die Einheit der Eingabedaten:", ["Volumen in m³", "Masse in t (Dichte erforderlich)"])

# Überprüfen, ob sich die Einheit geändert hat
if 'einheit' in st.session_state and st.session_state.einheit != einheit:
    # Löschen von m_achsen, falls es bereits existiert
    if 'm_achsen' in st.session_state:
        del st.session_state['m_achsen']
    # Löschen von vorhandenen Figuren, falls sie im session_state existieren
    if 'fig1' in st.session_state:
        del st.session_state['fig1']
    if 'fig2' in st.session_state:
        del st.session_state['fig2']
    # Optional: Anzeige einer Nachricht, dass m_achsen gelöscht wurde
    st.warning("Bitte laden Sie eine Blockdatei hoch. Achtung: Bitte stellen Sie sicher, dass alle Zahlen in der hochgeladenen Textdatei den Punkt ('.') statt des Kommas (',') als Dezimaltrennzeichen verwenden!")
    
# Speichern der Auswahl im session_state
st.session_state.einheit = einheit  # Speichert die ausgewählte Einheit


if einheit == "Volumen in m³":
    # Button für die Auswahl der Beispiel-Datei
    if st.button("Beispiel-Datei 'Dachsteinkalk' laden"):
        # Entferne die hochgeladene Datei aus der session_state, falls vorhanden
        if "uploaded_file" in st.session_state:
            del st.session_state.uploaded_file  # Löscht die hochgeladene Datei
        # Beispiel-Datei aus GitHub laden
        response = requests.get(example_file_url)
        
        if response.status_code == 200:
            # Erstelle ein 'BytesIO'-Objekt aus der heruntergeladenen Datei, um sie wie eine hochgeladene Datei zu behandeln
            example_file_content = response.content
            uploaded_file = io.BytesIO(example_file_content)  # Dies ist die "hochgeladene" Beispiel-Datei

            # Zeige die erfolgreiche Meldung an
            st.success("Die Beispiel-Datei 'Dachsteinkalk' wurde erfolgreich geladen.")
            st.write(st.session_state)
            
            if "uploaded_file" in st.session_state:
                st.warning("Achtung: eine bereits zuvor hochgeladene 'Eigene Liste mit m³-Werten' muss entfernt (Klick auf 'x') und die Beispiel-Datei neu geladen werden!")
            
            # Speichern der Datei im session_state
            st.session_state.uploaded_file = uploaded_file
            st.write(st.session_state)
            
            # Verarbeite die Datei, als ob sie über den file_uploader hochgeladen wurde
            file_content = uploaded_file.read().decode("utf-8")  # Beispiel: als Textdatei lesen
            st.text_area("Inhalt der Datei:", file_content, height=200)  # Zeige den Inhalt der Datei als Text an
            
            try:
                # Text in Zahlen (m³) umwandeln
                werte_liste = [float(val.strip()) for val in file_content.splitlines() if val.strip().replace(".", "", 1).isdigit()]
                
                # Filtere nur Werte mit genau drei Dezimalstellen und entferne 0.00-Werte
                werte = [wert for wert in werte_liste if wert >= 0.000]
                
                # Sortieren der Werte in aufsteigender Reihenfolge
                werte.sort()
                
                # Anzahl der Werte ausgeben
                st.write(f"Anzahl der Blöcke: {len(werte)}")
                
                # Berechnung der dritten Wurzel (Achsen in Metern)
                m_achsen = [berechne_dritte_wurzel(val) for val in werte]
                
                # Speichern von m_achsen in session_state für spätere Verwendung
                st.session_state.m_achsen = m_achsen
                
            except Exception as e:
                st.error(f"Fehler bei der Verarbeitung der Daten: {e}")
        
        else:
            st.error("Fehler beim Laden der Datei. Überprüfen Sie die URL oder das Netzwerk.")
    
    # Falls der Benutzer eine Datei hochladen möchte
    uploaded_file = st.file_uploader("Eigene Liste mit m³-Werten hochladen:", type=["txt"])
    
    if uploaded_file is not None:
        # Speichern der hochgeladenen Datei im session_state
        st.session_state.uploaded_file = uploaded_file
        st.write(st.session_state)
        # Datei verarbeiten wie oben
        file_content = uploaded_file.read().decode("utf-8")
        st.text_area("Inhalt der Datei:", file_content, height=200)
        
        try:
            # Text in Zahlen (m³) umwandeln
            werte_liste = [float(val.strip()) for val in file_content.splitlines() if val.strip().replace(".", "", 1).isdigit()]
            
            # Filtere nur Werte mit genau drei Dezimalstellen und entferne 0.00-Werte
            werte = [wert for wert in werte_liste if wert >= 0.000]
            
            # Sortieren der Werte in aufsteigender Reihenfolge
            werte.sort()
            
            # Anzahl der Werte ausgeben
            st.write(f"Anzahl der Blöcke: {len(werte)}")
            
            # Berechnung der dritten Wurzel (Achsen in Metern)
            m_achsen = [berechne_dritte_wurzel(val) for val in werte]
            
            # Speichern von m_achsen in session_state für spätere Verwendung
            st.session_state.m_achsen = m_achsen
            
        except Exception as e:
            st.error(f"Fehler bei der Verarbeitung der Daten: {e}")


# Datei-Upload für Masse in t (Dichte erforderlich)
if einheit == "Masse in t (Dichte erforderlich)":
    uploaded_file = st.file_uploader("Eigene Liste mit t-Werten hochladen:", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("Inhalt der Datei:", text, height=200)

        try:
            # Text in Zahlen (Tonnen) umwandeln
            tonnen = [float(val.strip()) for val in text.splitlines() if val.strip().replace(".", "", 1).isdigit()]
            
            # Sortieren der Werte in aufsteigender Reihenfolge
            tonnen.sort()
            
            # Anzahl der Werte ausgeben
            st.write(f"Anzahl der Blöcke: {len(tonnen)}")
            
            # Eingabe der Dichte in kg/m³
            dichte_kg_m3 = st.number_input("Geben Sie die Dichte in kg/m³ ein:", min_value=0, value=2650, step=10)
            
            # Umrechnung von Tonnen in m³
            werte_m3 = [val * 1000 / dichte_kg_m3 for val in tonnen]

            # Berechnung der dritten Wurzel (Achsen in Metern)
            m_achsen = [berechne_dritte_wurzel(val) for val in werte_m3]
            # st.write("Achsen in Metern:")
            # st.write(m_achsen)

            # Visualisierung der Histogramme
            # visualisiere_histogramm_m3_und_m(m_achsen, werte_m3)
            
            # Speichere m_achsen in session_state für spätere Verwendung
            st.session_state.m_achsen = m_achsen

        except Exception as e:
            st.error(f"Fehler bei der Verarbeitung der Daten: {e}")  


# Darstellung
st.subheader("Visualisierung der Wahrscheinlichkeitsverteilung")

# Berechnung und Visualisierung
if 'einheit' in st.session_state:
    if st.session_state.einheit == "Volumen in m³" and 'm_achsen' in st.session_state:
        # Aufruf der Funktion zur Berechnung und Visualisierung mit m_achsen
        fig1 = berechne_perzentile_und_visualisierung(st.session_state.m_achsen)
        st.session_state.fig1 = fig1  # Speichern von fig1 im session_state
    elif st.session_state.einheit == "Masse in t (Dichte erforderlich)" and 'm_achsen' in st.session_state:
        # Aufruf der Funktion zur Berechnung und Visualisierung mit m_achsen
        fig1 = berechne_perzentile_und_visualisierung(st.session_state.m_achsen)
        st.session_state.fig1 = fig1  # Speichern von fig1 im session_state

# Anzeige der gespeicherten Grafiken
if 'fig1' in st.session_state:
    st.pyplot(st.session_state.fig1)  # Zeigt fig1 an, wenn es im session_state gespeichert ist


# Anpassung einer Wahrscheinlichkeitsfunktion
st.subheader("Anpassung von Wahrscheinlichkeitsfunktionen")

# Alle Verteilungen werden automatisch berechnet und visualisiert
if 'einheit' in st.session_state:
    if st.session_state.einheit == "Volumen in m³" and 'm_achsen' in st.session_state:
        fig2 = passe_verteilungen_an_und_visualisiere(st.session_state.m_achsen, ['genexpon', 'expon', 'powerlaw'])
        st.session_state.fig2 = fig2
    elif st.session_state.einheit == "Masse in t (Dichte erforderlich)" and 'm_achsen' in st.session_state:
        # Aufruf der Funktion zur Berechnung und Visualisierung mit m_achsen
        fig2 = passe_verteilungen_an_und_visualisiere(st.session_state.m_achsen, ['genexpon', 'expon', 'powerlaw'])
        st.session_state.fig2 = fig2  # Speichern von fig2 im session_state

# Visualisierung der berechneten Verteilungen
if 'fig2' in st.session_state:
    st.pyplot(st.session_state.fig2)


# Tabelle mit Perzentilen 
st.subheader("Tabellenvergleich der Perzentilen")

if 'm_achsen' in st.session_state:
    Perc_steps_short = ['0', '25', '50', '75', '95', '96', '97', '98', '99', '100']
    percentiles = [0, 25, 50, 75, 95, 96, 97, 98, 99, 100]

    # Sicherstellen, dass alle notwendigen Parameter gespeichert sind
    if all(param in st.session_state for param in ['a1', 'b1', 'c1', 'loc1', 'scale1', 'loc3', 'scale3', 'a4', 'loc4', 'scale4']): # 'shape2', 'loc2', 'scale2', 
        try:
            # Berechnung der Perzentile für jede Verteilung
            L1s = calculate_percentiles(stats.genexpon, percentiles, 
                                        st.session_state.a1, st.session_state.b1, st.session_state.c1, 
                                        st.session_state.loc1, st.session_state.scale1)
            #L2s = calculate_percentiles(stats.lognorm, percentiles, 
            #                            st.session_state.shape2, st.session_state.loc2, st.session_state.scale2)
            L3s = calculate_percentiles(stats.expon, percentiles, 
                                        st.session_state.loc3, st.session_state.scale3)
            L4s = calculate_percentiles(stats.powerlaw, percentiles, 
                                        st.session_state.a4, st.session_state.loc4, st.session_state.scale4)
            
            # Sicherstellen, dass alle Perzentile als numpy-Array vorliegen
            upload_perz = berechne_perzentile(m_achsen, [0, 25, 50, 75, 95, 96, 97, 98, 99, 100])
            upload_perz = np.array(upload_perz)
            L1s = np.array(L1s)
            #L2s = np.array(L2s)
            L3s = np.array(L3s)
            L4s = np.array(L4s)

            upload_perz3 = upload_perz**3
            L1s3 = L1s**3
            #L2s3 = L2s**3
            L3s3 = L3s**3
            L4s3 = L4s**3
            
            df1 = pd.DataFrame({
                "percentile": Perc_steps_short,
                "upload [m³]": upload_perz3,
                "expon [m³]": L3s3,
                "genexpon [m³]": L1s3,
                "powerlaw [m³]": L4s3
            })
            # CSS-Styling für bestimmte Zeilen (5.-8. Zeile fett drucken)
            # Setze die Formatierung von Zeilen 5 bis 8 auf fett
            styled_df = df1.style.apply(lambda x: ['font-weight: bold' if 5 <= i <= 8 else '' for i in range(len(x))], axis=1)
            # Entferne die Indexspalte
            styled_df = styled_df.hide(axis="index")
            # Zeige den DataFrame ohne Index und mit den gestylten Zeilen
            st.dataframe(styled_df)

        except Exception as e:
            if 'einheit' in st.session_state:
                # Wenn sich die Einheit ändert (von m³ zu Tonnen oder umgekehrt)
                if 'm_achsen' not in st.session_state:
                    st.error("Blockliste erforderlich. Bitte auswählen oder hochladen!")
                else:
                    st.error(f"Bitte laden Sie die Beispiel-Datei neu.")