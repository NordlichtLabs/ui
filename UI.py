import hashlib
import time
from datetime import datetime
import streamlit as st

# --- 1. INITIALISIERUNG ---
if 'vault_time' not in st.session_state:
    st.session_state.vault_time = None
if 'v_hash' not in st.session_state:
    st.session_state.v_hash = None
if 'current_m_hash' not in st.session_state:
    st.session_state.current_m_hash = None

# --- 2. DESIGN & STYLING ---
st.set_page_config(page_title="VTL Erklär-Tool v2", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .step-number { font-size: 24px; font-weight: bold; color: #00d4ff; margin-bottom: 10px; }
    .explanation { font-size: 15px; line-height: 1.4; color: #ccc; margin-bottom: 25px; }
    
    /* Rechte Überschriften an linke anpassen */
    .right-header { font-size: 24px; font-weight: bold; color: #00d4ff; margin-bottom: 15px; display: block; }
    
    .explanation b { color: #00d4ff; font-size: 17px; }
    
    .vault-container {
        background-color: #1a1c23; 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid #00d4ff;
        margin-top: 10px;
    }
    .vault-hash-row { display: flex; align-items: flex-start; gap: 10px; }
    .algo-label { color: #00d4ff; font-weight: bold; font-family: monospace; white-space: nowrap; font-size: 14px; }
    .vault-hash { font-family: monospace; color: #00d4ff; word-break: break-all; font-size: 14px; }
    
    .vault-status-area { 
        margin-top: 12px; 
        border-top: 1px solid #333; 
        padding-top: 10px;
    }
    .status-text { color: #ff4b4b; font-weight: bold; font-size: 14px; font-family: monospace; }
    .timestamp-text { color: #ffffff; font-family: monospace; font-size: 14px; margin-top: 4px; }
    
    .validator-area {
        margin-top: 50px;
        padding-top: 30px;
        border-top: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ VTL (Verifiable Truth Layer): Interaktive Beweiskette")
st.write("Das Problem herkömmlicher Zufallsgeneratoren: Ein digitale Blindvertrauen. Ohne beweisbare Integrität bleibt jede digitale Entscheidung eine Vertrauensfrage, kein mathematischer Fakt.")

st.write("---")

# --- SCHRITT 1 ---
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('<div class="step-number">Schritt 1: Passwort festlegen</div>', unsafe_allow_html=True)
    user_salt = st.text_input("Gib hier Dein Passwort (Salt) ein:", placeholder="z. B. Sommer2026")
    
    if user_salt:
        if " " in user_salt:
            st.error("Leerzeichen sind nicht erlaubt!")
            st.session_state.vault_time = None
            st.session_state.v_hash = None
        else:
            if st.session_state.vault_time is None:
                st.session_state.vault_time = datetime.now().strftime("%H:%M:%S")
            
            v_hash = hashlib.sha256(user_salt.encode()).hexdigest()
            st.session_state.v_hash = v_hash
            
            st.markdown(f"**Dein Fingerabdruck im Vault:**")
            st.markdown(f"""
                <div class="vault-container">
                    <div class="vault-hash-row">
                        <span class="algo-label">SHA-256:</span>
                        <span class="vault-hash">{v_hash}</span>
                    </div>
                    <div class="vault-status-area">
                        <div class="status-text">STATUS: SEALED & LOCKED</div>
                        <div class="timestamp-text">TIMESTAMP: {st.session_state.vault_time} UTC</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.session_state.vault_time = None
        st.session_state.v_hash = None

with col2:
    st.markdown(f"""
    <div class="explanation">
        <span class="right-header">1. Die Versiegelung (COMMIT)</span>
        <b>Nutzer → Vault:</b> Der Nutzer gibt sein Passwort (Salt) ein.<br><br>
        <b>Vault:</b> Das System berechnet sofort den Vault-Hash.<br><br>
        <b>Vault → Nutzer:</b> Der Nutzer erhält eine Bestätigung mit Zeitstempel. Damit ist das Passwort (Salt) "eingeloggt".
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- SCHRITT 2 ---
col1, col2 = st.columns([1, 1])
today = datetime.now().strftime("%d.%m.%Y")
with col1:
    st.markdown('<div class="step-number">Schritt 2: Externe Datenquellen</div>', unsafe_allow_html=True)
    l_at = st.text_input(f"Quelle A (z. B. AT Lotto):", value="02, 18, 24, 33, 41, 45")
    l_it = st.text_input(f"Quelle B (z. B. IT Lotto):", value="11, 23, 35, 56, 62, 88")
    l_de = st.text_input(f"Quelle C (z. B. DE Lotto):", value="07, 14, 22, 31, 44, 49")
    
    entropy_string = f"{l_at}{l_it}{l_de}{today}"
    e_hash = hashlib.sha256(entropy_string.encode()).hexdigest()

with col2:
    st.markdown(f"""
    <div class="explanation">
        <span class="right-header">2. Die Gewinnung der Entropie (EXTERNAL)</span>
        <b>Welt:</b> Die Lotto-Ziehungen finden statt. Daten, die niemand kontrollieren kann.<br><br>
        <b>Generator:</b> Das System erstellt daraus den Entropy-Hash.
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Entropy-Hash:**")
    st.code(e_hash)

st.write("---")

# --- SCHRITT 3: DIE KOPPLUNG & ABLEITUNG ---
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('<div class="step-number">Schritt 3: Zufall generieren</div>', unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns([1, 1, 1])
    anzahl = p1.number_input("Anzahl:", value=5, min_value=1, key="count")
    range_min = p2.number_input("Zahlen von:", value=1, key="min")
    range_max = p3.number_input("Zahlen bis:", value=10000, key="max")
    
    calc_button = st.button("Zufallszahlen berechnen")

with col2:
    st.markdown(f"""
    <div class="explanation">
        <span class="right-header">3. Die Kopplung & Ableitung (GENERATE)</span>
        <b>Mathematik:</b> Aus Passwort und Entropy entsteht der Master-Hash.<br><br>
        <b>Ableitung:</b> Durch die Modulo-Formel werden die finalen Zufallszahlen erstellt.
    </div>
    """, unsafe_allow_html=True)

# Logik nach Button-Klick
if calc_button:
    if user_salt and " " not in user_salt:
        m_hash = hashlib.sha256(f"{e_hash}-{user_salt}".encode()).hexdigest()
        st.session_state.current_m_hash = m_hash
        
        results = []
        spanne = range_max - range_min + 1
        
        for i in range(1, int(anzahl) + 1):
            pick_hash = hashlib.sha256(f"{m_hash}-{i}".encode()).hexdigest()
            pick_int = int(pick_hash, 16)
            final_val = (pick_int % spanne) + range_min
            results.append(str(final_val))
        
        st.markdown(f"**Master-Hash = (Entropy-Hash + Passwort-Salt):**")
        st.code(m_hash)
        st.success(f"### Zufallszahlen: {', '.join(results)}")

        # --- NEU: DER MATHEMATISCHE BEWEIS (MODULO-LOGIK) ---
        st.write("---")
        st.subheader("🕵️‍♂️ Der mathematische Fairness-Beweis")
        st.info("Hier kannst du Schritt für Schritt nachrechnen, wie der Master-Hash in deine Zahlen umgewandelt wurde.")

        with st.expander("Rechenweg für jede Zahl einblenden"):
            for i in range(1, int(anzahl) + 1):
                derivation_input = f"{m_hash}-{i}"
                i_hash = hashlib.sha256(derivation_input.encode()).hexdigest()
                big_int = int(i_hash, 16)
                raw_result = big_int % spanne
                final_zahl = raw_result + range_min
                
                st.markdown(f"#### Zahl #{i}: **{final_zahl}**")
                st.code(f"""
1. Input: Master-Hash + Index "{i}"
2. Ableitungs-Hash (SHA-256): {i_hash}
3. Hexadezimal zu Dezimal: {big_int}
4. Modulo-Rechnung: {big_int} % {spanne} = {raw_result}
5. Finales Ergebnis (+ Min {range_min}): {final_zahl}
                """)
                if i < int(anzahl):
                    st.write("---")
        st.caption("Jeder SHA-256 Rechner im Internet wird bei diesen Eingaben zum exakt selben Ergebnis kommen.")

    elif " " in user_salt:
        st.error("Leerzeichen im Passwort sind nicht erlaubt!")
    else:
        st.error("Bitte gib zuerst ein Passwort in Schritt 1 ein!")

# --- SCHRITT 4: DIE VERIFIZIERUNG (AUDIT) ---
st.markdown('<div class="validator-area">', unsafe_allow_html=True)
st.markdown('<div class="step-number">🔍 Schritt 4: Die Verifizierung (AUDIT)</div>', unsafe_allow_html=True)

v_col1, v_col2 = st.columns([1, 1])
with v_col1:
    check_salt = st.text_input("Passwort zur Prüfung offenlegen:", type="password")
    if st.button("Integrität der Kette prüfen"):
        if " " in check_salt:
            st.error("Leerzeichen sind nicht erlaubt!")
        else:
            with st.spinner('Prüfung läuft...'):
                time.sleep(1)
                if check_salt and st.session_state.v_hash:
                    new_v_hash = hashlib.sha256(check_salt.encode()).hexdigest()
                    if new_v_hash == st.session_state.v_hash:
                        st.success(f"✅ Passwort passt zum Vault-Hash (Zeit: {st.session_state.vault_time})")
                        new_m_hash = hashlib.sha256(f"{e_hash}-{check_salt}".encode()).hexdigest()
                        if st.session_state.current_m_hash and new_m_hash == st.session_state.current_m_hash:
                            st.success("✅ Master-Hash korrekt rekonstruiert!")
                            st.info("### 🏆 STATUS: MATHEMATISCH BEWIESEN FAIR")
                        else:
                            st.error("❌ Master-Hash falsch. Die Datenquellen wurden verändert!")
                    else:
                        st.error("❌ Passwort passt nicht zum ursprünglichen Vault-Fingerabdruck!")
                else:
                    st.warning("Bitte Passwort eingeben.")

with v_col2:
    st.markdown(f"""
    <div class="explanation">
        <span class="right-header">4. Die Verifizierung (AUDIT)</span>
        <b>Nutzer:</b> Der Nutzer gibt sein ursprüngliches Passwort ein.<br><br>
        <b>Validator:</b> Das System berechnet die gesamte Kette neu. Nur wenn alle Hashes exakt übereinstimmen, gilt die Ziehung als verifiziert.
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
