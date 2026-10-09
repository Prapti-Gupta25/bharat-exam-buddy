import streamlit as st
import json
import os

st.set_page_config(
    page_title="Bharat Exam Buddy - AI Study Assistant",
    page_icon="🇮🇳",
    layout="centered"
)

# Toggle for real Bedrock usage (reads from environment if present)
USE_BEDROCK = os.getenv("USE_BEDROCK", "False").lower() in ("true", "1")

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding-bottom: 10px;
    }
    .badge {
        background-color: #ff9933;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .topic-pill {
        display: inline-block;
        padding: 5px 12px;
        margin: 4px;
        border-radius: 16px;
        background: #f0f2f6;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

st.title("🇮🇳 Bharat Exam Buddy")
st.write("✨ **AI-Powered Study Assistant for Indian Students (CBSE / ICSE / State Boards / JEE / NEET)**")

# Quick Example Selection
st.subheader("💡 Select a Popular Topic or Type Your Own:")
col1, col2, col3 = st.columns(3)

sample_q = ""
with col1:
    if st.button("🍎 Newton's Laws of Motion"):
        st.session_state["query"] = "Explain Newton's Laws of Motion with real-life examples"
    if st.button("⚡ Ohm's Law & Electricity"):
        st.session_state["query"] = "What is Ohm's Law and how is it used in electrical circuits?"
with col2:
    if st.button("🌿 Photosynthesis"):
        st.session_state["query"] = "Explain photosynthesis and its chemical equation"
    if st.button("📐 Pythagoras Theorem"):
        st.session_state["query"] = "What is the Pythagoras Theorem with proof formula?"
with col3:
    if st.button("🧬 DNA & Genetic Code"):
        st.session_state["query"] = "What is DNA structure and double helix model?"
    if st.button("🪐 Solar System & Gravity"):
        st.session_state["query"] = "Explain universal law of gravitation"

default_text = st.session_state.get("query", "")
user_input = st.text_area("Ask your academic question:", value=default_text, height=100, placeholder="e.g. Explain Newton's laws of motion or How does photosynthesis work?")

def mock_ai_response(question):
    q = question.lower()

    if "dna" in q or "genetic" in q:
        explanation = """
**DNA (Deoxyribonucleic Acid)** is the hereditary material in humans and almost all other organisms.
- **Double Helix Structure**: Discovered by Watson and Crick in 1953.
- **Nucleotide Bases**: Adenine (A) pairs with Thymine (T), and Cytosine (C) pairs with Guanine (G).
- **Function**: Encodes genetic instructions for biological development, cell function, and reproduction.
- **Exam Tip**: Remember the base pairing rule: **A-T** (2 hydrogen bonds) and **G-C** (3 hydrogen bonds).
"""
    elif "photosynthesis" in q:
        explanation = """
**Photosynthesis** is the process by which green plants and certain organisms transform light energy into chemical energy.
- **Chemical Equation**:
  `6CO₂ + 6H₂O + Sunlight ➔ C₆H₁₂O₆ (Glucose) + 6O₂`
- **Location**: Takes place inside chloroplasts containing chlorophyll pigment.
- **Two Phases**:
  1. *Light-dependent reactions* (Thylakoid membranes) - produces ATP & NADPH
  2. *Light-independent reactions (Calvin Cycle)* (Stroma) - synthesizes glucose
"""
    elif "newton" in q or "motion" in q:
        explanation = """
**Newton’s Three Laws of Motion**:

1️⃣ **First Law (Law of Inertia)**:
An object remains at rest or in uniform motion along a straight line unless acted upon by an unbalanced external force. *(Example: Passengers lurch forward when a bus suddenly stops).*

2️⃣ **Second Law (F = ma)**:
The rate of change of momentum is directly proportional to the applied force: **Force = Mass × Acceleration**. *(Example: Catching a cricket ball by pulling hands backward).*

3️⃣ **Third Law (Action & Reaction)**:
For every action, there is an equal and opposite reaction. *(Example: Rocket propulsion - burning gases push downwards, thrusting the rocket upwards).*
"""
    elif "ohm" in q or "electricity" in q:
        explanation = """
**Ohm's Law**:
At constant temperature, the current ($I$) flowing through a conductor is directly proportional to the potential difference ($V$) across its ends.

- **Formula**: $V = I \\times R$
- **Units**:
  - Voltage ($V$) in Volts
  - Current ($I$) in Amperes
  - Resistance ($R$) in Ohms ($\Omega$)
- **Graph**: A straight line through origin on a V-I graph confirms ohmic behavior.
"""
    elif "pythagor" in q or "triangle" in q:
        explanation = """
**Pythagoras Theorem**:
In any right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides.

- **Formula**: $a^2 + b^2 = c^2$
- **Where**:
  - $c$ = Hypotenuse (longest side opposite to 90° angle)
  - $a, b$ = Legs of the triangle
- **Common Pythagorean Triplets**: (3, 4, 5), (5, 12, 13), (7, 24, 25).
"""
    elif "gravit" in q or "solar" in q:
        explanation = """
**Universal Law of Gravitation (Newton)**:
Every particle of matter in the universe attracts every other particle with a force directly proportional to the product of their masses and inversely proportional to the square of the distance between them.

- **Formula**: $F = G \\frac{m_1 m_2}{r^2}$
- **Gravitational Constant**: $G \\approx 6.674 \\times 10^{-11} \\text{ N}\\cdot\\text{m}^2/\\text{kg}^2$
"""
    else:
        explanation = f"""
Here is a structured breakdown for **{question}**:

1. **Core Concept**:
   This fundamental topic is frequently tested in school and competitive board exams. It requires clear conceptual understanding of principles and definitions.

2. **Key Points to Remember for Exams**:
   - Define all primary terms clearly with SI units where applicable.
   - Draw neat, labeled diagrams for extra presentation marks.
   - Practice numerical problem sets related to the standard formulas.

3. **Sample Question**:
   *"Explain the principle with an example and state its practical applications."*
"""

    return f"""
### 📘 Academic Explanation & Solution

**Question:** {question}

{explanation}

---
💡 **Study Tip**: Always write formulas with proper units and state definitions verbatim in board exams!
🔗 *Powered by Bedrock-ready AI architecture designed for low-latency student assistance.*
"""

def call_bedrock(question):
    try:
        import boto3
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        body = json.dumps({
            "prompt": f"\n\nHuman: {question}\n\nAssistant:",
            "max_tokens_to_sample": 500
        })
        response = client.invoke_model(
            body=body,
            modelId="anthropic.claude-v2",
            accept="application/json",
            contentType="application/json"
        )
        result = json.loads(response["body"].read())
        return result.get("completion", str(result))
    except Exception as e:
        return mock_ai_response(question) + f"\n\n*(Note: Cloud Bedrock fallback activated: {e})*"

if st.button("🚀 Generate Answer", type="primary"):
    if user_input.strip():
        with st.spinner("Analyzing question and preparing step-by-step notes..."):
            if USE_BEDROCK:
                answer = call_bedrock(user_input)
            else:
                answer = mock_ai_response(user_input)
            st.markdown(answer)
    else:
        st.warning("⚠️ Please enter a question or select a topic above.")
