import streamlit as st

st.set_page_config(page_title="Credit Risk Predictor", page_icon="💳", layout="centered")

st.title("💳 Credit Risk Predictor")
st.caption("Loan affordability check (ML risk model coming soon)")

# ---------- Inputs ----------
st.subheader("Applicant details")
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=70, value=30)
    income = st.number_input("Monthly income (₹)", min_value=1000, value=40000, step=1000)
    existing_emi = st.number_input("Existing monthly EMIs (₹)", min_value=0, value=0, step=500)

with col2:
    employment = st.selectbox("Employment type", ["Salaried", "Self-employed", "Business"])
    loan = st.number_input("Loan amount (₹)", min_value=10000, value=300000, step=10000)
    tenure_years = st.slider("Tenure (years)", 1, 30, 5)

rate = st.slider("Interest rate (% per year)", 6.0, 24.0, 11.0, step=0.5)

# ---------- Calculation ----------
def calculate_emi(principal, annual_rate, years):
    r = annual_rate / 12 / 100
    n = years * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

if st.button("Check affordability", type="primary"):
    emi = calculate_emi(loan, rate, tenure_years)
    total_payment = emi * tenure_years * 12
    foir = (emi + existing_emi) / income * 100

    st.subheader("Results")
    m1, m2, m3 = st.columns(3)
    m1.metric("Monthly EMI", f"₹{emi:,.0f}")
    m2.metric("Total interest", f"₹{total_payment - loan:,.0f}")
    m3.metric("FOIR", f"{foir:.1f}%")

    if foir <= 40:
        st.success("Healthy: EMI burden is within the usual 40% guideline.")
    elif foir <= 50:
        st.warning("Borderline: EMI burden is high. Banks may ask for more documents.")
    else:
        st.error("High burden: EMI is above 50% of income. Approval is unlikely.")

    st.info("🚧 ML-based default risk prediction will be added once the model is trained on real data.")

st.divider()
st.caption("Educational project. Not financial advice.")