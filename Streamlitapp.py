import os
import json
import traceback
import streamlit as st
import PyPDF2
import pandas as pd
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from langchain_openai import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
from langchain_community.callbacks import get_openai_callback

#loading json file
with open('C:\\Users\\sauga\\AIPrj\\mcqgen\\Response.json','r') as file:
    RESPONSE_JSON = json.load(file)
#create a title for the app
st.title("MCQs creater application with langchain")
#create a form
with st.form("user inputs"):
    #file upload
    uploaded_file=st.file_uploader("upload a pdf or text file")

    #input Fields
    mcq_count=st.number_input("no of MCQs",min_value=3,max_value=50)

    #subject
    subject=st.text_input("Insert Subject",max_chars=20)
    #tone
    tone=st.text_input("complex Level of questions",max_chars=20, placeholder="Simple")
    #add button
    button=st.form_submit_button("Create MCQs")
    
    print(f"button: {button}" )
    print(f"uploaded_file: {uploaded_file}" )
    print(f"subject: {subject}" )
    print(f"tone: {tone}" )
    print(f"mcq count: {mcq_count}" )
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading...."):
            print("I am here")
            try:
                text=read_file(uploaded_file)
                #count token and cost of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json":json.dumps(RESPONSE_JSON)
                        }
                    )
                    #st.write(response)
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt tokens:{cb.prompt_tokens}")
                print(f"Completion tokens:{cb.completion_tokens}")
                print(f"total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    #extract the quiz data from the respponses
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in a text box as well
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)




