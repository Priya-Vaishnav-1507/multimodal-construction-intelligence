import json
import time
import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for UI Enhancement
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1E3A8A;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F8FAFC;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E0E7FF;
        color: #1E3A8A;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# MODULE 1: SIDEBAR & API CONFIGURATION
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/000000/crane.png", width=80)
st.sidebar.title("Construction AI Platform")
st.sidebar.caption("Skill Wallet Capstone Project 1")

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Authentication & Mode")

api_key = st.sidebar.text_input(
    "Enter Google Gemini API Key",
    type="password",
    help="Get an API key from Google AI Studio. Leave empty to use built-in Demo Mode."
)

demo_mode = False
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Simple instantiation test
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.success("✅ Gemini API Configured!")
    except Exception as e:
        st.sidebar.error("❌ Invalid Key. Falling back to Demo Mode.")
        demo_mode = True
else:
    demo_mode = True
    st.sidebar.warning("⚠️ Demo Mode Active (No API Key)")

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Platform Capabilities:**
* 🦺 PPE & Site Safety Vision Audit
* 🩺 Concrete Crack Diagnostics
* 📊 INR Real Estate Valuation & Material Calc
* 🌦️ Weather Advisory & Expert AI Chatbot
""")

# Title Header
st.markdown('<p class="main-header">🏗️ Multimodal Construction Intelligence Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Decision Support System for Site Safety, Structural Integrity & Cost Planning</p>', unsafe_allow_html=True)

# Main Tab Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Tab 1: PPE & Safety Audit",
    "🩺 Tab 2: Crack Diagnostics",
    "📊 Tab 3: Planning & Valuation",
    "💬 Tab 4: Assistant & Weather"
])

# Helper Function for Gemini Multimodal Analysis
def analyze_image_with_gemini(image, prompt, is_demo=False, demo_fallback_json=None):
    if is_demo:
        time.sleep(1.5) # Simulate processing delay
        return demo_fallback_json
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, image])
        # Attempt to parse response as JSON
        cleaned_response = response.text.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:-3].strip()
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:-3].strip()
        return json.loads(cleaned_response)
    except Exception as e:
        st.error(f"Gemini API Error or JSON Parsing issue: {e}. Showing structured analysis template.")
        return demo_fallback_json


# ==========================================
# MODULE 2: TAB 1 - PPE & SITE SAFETY AUDIT
# ==========================================
with tab1:
    st.header("🦺 Site Safety & PPE Compliance Audit")
    st.write("Upload construction site photography to automatically inspect worker PPE compliance (OSHA / IS 456 standards).")

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_safety_img = st.file_uploader("Upload Site Image (JPG/PNG)", type=["jpg", "jpeg", "png"], key="safety_uploader")
        
        if uploaded_safety_img:
            image = Image.open(uploaded_safety_img)
            st.image(image, caption="Uploaded Construction Site Image", use_container_width=True)
            analyze_safety_btn = st.button("🔍 Run Safety Inspection", type="primary")
        else:
            analyze_safety_btn = False

    with col2:
        if analyze_safety_btn and uploaded_safety_img:
            with st.spinner("Analyzing site hazards and PPE compliance..."):
                prompt = """
                You are an OSHA safety auditor. Inspect the attached construction site image.
                Return ONLY a valid raw JSON object matching this schema strictly without Markdown formatting:
                {
                    "safety_score": 82,
                    "overall_status": "Conditional Compliance",
                    "ppe_detection": {
                        "hard_hats": "3 detected, 1 missing",
                        "high_vis_jackets": "4 detected",
                        "safety_boots": "Compliant",
                        "safety_harnesses": "Not Applicable / Unused"
                    },
                    "hazards_identified": [
                        {"hazard": "Worker near edge without harness", "severity": "High", "remedy": "Enforce fall protection systems immediately."},
                        {"hazard": "Unsecured scaffolding boards", "severity": "Medium", "remedy": "Secure planks using standard scaffolding clamps."}
                    ]
                }
                """
                
                demo_data = {
                    "safety_score": 78,
                    "overall_status": "Needs Attention",
                    "ppe_detection": {
                        "hard_hats": "3/4 Workers Wearing",
                        "high_vis_jackets": "4/4 Compliant",
                        "safety_boots": "Compliant",
                        "safety_harnesses": "1 Worker at height unattached"
                    },
                    "hazards_identified": [
                        {"hazard": "Worker on elevated platform without safety lanyard", "severity": "High", "remedy": "Install life-lines and enforce double-hook lanyards."},
                        {"hazard": "Debris accumulated near walkway", "severity": "Low", "remedy": "Clear path to prevent tripping hazards."}
                    ]
                }

                result = analyze_image_with_gemini(image, prompt, is_demo=demo_mode, demo_fallback_json=demo_data)

                if result:
                    # Score gauge / metric
                    score = result.get("safety_score", 0)
                    status = result.get("overall_status", "N/A")

                    st.markdown("### Audit Summary")
                    m1, m2 = st.columns(2)
                    m1.metric("Safety Compliance Score", f"{score}/100")
                    m2.metric("Overall Site Status", status)

                    st.markdown("#### 👷 PPE Detection Checklist")
                    st.json(result.get("ppe_detection", {}))

                    st.markdown("#### ⚠️ Identified Hazards & Corrective Remedies")
                    hazards = result.get("hazards_identified", [])
                    if hazards:
                        df_hazards = pd.DataFrame(hazards)
                        st.dataframe(df_hazards, use_container_width=True)

                    st.download_button(
                        label="📥 Download Official Safety Audit Report (JSON)",
                        data=json.dumps(result, indent=4),
                        file_name="site_safety_audit_report.json",
                        mime="application/json"
                    )


# ==========================================
# MODULE 3: TAB 2 - CRACK DIAGNOSTICS & INTEGRITY
# ==========================================
with tab2:
    st.header("🩺 Crack Diagnostics & Structural Integrity")
    st.write("Upload high-resolution images of concrete/wall structural defects for automated severity scoring and repair protocols.")

    c1, c2 = st.columns([1, 1])

    with c1:
        uploaded_crack_img = st.file_uploader("Upload Surface Image", type=["jpg", "jpeg", "png"], key="crack_uploader")
        
        if uploaded_crack_img:
            crack_img = Image.open(uploaded_crack_img)
            st.image(crack_img, caption="Concrete Surface Image", use_container_width=True)
            analyze_crack_btn = st.button("🔬 Diagnose Structural Defect", type="primary")
        else:
            analyze_crack_btn = False

    with c2:
        if analyze_crack_btn and uploaded_crack_img:
            with st.spinner("Analyzing concrete crack geometry and structural severity..."):
                prompt = """
                You are a senior structural engineer. Analyze this surface crack image.
                Return ONLY a valid raw JSON object strictly adhering to this format without Markdown tags:
                {
                    "defect_classification": "Shear Wall Crack / Settlement",
                    "estimated_width_mm": "2.5 mm",
                    "severity_level": "Medium-High",
                    "root_causes": ["Foundation differential settlement", "Thermal expansion/contraction"],
                    "engineering_repairs": ["Pressure injection of low-viscosity epoxy resin", "Monitor with tell-tale crack gauges for 30 days"],
                    "urgency": "Action required within 14 days"
                }
                """

                demo_crack_data = {
                    "defect_classification": "Diagonal Shear Crack",
                    "estimated_width_mm": "3.1 mm",
                    "severity_level": "High",
                    "root_causes": [
                        "Excessive shear stress near support column",
                        "Inadequate shear reinforcement stirrups",
                        "Concrete drying shrinkage"
                    ],
                    "engineering_repairs": [
                        "Clean crack surface with oil-free compressed air",
                        "Install injection ports at 200mm intervals",
                        "Pressure-inject high-strength structural epoxy",
                        "Apply carbon-fiber reinforced polymer (CFRP) wrapping if active movement persists"
                    ],
                    "urgency": "Immediate Inspection Recommended (within 48 hours)"
                }

                crack_result = analyze_image_with_gemini(crack_img, prompt, is_demo=demo_mode, demo_fallback_json=demo_crack_data)

                if crack_result:
                    st.markdown("### Diagnostic Report")
                    
                    st.subheader(f"Type: {crack_result.get('defect_classification')}")
                    
                    col_a, col_b = st.columns(2)
                    col_a.metric("Est. Crack Width", crack_result.get("estimated_width_mm", "N/A"))
                    col_b.metric("Severity Level", crack_result.get("severity_level", "N/A"))

                    st.warning(f"**Urgency:** {crack_result.get('urgency')}")

                    st.markdown("#### 📌 Root Causes")
                    for rc in crack_result.get("root_causes", []):
                        st.write(f"- {rc}")

                    st.markdown("#### 🛠️ Recommended Engineering Repair Protocol")
                    for repair in crack_result.get("engineering_repairs", []):
                        st.write(f"1. {repair}")


# ==========================================
# MODULE 4: TAB 3 - PLANNING & REAL ESTATE VALUATION
# ==========================================
with tab3:
    st.header("📊 Project Planning & Real Estate Valuation (INR)")
    st.write("Calculate project budgets, material quantity estimates (Cement & Steel), and real estate asset valuation.")

    col_in1, col_in2 = st.columns(2)

    with col_in1:
        builtup_area = st.number_input("Built-up Area (Sq. Ft.)", min_value=100, max_value=1000000, value=2500, step=100)
        location_tier = st.selectbox("Location Tier (India)", ["Tier 1 (Metro: Mumbai, Delhi, BLR)", "Tier 2 (Pune, Ahmedabad, Jaipur)", "Tier 3 / Regional"])
        structure_type = st.selectbox("Structure Type", ["Residential Apartment", "Commercial Office", "Industrial Warehouse", "Independent Villa"])

    with col_in2:
        completion_pct = st.slider("Current Project Completion Stage (%)", 0, 100, 45)
        base_rate_sqft = st.number_input("Est. Base Construction Cost per Sq.Ft. (₹)", min_value=1000, max_value=10000, value=2200, step=100)

    st.markdown("---")

    if st.button("🚀 Calculate Cost, Materials & Valuation", type="primary"):
        # Financial & Material Calculations
        total_construction_budget = builtup_area * base_rate_sqft
        capital_expenditure_incurred = total_construction_budget * (completion_pct / 100.0)
        
        # Tier multiplier for market valuation
        tier_multipliers = {
            "Tier 1 (Metro: Mumbai, Delhi, BLR)": 2.8,
            "Tier 2 (Pune, Ahmedabad, Jaipur)": 1.9,
            "Tier 3 / Regional": 1.4
        }
        multiplier = tier_multipliers.get(location_tier, 1.5)
        projected_asset_valuation = total_construction_budget * multiplier

        # Rough Estimations (Standard Civil Benchmarks)
        cement_bags = int(builtup_area * 0.4) # ~0.4 bags per sqft
        steel_tons = round(builtup_area * 0.003, 2) # ~3kg to 4kg per sqft

        # Display Metrics
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Total Construction Budget", f"₹{total_construction_budget/100000:.2f} Lakhs")
        m_col2.metric("CapEx Incurred So Far", f"₹{capital_expenditure_incurred/100000:.2f} Lakhs")
        m_col3.metric("Projected Asset Market Value", f"₹{projected_asset_valuation/100000:.2f} Lakhs")

        st.markdown("---")
        
        c_mat1, c_mat2 = st.columns(2)
        with c_mat1:
            st.subheader("📦 Material Estimation Requirements")
            st.write(f"- **Cement Requirement:** ~{cement_bags:,} Bags (50kg each)")
            st.write(f"- **Steel Reinforcement:** ~{steel_tons} Metric Tons")
            st.write(f"- **Coarse Aggregates:** ~{int(builtup_area * 1.35)} Cu.Ft.")
            st.write(f"- **Sand / M-Sand:** ~{int(builtup_area * 0.8)} Cu.Ft.")

        with c_mat2:
            st.subheader("📈 Financial Progress Breakdown")
            df_chart = pd.DataFrame({
                "Category": ["Expended Budget", "Remaining Budget"],
                "Amount (INR)": [capital_expenditure_incurred, total_construction_budget - capital_expenditure_incurred]
            })
            fig = px.pie(df_chart, names="Category", values="Amount (INR)", hole=0.4, color_discrete_sequence=['#1E3A8A', '#93C5FD'])
            st.plotly_chart(fig, use_container_width=True)


# ==========================================
# MODULE 5: TAB 4 - ASSISTANT & WEATHER ADVISORY
# ==========================================
with tab4:
    st.header("🌦️ Daily Site Assistant & Weather Advisory")

    w_col1, w_col2 = st.columns([1, 1])

    with w_col1:
        st.subheader("🌦️ Site Weather Condition Selector")
        weather_state = st.selectbox(
            "Select Current On-Site Weather Condition:",
            ["Normal / Clear Skies", "High Wind Speeds (>40 km/h)", "Heavy Rainfall / Storm", "Extreme Heatwave (>42°C)"]
        )

        st.markdown("#### 🚨 Weather-Aware Operational Safety Protocol")
        if weather_state == "High Wind Speeds (>40 km/h)":
            st.error("⚠️ **CRITICAL PROTOCOL:** Suspend all tower crane lifting operations immediately. Secure high-altitude formwork and loose sheets.")
        elif weather_state == "Heavy Rainfall / Storm":
            st.warning("⚡ **WEATHER ALERT:** Halt electrical works and basement excavations. Inspect dewatering pumps and check site perimeter slopes.")
        elif weather_state == "Extreme Heatwave (>42°C)":
            st.info("🌡️ **HEAT SAFETY:** Shift concrete curing to early morning/evening. Implement compulsory 15-min hydration breaks every 2 hours for workers.")
        else:
            st.success("✅ **NORMAL OPERATIONS:** Standard site protocols active. All structural and lifting activities clear to proceed.")

    with w_col2:
        st.subheader("💬 AI Construction Engineering Chatbot")
        st.write("Ask structural, IS-code compliance, or site management questions.")

        # Session state for chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hello! I am your AI Construction Site Advisor. How can I assist you with site engineering, IS codes, or safety today?"}
            ]

        # Render chat messages
        chat_container = st.container(height=300)
        with chat_container:
            for msg in st.session_state.chat_history:
                st.chat_message(msg["role"]).write(msg["content"])

        # Chat Input
        if user_query := st.chat_input("Ask a construction question (e.g. 'What is the curing period for M25 concrete?'):"):
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            # Generate Response
            if demo_mode:
                bot_response = f"*(Demo Response)* For query '{user_query}': Under Indian Standards (IS 456:2000), standard OPC concrete curing should be maintained for a minimum of 7 days under normal weather, and 10 days when OPC with mineral admixtures or hot weather conditions apply."
            else:
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"You are an expert civil engineer and site safety officer. Answer concisely: {user_query}")
                    bot_response = response.text
                except Exception as e:
                    bot_response = f"Error querying Gemini: {e}"

            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            st.rerun()

# Footer
st.markdown("---")
st.caption("Skill Wallet Capstone Project 1 | Built with Streamlit & Google Gemini Vision AI")