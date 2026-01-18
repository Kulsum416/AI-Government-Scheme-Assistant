import streamlit as st
import os
import wikipedia
import re

st.title("Government Scheme Assistant")

SCHEME_FOLDER = "scheme_data"

def normalize(text):
    return text.lower().replace("_", "").replace(" ", "")

def structure_scheme_info(title, summary):
    return f"""
### Scheme Name
{title}

### Eligibility
Typically applicable to Indian citizens meeting scheme-specific age, income, or employment criteria.  
(Exact eligibility may vary — please check official government notifications.)

### Benefits
Provides financial, social security, or welfare benefits such as pension, subsidies, or direct benefit transfers depending on the scheme.

### How to Apply
Applications are usually accepted through:
- Official government portals  
- Banks / CSC centers  
- State or central welfare offices  

### Scheme Overview
{summary}

🔗 **Note:** For the latest and most accurate information, users should refer to the official government website.
"""

def fetch_online_scheme(query):
    try:
        wikipedia.set_lang("en")
        page = wikipedia.page(query, auto_suggest=True)
        summary = wikipedia.summary(query, sentences=3)
        return structure_scheme_info(page.title, summary)

    except wikipedia.exceptions.DisambiguationError as e:
        page = wikipedia.page(e.options[0])
        summary = wikipedia.summary(e.options[0], sentences=3)
        return structure_scheme_info(page.title, summary)

    except wikipedia.exceptions.PageError:
        return "No reliable online information found."

question = st.text_input("Enter scheme name")

if st.button("Search"):
    found = False
    user_query = normalize(question)

    # STEP 1: LOCAL SCHEME SEARCH
    if os.path.exists(SCHEME_FOLDER):
        for file in os.listdir(SCHEME_FOLDER):
            scheme_name = normalize(file.replace(".txt", ""))
            if scheme_name in user_query or user_query in scheme_name:
                with open(os.path.join(SCHEME_FOLDER, file), "r", encoding="utf-8") as f:
                    st.success("Found in local scheme database")
                    st.markdown(f.read())
                    found = True
                    break

    # STEP 2: ONLINE FETCH WITH STRUCTURE
    if not found:
        st.warning("Scheme not found locally. Fetching structured online information...")
        result = fetch_online_scheme(question)
        st.markdown(result)
