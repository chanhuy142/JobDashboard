import streamlit as st

import google.generativeai as genai

isFile=False
genai.configure(api_key="AIzaSyBbne8vLPP05PJsyoacNVMUe67KP3OSrGE")

model = genai.GenerativeModel('gemini-1.5-flash')



    
#sample_file=genai.upload_file(path="data.txt",name="mybobodata142")

file = genai.get_file(name="mybobodata142")



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
    try:
        response = response = model.generate_content(messages)
    except Exception as e:
        response = str(e)
    
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


