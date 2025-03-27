import os
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def app():
    # Input fields for means and standard deviations of 3 distributions
    means = []
    std_devs = []
    for i in range(3):
        cols = st.columns(2)
        with cols[0]:
            means.append(st.number_input(f"Mean {i+1}", value=0.0))
        with cols[1]:
            std_devs.append(st.number_input(f"Standard Deviation {i+1}", value=1.0))

    # Generate the normal distribution data
    x = np.linspace(min(means) - 3*max(std_devs), max(means) + 3*max(std_devs), 1000)
    y = np.zeros_like(x)

    for mean, std_dev in zip(means, std_devs):
        y += (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev)**2)

    # Plot the data
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Sum of 3 Normal Distributions")
    ax.set_xlabel("X")
    ax.set_ylabel("Probability Density")

    # Display the plot in the Streamlit app
    st.pyplot(fig)

# Load authentication config
with open('users.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Ensure the config file contains valid credentials
if not config or 'credentials' not in config or not config['credentials']:
    raise ValueError("Invalid or missing credentials in users.yaml")

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'])

# Display login widget
try:
    authenticator.login()
    if st.session_state.get('authentication_status'):
        authenticator.logout()
        st.write(f'Welcome *{st.session_state.get("name")}*')
        st.title('Some content')
        app()
    elif st.session_state.get('authentication_status') is False:
        st.error('Username/password is incorrect')
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please enter your username and password')
    
except Exception as e:
    st.error(e)

