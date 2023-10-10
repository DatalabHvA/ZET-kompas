import streamlit as st
import pandas as pd
import requests
import base64
from io import BytesIO

st.set_page_config(layout="wide")


def download_template():
	# Template file URL
	template_url = 'https://github.com/DatalabHvA/ZET-kompas/blob/main/input/wagenpark.xlsx'

	# Request the template file
	response = requests.get(template_url)

	# Create a BytesIO object
	template_data = BytesIO(response.content)

	# Offer the file download
	st.download_button('Download Template', template_data, file_name='wagenpark.xlsx')

# Streamlit app
st.title("ZET-kompas interface")

# Download template button
download_template()
	
# File upload
excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if excel_file is not None:
    # Make an API request (replace with your API endpoint and data)
	api_url = 'https://zet-kompas.vercel.app/external_excel?company=Input&scenarios=midden'
	
	#input_text = open(excel_file, 'rb')
	input_read = excel_file.read()
	input_encode = base64.b64encode(input_read).decode('ascii')

	scenarios_text = open('./input/scenarios.xlsx', 'rb')
	scenarios_read = scenarios_text.read()
	scenarios_encode = base64.b64encode(scenarios_read).decode('ascii')
	
	data = {
	  "fleet_data": input_encode,
	  "scenario_data": scenarios_encode
	}
	
	response = requests.post(api_url, json=data)

	if response.status_code == 200:
		# Display the HTML code returned by the API
		html_code = response.text
		st.components.v1.html(html_code, height = 600, scrolling=True)
	else:
		st.error("API request failed.")
