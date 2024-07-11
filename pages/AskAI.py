import streamlit as st

import google.generativeai as genai

isFile=False
#print(st.secrets["api_key"])
genai.configure(api_key=st.secrets["api_key"])

model = genai.GenerativeModel('gemini-1.5-flash')



    
#sample_file=genai.upload_file(path="./data/data.txt",name="huybhhus")
#file = genai.get_file(name="myjobdata1420032")
file=genai.get_file(name="huybhhus")

#sample_file=genai.upload_file(path="data.txt")
#file = genai.get_file(name="myjobdata1420032")

#sample_file=genai.upload_file(path="a.jpg",name="myimagedata1420032")
#file = genai.get_file(name="myimagedata1420032")

#generate session state if not exist

#image1=genai.upload_file(path="./data/db1.png",name="myimagedata14200321")
#image2=genai.upload_file(path="./data/db21.png",name="myimagedata14200322")
#image22=genai.upload_file(path="./data/db22.png",name="myimagedata14200323")
#image3=genai.upload_file(path="./data/db31.png",name="myimagedata14200324")
#image33=genai.upload_file(path="./data/db32.png",name="myimagedata14200325")

fileimage1=genai.get_file(name="myimagedata14200321")
fileimage2=genai.get_file(name="myimagedata14200322")
fileimage22=genai.get_file(name="myimagedata14200323")
fileimage3=genai.get_file(name="myimagedata14200324")
fileimage33=genai.get_file(name="myimagedata14200325")




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
    elif isImage:
        messages.append({'role':'user',
                    'parts':[fileimage1,fileimage2,fileimage22,fileimage3,fileimage33 ,input_message]})
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
isImage=st.checkbox('Use Image', key='isImage')


if submit and input:
    
    response = get_response(input)
    st.session_state['chat-history'].append(("You", input))
    st.session_state['chat-history'].append(("AI", response.text))
st.subheader("Chat history:")
for speaker, message in st.session_state['chat-history']:
    #st.write(f"{speaker}: {message}")
    #if speaker==AI, then display the message in a card in the left
    if speaker == "AI":
        st.markdown(f'<div style="background-color:#3191F6; padding:10px; border-radius:10px; margin:10px; width:50%;">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="background-color:#444546; padding:10px; border-radius:10px; margin:10px; width:50%; float:right;">{message}</div>', unsafe_allow_html=True)
    


