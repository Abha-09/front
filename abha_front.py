import streamlit as st
import requests
import json

# Set the page title to your roll number
st.set_page_config(page_title="Your Roll Number")

# Set the title of the app
st.title("API Input and Filter")

# Text area for JSON input
st.subheader("API Input")
json_input = st.text_area("Enter JSON data:", height=60)

# Button to submit JSON input
if st.button("Submit"):
    try:
        # Validate the JSON input
        parsed_json = json.loads(json_input)
        st.success("Valid JSON")
        
        # Call the backend API
        response = requests.post("https://your-backend-app.herokuapp.com/bfhl", json=parsed_json)
        response_data = response.json()

        # Save the response data in session state
        st.session_state['response_data'] = response_data
        st.session_state['valid_submission'] = True
    except json.JSONDecodeError:
        st.error("Invalid JSON input")
        st.session_state['valid_submission'] = False
    except requests.RequestException as e:
        st.error(f"Error calling API: {e}")
        st.session_state['valid_submission'] = False

# Display the multi-select dropdown if the submission was valid
if 'valid_submission' in st.session_state and st.session_state['valid_submission']:
    st.subheader("Multi Filter")
    options = st.multiselect(
        "Select filters:",
        ['Alphabets', 'Numbers', 'Highest lowercase alphabet']
    )

    # Filter and display the response based on the selected options
    if options:
        filtered_response = {
            key: st.session_state['response_data'].get(key)
            for key in options
        }
        st.subheader("Filtered Response")
        for key, value in filtered_response.items():
            st.write(f"{key}: {', '.join(value)}")
