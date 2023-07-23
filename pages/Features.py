import streamlit as st
import base64
import streamlit as st


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def describeDataSense():
    st.title("DataSense: Unlock Insights with Simple Questions")
    st.subheader("Project Name: DataSense")
    st.subheader("Tagline: Unlock Insights with Simple Questions")

    st.write("""
        DataSense is an intuitive and user-friendly data analysis tool designed for individuals with varying levels of data literacy. With DataSense, users can effortlessly upload their data in CSV or Excel format and obtain valuable analytical and graphical results by asking questions in plain English. The tool empowers users to explore their data and gain insights without the need for specialized technical skills or complex coding.
    """)

    st.write("""
        DataSense combines the power of natural language processing and data visualization to make data analysis accessible to everyone. Users can ask general questions about their uploaded data, such as average values, correlations, distributions, and trends, and DataSense will provide instant analytical responses and generate visual representations, enabling users to easily comprehend and communicate their findings.
    """)

    st.write("""
        Whether you're a novice or an experienced data enthusiast, DataSense simplifies the process of extracting meaningful information from data, making it a versatile tool for individuals, businesses, and organizations across various domains. Unleash the potential of your data with DataSense and make data-driven decisions with confidence.
    """)

# Run the DataSense description app
describeDataSense()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('featureImage.gif')