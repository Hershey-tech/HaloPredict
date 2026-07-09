import streamlit as st
import pickle
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
from collections import Counter
from google import genai

# Load protein model
with open('halopredict_protein_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('feature_names_protein.pkl', 'rb') as f:
    feature_names = pickle.load(f)

# Gemini setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

amino_acids = 'ACDEFGHIKLMNPQRSTVWY'

def extract_protein_features(seq):
    seq = seq.upper()
    seq = ''.join([c for c in seq if c in amino_acids])
    features = {}
    features['length'] = len(seq)
    counts = Counter(seq)
    for aa in amino_acids:
        features[f'aa_{aa}'] = counts.get(aa, 0) / len(seq) if len(seq) > 0 else 0
    return features

def prepare_input(seq):
    features = extract_protein_features(seq)
    input_vector = {f: [features.get(f, 0)] for f in feature_names}
    return pd.DataFrame(input_vector)

def get_gemini_explanation(seq, prediction, probability, features):
    label = "Halophile" if prediction == 1 else "Non-Halophile"
    confidence = probability[1]*100 if prediction == 1 else probability[0]*100
    
    prompt = f"""
You are a bioinformatics expert. A protein sequence has been classified by a machine learning model.

Classification Result: {label}
Confidence: {confidence:.2f}%

Amino Acid Composition (top relevant ones):
- Lysine (K): {features['aa_K']*100:.2f}%
- Arginine (R): {features['aa_R']*100:.2f}%
- Leucine (L): {features['aa_L']*100:.2f}%
- Threonine (T): {features['aa_T']*100:.2f}%
- Glutamate (E): {features['aa_E']*100:.2f}%
- Sequence Length: {features['length']} amino acids

In 3-4 sentences, explain why this protein sequence is classified as {label}, 
focusing on the biological significance of these amino acid patterns in halophilic organisms.
Keep it scientific but easy to understand.
End with one line: "Key discriminating amino acids: ..."
"""
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text

# Page config
st.set_page_config(page_title="HaloPredict", page_icon="🧬", layout="centered")

st.title("🧬 HaloPredict")
st.subheader("Salt-Tolerance Protein Classifier")
st.markdown("""
HaloPredict analyzes **protein sequences** and predicts whether an organism is a 
**Halophile** (salt-tolerant) or **Non-Halophile**, based on amino acid composition.
Built using a Random Forest Classifier achieving **96.67% accuracy**.
""")

st.divider()

sequence = st.text_area("🔬 Enter Protein Sequence:", height=200,
                         placeholder="e.g. MLELLPTAVEGVSQAQITGRPEWIWLALGTALMGLG...")

col1, col2 = st.columns(2)
with col1:
    predict_btn = st.button("🔍 Predict", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

if clear_btn:
    sequence = ""

if predict_btn:
    if sequence.strip() == "":
        st.warning("⚠️ Please enter a valid protein sequence before proceeding.")
    elif len(sequence.strip()) < 10:
        st.warning("⚠️ Sequence is too short. Please enter a longer protein sequence.")
    else:
        seq_clean = sequence.strip().upper()

        with st.spinner("Analyzing sequence..."):
            features = extract_protein_features(seq_clean)
            input_vec = prepare_input(seq_clean)
            prediction = model.predict(input_vec)[0]
            probability = model.predict_proba(input_vec)[0]

        st.divider()

        if prediction == 1:
            st.success("✅ This sequence is classified as a HALOPHILE protein")
            col1, col2 = st.columns(2)
            col1.metric("Prediction", "Halophile")
            col2.metric("Confidence Score", f"{probability[1]*100:.2f}%")
        else:
            st.error("❌ This sequence is classified as a NON-HALOPHILE protein")
            col1, col2 = st.columns(2)
            col1.metric("Prediction", "Non-Halophile")
            col2.metric("Confidence Score", f"{probability[0]*100:.2f}%")

        with st.spinner("Generating AI explanation..."):
            try:
                explanation = get_gemini_explanation(seq_clean, prediction, probability, features)
                st.info(f"🤖 **AI Explanation:**\n\n{explanation}")
            except Exception as e:
                st.warning(f"AI explanation unavailable: {e}")

        with st.expander("🔬 Amino Acid Composition Details"):
            aa_data = {aa: [f"{features[f'aa_{aa}']*100:.2f}%"] for aa in amino_acids}
            st.table(pd.DataFrame(aa_data, index=["Percentage"]).T)

st.divider()

with st.expander("ℹ️ About HaloPredict"):
    st.markdown("""
    **HaloPredict** classifies proteins as Halophilic or Non-Halophilic based on amino acid composition.

    **How it works:**
    - Extracts amino acid composition (21 features: length + 20 AA percentages)
    - Random Forest Classifier trained on 207 protein sequences from NCBI
    - Google Gemini AI generates biological explanation for each prediction
    - 96.67% accuracy

    **Dataset:**
    - Halophile proteins: bacteriorhodopsin, halorhodopsin, ribosomal proteins
    - Non-halophile: ribosomal proteins from *E. coli*, *B. subtilis*, *Pseudomonas*

    **Technologies:** Python, Biopython, Scikit-learn, Streamlit, Google Gemini AI
    """)

st.caption("HaloPredict v3.0 — Powered by Biopython, Scikit-learn, Streamlit & Google Gemini AI")