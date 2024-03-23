import os
import json
import traceback
import Streamlitapp as st
import PyPDF2
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from langchain_openai import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
from langchain_community.callbacks import get_openai_callback

#loading json file
with open('C:\Users\sauga\AIPrj\mcqgen\Response.json','r') as file:
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
    subject=st.text_input("complex Level of questions",max_chars=20, place_holder="Simple")
    #add button
    button=st.form_submit_button("Create MCQs")



