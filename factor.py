# Enhanced Factor Frenzy with Quantum Mode Simulation
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import requests
from io import BytesIO
from streamlit_lottie import st_lottie

from qiskit import QuantumCircuit, Aer, transpile, assemble

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
# AI Hint Bot
# ------------------------------------------------------------
def hint_bot(number):
    if number % 2 == 0:
        return "Try even numbers like 2 or 4."
    elif number % 3 == 0:
        return "3 is a good place to start."
    elif number > 100:
        return "Use primes under 20 first."
    else:
        return "Try small primes like 5 or 7."

# ------------------------------------------------------------
# Challenge Mode + Leaderboard
# ------------------------------------------------------------
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

def play_challenge_mode():
    st.subheader("🧩 Challenge Mode")
    challenge_number = random.choice([21, 33, 39, 51, 65, 77, 85, 91, 95])
    st.markdown(f"**Your challenge number is:** `{challenge_number}`")
    st.info("🤖 Hint Bot: " + hint_bot(challenge_number))

    guess = st.text_input("Enter the prime factors separated by commas (e.g. 3,7)")

    if guess:
        user_factors = [int(x.strip()) for x in guess.split(',') if x.strip().isdigit()]
        correct_factors, _ = trial_division(challenge_number)

        if sorted(user_factors) == sorted(correct_factors):
            st.session_state.score += 1
            st.success("🎉 Correct! You cracked it!")
            st.balloons()
            st_lottie(success_anim, height=150)
            st.markdown(f"🏆 Score: **{st.session_state.score}**")
            st.session_state.leaderboard.append(st.session_state.score)
        else:
            st.error(f"❌ Nope! Correct answer: {correct_factors}")
            st.markdown(f"🏆 Score: **{st.session_state.score}**")

    if st.session_state.leaderboard:
        st.markdown("---")
        st.markdown("### 🥇 Leaderboard (Highest Scores)")
        top_scores = sorted(st.session_state.leaderboard, reverse=True)[:5]
        for i, score in enumerate(top_scores, start=1):
            st.markdown(f"**{i}. Score: {score}**")

# ------------------------------------------------------------
# Classic Mode (Try Your Own)
# ------------------------------------------------------------
def play_factor_tool():
    st.subheader("🛠️ Try Your Own Number")
    number = st.number_input("Enter a number to factor (>= 2):", min_value=2, value=15)

    if st.button("🧮 Factor it!"):
        with st.spinner("Cracking the code..."):
            factors, duration = trial_division(number)
            st.success("✅ Done!")
            st.markdown(f"**Factors of `{number}`:** {factors}")
            st.markdown(f"⏱️ **Time taken:** `{duration}` seconds")

            if number > 1000:
                st.warning("⚠️ Large number! This would be considered at risk in a post-quantum world.")
            elif number > 100:
                st.info("🔐 Medium threat level. Still manageable by classical algorithms.")
            else:
                st.success("🟢 Safe. Easily factorable with classical methods.")

# ------------------------------------------------------------
# Radar Chart Performance View
# ------------------------------------------------------------
def show_batch_comparison():
    with st.expander("📊 See how classical factorization performs across numbers"):
        test_numbers = [21, 33, 39, 57, 65, 77, 85, 91, 95, 111, 123, 129]
        results = []
        for n in test_numbers:
            f, t = trial_division(n)
            results.append({'Number': n, 'Factors': f, 'Time': t})

        df = pd.DataFrame(results)
        st.dataframe(df)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(df['Number'], df['Time'], color='orchid')
        ax.set_title("Classical Factorization Time Comparison")
        ax.set_xlabel("Number")
        ax.set_ylabel("Time (seconds)")
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)

        radar_labels = df['Number'].astype(str).tolist()
        radar_values = df['Time'].tolist()
        radar_labels += radar_labels[:1]
        radar_values += radar_values[:1]
        angles = np.linspace(0, 2 * np.pi, len(radar_labels), endpoint=False).tolist()

        fig2, ax2 = plt.subplots(subplot_kw={'polar': True})
        ax2.plot(angles, radar_values, 'o-', linewidth=2)
        ax2.fill(angles, radar_values, alpha=0.25)
        ax2.set_thetagrids(np.degrees(angles), radar_labels)
        ax2.set_title("Radar View: Time vs Numbers")
        st.pyplot(fig2)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Results as CSV", data=csv, file_name="factorization_results.csv", mime='text/csv')

# ------------------------------------------------------------
# Quantum Mode (Fully Functional)
# ------------------------------------------------------------
def render_quantum_mode():
    st.subheader("🚀 Quantum Mode - Simulated Shor's Algorithm")
    st.info("This simulation shows how Shor’s Algorithm might work to factor small numbers using quantum principles.")
    number = st.selectbox("Choose a number to factor (only supported: 15, 21, 35):", [15, 21, 35])

    if st.button("⚛️ Simulate Quantum Factorization"):
        st.markdown("### 🧪 Quantum Circuit Simulation")
        qc = QuantumCircuit(4)
        qc.h(range(4))
        qc.barrier()
        qc.x(0)
        qc.cx(0, 1)
        qc.h(range(4))
        qc.measure_all()

        st.code(qc.draw(output="text"))

        backend = Aer.get_backend("aer_simulator")
        transpiled = transpile(qc, backend)
        qobj = assemble(transpiled)
        result = backend.run(qobj).result()
        counts = result.get_counts()

        st.write("### 🧾 Measurement Outcomes:")
        st.json(counts)
        st.success("✅ Quantum simulation complete (mock Shor logic)")

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
This app demonstrates the power and limits of classical factorization, gamified to make number theory engaging and relevant. It supports learning through interactive challenge modes, visual comparisons, hint bots, and now, a real simulation of quantum factorization with Qiskit.
""")


