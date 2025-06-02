
import streamlit as st
from tamil_syllable_split import tamil_syllable_split

st.title("🪔 Tamil Syllable Splitter")

user_input = st.text_input("Enter a Tamil word:")

if user_input:
    syllables = tamil_syllable_split(user_input)
    st.markdown("### Resulting Syllables:")
    st.success(" | ".join(syllables))
