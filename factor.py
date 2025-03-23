# Factor Frenzy: Quantum Crackdown Edition - ULTRA MEGA MODE 

import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import json
import requests
from datetime import datetime
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Factor Frenzy: Quantum Crackdown", layout="wide")

# ------------------------------------------------------------
# 🧠 Theme Toggle
# ------------------------------------------------------------
dark_mode = st.sidebar.toggle("🌗 Dark Mode", value=False)
if dark_mode:
    st.markdown("""
        <style>
        body, .main { background-color: #1e1e1e; color: white; }
        .stButton>button { background-color: #4CAF50; color: white; }
        </style>
    """, unsafe_allow_html=True)

st.title("🎯 Factor Frenzy: Quantum Crackdown Edition")
st.caption("Learn, play, and outsmart cryptographic systems.")

# ------------------------------------------------------------
# 🔥 Load Lottie Animations
# ------------------------------------------------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

success_anim = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json")
fail_anim = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jjj3gx1z.json")
quantumcat_anim = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_kqshlcsx.json")

# ------------------------------------------------------------
# 📘 Mini Explainer Cards
# ------------------------------------------------------------
def show_explainers():
    with st.expander("🧠 What is Factorization?"):
        st.write("Factorization breaks a number into its prime parts.")
    with st.expander("⚛️ Post-Quantum Cryptography?"):
        st.write("Quantum computers can break RSA using fast factoring.")
    with st.expander("🎮 Why a Game?"):
        st.write("Gamifying crypto builds intuition and makes it memorable.")

# ------------------------------------------------------------
# 🐱 QuantumCat Assistant
# ------------------------------------------------------------
def quantumcat(message):
    with st.chat_message("QuantumCat"):
        st_lottie(quantumcat_anim, height=100)
        st.markdown(f"**QuantumCat says:** {message}")

# ------------------------------------------------------------
# 💾 Game History and Leaderboard
# ------------------------------------------------------------
if 'game_log' not in st.session_state:
    st.session_state.game_log = []
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

# ------------------------------------------------------------
# 🧮 Trial Division Logic
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
# 🎯 Classic Mode
# ------------------------------------------------------------
def render_classic_mode():
    st.subheader("🔢 Classic Mode")
    difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard", "Insane"])
    defaults = {"Easy": 55, "Medium": 143, "Hard": 1763, "Insane": 10007}
    number = st.number_input("Enter number:", min_value=2, value=defaults[difficulty])
    if st.button("🧮 Factor it!"):
        factors, duration = trial_division(number)
        st.success("✅ Done!")
        st.write(f"Factors: {factors}")
        st.write(f"⏱ Time: {duration}s")
        st_lottie(success_anim if len(factors) <= 2 else fail_anim, height=200)
        st.session_state.game_log.append({"Mode": "Classic", "Input": number, "Factors": factors, "Time": duration, "When": str(datetime.now())})
        quantumcat("Nice job factoring that! Try a harder one next time.")

# ------------------------------------------------------------
# 🎮 Challenge Mode with Scoreboard
# ------------------------------------------------------------
def render_challenge_mode():
    st.subheader("🎮 Challenge Mode")
    num = random.choice([21, 33, 39, 57, 65, 77])
    st.write(f"Number: `{num}`")
    name = st.text_input("Your Name:")
    guess = st.text_input("Your Guess (comma-separated):")
    if st.button("Submit"):
        correct, _ = trial_division(num)
        user = [int(x.strip()) for x in guess.split(',') if x.strip().isdigit()]
        if sorted(user) == sorted(correct):
            st.success("✅ Correct!")
            st_lottie(success_anim, height=150)
            score = len(correct)
            st.session_state.leaderboard.append({"Name": name or "Anon", "Score": score, "Time": str(datetime.now())})
            quantumcat("That was purr-fectly factored! 🐾")
        else:
            st.error(f"❌ Nope. Correct: {correct}")
            st_lottie(fail_anim, height=150)

    if st.session_state.leaderboard:
        st.markdown("### 🏆 Scoreboard")
        df = pd.DataFrame(st.session_state.leaderboard)
        st.table(df.sort_values("Score", ascending=False).head(5))

# ------------------------------------------------------------
# 📋 Summary and Export
# ------------------------------------------------------------
def render_summary():
    st.subheader("📋 Game Summary")
    if not st.session_state.game_log:
        st.info("No game history yet.")
    else:
        df = pd.DataFrame(st.session_state.game_log)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Game Log", csv, "factor_log.csv", "text/csv")
        quantumcat("Great progress! Export your results for your report 🧾")

# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------
show_explainers()
st.sidebar.header("🕹 Modes")
mode = st.sidebar.radio("Select:", ["Classic", "Challenge", "Summary"])

if mode == "Classic":
    render_classic_mode()
elif mode == "Challenge":
    render_challenge_mode()
elif mode == "Summary":
    render_summary()

# Reflection
st.markdown("""
---
### 💡 Reflection
This ultra-mega mode app blends learning and fun with quantum-inspired exploration. Through interactive play, leaderboard competition, and exportable results, it becomes both an educational tool and a cryptography showcase.
""")
