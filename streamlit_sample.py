#from traitlets import default
import streamlit as st
import datetime

header = st.container()
calculator = st.container()
results = st.container()
inclusive = st.container()

with header:
    st.title("Arthur's lab Energy Cost Calculator")
    st.text("Welcome to the Energy Cost Calculator. Here you can automatically calculate you current enegry costs on a specific period of time.")

with calculator:
    st.subheader("Here is the awesome calculator")

    lef_col, rig_col = st.columns(2)

    first_reading = lef_col.number_input("Enter the previous reading: ", step=1)
    second_reading = rig_col.number_input("Enter the newest reading: ", step=1)

    first_date = lef_col.date_input("Enter the date of the previous reading: ", value = datetime.date(2022, 1, 1))
    second_date = rig_col.date_input("Enter the date of the newest reading: ")

    price_old = lef_col.number_input("Enter your price per kWh in Cent: ")
    price = price_old / 100
    basic_fee = rig_col.number_input("Plese enter your annual basic fee (in EUR)", step=1)

    reading_difference = float(second_reading) - float(first_reading)
 
    consumption_kwh = reading_difference * 0.9103 * 11.4070

    date_difference = (second_date - first_date).days

    consumption_kwh_a = consumption_kwh / date_difference * 365
    #price = 0.2326

    annual_energy_price = consumption_kwh_a * price
    annual_energy_price_euros = "{:,.2f}".format(annual_energy_price) + " €"

    monthly_energy_price = annual_energy_price / 12
    monthly_energy_price_euros = "{:,.2f}".format(monthly_energy_price) + " €"
    
    a_col, b_col, c_col = st.columns(3)

    a_col.markdown("**Measured consumption (kWh):**")
    a_col.text(consumption_kwh)
    
    b_col.markdown("**Consumption per year (kWh):**")
    b_col.text(consumption_kwh_a)

    c_col.markdown("**Date difference:**")
    c_col.text(date_difference)

with results:

    st.subheader("Here are the results:")

    one_col, two_col = st.columns(2)

    one_col.markdown("**Energy costs per year based on consumption(EUR/a):**")
    one_col.text(annual_energy_price_euros)

    two_col.markdown("**Energy costs per month based on consumption (EUR/m):**")
    two_col.text(monthly_energy_price_euros)

with inclusive:
    
    agree = one_col.checkbox('Show results including basic fee')

    if agree:

        fee_annual_energy_price = annual_energy_price + basic_fee
        fee_annual_energy_price_euros = "{:,.2f}".format(fee_annual_energy_price) + " €"

        one_col_a, two_col_a = st.columns(2)

        one_col_a.markdown("**Energy costs per year based on consumption including your basic fee (EUR/a):**")
        one_col_a.text(fee_annual_energy_price_euros)

        basic_fee_monthly = basic_fee / 12
        fee_monthly_energy_price = monthly_energy_price + basic_fee_monthly
        fee_monthly_energy_price_euros = "{:,.2f}".format(fee_monthly_energy_price) + " €"
        two_col_a.markdown("**Energy costs per month based on consumption including your basic fee (EUR/m):**")
        two_col_a.text(fee_monthly_energy_price_euros)
