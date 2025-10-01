import streamlit as st
import numpy as np
import seaborn as sns
import ctypes
import pandas as pd
import matplotlib.pyplot as plt
import os
from sqlalchemy import text

####################
# DB configuration #
####################

# Initialize connection.
conn = st.connection("neon", type="sql")

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

################################
# C++ Calculator Engine Config #
################################

# 1. Initialize clib and compilation result globally. This ensures they are always defined.
clib = None
compile_result = 1 # Initialize to a non-zero (failure) code

# 2. Compile the C++ code for Linux deployment
st.info("Attempting to compile C++ engine on the server...")
try:
    # On Linux (Streamlit Cloud), compile the C++ source into a Shared Object (.so)
    # -fPIC is essential for creating shared libraries
    # -lm links the math library (required for functions like std.sqrt)
    compile_cmd = "g++ -shared -o cpp-engine/calculator.so cpp-engine/calculator.cpp -fPIC -lm"
    # os.system runs the command and returns 0 if successful
    compile_result = os.system(compile_cmd)
    
    if compile_result != 0:
        st.error(f"C++ compilation failed with error code {compile_result}. Did you include 'g++' in packages.txt?")
    else:
        st.success("C++ engine compiled successfully (calculator.so).")
        
except Exception as e:
    st.error(f"Error during C++ compilation command execution: {e}")

# 3. Load the shared library
lib_path = "./cpp-engine/calculator.so"  # Linux path
try:
    if compile_result == 0 or os.path.exists(lib_path):
        clib = ctypes.CDLL(lib_path)
except OSError:
    st.error(f"Could not load the options calculator engine ({lib_path}). Please check compilation logs.")
    
# Define the argument and return types of C++ functions
if clib is not None:
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
    
    clib.calculateCallPnL.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculateCallPnL.restype = ctypes.c_double
    
    clib.calculatePutPnL.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
    clib.calculatePutPnL.restype = ctypes.c_double

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
    purchase_price = st.number_input("Purchase Price", value=10.0)

    st.markdown("---")
    calculate_btn = st.button('Heatmap Parameters')
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)
    
    
    ######################################
    # Black-Scholes Model Implementation #
    ######################################
    
def get_option_data(current_price, strike, interest_rate, time_to_maturity, volatility):
    call_price = clib.calculateCallPrice(current_price, strike, interest_rate, time_to_maturity, volatility)
    put_price = clib.calculatePutPrice(current_price, strike, interest_rate, time_to_maturity, volatility)
    delta_call = clib.calculateDeltaCall(current_price, strike, interest_rate, time_to_maturity, volatility)
    delta_put = clib.calculateDeltaPut(current_price, strike, interest_rate, time_to_maturity, volatility)
    gamma_call = clib.calculateGammaCall(current_price, strike, interest_rate, time_to_maturity, volatility)
    gamma_put = clib.calculateGammaPut(current_price, strike, interest_rate, time_to_maturity, volatility)
    vega_call = clib.calculateVegaCall(current_price, strike, interest_rate, time_to_maturity, volatility)
    vega_put = clib.calculateVegaPut(current_price, strike, interest_rate, time_to_maturity, volatility)
    theta_call = clib.calculateThetaCall(current_price, strike, interest_rate, time_to_maturity, volatility)
    theta_put = clib.calculateThetaPut(current_price, strike, interest_rate, time_to_maturity, volatility)
    rho_call = clib.calculateRhoCall(current_price, strike, interest_rate, time_to_maturity, volatility)
    rho_put = clib.calculateRhoPut(current_price, strike, interest_rate, time_to_maturity, volatility)

    
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
        "rho_put": rho_put,
    }


def plot_black_scholes_heatmap(current_price, strike, interest_rate, time_to_maturity, volatility, spot_range, vol_range):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))
    
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            call_prices[i, j] = clib.calculateCallPrice(
                spot,  # current_price 
                strike,
                interest_rate,
                time_to_maturity,
                vol,   
            )
            put_prices[i, j] = clib.calculatePutPrice(
                spot,  
                strike,
                interest_rate,
                time_to_maturity,
                vol,   
            )
    
    return call_prices, put_prices


def plot_pnl_heatmap(strike, spot_T, purchase_price, spot_range, vol_range):
    call_pnls = np.zeros((len(vol_range), len(spot_range)))
    put_pnls = np.zeros((len(vol_range), len(spot_range)))
        
    for i in range(len(vol_range)):
        for j, spot_T in enumerate(spot_range):
            call_pnls[i, j] = clib.calculateCallPnL(
                strike,
                spot_T,
                purchase_price
            )
            put_pnls[i, j] = clib.calculatePutPnL(
                strike,
                spot_T,
                purchase_price
            )
    
    return call_pnls, put_pnls

def log_calculations_to_db(conn, inputs, outputs):
    log_data = {**inputs, **outputs}
    columns = ', '.join(log_data.keys())
    placeholders = ', '.join([f":{col}" for col in log_data.keys()])
    query = f"INSERT INTO black_scholes_logs ({columns}) VALUES ({placeholders})"
    
    try:
        with conn.session as session:
            session.execute(text(query), log_data)
            session.commit()
        st.success("Calculation logged to database.")
    except Exception as e:
        st.error(f"Failed to log calculation to Neon database: {e}")

# Main Page for Output Display
st.title("Black-Scholes Pricing Model")

# Table of Inputs
input_data = {
    "Current Asset Price": [f"{current_price:.2f}"],
    "Strike Price": [f"{strike:.2f}"],
    "Time to Maturity (Years)": [f"{time_to_maturity:.2f}"],
    "Volatility (σ)": [f"{volatility:.2f}"],
    "Risk-Free Interest Rate": [f"{interest_rate:.2f}"],
    "Purchase Price": [f"{purchase_price:.2f}"],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

# Calculate Greeks, Call and Put Prices
greeks_data = get_option_data(current_price, strike, interest_rate, time_to_maturity, volatility)
call_price = greeks_data["call_price"]
put_price = greeks_data["put_price"]

# Prepare data for logging and log to DB
inputs = {
    "current_price": current_price,
    "strike": strike,
    "time_to_maturity": time_to_maturity,
    "volatility": volatility,
    "interest_rate": interest_rate,
    "purchase_price": purchase_price
}

outputs = greeks_data

log_calculations_to_db(conn, inputs, outputs)

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
st.info("Discover how option prices fluctuate with varying 'Spot Prices and Volatility' levels using interactive heatmap parameters, all while maintaining a constant 'Strike Price'. Then analyse the P&L heatmaps based on your 'Purchase Price'.")

# Interactive Sliders and Heatmaps for Call and Put Options
col1, col2 = st.columns([1,1], gap="small")

# Calculate the heatmap data
call_prices, put_prices = plot_black_scholes_heatmap(
    current_price,
    strike,
    interest_rate,
    time_to_maturity,
    volatility,
    spot_range,
    vol_range
)

# Calculate P&L heatmap data (assuming purchase price is the current call/put price)
call_pnls, put_pnls = plot_pnl_heatmap(
    strike,
    current_price,  # Assuming spot_T is current price for simplicity
    purchase_price,
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
    
    st.subheader("Call Price Greeks")
    greeks = get_option_data(current_price, strike, interest_rate, time_to_maturity, volatility)
    greeks_data = {
        "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
        "Call": [greeks["delta_call"], greeks["gamma_call"], greeks["vega_call"], greeks["theta_call"], greeks["rho_call"]],
    }
    greeks_df = pd.DataFrame(greeks_data)
    greeks_df["Call"] = greeks_df["Call"].apply(lambda x: f"{x:.4f}")
    st.table(greeks_df)
    
    st.subheader("Call P&L Heatmap")
    # Create heatmap for call P&L
    fig_call_pnl, ax_call_pnl = plt.subplots()
    sns.heatmap(call_pnls, xticklabels=np.round(spot_range,2), yticklabels=np.round(vol_range,2), ax=ax_call_pnl, cmap='RdYlGn',
    annot=True, fmt=".1f", center=0)
    ax_call_pnl.set_xlabel('Spot Price')
    ax_call_pnl.set_ylabel('Volatility')
    st.pyplot(fig_call_pnl)
    

with col2:
    st.subheader("Put Price Heatmap")
    # Create heatmap for put prices
    fig_put, ax_put = plt.subplots()
    sns.heatmap(put_prices, xticklabels=np.round(spot_range,2), yticklabels=np.round(vol_range,2), ax=ax_put, cmap='RdYlGn',
    annot=True, fmt=".1f")
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')
    st.pyplot(fig_put)
    
    st.subheader("Put Price Greeks")
    greeks = get_option_data(current_price, strike, interest_rate, time_to_maturity, volatility)
    greeks_data = {
        "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
        "Put": [greeks["delta_put"], greeks["gamma_put"], greeks["vega_put"], greeks["theta_put"], greeks["rho_put"]],
    }
    greeks_df = pd.DataFrame(greeks_data)
    greeks_df["Put"] = greeks_df["Put"].apply(lambda x: f"{x:.4f}")
    st.table(greeks_df)
    
    st.subheader("Put P&L Heatmap")
    # Create heatmap for put P&L
    fig_put_pnl, ax_put_pnl = plt.subplots()
    sns.heatmap(put_pnls, xticklabels=np.round(spot_range,2), yticklabels=np.round(vol_range,2), ax=ax_put_pnl, cmap='RdYlGn',
    annot=True, fmt=".1f", center=0)
    ax_put_pnl.set_xlabel('Spot Price')
    ax_put_pnl.set_ylabel('Volatility')
    st.pyplot(fig_put_pnl)