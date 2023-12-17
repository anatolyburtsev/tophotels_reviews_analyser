import re

import streamlit as st

from evaluate_scores import answer_question
from reviews_utils import get_scores_conditional_download


def extract_hotel_id(url):
    pattern = r'al(\d+)'
    match = re.search(pattern, url)
    if match:
        return match.group(0)  # Returns the entire match (e.g., 'al7183')
    else:
        return None


# Streamlit app
def main():
    st.title('Hotel Reviews QA')

    # Text input for hotel ID with default value
    hotel_url = st.text_input('Hotel url or id', value='https://tophotels.ru/hotel/al54199')
    hotel_id = extract_hotel_id(hotel_url)

    # Text input for the question
    question = st.text_input('Question', value='Есть ли проблема с мухами или тараканами?')

    # Button to submit
    if st.button('Submit'):
        scores_data = ""
        with st.spinner('Fetching data...'):
            # Call the function and display the output
            scores_data = get_scores_conditional_download(hotel_id)

        with st.spinner('Analysing data'):
            response = answer_question(question, scores_data)
        st.write(response)


if __name__ == "__main__":
    main()
