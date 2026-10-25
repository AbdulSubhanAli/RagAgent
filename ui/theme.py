import streamlit as st

def apply_aurora_theme():
    """
    Injects global CSS variables, Google Sora font, background aurora orbs,
    file uploader glass styling, fixed bottom prompt bar, high-contrast inputs,
    and crystal-clear slider values & limit ticks.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap');

    /* DESIGN TOKENS */
    :root {
      --bg: #0B0820;
      --text: #EDEBFF;
      --muted: #B7B2E6;
      --icon: #C9C4F5;
      --violet: #7C5CFF;
      --teal: #2DE2C8;
      --teal-text: #5CF0DA;
      --magenta: #FF4FD8;
      --glass-bg: linear-gradient(135deg, rgba(255,255,255,.12), rgba(255,255,255,.03));
      --glass-border: 1px solid rgba(255,255,255,.2);
      --glass-blur: blur(18px);
      --radius: 22px;
      --font-sora: 'Sora', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* GLOBAL RESET & BASE STYLES */
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
      background-color: var(--bg) !important;
      color: var(--text) !important;
      font-family: var(--font-sora) !important;
      overflow-x: hidden;
    }

    /* Add bottom padding so scrolled messages stay above the fixed bottom bar */
    .main .block-container {
      padding-bottom: 120px !important;
    }

    /* HEADER & SIDEBAR TOGGLE FIX */
    header[data-testid="stHeader"] {
      background: transparent !important;
      z-index: 999 !important;
    }

    /* Hide unwanted default elements (footer, deploy button, main menu) */
    footer, #MainMenu, .stDeployButton, [data-testid="stDecoration"] {
      display: none !important;
      visibility: hidden !important;
    }

    /* STYLED SIDEBAR EXPAND / COLLAPSE BUTTONS (<< AND >>) */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    button[aria-label="Expand sidebar"],
    button[aria-label="Collapse sidebar"] {
      display: flex !important;
      visibility: visible !important;
      color: #5CF0DA !important;
      background: rgba(255, 255, 255, 0.12) !important;
      border: 1px solid rgba(255, 255, 255, 0.25) !important;
      backdrop-filter: blur(12px) !important;
      -webkit-backdrop-filter: blur(12px) !important;
      border-radius: 12px !important;
      z-index: 100000 !important;
      transition: all 0.2s ease !important;
    }

    [data-testid="stSidebarCollapsedControl"]:hover,
    [data-testid="collapsedControl"]:hover,
    button[aria-label="Expand sidebar"]:hover,
    button[aria-label="Collapse sidebar"]:hover {
      background: rgba(45, 226, 200, 0.25) !important;
      border-color: #2DE2C8 !important;
      box-shadow: 0 0 15px rgba(45, 226, 200, 0.5) !important;
    }

    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg,
    button[aria-label="Expand sidebar"] svg,
    button[aria-label="Collapse sidebar"] svg {
      fill: #5CF0DA !important;
      color: #5CF0DA !important;
    }

    /* ANIMATED AURORA BACKGROUND ORBS */
    .aurora-bg-container {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      overflow: hidden;
      pointer-events: none;
      z-index: 0;
    }

    .aurora-orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(50px);
      animation: float 8s ease-in-out infinite;
    }

    .orb-violet {
      width: 560px; height: 560px;
      background: var(--violet);
      opacity: 0.6;
      top: -120px; left: -140px;
    }

    .orb-teal {
      width: 520px; height: 520px;
      background: var(--teal);
      opacity: 0.4;
      bottom: -140px; right: -100px;
      animation-delay: -3s;
    }

    .orb-magenta {
      width: 360px; height: 360px;
      background: var(--magenta);
      opacity: 0.3;
      top: 380px; left: 520px;
      animation-delay: -5s;
    }

    @keyframes float {
      0%, 100% { transform: translate(0, 0); }
      50% { transform: translate(0, -14px); }
    }

    [data-testid="stAppViewContainer"] > .main {
      position: relative;
      z-index: 1;
      background: transparent !important;
    }

    /* SIDEBAR GLASS PANEL */
    [data-testid="stSidebar"] {
      background: transparent !important;
      border-right: none !important;
    }

    [data-testid="stSidebarContent"] {
      background: var(--glass-bg) !important;
      border: var(--glass-border) !important;
      backdrop-filter: var(--glass-blur) !important;
      -webkit-backdrop-filter: var(--glass-blur) !important;
      border-radius: var(--radius) !important;
      margin: 16px !important;
      box-shadow: 0 30px 60px rgba(0,0,0,.45) !important;
      padding: 20px !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
      color: var(--text) !important;
      font-weight: 600 !important;
      font-size: 14px !important;
    }

    .sidebar-title {
      font-size: 22px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 20px;
    }

    /* SOLID WHITE INPUT WITH CRISP BLACK TEXT FOR API KEY */
    [data-testid="stTextInput"] input {
      background: #FFFFFF !important;
      border: 1px solid rgba(255, 255, 255, 0.4) !important;
      border-radius: 14px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-family: var(--font-sora) !important;
      font-weight: 600 !important;
    }

    [data-testid="stTextInput"] input::placeholder {
      color: #666666 !important;
      -webkit-text-fill-color: #666666 !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] {
      background: rgba(255,255,255,.08) !important;
      border: 1px solid rgba(255,255,255,.2) !important;
      border-radius: 14px !important;
      color: var(--text) !important;
      font-family: var(--font-sora) !important;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
      border-color: var(--teal) !important;
      box-shadow: 0 0 0 2px var(--teal) !important;
    }

    /* SLIDER VISIBILITY & HIGH-CONTRAST LABELS FIX */
    [data-testid="stSlider"] label,
    [data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
      color: #EDEBFF !important;
      -webkit-text-fill-color: #EDEBFF !important;
      font-weight: 600 !important;
    }

    /* Active selected value floating above knob (1000, 150, 4) */
    [data-testid="stSlider"] div[data-testid="stSliderThumbValue"],
    [data-testid="stSlider"] [data-baseweb="tooltip"],
    [data-testid="stSlider"] div[class*="StyledThumbValue"] {
      color: #5CF0DA !important;
      -webkit-text-fill-color: #5CF0DA !important;
      font-weight: 700 !important;
      font-size: 14px !important;
    }

    /* Slider Min & Max Limit Numbers (500, 2000, 0, 400, etc.) */
    [data-testid="stSlider"] [data-testid="stTickBarValue"],
    [data-testid="stSlider"] div[data-testid="stSliderTickBar"] span,
    [data-testid="stSlider"] div[data-testid="stSliderTickBar"] div,
    [data-testid="stSlider"] div[class*="st-"] p,
    [data-testid="stSlider"] span {
      color: #B7B2E6 !important;
      -webkit-text-fill-color: #B7B2E6 !important;
      font-weight: 600 !important;
      opacity: 1 !important;
    }

    /* Slider Knob Thumb Button */
    [data-testid="stSlider"] div[role="slider"] {
      background: linear-gradient(135deg, #2DE2C8, #7C5CFF) !important;
      box-shadow: 0 0 16px rgba(45,226,200,.8) !important;
      border: 2px solid #FFFFFF !important;
    }

    /* UPLOAD DOCUMENT GLASS CONTAINER */
    [data-testid="stFileUploader"] {
      background: var(--glass-bg) !important;
      border: 1.5px dashed rgba(255,255,255,.3) !important;
      backdrop-filter: var(--glass-blur) !important;
      -webkit-backdrop-filter: var(--glass-blur) !important;
      border-radius: var(--radius) !important;
      padding: 18px 22px !important;
      margin-bottom: 24px !important;
    }

    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploaderDropzone"] > div {
      background: transparent !important;
      border: none !important;
    }

    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span {
      color: #EDEBFF !important;
      -webkit-text-fill-color: #EDEBFF !important;
      opacity: 1 !important;
      font-weight: 600 !important;
    }

    /* Dark Translucent Glass Chips for Uploaded Files */
    [data-testid="stFileUploaderFile"],
    [data-testid="stFileUploaderFileData"] {
      background: rgba(11, 8, 32, 0.75) !important;
      border: 1px solid rgba(255, 255, 255, 0.25) !important;
      border-radius: 14px !important;
      padding: 8px 14px !important;
    }

    [data-testid="stFileUploaderFile"] *,
    [data-testid="stFileUploaderFileData"] * {
      color: #EDEBFF !important;
      -webkit-text-fill-color: #EDEBFF !important;
    }

    [data-testid="stFileUploaderDeleteBtn"],
    [data-testid="stFileUploaderFile"] button {
      color: #FF4FD8 !important;
      fill: #FF4FD8 !important;
    }

    /* PRIMARY BUTTONS */
    [data-testid="stButton"] button,
    [data-testid="stFileUploader"] button {
      background: linear-gradient(135deg, #2DE2C8, #7C5CFF) !important;
      color: #0B0820 !important;
      font-weight: 700 !important;
      font-family: var(--font-sora) !important;
      border-radius: 16px !important;
      border: none !important;
      box-shadow: 0 0 24px rgba(45,226,200,.5) !important;
      transition: all 0.2s ease !important;
    }

    [data-testid="stButton"] button:hover,
    [data-testid="stFileUploader"] button:hover {
      transform: translateY(-2px) !important;
      box-shadow: 0 0 32px rgba(45,226,200,.8) !important;
    }

    /* FIXED BOTTOM CENTER PROMPT BAR */
    [data-testid="stChatInput"] {
      position: fixed !important;
      bottom: 24px !important;
      left: 50% !important;
      transform: translateX(-50%) !important;
      width: 90% !important;
      max-width: 700px !important;
      z-index: 9999 !important;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      padding: 0 !important;
    }

    /* Strip inner Streamlit wrapper borders */
    [data-testid="stChatInput"] * {
      border: none !important;
      box-shadow: none !important;
      background: transparent !important;
      outline: none !important;
    }

    /* Glass pill wrapper */
    [data-testid="stChatInput"] > div {
      background: linear-gradient(135deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.05)) !important;
      border: 1px solid rgba(255, 255, 255, 0.3) !important;
      backdrop-filter: blur(22px) !important;
      -webkit-backdrop-filter: blur(22px) !important;
      border-radius: 99px !important;
      padding: 4px 8px 4px 22px !important;
      display: flex !important;
      align-items: center !important;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6) !important;
      transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    [data-testid="stChatInput"] > div:focus-within {
      border-color: #2DE2C8 !important;
      box-shadow: 0 0 25px rgba(45, 226, 200, 0.45), 0 20px 45px rgba(0, 0, 0, 0.6) !important;
    }

    [data-testid="stChatInput"] textarea {
      color: #FFFFFF !important;
      -webkit-text-fill-color: #FFFFFF !important;
      font-family: var(--font-sora) !important;
      font-size: 14px !important;
      font-weight: 500 !important;
      caret-color: #2DE2C8 !important;
      padding: 8px 0 !important;
      min-height: 24px !important;
      max-height: 90px !important;
      line-height: 1.4 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
      color: #B7B2E6 !important;
      -webkit-text-fill-color: #B7B2E6 !important;
      opacity: 0.85 !important;
    }

    /* Send Button */
    [data-testid="stChatInput"] button {
      background: linear-gradient(135deg, #2DE2C8, #7C5CFF) !important;
      color: #0B0820 !important;
      border-radius: 50% !important;
      min-width: 38px !important;
      width: 38px !important;
      height: 38px !important;
      box-shadow: 0 0 18px rgba(45, 226, 200, 0.6) !important;
      transition: transform 0.2s ease, box-shadow 0.2s ease !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      margin-left: 8px !important;
    }

    [data-testid="stChatInput"] button:hover {
      transform: scale(1.06) !important;
      box-shadow: 0 0 26px rgba(45, 226, 200, 0.85) !important;
    }

    [data-testid="stChatInput"] button svg {
      fill: #0B0820 !important;
      color: #0B0820 !important;
    }

    /* HERO BANNER ANIMATION */
    @keyframes colorSlide {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    .hero-banner-text {
      text-align: center;
      font-size: clamp(2rem, 4.5vw, 3.5rem);
      font-weight: 700;
      letter-spacing: -0.5px;
      margin: 0 auto 16px auto;
      background: linear-gradient(90deg, #2DE2C8, #7C5CFF, #FF4FD8, #5CF0DA, #2DE2C8);
      background-size: 300% 100%;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: colorSlide 6s linear infinite;
    }

    @media (prefers-reduced-motion: reduce) {
      *, ::before, ::after {
        animation: none !important;
        transition: none !important;
      }
    }
    </style>

    <!-- Background Orbs -->
    <div class="aurora-bg-container" aria-hidden="true">
      <div class="aurora-orb orb-violet"></div>
      <div class="aurora-orb orb-teal"></div>
      <div class="aurora-orb orb-magenta"></div>
    </div>
    """, unsafe_allow_html=True)
