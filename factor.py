import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import requests
from datetime import datetime
from io import BytesIO
from streamlit_lottie import st_lottie

# App Configuration
st.set_page_config(page_title="Factor Frenzy: Can You Beat the Machine?", layout="centered")
st.title("🎯 Factor Frenzy")
st.caption("Crack the code. Learn the logic. Outsmart the system.")

# Theme Toggle
dark_mode = st.sidebar.toggle("🌗 Dark Mode", value=False)
if dark_mode:
    st.markdown("""
        <style>
            body, .main { background-color: #1e1e1e; color: white; }
            .stButton>button { background-color: #4CAF50; color: white; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .main { background-color: #f5f5f5; }
            .stButton>button { background-color: #4CAF50; color: white; border-radius: 12px; padding: 10px 20px; font-weight: bold; }
            .stRadio>div>div { padding: 5px; }
        </style>
    """, unsafe_allow_html=True)

# Load Lottie Animations
@st.cache_data

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

success_anim = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json")
fail_anim = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jjj3gx1z.json")
quantumcat_anim = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_kqshlcsx.json")

# QuantumCat Assistant
def quantumcat(message):
    with st.chat_message("QuantumCat"):
        st_lottie(quantumcat_anim, height=100)
        st.markdown(f"**QuantumCat says:** {message}")

# Trial Division Factorization
if 'game_log' not in st.session_state:
    st.session_state.game_log = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

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

# AI Hint Bot

def hint_bot(number):
    if number % 2 == 0:
        return "Try even numbers like 2 or 4."
    elif number % 3 == 0:
        return "3 is a good place to start."
    elif number > 100:
        return "Use primes under 20 first."
    else:
        return "Try small primes like 5 or 7."

# Challenge Mode Logic + Leaderboard

def play_challenge_mode():
    st.subheader("🧩 Challenge Mode")
    challenge_number = random.choice([21, 33, 39, 51, 65, 77, 85, 91, 95])
    st.markdown(f"**Your challenge number is:** `{challenge_number}`")
    st.info("🤖 Hint Bot: " + hint_bot(challenge_number))
    quantumcat("Focus and factor fast!")

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
            st.session_state.leaderboard.append({"Score": st.session_state.score, "Time": str(datetime.now())})
            st.session_state.game_log.append({"Mode": "Challenge", "Input": challenge_number, "Result": "Correct", "Time": str(datetime.now())})
        else:
            st.error(f"❌ Nope! Correct answer: {correct_factors}")
            st_lottie(fail_anim, height=150)
            st.session_state.game_log.append({"Mode": "Challenge", "Input": challenge_number, "Result": "Incorrect", "Time": str(datetime.now())})
            st.markdown(f"🏆 Score: **{st.session_state.score}**")

    if st.session_state.leaderboard:
        st.markdown("---")
        st.markdown("### 🥇 Leaderboard (Highest Scores)")
        top_scores = sorted(st.session_state.leaderboard, key=lambda x: x['Score'], reverse=True)[:5]
        for i, row in enumerate(top_scores, start=1):
            st.markdown(f"**{i}. Score: {row['Score']}** — *{row['Time']}*")

# Main Factorization Tool

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

            st.session_state.game_log.append({"Mode": "Try It", "Input": number, "Factors": str(factors), "TimeTaken": duration, "When": str(datetime.now())})
            quantumcat("Nice work! Want to try a bigger challenge?")

# Batch Factor & Compare with Radar Chart

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
        quantumcat("This radar chart is sharp! 🧠")

# Summary Export

def show_summary():
    st.subheader("📋 Game Summary & Export")
    if st.session_state.game_log:
        df = pd.DataFrame(st.session_state.game_log)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full Game Log", data=csv, file_name="factor_frenzy_log.csv", mime='text/csv')
        quantumcat("Perfect! Now you can include this in your assignment 📘")
    else:
        st.info("No games played yet.")

# App Sections

with st.sidebar:
    st.header("🧭 Navigation")
    page = st.radio("Choose a mode:", ["Try It Yourself", "Challenge Mode", "Performance Chart", "Summary"])
    st.markdown("---")
    st.markdown("Made with ❤️ using Python & Streamlit")

if page == "Try It Yourself":
    play_factor_tool()
elif page == "Challenge Mode":
    play_challenge_mode()
elif page == "Performance Chart":
    show_batch_comparison()
elif page == "Summary":
    show_summary()

st.markdown("""
---
### 💡 Reflection
This app shows how classical factorization can scale across different inputs. It reflects the cryptographic challenges that quantum algorithms like Shor’s seek to overcome. While we do not simulate a full quantum circuit, this project highlights real-world performance, user interactivity, and educational design.

We enhanced engagement through gamification, scoring, QuantumCat assistant, leaderboard tracking, export options, hint suggestions, and radar plots.
""")
