import streamlit as st
import requests
import base64
import urllib.parse

st.set_page_config(page_title="Simple Social Media Web App", layout="wide")

if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
    
    
def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def login_page():
    st.title("Welcome to Simple Social Media Web App")
    
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")
    
    if email and password:
        col1 , col2 = st.columns(2)
        
        
        with col1:
            if st.button("Login", type ="primary", use_container_width=True):
                
                login_data = {"username":email, "password":password}
                response = requests.post("http://localhost:8001/authjwt/login", data=login_data)
                
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data["access_token"]
                    
                    #Get User Info
                    user_response = requests.get("http://localhost:8001/users/me", headers=get_headers())
                    if user_response.status_code == 200:
                        st.session_state.user = user_response.json()
                        st.rerun()
                    else:
                        st.error("Failed to fetch user info.")
                else:
                    st.error("Login failed. Please check your credentials.")
        with col2:
            if st.button("Sign Up", type="secondary", use_container_width=True):
                signup_data = {"email":email, "password":password}
                response = requests.post("http://localhost:8001/authjwt/register", json=signup_data)
                
                if response.status_code == 201:
                    st.success("Registration successful! Please log in.")
                else:
                    st.error("Registration failed. Please try again.")
                    st.error(f"Registration Failed: {response.text}")
                    
    else:
        st.info("Please enter both email and password.")
        
        
def upload_page():
    st.title("Upload a New Post")
    
    uploaded_file = st.file_uploader("choose media", type =['png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'mkv', 'webm'])
    caption = st.text_area("Caption:", placeholder = "Write a caption for your post...")
    
    if uploaded_file and st.button("Share", type= "primary"):
        with st.spinner("Uploading..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"caption": caption}
            response = requests.post("http://localhost:8001/upload", headers=get_headers(), files=files, data=data)
            
            if response.status_code == 200:
                st.success("Post uploaded successfully!")
            else:
                st.error("Failed to upload post.")
                st.error(f"Upload Failed: {response.text}")
                
                
                
def encode_text_for_overlay(text):
    if not text:
        return ""
    base64_bytes = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    return urllib.parse.quote(base64_bytes)



def create_transformed_url(original_url,transformation_paras, caption =None):
    if caption:
        encoded_caption =  encode_text_for_overlay(caption)
        text_overlay = f"l_text:Arial_40_bold:{encoded_caption},co_rgb:FFFFFF,g_south,y_30/"
        transformation_paras= text_overlay
        
        
        if not transformation_paras:
            
            return original_url
        
        parts = original_url.split("/")
        
        imagekit_id = parts[3]
        file_path= "/".join(parts[4:])
        base_url = "/".join(parts[:4])
        return f"{base_url}/tr:{transformation_paras}/{file_path}"
    
    
def feed_page():
    st.title("Feed")
    
    response =  requests.get("http://localhost:8001/feed", headers=get_headers())
    if response.status_code == 200:
        posts = response.json()["posts"]
        
        
        if not posts:
            st.info("No posts available. Upload a post to get started!")
            return
        
        for post in posts:
            st.markdown("---")
            
            
            
            # Header with user, date, and delete button (if owner)
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{post['email']}** • {post['created_at'][:10]}")
            with col2:
                if post.get('isowner', False):
                    if st.button("🗑️", key=f"delete_{post['id']}", help="Delete post"):
                        # Delete the post
                        response = requests.delete(f"http://localhost:8001/posts/{post['id']}", headers=get_headers())
                        if response.status_code == 200:
                            st.success("Post deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete post!")
                            
                            
            caption = post.get("caption", "")
            if post['file_type'] == "image":
                transformed_url = create_transformed_url(post['url'], "c_scale,w_600", caption)
                st.image(transformed_url, use_column_width=True)
                
                
            else:
                uniform_video_url = create_transformed_url(post['url'], "c_scale,w_600")
                st.video(uniform_video_url, width=300)
                st.caption(caption)
                
            st.markdown("")
                            
    else:
        st.error("Failed to fetch feed.")
        
        
if st.session_state.user is None:
    login_page()
else:
    st.sidebar.title(f"Hello, {st.session_state.user['email']}!")
    
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()
        
        
    st.sidebar.markdown("---")
    page = st.sidebar.selectbox("Select Page", ["Feed", "Upload"])
    
    if page == "Feed":
        feed_page()
        
    elif page == "Upload":
        upload_page()
            
        
                        
