# Enhanced Factor Frenzy with Qiskit Quantum Mode (Cloud-Safe)
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import requests
from io import BytesIO
from streamlit_lottie import st_lottie

from qiskit import QuantumCircuit

# ------------------------------------------------------------
# 🧠 Page Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="Factor Frenzy: Can You Beat the Machine?", layout="wide")
st.title("🎯 Factor Frenzy")
st.caption("Crack the code. Learn the logic. Outsmart the system.")

st.markdown("""
<style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 12px; padding: 10px 20px; font-weight: bold; }
    .stRadio>div>div { padding: 5px; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🪄 Lottie Animations
# ------------------------------------------------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

success_anim = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json")
fail_anim = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jjj3gx1z.json")

# ------------------------------------------------------------
# 📘 Mini Explainer Cards
# ------------------------------------------------------------
def show_explainers():
    with st.expander("🧠 What is Factorization?"):
        st.write("Factorization is the process of breaking down a number into its prime factors. It's a core principle of encryption.")
    with st.expander("⚛️ Post-Quantum Cryptography"):
        st.write("Quantum computers can factor large numbers very quickly, threatening current RSA encryption. That's why learning this matters.")
    with st.expander("🎮 Why Gamify It?"):
        st.write("Making learning fun boosts understanding and retention — and shows how theory applies in practice.")

# ------------------------------------------------------------
# Trial Division Factorization
# ------------------------------------------------------------
def trial_division(n):
    start = time.time()
    factors = []
    for i in range(2, int(n**0.5) + 1):
        while n % i == 0:
            factors.append(i)
            n = n // i
    if n > 1:
        factors.append(n)
    end = time.time()
    return factors, round(end - start, 6)

# ------------------------------------------------------------
# Quantum Mode Simulation - Qiskit (No Aer)
# ------------------------------------------------------------
def render_quantum_mode():
    st.subheader("🚀 Quantum Mode — Shor's Algorithm Circuit (Visual Demo)")
    st.markdown("This simplified circuit mimics key steps in Shor's Algorithm for factoring 15.")
    
    # Build Shor-style circuit: superposition + controlled gates + inverse QFT
    qc = QuantumCircuit(4, 4)

    st.markdown("#### Step 1: Initialize superposition")
    qc.h(0)
    qc.h(1)

    st.markdown("#### Step 2: Mock controlled modular exponentiation")
    qc.cx(0, 2)
    qc.cx(1, 3)
    qc.barrier()

    st.markdown("#### Step 3: Apply inverse QFT (simplified)")
    qc.h(0)
    qc.h(1)
    qc.barrier()

    st.markdown("#### Step 4: Measure result")
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])

    # Display circuit diagram
    st.code(qc.draw(output='text'), language='qiskit')

    # Show example result (mocked counts)
    st.markdown("#### Simulated Measurement Outcome (Static Preview)")
    example_counts = {"0000": 250, "0011": 150, "1111": 120, "1001": 200}
    st.json(example_counts)

    st.success("✅ This Qiskit circuit mimics core steps of Shor's Algorithm for factoring 15.")
    st.info("For actual execution, run locally using Qiskit Aer and real modular exponentiation gates.")


# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------
show_explainers()

with st.sidebar:
    st.header("🧭 Navigation")
    page = st.radio("Choose a mode:", ["Classic Mode", "Challenge Mode", "Stats & Radar Chart", "Quantum Mode"])
    st.markdown("---")
    st.markdown("Made with ❤️ using Python & Streamlit")

# ------------------------------------------------------------
# Dummy Mode Logic for Other Sections (Preserve Existing)
# ------------------------------------------------------------
def play_factor_tool():
    st.subheader("🛠️ Try Your Own Number")
    number = st.number_input("Enter a number to factor (>= 2):", min_value=2, value=15)
    if st.button("🧮 Factor it!"):
        factors, duration = trial_division(number)
        st.success("✅ Done!")
        st.write(f"Factors: {factors}  |  Time: {duration}s")

def play_challenge_mode():
    st.subheader("🧩 Challenge Mode")
    challenge_number = random.choice([21, 33, 39])
    st.write(f"Your challenge: `{challenge_number}`")
    guess = st.text_input("Guess the prime factors (comma-separated):")
    if guess:
        user = [int(i.strip()) for i in guess.split(',') if i.strip().isdigit()]
        correct, _ = trial_division(challenge_number)
        if sorted(user) == sorted(correct):
            st.success("🎉 Correct!")
        else:
            st.error(f"❌ Incorrect. Actual: {correct}")

def show_batch_comparison():
    st.subheader("📊 Radar Stats")
    nums = [21, 33, 57, 65]
    times = [trial_division(n)[1] for n in nums]
    df = pd.DataFrame({"Number": nums, "Time": times})
    st.bar_chart(df.set_index("Number"))

# ------------------------------------------------------------
# Mode Switching
# ------------------------------------------------------------
if page == "Classic Mode":
    play_factor_tool()
elif page == "Challenge Mode":
    play_challenge_mode()
elif page == "Stats & Radar Chart":
    show_batch_comparison()
elif page == "Quantum Mode":
    render_quantum_mode()

# ------------------------------------------------------------
# 💬 Reflection Section
# ------------------------------------------------------------
st.markdown("""
---
### 💡 Reflection
This app demonstrates the power and limits of classical factorization, gamified to make number theory engaging and relevant. The Qiskit-based Quantum Mode offers real quantum circuit construction, designed to run locally, while still being displayed live on the cloud for educational use.
""")


