def get_custom_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Theme override and global reset */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0B0D1B !important;
        font-family: 'Inter', sans-serif !important;
        color: #FFFFFF !important;
        overflow-x: hidden;
    }

    /* Remove unnecessary empty whitespace from top, bottom, left, and right */
    .main .block-container, div[data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 98% !important;
    }

    /* Hide standard Streamlit header/footer padding and widgets */
    div[data-testid="stHeader"] {
        height: 0px !important;
        background: transparent !important;
    }

    /* Ambient soft radial background blurs */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: -10%;
        right: -10%;
        width: 60vw;
        height: 60vh;
        background: radial-gradient(circle, rgba(0, 200, 255, 0.15) 0%, rgba(0, 0, 0, 0) 70%);
        z-index: -1;
        pointer-events: none;
    }

    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        bottom: -10%;
        left: -10%;
        width: 60vw;
        height: 60vh;
        background: radial-gradient(circle, rgba(255, 0, 127, 0.12) 0%, rgba(0, 0, 0, 0) 70%);
        z-index: -1;
        pointer-events: none;
    }

    /* Header adjustments */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Hide default Streamlit decoration */
    [data-testid="stDecoration"] {
        background: linear-gradient(90deg, #00C8FF, #FF007F) !important;
        height: 3px !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0B0D1B;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 0, 127, 0.4);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 0, 127, 0.8);
    }

    /* Glassmorphic Container Cards */
    .card-container, div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(26, 21, 44, 0.65) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 0, 127, 0.2) !important;
        border-radius: 16px !important;
        padding: 12px 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s ease-in-out !important;
        margin-bottom: 0px !important;
        margin-top: 0px !important;
    }

    .card-container:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px) !important;
        border: 1px solid rgba(255, 0, 127, 0.5) !important;
        box-shadow: 0 12px 40px 0 rgba(255, 0, 127, 0.15) !important;
    }

    /* Specific small container overrides */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div {
        border-radius: 16px;
    }

    /* Metric card custom styling */
    div[data-testid="stMetric"] {
        background: rgba(26, 21, 44, 0.65) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 0, 127, 0.25) !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px) !important;
        border: 1px solid rgba(255, 0, 127, 0.55) !important;
        box-shadow: 0 10px 30px 0 rgba(255, 0, 127, 0.2) !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #A0A5C1 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        text-shadow: 0 0 10px rgba(0, 200, 255, 0.3);
    }

    div[data-testid="stMetricDelta"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    /* Custom delta representation for negative/drops */
    .delta-down {
        color: #FF4B72 !important;
        font-weight: 600;
        margin-top: 4px;
        font-size: 0.95rem;
    }

    /* Sidebar custom styling */
    section[data-testid="stSidebar"] {
        background-color: #070914 !important;
        border-right: 1px solid rgba(255, 0, 127, 0.15) !important;
    }

    section[data-testid="stSidebar"] div.stButton > button {
        background: rgba(26, 21, 44, 0.8) !important;
        border: 1px solid rgba(255, 0, 127, 0.2) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        transition: all 0.2s;
    }

    section[data-testid="stSidebar"] div.stButton > button:hover {
        border-color: rgba(255, 0, 127, 0.6) !important;
        box-shadow: 0 0 10px rgba(255, 0, 127, 0.2) !important;
    }

    /* Sidebar option menu overrides */
    .nav-link {
        font-family: 'Inter', sans-serif !important;
        border-radius: 8px !important;
        margin: 4px 0px !important;
        transition: all 0.2s ease !important;
    }
    
    .nav-link:hover {
        background-color: rgba(255, 0, 127, 0.1) !important;
        color: #FF007F !important;
    }

    .nav-link.active {
        background: linear-gradient(135deg, rgba(255, 0, 127, 0.3) 0%, rgba(0, 200, 255, 0.3) 100%) !important;
        border: 1px solid rgba(255, 0, 127, 0.4) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* General widgets custom overrides (Selectboxes, inputs, etc) */
    div[data-baseweb="select"] {
        background-color: rgba(26, 21, 44, 0.7) !important;
        border: 1px solid rgba(255, 0, 127, 0.25) !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"]:hover {
        border-color: rgba(255, 0, 127, 0.5) !important;
    }

    div[data-baseweb="select"] div {
        background-color: transparent !important;
        color: #FFFFFF !important;
    }

    /* Custom top banner style */
    .title-banner {
        background: linear-gradient(90deg, rgba(26, 21, 44, 0.9) 0%, rgba(45, 15, 66, 0.9) 100%);
        border: 1.5px solid rgba(255, 0, 127, 0.4);
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.15);
    }

    .title-banner h1 {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        font-size: 2rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.15em;
        margin: 0;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(0, 200, 255, 0.5), 0 0 20px rgba(255, 0, 127, 0.3);
    }

    /* Side list for vehicles */
    .vehicle-list-container {
        background: rgba(26, 21, 44, 0.65);
        border: 1px solid rgba(255, 0, 127, 0.25);
        border-radius: 16px;
        padding: 20px;
        height: 100%;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    .vehicle-title {
        color: #FFFFFF;
        font-weight: 700;
        font-size: 1.1rem;
        text-align: center;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 0, 127, 0.2);
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .vehicle-item {
        margin-bottom: 14px;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(11, 13, 27, 0.4);
        border-left: 3px solid #00C8FF;
    }

    .vehicle-item-label {
        color: #A0A5C1;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .vehicle-item-val {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 4px;
        font-family: monospace;
        text-shadow: 0 0 5px rgba(0, 200, 255, 0.3);
    }

    /* Empty state card styling */
    .empty-state {
        text-align: center;
        padding: 40px;
        background: rgba(26, 21, 44, 0.4);
        border-radius: 12px;
        border: 1px dashed rgba(255, 0, 127, 0.3);
    }

    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 12px;
    }

    .empty-state-text {
        color: #A0A5C1;
        font-size: 1rem;
    }
    </style>
    """
