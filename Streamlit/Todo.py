import streamlit as st
import requests
import datetime
from datetime import datetime
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_modal import Modal


st.set_page_config(layout="wide",initial_sidebar_state="expanded",)

local_host = 'http://localhost:8000/'

session_state = st.session_state

def get_jwt_token(username, password):
    
    url = local_host + 'api/token/'
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access']
        return access_token
    else:
        return None
    

def get_data(token):
    url = local_host + 'data/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return token
    else:
        return None

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    
    st.markdown("<h1 style='text-align: center; '>LOGIN</h1> <br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 ,col3= st.columns(3)
        with col2:
            login_button = st.button("Login")

    if login_button:
        token = get_jwt_token(username, password)
        
        if token:
            data = get_data(token)
            
            if data:
                st.session_state['logged_in'] = True
                st.session_state['token'] = token
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                 st.write("You do not have permission to access the next page")

        else:
            st.error("Invalid username or password.")
            
    

if 'logged_in' in st.session_state and st.session_state['logged_in']:

    token = st.session_state['token']  
    UserName = st.session_state['username']
    col1,col2 = st.columns(2)
    with col1:
        selected = option_menu(
            menu_title="",
            options=["Todo","History",],
            icons=["card-checklist","journal-text"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )
    
            
        if selected == "Todo":
            with st.sidebar:
                # with st.form(key="form",clear_on_submit=True):
                if 'session_state' not in st.session_state:
                    st.session_state['session_state'] = {'task': ''}
                task = st.text_input("Tasks",key='task',value=st.session_state['session_state']['task'])
                
                if 'session_state' in st.session_state:
                        st.session_state['session_state'] = {'task': task}
                else:
                    st.session_state['session_state'] = {'task': ''}
                    
                add = st.button("ADD")    
                
            boolean = True
            
            if task:
                if add:
                    st.session_state['session_state'] = {'task': ''}
                    url = local_host + "todo/?type=create"
                    headers = {'Authorization': f'Bearer {token}'}
                    params={
                        "userName":UserName,
                        "task":task,
                        "discription":"",
                        "status":"Pending",
                    }        
                    response = requests.get(url,headers=headers,params=params)
                    if response.status_code == 200: 
                        pass
                    else:
                        st.error("You dont have permission to create the task")
                    
            params={
                        "userName":UserName,
                    }     
            
            url = local_host + "todo/?type=read"
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url,headers=headers,params=params)
            if response.status_code == 200:
                data = response.json()
                task = data['task']
                
                for i in range(len(task)):
                    tasks = st.checkbox(task[i],key=task[i])
                    modal = Modal(key="key",title="update")
                    if tasks:
                        # st.set_page_config(initial_sidebar_state="collapsed")
                        with modal.container():
                            with st.form(key="forms",clear_on_submit=True):
                                description = st.text_area("Description")
                                file=st.file_uploader("please choose a file")
                                submit = st.form_submit_button("submit")
                                if description:
                                    if submit :
                                        url = local_host + "todo/?type=uploadfile"
                                        headers = {'Authorization': f'Bearer {token}'}
                                        params = {
                                            "userName":UserName,
                                            "description":description,
                                            "status":"Completed",
                                            "task":task[i],
                                        }
                                        files = {
                                            'file': file
                                        }
                                        st.success("Submited successfully")
                                        response = requests.post(url,headers=headers,params=params,files=files)
                                        if response.status_code == 200:
                                            st.success("WOW")
                                        else:
                                            st.error("ERROR")
        
            
            else:
                st.error(f'Error: {response.status_code}')
                
            
                
        if selected == "History":
            params={
                    "userName":UserName,
                }     
            
            url = local_host + "todo/?type=history"
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url,headers=headers,params=params)
            
            if response.status_code == 200:
                data = response.json()
                task = data['task']
                for i in range(len(task)):
                    st.subheader(task[i])
            else:
                st.error(f'Error: {response.status_code}')
            
            
    with col2:
        col1,col2 = st.columns(2)
        with col2:
            image = "/home/gopikrishna/Todo/Todo_Env/Todo_Project/images/profile_photo.jpg"
            st.image(image, caption=UserName, width=180)
        
        