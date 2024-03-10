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

       class PDF(FPDF):
            def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(10)

            def chapter_body(self, body):
                self.set_font('Arial', '', 12)
                self.multi_cell(0, 10, body)
                self.ln()

    def create_pdf(chapters):
        pdf = PDF()
        pdf.add_page()
        for title, body in chapters.items():
            pdf.chapter_title(title)
            pdf.chapter_body(body)
        return pdf.output(dest='S').encode('latin1')
 
if __name__ == "__main__":
    main()
    
