import streamlit as st
import openai
import os
from fpdf import FPDF

# OpenAI API key setup
openai.api_key = st.secrets["secrets"]["OPENAI_API_KEY"]

def generate_text(prompt, max_tokens=1000):
    try:
        response = openai.ChatCompletion.create(
          model="gpt-4",  # Adjust according to the available models
          messages=[{"role": "system", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"An error occurred while generating the script: {e}")
        return ""


def main():
    """Main app function."""
    st.title("E-Book Creator")

    with st.form("book_input_form"):
        title = st.text_input("Title")
        genre = st.selectbox("Genre", ['Fiction', 'None Fiction'])
        age = st.number_input("Target Age", min_value=18, value=18)
        language = st.text_input("Language", value="English")
        sex = st.selectbox("Sex", ['Male', 'Female', 'Other'])
        interests = st.text_area("Interests", value='Write a short description of the use case/purpose for your eBook.')
        submit_button = st.form_submit_button("Generate Outline")

    if submit_button:
        prompt = f"Create a book outline for a {genre} book titled '{title}', aimed at {age}-year-olds, in {language}. The main character is {sex} with interests in {interests}."
        outline = generate_text(prompt)
        st.session_state['outline'] = outline.split('\n')
        st.write("Generated Outline:")
        for idx, item in enumerate(st.session_state['outline']):
            st.text(f"{idx+1}. {item}")

      
   # Place this part inside your main function to check if the button is being clicked
    if st.button("Finalize Outline and Generate Chapter Excerpt"):
        if 'outline' in st.session_state:
            book_prompt = "Based on the following outline, generate a book:\n\n" + "\n".join(st.session_state['outline'])
            book = generate_text(book_prompt, max_tokens=2048)
            st.write(book)
    else:
        st.write("No outline available to generate book.")

    def generate_book_content(outline):
        chapters_content = {}
        for idx, chapter_title in enumerate(outline, start=1):
            chapter_prompt = f"Write a detailed chapter about {chapter_title}, consisting of approximately 1000 words."
            chapter_content = generate_text(chapter_prompt, max_tokens=2000)  # Adjust max_tokens as needed
            chapters_content[f"Chapter {idx}: {chapter_title}"] = chapter_content
        return chapters_content

    def create_and_download_pdf(chapters_content):
        pdf = PDF()
        pdf.add_page()
        for chapter_title, chapter_content in chapters_content.items():
            pdf.chapter_title(chapter_title)
            pdf.chapter_body(chapter_content)
        
        pdf_file = pdf.output(dest='S').encode('latin1')
        
        st.download_button(
            label="Download eBook as PDF",
            data=pdf_file,
            file_name="Generated_Book.pdf",
            mime="application/pdf"
        )

    if st.button("Generate Complete Book"):
        chapters_content = generate_book_content(st.session_state['outline'])
        create_and_download_pdf(chapters_content)


if __name__ == "__main__":
    main()
    
