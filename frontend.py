import streamlit as st
import requests
import base64
import urllib.parse
from datetime import datetime

# Page config with custom theme
st.set_page_config(
    page_title="Wave | Social", 
    layout="wide",
    page_icon="🌊",
    initial_sidebar_state="expanded"
)

# Clean Dark Blue Theme
st.markdown("""
<style>
    /* Import Google Fonts - Clean readable fonts */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* CSS Variables - Dark Blue Theme */
    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --primary-light: #3b82f6;
        --secondary: #1e40af;
        --accent: #60a5fa;
        --success: #22c55e;
        --warning: #eab308;
        --error: #ef4444;
        --bg-dark: #0a0f1a;
        --bg-card: #111827;
        --bg-card-hover: #1f2937;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border: #1e293b;
        --gradient-primary: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        --gradient-card: linear-gradient(145deg, rgba(17, 24, 39, 0.98), rgba(10, 15, 26, 0.99));
        --shadow-card: 0 10px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Global styles - Clean fonts */
    * {
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        letter-spacing: -0.01em;
    }
    
    h1, h2, h3, .hero-header h1, .login-logo h1 {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.02em;
    }
    
    /* Main app background - clean dark blue */
    .stApp {
        background: linear-gradient(180deg, #0a0f1a 0%, #0f172a 100%);
        min-height: 100vh;
    }
    
    /* Subtle background gradient */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 20% 0%, rgba(30, 58, 138, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 100%, rgba(30, 64, 175, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary), var(--secondary));
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--primary-light), var(--accent));
    }
    
    /* ===== HEADER STYLES with 3D effect ===== */
    .hero-header {
        background: var(--gradient-card);
        border: 1px solid rgba(37, 99, 235, 0.15);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        perspective: 1000px;
        animation: slideUp 0.6s ease-out;
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.05),
            0 20px 40px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.05);
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--gradient-primary);
        animation: gradientShift 3s ease infinite;
        background-size: 200% 100%;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .hero-header::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255,255,255,0.03) 50%,
            transparent 70%
        );
        animation: shine 4s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .hero-header h1 {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .hero-header p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin: 0;
        font-weight: 400;
    }
    
    .hero-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ===== LOGIN PAGE STYLES with 3D ===== */
    .login-container {
        max-width: 420px;
        margin: 2rem auto;
        background: var(--gradient-card);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(37, 99, 235, 0.2);
        border-radius: 32px;
        padding: 3rem;
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.05),
            var(--shadow-glow), 
            var(--shadow-card),
            0 0 100px rgba(30, 64, 175, 0.1);
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        animation: floatCard 6s ease-in-out infinite, slideUp 0.8s ease-out;
    }
    
    @keyframes floatCard {
        0%, 100% { transform: translateY(0) rotateX(0deg) rotateY(0deg); }
        25% { transform: translateY(-5px) rotateX(1deg) rotateY(-1deg); }
        75% { transform: translateY(-3px) rotateX(-1deg) rotateY(1deg); }
    }
    
    .login-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
        background-size: 200% 100%;
        animation: gradientShift 2s ease infinite;
    }
    
    .login-container::after {
        content: '';
        position: absolute;
        top: -100%;
        left: -100%;
        width: 300%;
        height: 300%;
        background: linear-gradient(
            45deg,
            transparent 40%,
            rgba(255,255,255,0.02) 50%,
            transparent 60%
        );
        animation: shine 6s ease-in-out infinite;
        pointer-events: none;
    }
    
    .login-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-logo .logo-icon {
        font-size: 4.5rem;
        display: block;
        margin-bottom: 1rem;
        animation: float3D 4s ease-in-out infinite;
        filter: drop-shadow(0 10px 20px rgba(37, 99, 235, 0.3));
    }
    
    @keyframes float3D {
        0%, 100% { 
            transform: translateY(0) rotateY(0deg) scale(1); 
            filter: drop-shadow(0 10px 20px rgba(37, 99, 235, 0.3));
        }
        25% { 
            transform: translateY(-8px) rotateY(10deg) scale(1.05); 
            filter: drop-shadow(0 20px 30px rgba(30, 64, 175, 0.4));
        }
        50% { 
            transform: translateY(-12px) rotateY(0deg) scale(1.08); 
            filter: drop-shadow(0 25px 35px rgba(29, 78, 216, 0.35));
        }
        75% { 
            transform: translateY(-8px) rotateY(-10deg) scale(1.05); 
            filter: drop-shadow(0 20px 30px rgba(30, 64, 175, 0.4));
        }
    }
    
    .login-logo h1 {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
        animation: textGlow 2s ease-in-out infinite alternate;
    }
    
    .login-logo p {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-top: 0.5rem;
        opacity: 0.8;
    }
    
    .login-divider {
        display: flex;
        align-items: center;
        margin: 1.5rem 0;
        gap: 1rem;
    }
    
    .login-divider::before,
    .login-divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
    }
    
    .login-divider span {
        color: var(--text-muted);
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* ===== POST CARD STYLES with 3D Effects ===== */
    .post-card {
        background: var(--gradient-card);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(37, 99, 235, 0.15);
        border-radius: 24px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        perspective: 1000px;
        animation: cardEntrance 0.5s ease-out backwards;
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.03),
            0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes cardEntrance {
        from { 
            opacity: 0; 
            transform: translateY(40px) rotateX(-5deg) scale(0.95); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0) rotateX(0) scale(1); 
        }
    }
    
    .post-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.03),
            transparent
        );
        transition: left 0.5s ease;
    }
    
    .post-card:hover::before {
        left: 100%;
    }
    
    .post-card:hover {
        border-color: rgba(37, 99, 235, 0.35);
        transform: translateY(-8px) rotateX(2deg);
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.05),
            var(--shadow-glow), 
            0 30px 60px rgba(0, 0, 0, 0.4),
            0 0 80px rgba(37, 99, 235, 0.1);
    }
    
    .post-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        gap: 12px;
    }
    
    .avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: var(--gradient-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        flex-shrink: 0;
    }
    
    .user-info {
        flex: 1;
        min-width: 0;
    }
    
    .username {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.95rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .post-date {
        color: var(--text-muted);
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 4px;
        margin-top: 2px;
    }
    
    .caption {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
        margin-top: 1rem;
        padding: 1rem 1.25rem;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.6), rgba(10, 10, 20, 0.5));
        border-radius: 16px;
        border-left: 3px solid;
        border-image: var(--gradient-primary) 1;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .caption:hover {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(10, 10, 20, 0.7));
        transform: translateX(4px);
    }
    
    /* ===== UPLOAD SECTION STYLES with 3D ===== */
    .upload-zone {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.5), rgba(15, 23, 42, 0.7));
        border: 2px dashed rgba(37, 99, 235, 0.3);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .upload-zone::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 150%;
        height: 150%;
        background: radial-gradient(circle, rgba(37, 99, 235, 0.1) 0%, transparent 70%);
        transform: translate(-50%, -50%) scale(0);
        transition: transform 0.5s ease;
    }
    
    .upload-zone:hover::before {
        transform: translate(-50%, -50%) scale(1);
    }
    
    .upload-zone:hover {
        border-color: rgba(37, 99, 235, 0.6);
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.85));
        box-shadow: 
            var(--shadow-glow),
            inset 0 0 60px rgba(37, 99, 235, 0.05);
        transform: translateY(-4px);
    }
    
    .upload-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: block;
        opacity: 0.9;
        animation: bounceIcon 2s ease-in-out infinite;
    }
    
    @keyframes bounceIcon {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    
    .upload-text {
        color: var(--text-secondary);
        font-size: 1rem;
    }
    
    .upload-text strong {
        color: var(--primary-light);
    }
    
    /* ===== TIPS CARD with 3D ===== */
    .tips-card {
        background: var(--gradient-card);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(37, 99, 235, 0.12);
        border-radius: 20px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        animation: slideUp 0.6s ease-out 0.2s backwards;
    }
    
    .tips-card:hover {
        border-color: rgba(37, 99, 235, 0.25);
        transform: translateY(-4px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .tips-card h3 {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .tip-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(51, 65, 85, 0.3);
        color: var(--text-secondary);
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .tip-item:hover {
        padding-left: 8px;
        color: var(--text-primary);
    }
    
    .tip-item:last-child {
        border-bottom: none;
    }
    
    .tip-icon {
        color: var(--primary-light);
        flex-shrink: 0;
    }
    
    /* ===== SIDEBAR STYLES with 3D ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121a 0%, #0a0a10 100%) !important;
        border-right: 1px solid rgba(37, 99, 235, 0.1);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    .sidebar-profile {
        text-align: center;
        padding: 1.75rem;
        background: var(--gradient-card);
        border-radius: 24px;
        margin: 0 1rem 1.5rem 1rem;
        border: 1px solid rgba(37, 99, 235, 0.15);
        position: relative;
    }
    
    .sidebar-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: var(--gradient-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 2rem;
        margin: 0 auto 1rem auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .sidebar-name {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .sidebar-email {
        color: var(--text-muted);
        font-size: 0.85rem;
        word-break: break-all;
        opacity: 0.8;
    }
    
    .sidebar-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
        border-radius: 20px;
        font-size: 0.75rem;
        color: var(--success);
        margin-top: 0.75rem;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .sidebar-status::before {
        content: '';
        width: 8px;
        height: 8px;
        background: var(--success);
        border-radius: 50%;
        animation: pulseGreen 2s infinite;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }
    
    @keyframes pulseGreen {
        0%, 100% { 
            opacity: 1;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
        }
        50% { 
            opacity: 0.6;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.8);
        }
    }
    
    /* ===== BUTTON STYLES - Clean ===== */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
        text-transform: none !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary button style */
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        border: 2px solid var(--primary) !important;
        color: var(--primary-light) !important;
        box-shadow: none !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(14, 165, 233, 0.1) !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.2) !important;
    }
    
    /* ===== INPUT STYLES ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.15) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Label styling */
    .stTextInput > label,
    .stTextArea > label,
    .stFileUploader > label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* ===== FILE UPLOADER ===== */
    .stFileUploader > div > div {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: var(--primary) !important;
        background: rgba(14, 165, 233, 0.05) !important;
    }
    
    /* ===== RADIO BUTTONS (Navigation) ===== */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .stRadio > div > label {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid transparent !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    
    .stRadio > div > label:hover {
        background: rgba(14, 165, 233, 0.1) !important;
        border-color: rgba(14, 165, 233, 0.3) !important;
        color: var(--text-primary) !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: var(--gradient-primary) !important;
        border-color: transparent !important;
        color: white !important;
    }
    
    /* ===== ALERTS & MESSAGES ===== */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px !important;
        color: var(--success) !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
        color: var(--error) !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        color: var(--warning) !important;
    }
    
    .stInfo {
        background: rgba(14, 165, 233, 0.1) !important;
        border: 1px solid rgba(14, 165, 233, 0.3) !important;
        border-radius: 12px !important;
        color: var(--primary-light) !important;
    }
    
    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background: var(--border) !important;
        border-radius: 10px !important;
    }
    
    .stProgress > div > div > div {
        background: var(--gradient-primary) !important;
        border-radius: 10px !important;
    }
    
    /* ===== SPINNER ===== */
    .stSpinner > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }
    
    /* ===== EMPTY STATE ===== */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: var(--gradient-card);
        border-radius: 24px;
        border: 1px solid rgba(14, 165, 233, 0.12);
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: block;
        opacity: 0.8;
    }
    
    .empty-state h2 {
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .empty-state p {
        color: var(--text-muted);
        font-size: 1rem;
    }
    
    /* ===== DIVIDERS ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 1.5rem 0;
    }
    
    /* ===== MEDIA CONTAINER ===== */
    .media-container {
        border-radius: 16px;
        overflow: hidden;
        background: var(--bg-dark);
        margin: 1rem 0;
    }
    
    .media-container img,
    .media-container video {
        border-radius: 16px;
        width: 100%;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in {
        animation: fadeIn 0.4s ease-out forwards;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .loading-shimmer {
        background: linear-gradient(90deg, var(--bg-card) 25%, var(--bg-card-hover) 50%, var(--bg-card) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
    
    /* ===== IMAGE/VIDEO STYLING ===== */
    .stImage > img {
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stVideo > video {
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* ===== MARKDOWN TEXT ===== */
    .stMarkdown {
        color: var(--text-secondary);
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-primary) !important;
    }
    
    /* ===== RESPONSIVE ADJUSTMENTS ===== */
    @media (max-width: 768px) {
        .hero-header {
            padding: 2rem 1rem;
        }
        
        .hero-header h1 {
            font-size: 1.8rem;
        }
        
        .login-container {
            padding: 2rem 1.5rem;
            margin: 1rem;
        }
        
        .sidebar-profile {
            margin: 0 0.5rem 1rem 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'upload_status' not in st.session_state:
    st.session_state.upload_status = None

def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def get_initials(email):
    """Get initials from email for avatar"""
    return email[0].upper() if email else "U"

def format_date(date_string):
    """Format date string to a more readable format"""
    try:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime("%b %d, %Y")
    except:
        return date_string[:10] if date_string else ""

def login_page():
    # Centered login form with modern design
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-logo">
                <span class="logo-icon">🌊</span>
                <h1>Wave</h1>
                <p>Share your world</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-divider"><span>Sign in to continue</span></div>', unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if email and password:
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("Sign In", type="primary", use_container_width=True):
                    with st.spinner("Authenticating..."):
                        login_data = {"username": email, "password": password}
                        try:
                            response = requests.post("https://simple-social-media-web-app-5.onrender.com/authjwt/login", data=login_data)
                            
                            if response.status_code == 200:
                                token_data = response.json()
                                st.session_state.token = token_data["access_token"]
                                
                                user_response = requests.get("https://simple-social-media-web-app-5.onrender.com/users/me", headers=get_headers())
                                if user_response.status_code == 200:
                                    st.session_state.user = user_response.json()
                                    st.success("Welcome back!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to fetch user info.")
                            else:
                                st.error("❌ Invalid credentials. Please try again.")
                        except requests.exceptions.ConnectionError:
                            st.error("❌ Cannot connect to server. Please ensure the backend is running.")
            
            with col_btn2:
                if st.button("Create Account", type="secondary", use_container_width=True):
                    with st.spinner("Creating your account..."):
                        signup_data = {"email": email, "password": password}
                        try:
                            response = requests.post("https://simple-social-media-web-app-5.onrender.com/authjwt/register", json=signup_data)
                            
                            if response.status_code == 201:
                                st.success("Account created! You can now sign in.")
                            else:
                                error_detail = response.json().get('detail', 'Unknown error')
                                if 'ALREADY_EXISTS' in str(error_detail):
                                    st.warning("⚠️ This email is already registered. Try signing in!")
                                else:
                                    st.error(f"❌ Registration failed: {error_detail}")
                        except requests.exceptions.ConnectionError:
                            st.error("❌ Cannot connect to server. Please ensure the backend is running.")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: rgba(14, 165, 233, 0.1); 
                        border-radius: 12px; border: 1px solid rgba(14, 165, 233, 0.2);">
                <p style="color: #38bdf8; margin: 0; font-size: 0.95rem;">
                    👆 Enter your credentials to get started
                </p>
            </div>
            """, unsafe_allow_html=True)

def upload_page():
    st.markdown("""
    <div class="hero-header">
        <h1>New Post</h1>
        <p>Share something with your community</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a photo or video",
            type=['png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'mkv', 'webm'],
            help="PNG, JPG, GIF, MP4, MOV, WEBM"
        )
        
        caption = st.text_area(
            "Caption",
            placeholder="What's on your mind?",
            height=100
        )
        
        if uploaded_file:
            st.markdown("---")
            st.markdown("**Preview**")
            
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, width=500)
            else:
                st.video(uploaded_file)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Share", type="primary", use_container_width=True):
                # Show progress
                progress_bar = st.progress(0, text="Preparing your post...")
                status_text = st.empty()
                
                try:
                    progress_bar.progress(20, text="Reading file...")
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"caption": caption}
                    
                    progress_bar.progress(40, text="Uploading to server...")
                    status_text.markdown("""
                    <div style="padding: 1rem; background: rgba(14, 165, 233, 0.1); border-radius: 12px; 
                                border: 1px solid rgba(14, 165, 233, 0.2); text-align: center;">
                        <p style="color: #38bdf8; margin: 0;">⏳ Uploading... This may take a moment for larger files.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    response = requests.post(
                        "https://simple-social-media-web-app-5.onrender.com/upload",
                        headers=get_headers(),
                        files=files,
                        data=data,
                        timeout=120
                    )
                    
                    progress_bar.progress(80, text="Processing...")
                    
                    if response.status_code == 200:
                        progress_bar.progress(100, text="Done!")
                        status_text.empty()
                        st.success("Posted successfully!")
                        
                        import time
                        time.sleep(1)
                        st.session_state.page = "Feed"
                        st.rerun()
                    else:
                        progress_bar.empty()
                        status_text.empty()
                        st.error(f"❌ Upload failed: {response.text}")
                        
                except requests.exceptions.Timeout:
                    progress_bar.empty()
                    status_text.empty()
                    st.error("⏰ Upload timed out. Please try with a smaller file or check your connection.")
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("""
        <div class="tips-card">
            <h3>Tips</h3>
            <div class="tip-item">
                <span class="tip-icon">•</span>
                <span>Use PNG or JPEG for images</span>
            </div>
            <div class="tip-item">
                <span class="tip-icon">•</span>
                <span>MP4 works best for videos</span>
            </div>
            <div class="tip-item">
                <span class="tip-icon">•</span>
                <span>Keep files under 50MB</span>
            </div>
            <div class="tip-item">
                <span class="tip-icon">•</span>
                <span>Add captions to engage</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def feed_page():
    st.markdown("""
    <div class="hero-header">
        <h1>Feed</h1>
        <p>See what's new</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with st.spinner("Loading your feed..."):
            response = requests.get("https://simple-social-media-web-app-5.onrender.com/feed", headers=get_headers())
        
        if response.status_code == 200:
            posts = response.json()["posts"]
            
            if not posts:
                st.markdown("""
                <div class="empty-state">
                    <h2>No posts yet</h2>
                    <p>Be the first to share something.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Create Post", type="primary", use_container_width=True):
                    st.session_state.page = "Upload"
                    st.rerun()
                return
            
            # Display posts with modern card design
            for idx, post in enumerate(posts):
                with st.container():
                    # Post card header
                    col1, col2 = st.columns([6, 1])
                    
                    with col1:
                        email = post.get('email', 'Unknown')
                        initial = get_initials(email)
                        date = format_date(post.get('created_at', ''))
                        
                        st.markdown(f"""
                        <div class="post-header">
                            <div class="avatar">{initial}</div>
                            <div class="user-info">
                                <div class="username">{email}</div>
                                <div class="post-date">{date}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if post.get('isowner', False):
                            if st.button("🗑️", key=f"delete_{post['id']}", help="Delete this post"):
                                with st.spinner("Deleting..."):
                                    del_response = requests.delete(
                                        f"https://simple-social-media-web-app-5.onrender.com/posts/{post['id']}",
                                        headers=get_headers()
                                    )
                                    if del_response.status_code == 200:
                                        st.success("Post deleted successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete post.")
                    
                    # Media display
                    if post['file_type'] == "image":
                        st.image(post['url'], use_container_width=True)
                    else:
                        st.video(post['url'])
                    
                    # Caption
                    caption = post.get("caption", "")
                    if caption:
                        st.markdown(f"""
                        <div class="caption">
                            {caption}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
        else:
            st.error("❌ Failed to load feed. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to server. Please ensure the backend is running.")

# Main app logic
if st.session_state.user is None:
    login_page()
else:
    # Sidebar with modern design
    with st.sidebar:
        user_email = st.session_state.user.get('email', 'User')
        initial = get_initials(user_email)
        
        st.markdown(f"""
        <div class="sidebar-profile">
            <div class="sidebar-avatar">{initial}</div>
            <div class="sidebar-name">{user_email.split('@')[0]}</div>
            <div class="sidebar-email">{user_email}</div>
            <div class="sidebar-status">Active</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigate",
            ["Feed", "New Post"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick stats placeholder
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: rgba(30, 41, 59, 0.6); 
                    border-radius: 12px; margin-bottom: 1rem;">
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Share moments that matter</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sign Out", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    # Page routing
    if "Feed" in page:
        feed_page()
    elif "New Post" in page:
        upload_page()
