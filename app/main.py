import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# ✅ Set Streamlit page config at the very beginning
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # Collect user info from the sidebar
    st.sidebar.header("👤 Your Info")
    user_name = st.sidebar.text_input("Your Name", value="Mohan")
    company_name = st.sidebar.text_input("Your Company", value="AtliQ")
    user_role = st.sidebar.text_input("Your Role", value="Business Development Executive")
    user_experience = st.sidebar.text_input("Your Experience", value="5 years in AI & Software Consulting")

    # URL input in main area
    url_input = st.text_input("Enter a URL:", value="https://careers.nike.com/director-software-engineering-itc/job/R-49416")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            user_info = {
                "name": user_name,
                "company": company_name,
                "role": user_role,
                "experience": user_experience
            }

            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links, user_info)
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
