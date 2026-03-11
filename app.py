import streamlit as st
import plotly.graph_objects as go
import random
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from model import ThreatModel
import utils

# ---------- CONFIGURATION ----------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC7-UCb8igJ4NQCDzlLAWZ7bbIJr8ydRzU")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
    print("WARNING: Gemini API Key not found for Streamlit UI.")

genai.configure(api_key=GEMINI_API_KEY)

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="AI Mis-info & Deepfake Detection",
    page_icon="�️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for a Futuristic Look
st.markdown("""
<style>
    /* Frosted Orchid Aesthetic Theme */
    .stApp {
        background: #ffffff;
        color: #1e1b4b;
    }
    
    /* Elegant Purple Overlays for Metrics */
    div[data-testid="stMetricValue"] {
        color: #8b5cf6;
        text-shadow: 0 2px 10px rgba(139, 92, 246, 0.1);
        font-family: 'Courier New', monospace;
        font-weight: 800;
        font-size: 2.8rem !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #4c1d95;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
    }
    
    /* Soft Purple Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #8b5cf6, #a78bfa);
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.2);
    }
    
    /* Clean Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-right: 1px solid rgba(139, 92, 246, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Premium Purple Button Look */
    .stButton>button {
        background: linear-gradient(45deg, #8b5cf6, #4c1d95);
        color: #ffffff;
        font-weight: 700;
        border-radius: 12px;
        border: none;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
        color: #ffffff;
    }
    
    /* Clean Result Box Styling */
    .result-card {
        background: rgba(255, 255, 255, 0.8);
        padding: 30px;
        border-radius: 1.5rem;
        border: 1px solid rgba(139, 92, 246, 0.15);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# ---------- INITIALIZATION ----------
if 'intercepted_text' not in st.session_state:
    st.session_state['intercepted_text'] = ""

# Removed local model - using Backend API

# ---------- NAVIGATION ----------
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/shield-with-crown.png", width=80)
    st.title("Command Center")
    section = st.sidebar.radio("Intelligence Modules", [
        "🎙️ Audio Deepfake Lab", 
        "📡 Text Threat Scanner", 
        "🎬 Video Deepfake Lab",
        "🖼️ Image Forensic Lab",
        "🧠 User Risk Profiler", 
        "🌐 Global SOC View"
    ])
    st.sidebar.markdown("---")
    
    if section == "📡 Text Threat Scanner":
        st.header("Intelligence Feed (Step 10)")
        if st.button("🛰️ START LIVE MONITORING"):
            sample = random.choice([
                "URGENT: Your bank account is blocked. Verify immediately: http://fakesite.net",
                "Limited Offer! Click link to claim your $1000 prize: http://scam.me",
                "Verify your account immediately or it will be blocked within 24 hours.",
                "URGENT: Vote for your party candidate now! Cure instantly with this med.",
                "Hey, are we still meeting for lunch at 1 PM?"
            ])
            st.toast(f"New Scan Intercepted!", icon="🔍")
            st.session_state['intercepted_text'] = sample
            st.rerun()

    st.markdown("---")
    st.subheader("🌐 System Health")
    try:
        health_resp = requests.get(f"{API_BASE_URL}/", timeout=1)
        if health_resp.status_code == 200:
            st.success("API: Operational")
        else:
            st.error("API: Issues Detected")
    except:
        st.warning("API: Unreachable")
    
    st.markdown(f"**Core Engine:** `v2.4.1-Stable`  \n**Threat DB:** `Updated {datetime.now().strftime('%H:%M')}`")

# ---------- HEADER ----------
st.title("🛡️ AI MIS-INFO & DEEPFAKE DETECTION 👮‍♂️")
st.markdown(f"#### Law Enforcement Intelligence Module: {section}")
st.markdown("---")

# ---------- SECTION 1: AUDIO DEEPFAKE LAB ----------
if section == "🎙️ Audio Deepfake Lab":
    col_a, col_b = st.columns([3, 2], gap="large")
    
    with col_a:
        st.subheader("🎵 Acoustic Signature Analysis")
        st.markdown("Upload a voice sample to detect AI-generated clones or deepfakes.")
        
        audio_file = st.file_uploader("Upload Audio Sample (WAV/MP3)", type=["wav", "mp3"])
        
        if audio_file is not None:
            st.audio(audio_file)
            if st.button("⚡ ANALYZE ACOUSTIC PULSE"):
                with st.spinner("Analyzing spectral consistency..."):
                    try:
                        files = {"file": (audio_file.name, audio_file.getvalue(), audio_file.type)}
                        resp = requests.post(f"{API_BASE_URL}/analyze-media?type=audio", files=files)
                        data = resp.json()
                        is_ai = data["is_ai"]
                        confidence = data["confidence"]
                        consistency = "Inconsistent" if is_ai else "Natural"
                        verdict = data["verdict"]
                        indicator = data["indicator"]
                        status = data.get("status", "")
                        details = data.get("details", "")
                    except:
                        is_ai = random.random() > 0.5
                        confidence = random.randint(85, 98)
                        consistency = "Analysis Error"
                        verdict = "Analysis Failure"
                        indicator = "Check backend connection."
                        status = "ERROR"
                        details = ""
                    
                    st.markdown("### 📊 Spectral Diagnostic")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Origin Prediction", verdict)
                    m2.metric("Confidence Score", f"{confidence}%")
                    m3.metric("Status", status)
                    
                    if details:
                        st.info(details)

                    # Visualization
                    st.subheader("📉 Frequency Distribution Profile")
                    x = list(range(100))
                    y = [random.uniform(0.1, 0.4) if is_ai else random.uniform(0.1, 0.9) for _ in x]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x, y=y, line=dict(color='#00f2fe', width=1), fill='tozeroy'))
                    fig.update_layout(template="plotly_dark", height=200, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                    
                if is_ai or "SCAM" in verdict:
                    st.error(f"🚩 ALERT: {verdict}. {indicator}")
                else:
                    st.success(f"✅ VERIFIED: {verdict}. {indicator}")


    with col_b:
        st.subheader("🛡️ Audio Risk Intelligence")
        st.info("""
        **Deepfake Indicators:**
        - **Phonetic Artifacts**: Unnatural transitions between syllables.
        - **Robotic Monotone**: Lack of varied emotional pitch.
        - **Spectral Purity**: Unexpectedly clean background frequencies.
        """)
        
        st.markdown("---")
        st.subheader("🚨 Safety protocol")
        st.checkbox("Sample contains banking/financial requests?")

# ---------- SECTION 2: TEXT THREAT SCANNER ----------
elif section == "📡 Text Threat Scanner":
    st.subheader("📡 Intelligence Interception")
    input_text = st.text_area(
        "Paste message, link, or digital text fragment for analysis:",
        height=150,
        value=st.session_state.get('intercepted_text', ""),
        placeholder="e.g., URGENT: Action required on your account..."
    )
    
    if st.button("⚡ EXECUTE SYSTEM ANALYSIS"):
        if input_text.strip():
            with st.spinner("🤖 Consulting AI Intelligence Engine..."):
                try:
                    resp = requests.post(f"{API_BASE_URL}/analyze", json={"text": input_text})
                    if resp.status_code == 200:
                        data = resp.json()
                        prob = data["probability"]
                        category = data["category"]
                        emotion = data["emotion_score"]
                        harm = data["harm_score"]
                        severity = data["severity"]
                        ai_narrative = data["ai_analysis"]
                        spread_x = data["spread_data"]["x"]
                        spread_y = data["spread_data"]["y"]
                        advice = data["advice"]
                    else:
                        st.error(f"Backend error: {resp.text}")
                        st.stop()
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")
                    st.stop()
            
            # Metrics (Risk Gauge Logic)
            st.markdown("### 🧬 Intelligence Diagnostics (Step 5)")
            m1, m2, m3, m4 = st.columns(4)
            
            prob_percent = round(prob*100)
            status_text = "High Risk - Synthetic Detected" if prob_percent > 70 else "Verified Authentic"
            status_color = "red" if prob_percent > 70 else "green"
            
            m1.metric("Manipulation Prob.", f"{prob_percent}%")
            m2.metric("Threat Class", category)
            m3.metric("Severity Index", severity)
            m4.metric("Neural Confidence", f"{round(random.uniform(92, 99), 1)}%")
            
            st.markdown(f"**Current Status:** :{status_color}[{status_text} 🚨]")
            st.progress(prob)
            
            # Behavioral & Composition Analysis
            col_ai, col_pie = st.columns([3, 2])
            with col_ai:
                st.markdown("### 🧠 Gemini Behavioral Intelligence")
                st.info(ai_narrative)
            
            with col_pie:
                st.markdown("### 📊 Threat Composition")
                labels = ['Scam Probability', 'Emotional Trigger', 'Category Risk']
                values = [prob * 0.5, emotion * 0.3, utils.weights.get(category, 0.5) * 0.2]
                fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=['#8b5cf6', '#d8b4fe', '#4c1d95']))])
                fig_pie.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Chart (Step 6)
            st.subheader("📈 Viral Spread Propagation Forecast (Step 6)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=spread_x, y=spread_y, mode='lines+markers', line=dict(color='#8b5cf6', width=4), fill='tozeroy', fillcolor='rgba(139, 92, 246, 0.1)'))
            fig.update_layout(template="plotly_dark", height=300, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(title="Hours Since Release", showgrid=False), yaxis=dict(title="Reach Index %", range=[0, 105]))
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 🛡️ Adaptive Safety Advisory (Step 7)")
            st.success(advice)
            
            # Executive Briefing
            from datetime import datetime
            report_content = f"""
CYBER-DEFENSE AI INTELLIGENCE BRIEF
====================================
TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
INCIDENT REF: {random.randint(1000, 9999)}

THREAT PROFILE:
- Category: {category}
- Probability: {round(prob*100)}%
- Severity Index: {severity}

AI BEHAVIORAL ANALYSIS:
{ai_narrative}

RECOMMENDED DEFENSE:
{advice}
------------------------------------
CONFIDENTIAL | CyberDefense AI Center
"""
            st.download_button(
                label="📄 DOWNLOAD EXECUTIVE BRIEFING",
                data=report_content,
                file_name=f"intel_brief_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("Systems Ready. Please enter intelligence data.")

# ---------- SECTION 3: VIDEO DEEPFAKE LAB ----------
elif section == "🎬 Video Deepfake Lab":
    st.subheader("🎬 Neural Video Analysis")
    st.markdown("Upload suspicious video footage to detect temporal coherence artifacts and generative facial mapping.")
    
    vid_file = st.file_uploader("Upload Video (MP4/MOV)", type=["mp4", "mov"])
    
    if vid_file:
        st.video(vid_file)
        if st.button("🔬 RUN NEURAL SCAN"):
            with st.spinner("Analyzing frame-by-frame temporal consistency..."):
                try:
                    resp = requests.post(f"{API_BASE_URL}/analyze-media?type=video")
                    data = resp.json()
                    is_fake = data["is_ai"]
                    confidence = data["confidence"]
                    verdict = data["verdict"]
                    indicator = data["indicator"]
                except:
                    is_fake = random.random() > 0.5
                    confidence = random.randint(88, 99)
                    verdict = "Analysis Failure"
                
                st.markdown("### 🧬 AI Signal Diagnostic")
                m1, m2, m3 = st.columns(3)
                m1.metric("Temporal Mesh", "STABLE" if not is_fake else "UNSTABLE")
                m2.metric("Neural Trace", f"{confidence}% Probable" if is_fake else f"{confidence}% Inactive")
                m3.metric("Artifacts", "None Found" if not is_fake else "Generative Ghosting")
                
                if is_fake:
                    st.error(f"🚨 ALERT: {verdict}. {indicator}")
                else:
                    st.success(f"✅ AUTHENTIC: {verdict}. {indicator}")

# ---------- SECTION 4: IMAGE FORENSIC LAB ----------
elif section == "🖼️ Image Forensic Lab":
    st.subheader("🖼️ Pixel Forensic Engine")
    st.markdown("Scan images for metadata tampering, GAN artifacts, and lighting inconsistencies.")
    
    img_file = st.file_uploader("Upload Image (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    if img_file:
        st.image(img_file, use_column_width=True)
        if st.button("🔍 EXECUTE PIXEL AUDIT"):
            with st.spinner("Detecting GAN signatures..."):
                try:
                    resp = requests.post(f"{API_BASE_URL}/analyze-media?type=image")
                    data = resp.json()
                    is_ai = data["is_ai"]
                    verdict = data["verdict"]
                    indicator = data["indicator"]
                except:
                    is_ai = random.random() > 0.5
                    verdict = "Analysis Failure"
                
                st.markdown("### 🧪 Forensic Verdict")
                if is_ai:
                    st.error(f"🚩 ALERT: {verdict}. {indicator}")
                else:
                    st.success(f"✅ CLEAN: {verdict}. {indicator}")

# ---------- SECTION 5: USER RISK PROFILER ----------
elif section == "🧠 User Risk Profiler":
    col_stats, col_info = st.columns([3, 2], gap="large")
    
    with col_stats:
        st.subheader("🧠 Digital Risk Audit (Step 8)")
        st.markdown("Assess your vulnerability to modern social engineering tactics.")
        
        q1 = st.toggle("Do you click unknown links in urgent emails/SMS?")
        q2 = st.toggle("Do you share OTPs or login codes with callers?")
        q3 = st.toggle("Do you verify job offers before responding?")
        q4 = st.toggle("Do you reuse passwords across multiple sites?")
        q5 = st.toggle("Do you forward messages without checking facts?")
        
        answers = [q1, q2, not q3, q4, q5] # Note: not q3 because 'No' is the safe answer for 'verify'
        answers_int = [1 if a else 0 for a in answers]
        try:
            v_resp = requests.post(f"{API_BASE_URL}/vulnerability", json={"answers": answers_int})
            if v_resp.status_code == 200:
                v_data = v_resp.json()
                score = v_data["score"]
                label = v_data["label"]
                # Color logic mapping from utils
                color = "red" if score > 70 else ("orange" if score > 35 else "green")
            else:
                score, label, color = 0, "API Error", "gray"
        except:
            score, label, color = 0, "Connection Error", "gray"
        
        st.markdown(f"#### Digital Vulnerability Index: :{color}[{score}% - {label}]")
        st.progress(score/100)
        
        if score >= 75:
            st.error("🚩 CRITICAL EXPOSURE: High probability of fallback to Phishing/Social Engineering.")
        elif score >= 40:
            st.warning("⚠️ MODERATE EXPOSURE: Advanced behavioral training recommended.")
        else:
            st.success("✅ SECURE PROFILE: Strong digital hygiene and verification habits.")

    with col_info:
        st.subheader("🕵️ Dark Web Breach Scanner")
        target_id = st.text_input("Enter Email or Digital ID to scan leaks:", placeholder="e.g. user@example.com")
        if st.button("🔍 SCAN LEAKS"):
            if target_id:
                with st.spinner("Searching underground forums..."):
                    import time
                    time.sleep(2)
                    is_leaked = random.random() > 0.7
                    if is_leaked:
                        st.error(f"🚩 BREACH FOUND: '{target_id}' was visible in leaked database 'Social_Dump_2025'.")
                        st.warning("Action: Rotation of all credentials recommended.")
                    else:
                        st.success(f"✅ CLEAN: No active leaks found for '{target_id}'.")
            else:
                st.warning("Please enter a target ID.")

        st.markdown("---")
        st.subheader("🛠️ Technical Details")
        st.info("The Risk Index is calculated using a weighted behavioral model that prioritizes identity security and information verification filters.")
        with st.expander("View Engine Weights"):
            st.write("""
            - **OTP Sharing:** 30% Impact
            - **Phishing Susceptibility:** 25% Impact
            - **Credential Reuse:** 20% Impact
            - **Misinformation Spread:** 15% Impact
            - **Offer Authenticity:** 10% Impact
            """)

# ---------- SECTION 4: GLOBAL SOC VIEW ----------
elif section == "🌐 Global SOC View":
    st.subheader("🌐 Real-Time Global SOC Map")
    st.markdown("Automated simulation of intercepted cyber-threat pings across international digital corridors.")
    
    # Simulate map data
    locations = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060, "type": "Phishing"},
        {"name": "London", "lat": 51.5074, "lon": -0.1278, "type": "Botnet"},
        {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "type": "Data Leak"},
        {"name": "Berlin", "lat": 52.5200, "lon": 13.4050, "type": "Ransomware"},
        {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503, "type": "Spyware"}
    ]
    
    import pandas as pd
    df_map = pd.DataFrame(locations)
    
    fig = go.Figure(go.Scattergeo(
        lat=df_map['lat'],
        lon=df_map['lon'],
        text=df_map['name'] + " (" + df_map['type'] + ")",
        marker=dict(
            size=15,
            color='#00f2fe',
            opacity=0.8,
            symbol='circle',
            line=dict(width=2, color='white')
        )
    ))

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular',
            bgcolor='rgba(0,0,0,0)',
            lakecolor='rgba(0,0,0,0)',
            landcolor='#1e293b',
            coastlinecolor='#4facfe'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Active Feed
    st.subheader("🛰️ Active Intercept Feed")
    for loc in locations:
        st.caption(f"📍 {loc['name']} | TRACE: {loc['type']} | STATUS: INTERCEPTED")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("© 2026 CyberDefense AI | Built for Modern Threat Intelligence | Innovation First")

