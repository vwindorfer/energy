#from traitlets import default
import streamlit as st
import datetime
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
#import seaborn as sns
import base64


header = st.container()
calculator = st.container()
results = st.container()
inclusive = st.container()

today = date.today()

with header:
    st.title("brandmill's Energy Cost Calculator")
    st.text("All rights belong to the owner and creator of the application. VW.")

with calculator:
    st.subheader("Here is the awesome calculator")

    lef_col, rig_col = st.columns(2)

    first_reading = lef_col.number_input("Enter the previous reading: ", step=1)
    rounded_first_reading = (format(first_reading, ',d'))
    second_reading = rig_col.number_input("Enter the newest reading: ", step=1)
    rounded_second_reading = (format(second_reading, ',d'))

    first_date = lef_col.date_input("Enter the date of the previous reading: ", value = datetime.date(2022, 1, 1))
    second_date = rig_col.date_input("Enter the date of the newest reading: ")

    price_old = lef_col.number_input("Enter your price per kWh in Cent: ")
    rounded_price_old = "{:,.2f}".format(price_old)
    price = price_old / 100
    basic_fee = rig_col.number_input("Plese enter your annual basic fee (in EUR)", step=1)
    rounded_basic_fee = "{:,.2f}".format(basic_fee)

    reading_difference = float(second_reading) - float(first_reading)
 
    consumption_kwh = reading_difference * 0.9103 * 11.4070

    date_difference = (second_date - first_date).days

    consumption_kwh_a = consumption_kwh / date_difference * 365
    #price = 0.2326

    annual_energy_price = consumption_kwh_a * price
    rounded_annual_energy_price = "{:,.2f}".format(annual_energy_price)
    annual_energy_price_euros = "{:,.2f}".format(annual_energy_price) + " €"

    monthly_energy_price = annual_energy_price / 12
    rounded_monthly_energy_price = "{:,.2f}".format(monthly_energy_price)
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

    fee_annual_energy_price = annual_energy_price + basic_fee
    rounded_fee_annual_energy_price = "{:,.2f}".format(fee_annual_energy_price)
    fee_annual_energy_price_euros = "{:,.2f}".format(fee_annual_energy_price) + " €"

    basic_fee_monthly = basic_fee / 12
    fee_monthly_energy_price = monthly_energy_price + basic_fee_monthly
    rounded_fee_monthly_energy_price = "{:,.2f}".format(fee_monthly_energy_price)
    fee_monthly_energy_price_euros = "{:,.2f}".format(fee_monthly_energy_price) + " €"

    if agree:

        one_col_a, two_col_a = st.columns(2)

        one_col_a.markdown("**Energy costs per year based on consumption including your basic fee (EUR/a):**")
        one_col_a.text(fee_annual_energy_price_euros)

        two_col_a.markdown("**Energy costs per month based on consumption including your basic fee (EUR/m):**")
        two_col_a.text(fee_monthly_energy_price_euros)

# Create a Dictionary
data = {'first_reading': [first_reading],
        'second_reading': [second_reading],
        'first_date': [first_date],
        'second_date': [second_date],
        'price': [price],
        'basic_fee': [basic_fee],
        'annual_energy_price': [annual_energy_price],
        'monthly_energy_price': [monthly_energy_price]
       }

#Create the data frame
df = pd.DataFrame(data)

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

#st.dataframe(df)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Energy Costs Calculator", border=False, ln=1)
        self.set_font("Arial", "", 11)
        self.cell(0, 10, 'All rights belong the the developer and owner of the application. VW.')
        self.ln(10)

if st.button('Download Report as PDF'):
    pdf = PDF("P", "mm", "Letter")
    pdf.add_page()
    pdf.set_font('Arial', '', 11)
    pdf.cell(70, 5, f'Date:')
    pdf.cell(0, 5, f'{today}', ln=True)
    pdf.ln(15)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, f'Excluding Basic Fee', ln=True)
    pdf.ln(2)
    pdf.set_font('Arial', '', 11)
    pdf.cell(70, 5, f'Monthly Gas Costs:')
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, f'{rounded_monthly_energy_price} EUR', ln=True)
    pdf.set_font('Arial', '', 11)
    pdf.cell(70, 5, f'Annual Gas Costs:')
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, f'{rounded_annual_energy_price} EUR', ln=True)
    pdf.ln(7)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, f'Including Basic Fee', ln=True)
    pdf.ln(2)
    pdf.set_font('Arial', '', 11)
    pdf.cell(70, 5, f'Monthly Gas Costs:')
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, f'{rounded_fee_monthly_energy_price} EUR', ln=True)
    pdf.set_font('Arial', '', 11)
    pdf.cell(70, 5, f'Annual Gas Costs:')
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, f'{rounded_fee_annual_energy_price} EUR', ln=True)
    pdf.ln(7)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, f'Input', ln=True)
    pdf.ln(2)
    pdf.set_font('Arial', '', 11)
    pdf.cell(70, 5, f'Date of the First Reading:')
    pdf.cell(0, 5, f'{first_date}', ln=True)
    pdf.cell(70, 5, f'Date of the Second Reading:')
    pdf.cell(0, 5, f'{second_date}', ln=True)
    pdf.ln(2)
    pdf.cell(70, 5, f'Amount at the First Reading:')
    pdf.cell(0, 5, f'{rounded_first_reading}', ln=True)
    pdf.cell(70, 5, f'Amount at the Second Reading:')
    pdf.cell(0, 5, f'{rounded_second_reading}', ln=True)
    pdf.ln(2)
    pdf.cell(70, 5, f'Your Price per kWh:')
    pdf.cell(0, 5, f'{rounded_price_old} Cent', ln=True)
    pdf.cell(70, 5, f'Your Basic Fee:')
    pdf.cell(0, 5, f'{rounded_basic_fee} EUR', ln=True)
    pdf.ln(7)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, f'Detailed Report', ln=True)
    pdf.ln(2)
    pdf.set_font('Arial', '', 11)
    pdf.cell(70, 5, f'Date Difference:')
    pdf.cell(0, 5, f'{date_difference} Days', ln=True)
    pdf.cell(70, 5, f'Measured Consumptions:')
    pdf.cell(0, 5, f'{consumption_kwh} kWh', ln=True)
    pdf.cell(70, 5, f'Measured Consumptions per Year:')
    pdf.cell(0, 5, f'{consumption_kwh_a} kWh', ln=True)
    #pdf.output('energy_report.pdf', "F")
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "energy_report")

    st.markdown(html, unsafe_allow_html=True)


st.text("")
st.text("")
st.text("")
st.write("Version Streamlit:")
st.write(st.__version__)
st.write("Version Pandas:")
st.write(pd.__version__)
