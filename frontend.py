import streamlit as st
import requests
import base64
import urllib.parse

# Page config with custom theme
st.set_page_config(
    page_title="SocialVibe - Share Your Moments", 
    layout="wide",
    page_icon="📸"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Post card styling */
    .post-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #eee;
        transition: transform 0.2s ease;
    }
    
    .post-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .post-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        margin-right: 12px;
    }
    
    .user-info {
        flex: 1;
    }
    
    .username {
        font-weight: 600;
        color: #333;
        font-size: 1rem;
    }
    
    .post-date {
        color: #888;
        font-size: 0.85rem;
    }
    
    .caption {
        color: #444;
        font-size: 1rem;
        margin-top: 1rem;
        line-height: 1.5;
    }
    
    /* Login card */
    .login-card {
        max-width: 450px;
        margin: 3rem auto;
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    /* Upload section */
    .upload-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError {
        border-radius: 10px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* Progress indicator */
    .upload-progress {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem 2rem;
        color: white;
        text-align: center;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        color: #888;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'upload_status' not in st.session_state:
    st.session_state.upload_status = None

def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def get_initials(email):
    """Get initials from email for avatar"""
    return email[0].upper() if email else "U"

def login_page():
    # Centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-size: 3rem; margin-bottom: 0.5rem;">📸 SocialVibe</h1>
            <p style="color: #666; font-size: 1.1rem;">Share your moments with the world</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        email = st.text_input("📧 Email", placeholder="Enter your email...")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if email and password:
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🚀 Login", type="primary", use_container_width=True):
                    with st.spinner("Logging in..."):
                        login_data = {"username": email, "password": password}
                        response = requests.post("http://localhost:8001/authjwt/login", data=login_data)
                        
                        if response.status_code == 200:
                            token_data = response.json()
                            st.session_state.token = token_data["access_token"]
                            
                            user_response = requests.get("http://localhost:8001/users/me", headers=get_headers())
                            if user_response.status_code == 200:
                                st.session_state.user = user_response.json()
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Failed to fetch user info.")
                        else:
                            st.error("❌ Login failed. Please check your credentials.")
            
            with col_btn2:
                if st.button("✨ Sign Up", type="secondary", use_container_width=True):
                    with st.spinner("Creating account..."):
                        signup_data = {"email": email, "password": password}
                        response = requests.post("http://localhost:8001/authjwt/register", json=signup_data)
                        
                        if response.status_code == 201:
                            st.success("🎉 Registration successful! Please log in.")
                        else:
                            error_detail = response.json().get('detail', 'Unknown error')
                            if 'ALREADY_EXISTS' in str(error_detail):
                                st.warning("⚠️ This email is already registered. Try logging in!")
                            else:
                                st.error(f"❌ Registration failed: {error_detail}")
        else:
            st.info("👆 Please enter both email and password to continue.")

def upload_page():
    st.markdown("""
    <div class="main-header">
        <h1>📤 Create New Post</h1>
        <p>Share your photos and videos with the community</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📷 Choose your media",
            type=['png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'mkv', 'webm'],
            help="Supported formats: PNG, JPG, JPEG, GIF, MP4, AVI, MOV, MKV, WEBM"
        )
        
        caption = st.text_area(
            "✍️ Caption",
            placeholder="Write something about your post...",
            height=120
        )
        
        if uploaded_file:
            st.markdown("---")
            st.markdown("### 👁️ Preview")
            
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, width=400)
            else:
                st.video(uploaded_file)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Share Post", type="primary", use_container_width=True):
                # Show progress
                progress_bar = st.progress(0, text="Preparing upload...")
                status_text = st.empty()
                
                try:
                    progress_bar.progress(20, text="Reading file...")
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"caption": caption}
                    
                    progress_bar.progress(40, text="Uploading to server...")
                    status_text.markdown("⏳ *Uploading your media... This may take a moment for larger files.*")
                    
                    response = requests.post(
                        "http://localhost:8001/upload",
                        headers=get_headers(),
                        files=files,
                        data=data,
                        timeout=120  # 2 minute timeout for large files
                    )
                    
                    progress_bar.progress(80, text="Processing...")
                    
                    if response.status_code == 200:
                        progress_bar.progress(100, text="Complete!")
                        status_text.empty()
                        st.success("🎉 Post uploaded successfully!")
                        st.balloons()
                        
                        # Brief delay then redirect to feed
                        import time
                        time.sleep(1)
                        st.session_state.page = "Feed"
                        st.rerun()
                    else:
                        progress_bar.empty()
                        status_text.empty()
                        st.error(f"❌ Upload failed: {response.text}")
                        
                except requests.exceptions.Timeout:
                    progress_bar.empty()
                    status_text.empty()
                    st.error("⏰ Upload timed out. Please try with a smaller file or check your connection.")
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("""
        ### 💡 Tips
        
        - **Images**: Best results with PNG or JPEG
        - **Videos**: MP4 format recommended
        - **Size**: Keep files under 50MB for faster uploads
        - **Captions**: Add context to engage viewers!
        """)

def feed_page():
    st.markdown("""
    <div class="main-header">
        <h1>🏠 Your Feed</h1>
        <p>See what's happening in your community</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Loading feed..."):
        response = requests.get("http://localhost:8001/feed", headers=get_headers())
    
    if response.status_code == 200:
        posts = response.json()["posts"]
        
        if not posts:
            st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <h2>📭 No posts yet!</h2>
                <p style="color: #666;">Be the first to share something amazing.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📤 Create Your First Post", type="primary"):
                st.session_state.page = "Upload"
                st.rerun()
            return
        
        # Display posts in a nice grid
        for post in posts:
            with st.container():
                # Post card
                col1, col2 = st.columns([6, 1])
                
                with col1:
                    # User info with avatar
                    email = post.get('email', 'Unknown')
                    initial = get_initials(email)
                    date = post['created_at'][:10] if post.get('created_at') else ''
                    
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; 
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    display: flex; align-items: center; justify-content: center;
                                    color: white; font-weight: bold; margin-right: 10px;">
                            {initial}
                        </div>
                        <div>
                            <div style="font-weight: 600; color: #333;">{email}</div>
                            <div style="color: #888; font-size: 0.85rem;">📅 {date}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if post.get('isowner', False):
                        if st.button("🗑️", key=f"delete_{post['id']}", help="Delete this post"):
                            with st.spinner("Deleting..."):
                                del_response = requests.delete(
                                    f"http://localhost:8001/posts/{post['id']}",
                                    headers=get_headers()
                                )
                                if del_response.status_code == 200:
                                    st.success("Post deleted!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete post.")
                
                # Media display - FIXED: using width instead of deprecated use_column_width
                if post['file_type'] == "image":
                    st.image(post['url'], width=600)
                else:
                    st.video(post['url'])
                
                # Caption
                caption = post.get("caption", "")
                if caption:
                    st.markdown(f"""
                    <div style="padding: 0.5rem 0; color: #444; font-size: 1rem;">
                        💬 {caption}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
    else:
        st.error("❌ Failed to load feed. Please try again.")

# Main app logic
if st.session_state.user is None:
    login_page()
else:
    # Sidebar with user info
    with st.sidebar:
        user_email = st.session_state.user.get('email', 'User')
        initial = get_initials(user_email)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <div style="width: 80px; height: 80px; border-radius: 50%; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        display: flex; align-items: center; justify-content: center;
                        color: white; font-weight: bold; font-size: 2rem;
                        margin: 0 auto 1rem auto;">
                {initial}
            </div>
            <h3 style="margin: 0; color: #333;">Welcome!</h3>
            <p style="color: #666; font-size: 0.9rem; word-break: break-all;">{user_email}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "📍 Navigate",
            ["🏠 Feed", "📤 Upload"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    # Page routing
    if "Feed" in page:
        feed_page()
    elif "Upload" in page:
        upload_page()
