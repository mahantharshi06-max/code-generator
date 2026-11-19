# Code Generator

import requests
import streamlit as st

API_KEY = st.secrets["OPENROUTER_API_KEY"]
URL = "https://openrouter.ai/api/v1/chat/completions"

st.title("Code Generator")

prompt = st.text_area("Enter your prompt", height=150)
language = st.selectbox("Select language", ["Python", "Java", "C", "C++", "JavaScript"])

if st.button("Generate"):
    if not prompt.strip():
        st.warning("Please enter a prompt before generating code.")
    else:
        with st.spinner("Generating code..."):
            try:
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                }

                body = {
                    "model": "openai/gpt-4o-mini",
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                f"Generate beginner-friendly code in {language} for this requirement: "
                                f"{prompt}. Return only the code in a code block."
                            ),
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }

                response = requests.post(URL, headers=headers, json=body, timeout=60)
                response.raise_for_status()
                data = response.json()
                result = data["choices"][0]["message"]["content"]

                st.subheader("Generated code")
                st.code(result, language=language.lower())

            except requests.RequestException as e:
                st.error(f"Request failed: {e}")
            except (KeyError, IndexError, ValueError) as e:
                st.error(f"Could not parse the API response: {e}")