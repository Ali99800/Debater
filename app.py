import streamlit as st

st.set_page_config(
    page_title="Rycroft Grid Solutions",
    page_icon="⚡",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at top, #0f172a 0%, #020617 40%, #000000 100%);
            color: #e2e8f0;
        }
        .hero-card {
            padding: 3rem;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.75));
            border: 1px solid rgba(148,163,184,0.2);
            box-shadow: 0 24px 60px rgba(15, 23, 42, 0.45);
            backdrop-filter: blur(8px);
        }
        .section-card {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(148,163,184,0.2);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        .kpi {
            background: linear-gradient(160deg, rgba(15,23,42,0.95), rgba(30,41,59,0.75));
            border-radius: 16px;
            padding: 1.25rem;
            border: 1px solid rgba(148,163,184,0.2);
            text-align: center;
        }
        .kpi h3 {
            margin-bottom: 0.25rem;
            font-size: 2rem;
            color: #38bdf8;
        }
        .kpi p {
            margin: 0;
            color: #cbd5e1;
        }
        .stButton > button {
            border-radius: 999px;
            border: 1px solid #38bdf8;
            background: linear-gradient(90deg, #0ea5e9, #38bdf8);
            color: #082f49;
            font-weight: 700;
            padding: 0.6rem 1.3rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <h4 style="color:#38bdf8; letter-spacing:0.2rem; margin-bottom:0.5rem;">RYCROFT GRID SOLUTIONS</h4>
        <h1 style="font-size:3rem; margin:0; color:#f8fafc;">Engineering the Next Era of Intelligent Grid Infrastructure</h1>
        <p style="font-size:1.1rem; line-height:1.7; color:#cbd5e1; max-width:900px; margin-top:1rem;">
            Rycroft Grid Solutions delivers premium transmission, distribution, and digital grid modernization programs for utilities,
            industrial operators, and governments. We combine systems engineering precision with AI-powered forecasting to make
            energy networks more resilient, secure, and future-ready.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
for col, number, label in [
    (kpi1, "99.98%", "Operational Uptime Target"),
    (kpi2, "42GW+", "Grid Capacity Enabled"),
    (kpi3, "28", "National Infrastructure Programs"),
    (kpi4, "24/7", "Network Operations Coverage"),
]:
    with col:
        st.markdown(f"<div class='kpi'><h3>{number}</h3><p>{label}</p></div>", unsafe_allow_html=True)

st.write("")

left, right = st.columns([1.1, 0.9], gap="large")
with left:
    st.markdown("### Premium Services")
    st.markdown(
        """
        <div class="section-card">
            <h4 style="color:#7dd3fc;">Grid Modernization Architecture</h4>
            <p>Future-state planning, digital twin simulations, and phased implementation roadmaps for high-value, low-risk transformations.</p>
        </div>
        <div class="section-card">
            <h4 style="color:#7dd3fc;">Protection, Controls & SCADA</h4>
            <p>Advanced relay schemes, IEC 61850 integration, and secure telemetry frameworks to ensure deterministic, real-time control.</p>
        </div>
        <div class="section-card">
            <h4 style="color:#7dd3fc;">Resilience & Cyber Hardening</h4>
            <p>NERC/CIP-aligned control baselines, segmentation strategy, and incident readiness for mission-critical grid operations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown("### Why Rycroft")
    st.markdown(
        """
        <div class="section-card">
            <ul style="line-height:1.9; padding-left:1.2rem; margin:0;">
                <li><strong>Executive-grade delivery:</strong> Program governance built for board-level visibility.</li>
                <li><strong>Cross-domain expertise:</strong> Power systems, software, data, and OT security under one practice.</li>
                <li><strong>Precision execution:</strong> Structured PMO, milestone assurance, and vendor orchestration.</li>
                <li><strong>Measured outcomes:</strong> Every initiative tied to reliability, capacity, and ROI objectives.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Schedule a Strategic Consultation")
    name = st.text_input("Full Name")
    email = st.text_input("Work Email")
    challenge = st.text_area("Primary Grid Challenge", placeholder="Tell us what you need to modernize, secure, or scale.")
    if st.button("Request Private Briefing"):
        if name and email and challenge:
            st.success("Thank you. A senior Rycroft advisor will reach out within one business day.")
        else:
            st.warning("Please complete all fields before submitting.")

st.markdown(
    """
    <hr style="border:1px solid rgba(148,163,184,0.2); margin-top:2rem;" />
    <p style="text-align:center; color:#94a3b8;">
        © 2026 Rycroft Grid Solutions — Premium Grid Advisory, Engineering, and Operations Excellence.
    </p>
    """,
    unsafe_allow_html=True,
)
