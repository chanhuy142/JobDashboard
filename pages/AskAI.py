import streamlit as st

import google.generativeai as genai

isFile=False
#print(st.secrets["api_key"])
genai.configure(api_key=st.secrets["api_key"])

model = genai.GenerativeModel('gemini-1.5-flash')



    
#sample_file=genai.upload_file(path="./data/cleaned_dataset.csv",name="huybhhu")
#file = genai.get_file(name="myjobdata1420032")
file=genai.get_file(name="huybhhu")

#sample_file=genai.upload_file(path="data.txt")
#file = genai.get_file(name="myjobdata1420032")

#sample_file=genai.upload_file(path="a.jpg",name="myimagedata1420032")
#file = genai.get_file(name="myimagedata1420032")

#generate session state if not exist
if 'chat-history' not in st.session_state:
    st.session_state['chat-history'] = []

messages = []

#generate old messages from session state
for speaker, message in st.session_state['chat-history']:
    if speaker == "You":
        messages.append({'role':'user',
                 'parts':[message]})
    else:
        messages.append({'role':'model',
                 'parts':[message]})



def get_response(input_message):
    global messages
    if isFile:
        messages.append({'role':'user',
                    'parts':[file ,input_message]})
    else:
        messages.append({'role':'user',
                    'parts':[input_message]})
    
    response = response = model.generate_content(messages)
   
    
    return response

if 'chat-history' not in st.session_state:
    st.session_state['chat-history'] = []

input=st.text_input('Input:', key='input')
submit=st.button('Submit')

#check box to use file or not
isFile=st.checkbox('Use File', key='isFile')


if submit and input:
    
    response = get_response(input)
    st.session_state['chat-history'].append(("You", input))
    st.session_state['chat-history'].append(("AI", response.text))
st.subheader("Chat history:")
for speaker, message in st.session_state['chat-history']:
    st.write(f"{speaker}: {message}")


