
import streamlit as st
import pandas as pd
import base64
from gpt4free import you
import os
import sys
import numpy as np
import plotly.figure_factory as ff
import re
import json
import pyperclip
import streamlit as st
import base64


if "Graphical_Results" not in st.session_state:
    st.session_state.num_questions = 0

for k, v in st.session_state.items():
    st.session_state[k] = v

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
   


def displayRecommendations(data_dict):
    # Display description
    st.subheader("Some Recommendations for your uploaded data")
    st.subheader('Description')
    st.write(data_dict["description"])

    # Display analytical questions
    st.subheader('Analytical Questions')
    for i, question in enumerate(data_dict["analyticalQuestions"]):
        st.write(f'Question {i+1}:')
        st.code(f"{question}", language='python')

    # Display graphical questions
    st.subheader('Graphical Questions')
    for i, question in enumerate(data_dict["graphicalQuestions"]):
        st.write(f'Question {i+1}:')
        st.code(f"{question}", language='python')

def get_answer(question: str) -> str:
    # Set cloudflare clearance cookie and get answer from GPT-4 model
    try:
        result = you.Completion.create(prompt=question)

        return result.text

    except Exception as e:
        # Return error message if an exception occurs
        return (
            f'An error occurred: {e}. Please make sure you are using a valid cloudflare clearance token and user agent.'
        )


def getSuggestedQuestions(dataFrame):
    sampleFrame = dataFrame.head()

    prompt = f'''
    You have been provided with a CSV file containing data. 
    Please analyze the sample data of the first 5 rows to give the description and 
    generate 5 analytical questions and 5 graphical questions based on the dataset,
    in a dictionary format of 3 keys, description, analyticalQuestions, graphicalQuestions give it 
    just string json format
    {sampleFrame}
    '''

    answer = get_answer(prompt)
    escaped = answer.encode('utf-8').decode('unicode-escape')
    data_dict = json.loads(escaped)
    displayRecommendations(data_dict)








def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():


    project_name = "DataSense"
    tagline = "Empowering Data Analysis for Everyone"
    side_bg = 'mainPage.gif'
    sidebar_bg(side_bg)
    

    # Display project name with custom styling
    st.title(project_name)
    st.markdown('<style>h1{color: #1919FF;}</style>', unsafe_allow_html=True)
    

    # Display tagline with custom styling
    st.subheader(tagline)


    # st.markdown('<p class="my-tagline">' + tagline + '</p>', unsafe_allow_html=True)
    st.markdown('<style>h1{color: #FF5E5E;}</style>', unsafe_allow_html=True)
    st.sidebar.title('Developer\'s Contact')
    st.sidebar.markdown('[![Chethan-Reddy]'
                    '(https://img.shields.io/badge/Author-Chethan%20Reddy-brightred)]'
                    '(https://www.linkedin.com/in/chethan-reddy-0201791ba/)') 
    
    

    st.sidebar.success("\n\n\nSpecial Thanks for GPT4 repo by OpenAI")


    # Upload file
    uploaded_file = st.file_uploader('Upload CSV or Excel file', type=['csv', 'xlsx'])
    st.caption("Please do re-load the page if there is any error!")

    if uploaded_file == None:
        file_ = open("mainPage.avif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown('''


            **Tagline:** :red[Unlock Insights with Simple Questions]

            **DataSense is an **:red[intuitive and user-friendly data 
            analysis tool]** designed for individuals with varying 
            levels of data literacy. With DataSense, users can 
            effortlessly **:red[upload their data in CSV or Excel format]** 
            and obtain valuable **:red[analytical and graphical]** results 
            by asking questions in plain English. The tool empowers 
            users to explore their data and gain insights **:red[without the 
            need for specialized technical skills or complex coding]**.**
        ''')

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
        )

        st.write("\n")

        st.markdown('''


            **Tagline: :blue[Unlock Insights with Simple Questions]**

            
            **DataSense is an **:red[intuitive and user-friendly data 
            analysis tool]** designed for individuals with varying 
            levels of data literacy. With DataSense, users can 
            effortlessly **:red[upload their data in CSV or Excel format]** 
            and obtain valuable **:red[analytical and graphical]** results 
            by asking questions in plain English. The tool empowers 
            users to explore their data and gain insights **:red[without the 
            need for specialized technical skills or complex coding]**.

            DataSense combines the **:red[power of Generative AI, Natural Language Processing and 
            Data Visualization]** to make data analysis accessible to everyone. 
            Users can ask general questions about their uploaded data, such as 
            **:red[average values, correlations, distributions, and trends, and DataSense 
            will provide instant analytical responses and generate visual representations]**, 
            enabling users to easily comprehend and communicate their findings.

            Whether you're a novice or an experienced data enthusiast, 
            DataSense simplifies the process of **:red[extracting meaningful information 
            from data]**, making it a versatile tool for individuals, businesses, 
            and organizations across various domains. Unleash the potential 
            of your data with **:red[DataSense and make data-driven decisions with confidence]**.**''')


    if uploaded_file is not None:
        try:
            # Read data from the uploaded file
            data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            data.to_csv('data.csv')

            # Display the data
            st.subheader('Data Preview')
            st.dataframe(data)
         

            with st.spinner('Wait for recommendation questions...'):
               getSuggestedQuestions(data)
            st.success('Basic Recommendations and description is generated!')

             # Get user input for query
            query = st.text_input('Enter your question', '')
            click = st.button('Query')
            st.caption("Note: if the query is not getting processes try again")



            

            if click:
                if query:
                    # Execute the query on the data:
                    try:
                        prompt = f'''Act like an expert Data Scientist,  Data Engineer and Data Analyst. 

                        User Query:  {query} , give a simple code with streamlit and plotly.
                        Sample Data Frame:  :

                        {data.head(5)}

                        Now we need to structure the prompt using the above question with the following pointers:
                        1. Write the streamlit Python code where the code should cater to all the answers of the "User Query" and the streamlit app design should be really good with all relevant subtitles and other elements in it. 
                        2. Maximum try to use the Plotly module in Python.
                        3. The CSV file name is always data.csv .
                        4. Don't give incomplete code at any case.
                        5. The code should not contain any kind of errors, try to handle all the errors.
                        6. Give the complete code at once.
                        7. Keep the code as short as possible.
                        8. For any query max try to use Plotly, NumPy, Keras, Pandas, PyTorch, SciPy, Scikit-Learn, TensorFlow, Matplotlib, Seaborn 
                        '''
                        answer = get_answer(prompt)
                        escaped = answer.encode('utf-8').decode('unicode-escape')
                        print(escaped)
                        if 'python' in escaped:
                            pattern = r'```python(.+?)```'
                        else:
                            pattern = r'```(.+?)```'
                        matches = re.findall(pattern, escaped, re.DOTALL)
                        f = open("pages/Graphical_Results.py", "w")
                        f.write(matches[0])
                        f.close()
                        st.success("Results Generated Successfully please do navigate to Graphical Results Page!")
                    except Exception as e:
                        st.warning("Couldn't process your Query Try again")
                else:
                    st.warning('Please enter a query.')
        except Exception as e:
            st.error(f'Error: {str(e)}')

if __name__ == '__main__':
    main()
    