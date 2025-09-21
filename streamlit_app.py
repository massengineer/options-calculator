import streamlit as st
import numpy as np
import seaborn as sns

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
    
    # def plot_heatmap(bs_model, spot_range, vol_range, strike):
    #   call_prices = np.zeros((len(vol_range), len(spot_range)))
    #   put_prices = np.zeros((len(vol_range), len(spot_range)))
      
    #   for i, vol in enumerate(vol_range):
    #       for j, spot in enumerate(spot_range):
    #           bs_temp = BlackScholes(
    #               time_to_maturity=bs_model.time_to_maturity,
    #               strike=strike,
    #               current_price=spot,
    #               volatility=vol,
    #               interest_rate=bs_model.interest_rate
    #           )
    #           bs_temp.calculate_prices()
    #           call_prices[i, j] = bs_temp.call_price
    #           put_prices[i, j] = bs_temp.put_price
      
    #   # Plotting Call Price Heatmap
    #   fig_call, ax_call = plt.subplots(figsize=(10, 8))
    #   sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_call)
    #   ax_call.set_title('CALL')
    #   ax_call.set_xlabel('Spot Price')
    #   ax_call.set_ylabel('Volatility')
      
    #   # Plotting Put Price Heatmap
    #   fig_put, ax_put = plt.subplots(figsize=(10, 8))
    #   sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_put)
    #   ax_put.set_title('PUT')
    #   ax_put.set_xlabel('Spot Price')
    #   ax_put.set_ylabel('Volatility')
      
    #   return fig_call, fig_put