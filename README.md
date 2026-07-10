# 🧬 HaloPredict
### Salt-Tolerance Protein Classifier using Machine Learning & Generative AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://halopredict.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange)](https://scikit-learn.org)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Flash-green)](https://ai.google.dev)

---

##  Short Description
HaloPredict is an AI-powered bioinformatics web application that analyzes protein sequences and classifies organisms as **Halophile** (salt-tolerant) or **Non-Halophile** using a Random Forest ML model with Google Gemini AI-generated biological explanations.

---

##  Project Overview
Halophilic organisms thrive in extreme high-salt environments and are of significant interest in biotechnology, industrial enzymes, and astrobiology. HaloPredict automates the identification of halophilic proteins using amino acid composition analysis — eliminating the need for manual biological expertise for initial screening.

This project was built as part of an internship project titled:
> **"Computational Modelling Using Artificial Intelligence for Biomedical Data Interpretation"**

---

## Why This Project Was Built
Traditional methods of identifying halophilic organisms require expensive lab experiments or deep biological expertise. This project demonstrates that machine learning trained on protein sequence features can:
- Rapidly classify protein sequences with 96.67% accuracy
- Generate human-readable biological explanations using Generative AI
- Make bioinformatics accessible through a simple web interface

**Note on Pivot:** The project initially used DNA-based 16S rRNA sequences (459 sequences, GC content + k-mer features) but the GC content difference between halophiles and non-halophiles was only ~2.7%, causing real-world classification failure despite high training accuracy. The approach was revised to use protein sequences with amino acid composition features, which provided biologically meaningful discrimination signals.

---

## Key Features
-  Protein sequence classification — Halophile or Non-Halophile
-  Confidence score for every prediction
-  AI-generated biological explanation (Google Gemini 2.5 Flash)
-  Amino acid composition breakdown table
-  Amazon Braket quantum demo (proof-of-concept)
-  Deployed on Streamlit Cloud — accessible anywhere

---

## Tech Stack
| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Machine Learning | Scikit-learn (Random Forest) |
| Data Collection | Biopython + NCBI Protein API |
| Generative AI | Google Gemini 2.5 Flash |
| Web Application | Streamlit |
| Deployment | Streamlit Cloud |
| Quantum Demo | Amazon Braket LocalSimulator |
| Version Control | GitHub |

---

## Architecture / Workflow

```
User inputs Protein Sequence
            ↓
Amino Acid Composition Extraction (21 features)
            ↓
Random Forest Classifier
            ↓
    ┌───────────────────┐
    │  Prediction Result │
    │  + Confidence Score│
    └───────────────────┘
            ↓
Google Gemini 2.5 Flash API
            ↓
    ┌───────────────────┐
    │ Biological         │
    │ Explanation        │
    └───────────────────┘
            ↓
Streamlit Web Interface displays results
```

---

##  Project Structure
```
HaloPredict/
├── halo.py                        # Main Streamlit application
├── halopredict_protein_model.pkl  # Trained Random Forest model
├── feature_names_protein.pkl      # Feature names for prediction
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── .env                           # API keys (NOT in GitHub)
└── README.md                      # Project documentation
```

---

## Dataset
| Category | Count | Species | Proteins |
|---|---|---|---|
| Halophile | 149 | *Halobacterium salinarum, Haloarcula marismortui, Halorubrum, Haloquadratum walsbyi* | bacteriorhodopsin, halorhodopsin, ribosomal proteins |
| Non-Halophile | 58 | *Escherichia coli, Bacillus subtilis, Pseudomonas* | ribosomal proteins |
| **Total** | **207** | **40+ species** | **NCBI Protein Database** |

**Feature Engineering:**
- 21 features extracted per sequence
- Sequence length (1 feature)
- Amino acid percentage for all 20 standard amino acids
- Key discriminating amino acids: **K (Lysine), R (Arginine), L (Leucine), T (Threonine), E (Glutamate)**

---

## Model Performance
| Metric | Score |
|---|---|
| Overall Accuracy | **96.67%** |
| Halophile Precision | 100% |
| Non-Halophile Precision | 93% |
| F1 Score | 0.97 |
| Training Split | 80% train / 20% test |
| Algorithm | Random Forest (100 estimators) |

---

## Prerequisites
- Python 3.10+
- pip
- Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))

---

##  Installation Steps

```bash
# Step 1 — Clone the repository
git clone https://github.com/Hershey-tech/HaloPredict.git

# Step 2 — Navigate to project folder
cd HaloPredict

# Step 3 — Install dependencies
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free Gemini API key at: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## How to Run Locally

```bash
streamlit run halo.py
```

App will open at: `http://localhost:8501`

---

## How to Use the Project

1. Open the app at [halopredict.streamlit.app](https://halopredict.streamlit.app)
2. Paste a protein sequence in the text area
3. Click **"Predict"**
4. View:
   - Halophile or Non-Halophile classification
   - Confidence score
   - AI-generated biological explanation
   - Amino acid composition breakdown

**Example Halophile Sequence (Bacteriorhodopsin — Halobacterium salinarum):**
```
MLELLPTAVEGVSQAQITGRPEWIWLALGTALMGLGTLYFLVKGMGVSDPDAKKFYAITTLVPAIAFTMYLSMLLGYGLTMVPFGGEQNPIYWARYADWLFTTPLLLLDLALLVDADQGTILALVGADGIMIGTGLVGALTKVYSYRFVWWAISTAAMLYILYVLFFGFTSKAESMRPEVASTFKVLRNVTVVLWSAYPVVWLIGSEGAGIVPLNIETLLFMVLDVSAKVGFGLILLRSRAIFGEAEAPEPSAGDGAAATSD
```

**Example Non-Halophile Sequence (Ribosomal protein — E. coli):**
```
MAKKTSSKNLVVKIRDLEHQKEIEELQAQLGQVTVRIDDGKQVQFDSSPYAAKLFKTSEQILAKLNELRAEAEKALADEGKISTKELIQKLNQEFQTLNAQLRRMQQQMQQQQRAGSSN
```

---

## Screenshots / Demo

🔗 **Live Demo:** [halopredict.streamlit.app](https://halopredict.streamlit.app)


---

## Data Flow

```
NCBI Protein Database
        ↓
Biopython (data collection)
        ↓
CSV Dataset (207 sequences, labeled)
        ↓
Feature Extraction (21 amino acid features)
        ↓
Balanced Dataset (oversampling)
        ↓
Random Forest Training
        ↓
.pkl Model Files
        ↓
Streamlit App → User Prediction
```

---

## Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repository
4. Set main file as `halo.py`
5. Add `GEMINI_API_KEY` in Streamlit Secrets
6. Deploy!

---

## Limitations
- Model trained on 207 sequences — larger dataset would improve accuracy
- Amino acid composition features do not capture sequence order information
- Google Gemini API has rate limits on free tier
- Quantum demo is proof-of-concept only — not a functional classifier
- Model may not generalize well to highly novel or synthetic protein sequences

---

## Quantum Computing — Future Scope

A proof-of-concept quantum demo was built using **Amazon Braket LocalSimulator**:
- 4 qubits encoding key amino acids (K, R, L, T)
- Hadamard gates for superposition
- RX rotation gates encoding amino acid composition values
- CNOT gates for qubit entanglement
- Result: Distinct dominant quantum states observed for halophilic vs non-halophilic proteins

**Future Possibilities:**
| Algorithm | Application |
|---|---|
| VQE (Variational Quantum Eigensolver) | Protein energy minimization |
| QAOA | Protein folding optimization |
| Quantum Feature Encoding | Enhanced sequence representation |

> Current limitation: NISQ-era quantum hardware has insufficient qubits and high noise for real protein classification. Quantum advantage in bioinformatics is expected post-2030.

---

## Future Improvements
- 🔲 3D Protein Structure Visualization (py3Dmol + AlphaFold API)
- 🔲 AWS Cloud Deployment (S3 + Lambda + API Gateway)
- 🔲 Expanded dataset with more halophile species
- 🔲 Deep learning model (CNN/LSTM on raw sequences)
- 🔲 BLAST sequence search integration
- 🔲 Multi-class classification (extreme halophile, moderate halophile, non-halophile)

---

## Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'Bio'` | Run `pip install biopython` |
| `ModuleNotFoundError: No module named 'dotenv'` | Run `pip install python-dotenv` |
| `API explanation unavailable: 429` | Gemini rate limit hit — wait 1 min and retry |
| `API explanation unavailable: 503` | Gemini server busy — fallback explanation shown |
| `FileNotFoundError: .pkl not found` | Ensure model files are in the same folder as `halo.py` |

---

## Security Notes
- Gemini API key is stored in `.env` file locally
- `.env` is listed in `.gitignore` — never pushed to GitHub
- Streamlit Cloud uses Secrets management for API key
- Never hardcode API keys directly in source code

---

## Author
**Harshita Prajapati**
B.Tech Biotechnology (AI/ML)
Amity University, Noida — Batch 2023–2027

---

## License
© 2025 Harshita Prajapati — All Rights Reserved
