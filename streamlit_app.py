import streamlit as st
import numpy as np
import seaborn as sns
import ctypes
import pandas as pd
import matplotlib.pyplot as plt

######################
# Page configuration #
######################
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)

# Sidebar for User Inputs
with st.sidebar:
    st.title("📈 Black-Scholes Options Calculator")
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/louis-massingham/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Louis Massingham, London`</a>', unsafe_allow_html=True)

    current_price = st.number_input("Current Asset Price", value=100.0)
    strike = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

    st.markdown("---")
    calculate_btn = st.button('Heatmap Parameters')
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)
    
    
    ################################
    # C++ Calculator Engine Config #
    ################################
    
    # 1. Load the shared library
    lib_path = "./cpp-engine/calculator.dll"  # For Windows
    try:
        clib = ctypes.CDLL(lib_path)
    except OSError:
        st.error(f"Could not load the shared library at {lib_path}. Did you compile your C++ code?")
        
    # 2. Define the argument and return types of C++ functions
    clib.calculateCallPrice.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateCallPrice.restype = ctypes.c_double
    
    clib.calculatePutPrice.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculatePutPrice.restype = ctypes.c_double
    
    clib.calculateDeltaCall.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateDeltaCall.restype = ctypes.c_double
    
    clib.calculateDeltaPut.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateDeltaPut.restype = ctypes.c_double
    
    clib.calculateGammaCall.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateGammaCall.restype = ctypes.c_double
    
    clib.calculateGammaPut.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateGammaPut.restype = ctypes.c_double
    
    clib.calculateVegaCall.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateVegaCall.restype = ctypes.c_double
    
    clib.calculateVegaPut.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateVegaPut.restype = ctypes.c_double
    
    clib.calculateThetaCall.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateThetaCall.restype = ctypes.c_double
    
    clib.calculateThetaPut.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateThetaPut.restype = ctypes.c_double
    
    clib.calculateRhoCall.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateRhoCall.restype = ctypes.c_double
    
    clib.calculateRhoPut.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateRhoPut.restype = ctypes.c_double
    
    ######################################
    # Black-Scholes Model Implementation #
    ######################################
    
def get_option_data(current_price, strike, time_to_maturity, volatility, interest_rate):
    call_price = clib.calculateCallPrice(current_price, strike, time_to_maturity, volatility, interest_rate)
    put_price = clib.calculatePutPrice(current_price, strike, time_to_maturity, volatility, interest_rate)
    delta_call = clib.calculateDeltaCall(current_price, strike, time_to_maturity, volatility, interest_rate)
    delta_put = clib.calculateDeltaPut(current_price, strike, time_to_maturity, volatility, interest_rate)
    gamma_call = clib.calculateGammaCall(current_price, strike, time_to_maturity, volatility, interest_rate)
    gamma_put = clib.calculateGammaPut(current_price, strike, time_to_maturity, volatility, interest_rate)
    vega_call = clib.calculateVegaCall(current_price, strike, time_to_maturity, volatility, interest_rate)
    vega_put = clib.calculateVegaPut(current_price, strike, time_to_maturity, volatility, interest_rate)
    theta_call = clib.calculateThetaCall(current_price, strike, time_to_maturity, volatility, interest_rate)
    theta_put = clib.calculateThetaPut(current_price, strike, time_to_maturity, volatility, interest_rate)
    rho_call = clib.calculateRhoCall(current_price, strike, time_to_maturity, volatility, interest_rate)
    rho_put = clib.calculateRhoPut(current_price, strike, time_to_maturity, volatility, interest_rate)
    
    return {
        "call_price": call_price,
        "put_price": put_price,
        "delta_call": delta_call,
        "delta_put": delta_put,
        "gamma_call": gamma_call,
        "gamma_put": gamma_put,
        "vega_call": vega_call,
        "vega_put": vega_put,
        "theta_call": theta_call,
        "theta_put": theta_put,
        "rho_call": rho_call,
        "rho_put": rho_put
    }

def plot_heatmap(current_price, strike, time_to_maturity, volatility, interest_rate, spot_range, vol_range):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))
    
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            call_prices[i, j] = clib.calculateCallPrice(
                spot,  # current_price 
                strike,
                time_to_maturity,
                vol,   
                interest_rate
            )
            put_prices[i, j] = clib.calculatePutPrice(
                spot,  
                strike,
                time_to_maturity,
                vol,   
                interest_rate
            )
    
    return call_prices, put_prices

# Main Page for Output Display
st.title("Black-Scholes Pricing Model")

# Table of Inputs
input_data = {
    "Current Asset Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [interest_rate],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

# Calculate Call and Put values
call_price, put_price = clib.calculateCallPrice(current_price, strike, time_to_maturity, volatility, interest_rate), clib.calculatePutPrice(current_price, strike, time_to_maturity, volatility, interest_rate)

# Display Call and Put Values in colored tables
col1, col2 = st.columns([1,1], gap="small")

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.title("Options Price - Interactive Heatmap")
st.info("Explore how option prices fluctuate with varying 'Spot Prices and Volatility' levels using interactive heatmap parameters, all while maintaining a constant 'Strike Price'.")

# Interactive Sliders and Heatmaps for Call and Put Options
col1, col2 = st.columns([1,1], gap="small")

# Calculate the heatmap data
call_prices, put_prices = plot_heatmap(
    current_price,
    strike,
    time_to_maturity,
    volatility,
    interest_rate,
    spot_range,
    vol_range
)

with col1:
    st.subheader("Call Price Heatmap")
    # Create heatmap for call prices
    fig_call, ax_call = plt.subplots()
    sns.heatmap(call_prices, xticklabels=np.round(spot_range,2), yticklabels=np.round(vol_range,2), ax=ax_call, cmap='RdYlGn',
    annot=True, fmt=".1f")
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')
    st.pyplot(fig_call)

with col2:
    st.subheader("Put Price Heatmap")
    # Create heatmap for put prices
    fig_put, ax_put = plt.subplots()
    sns.heatmap(put_prices, xticklabels=np.round(spot_range,2), yticklabels=np.round(vol_range,2), ax=ax_put, cmap='RdYlGn',
    annot=True, fmt=".1f")
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')
    st.pyplot(fig_put)