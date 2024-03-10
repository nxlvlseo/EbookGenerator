import streamlit as st
import openai
import os

# OpenAI API key setup
openai.api_key = st.secrets["secrets"]["OPENAI_API_KEY"]

def generate_text(prompt):
    try:
        response = openai.ChatCompletion.create(
          model="gpt-4",  # Adjust according to the available models
          messages=[{"role": "system", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"An error occurred while generating the script: {e}")
        return ""


def app():
    """Main app function."""
    st.title("E-Book Creator")

    with st.form("book_input_form"):
        title = st.text_input("Title")
        genre = st.text_input("Genre")
        age = st.number_input("Target Age", min_value=0, value=18)
        language = st.text_input("Language", value="English")
        sex = st.selectbox("Sex", ['Male', 'Female', 'Other'])
        interests = st.text_area("Interests")
        submit_button = st.form_submit_button("Generate Outline")

    if submit_button:
        prompt = f"Create a book outline for a {genre} book titled '{title}', aimed at {age}-year-olds, in {language}. The main character is {sex} with interests in {interests}."
        outline = generate_text(prompt, max_tokens=500)
        st.session_state['outline'] = outline.split('\n')
        st.write("Generated Outline:")
        for idx, item in enumerate(st.session_state['outline']):
            st.text(f"{idx+1}. {item}")

        # Buttons for outline interaction
        if st.button("Regenerate Outline"):
            st.session_state['outline'] = generate_text(prompt, max_tokens=500).split('\n')
        
        updated_outline = []
        for idx, item in enumerate(st.session_state['outline']):
            new_item = st.text_input(f"Item {idx+1}", value=item)
            updated_outline.append(new_item)
        st.session_state['outline'] = updated_outline

        if st.button("Finalize Outline and Generate Book"):
            book_prompt = "Based on the following outline, generate a book:\n\n" + "\n".join(st.session_state['outline'])
            book = generate_text(book_prompt, max_tokens=2048)
            st.write(book)

if __name__ == "__main__":
    app()
    
