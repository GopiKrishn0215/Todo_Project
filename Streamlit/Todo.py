import streamlit as st
import requests
from streamlit_option_menu import option_menu


st.set_page_config(layout="wide")

local_host = 'http://192.168.70.4:8002/'

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

def get_user_id():
    url = local_host + 'getid/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        response = data['response']
        return response



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
    col1,col2 = st.columns([8,2])
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
            
            a,c,b = st.columns([3,0.5,6.5])
            with a:
                # #with st.form(key="form",clear_on_submit=True):
                url = local_host + "save/"
                # # headers = {'Authorization': f'Bearer {token}'}      
                # response = requests.get(url)
                # # st.write(response)
                # # saved_data = None
                # if response.status_code == 200: 
                #     # st.write(response.status_code)
                #     data = response.json()
                #     saved_data = data['saved_data']
                #     st.write(saved_data)
                #     if saved_data == None:
                #         saved_data=""
                
                saved_data = ""
                if 'task_back' in st.session_state:
                    saved_data = st.session_state['task_back']
                task = st.text_input("Tasks",key='task',help="add your task here",value=saved_data)
                if 'task' not in  st.session_state:
                    st.write("add session ")
                    st.session_state['task'] = task
                
                add = st.button("ADD")
                    
                if task:
                    url = local_host + "save/"
                    # headers = {'Authorization': f'Bearer {token}'}      
                    response = requests.post(url,params={"user_input":task})
                    if response.status_code == 200: 
                        data = response.json()
                        aa = data['input']
                        # st.write(aa)
                    
                    if add:
                        url = local_host + "todo/?type=create"
                        headers = {'Authorization': f'Bearer {token}'}
                        params={
                            "userName":UserName,
                            "task":task,
                            "discription":"",
                            "status":"Pending",
                        }        
                        response = requests.post(url,headers=headers,params=params)
                        if response.status_code == 200: 
                            st.success("added successfully")
                            del st.session_state['task']
                            del st.session_state['task_back']
                            st.experimental_rerun()
                            
                        else:
                            st.error("You dont have permission to create the task")
            with b:
                         
                params={
                            "userName":UserName,
                        }     
                
                url = local_host + "todo/?type=read"
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(url,headers=headers,params=params)
                if response.status_code == 200:
                    data = response.json()
                    task = data['task']
                    if len(task)>0:
                        st.subheader("Pending Tasks:")     
                    count = 0
                    for i in range(len(task)):
                        tasks = st.checkbox(task[i],key=task[i])                        
                        if tasks:
                            count +=1
                            if count == 1:
                                with st.container():
                                    # with st.form(key=f"forms{i}",clear_on_submit=True):
                                    description = st.text_area("Description")
                                    file=st.file_uploader("please choose a file",help="Attach only csv files and documents")
                                    # st.write(description)
                                    submit = st.button("submit")
                                    if submit :
                                        if description == "" and file != None:
                                            st.error("Please fill description")
                                        elif file == None and description!="":
                                            st.error("PLease upload file")
                                        elif description and file:
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
                                            
                                            response = requests.post(url,headers=headers,params=params,files=files)
                                            if response.status_code == 200:
                                                st.success("Submited successfully")
                                                st.experimental_rerun()
                                            else:
                                                st.error("ERROR")
                                        else:
                                            st.error("Fill all fields")
                                                     
                                break      
                else:
                    st.error(f'Error: {response.status_code}')
                    
        if selected == "History":
            todo_task = st.session_state['task']
            st.session_state['task_back'] = todo_task
            params={
                    "userName":UserName,
                    "status":"Completed"
                }     
            
            url = local_host + "todo/?type=history"
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url,headers=headers,params=params)
            a,b = st.columns([6,4])    
            if response.status_code == 200:
                data = response.json()
                tasks = data['tasks']
                files = data['files']
                description = data['description']
                
                with a:
                    count1=0
                    for i in range(len(tasks)):
                        if count1==0:
                            st.header("Completed Tasks")
                        details = st.button(f'{i+1}.{tasks[i]}')
                        count1+=1
                        # Apply CSS styles to hide the button structure
                        button_style = """
                            <style>
                            .stButton>button {
                                background: none;
                                border: none;
                                padding: 0;
                                margin: 0;
                                font-size: inherit;
                                font-family: inherit;
                                cursor: pointer;
                                outline: inherit;
                            }
                            </style>
                        """

                        st.markdown(button_style, unsafe_allow_html=True)
                        
                        if details:
                            with b:
                                st.subheader("Description:")
                                st.write(description[i])                        
                            st.write(files[i])      
            else:
                st.error("Failed to fetch data from the backend")

                       
    with col2:
        a,b = st.columns([4,6])
        with b:
            image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1bXeus9y2Wsba6hsXUYIToDMEMM5Dx19wDxLDjB7Puw&s"
            st.image(image, caption=UserName, width=180)
        




