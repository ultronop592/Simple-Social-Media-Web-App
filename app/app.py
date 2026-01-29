from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse,UserRead, UserCreate, UserUpdate,userUpdate
from app.db import Post, create_db_and_tables, get_async_session, User  # Fixed: Port -> Post
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.image import imagekit
import shutil
import os
import uuid
import tempfile
from app.user import auth_backend, current_active_user, fastapi_users



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)  


app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/authjwt', tags=['auth'])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix='/authjwt', tags=['auth'])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix='/users', tags=['users'])
app.include_router(fastapi_users.get_reset_password_router(), prefix='/authjwt', tags=['auth'])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix='/authjwt', tags=['auth'])




@app.post("/upload")
async def upload_file(  # Fixed typo: uplaod_file -> upload_file
    file: UploadFile = File(...),
    caption: str = Form(""),  # Added missing comma
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
            
            
        upload_result = imagekit.files.upload(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options={
                "use_unique_file_name": True,
                "tags": ["backend-upload"]
            }
        )

        # The new API returns a dict, so update the usage below
        if upload_result.get("response_metadata", {}).get("http_status_code") == 200:
            post = Post(  # Fixed typo: Port -> Post
                user_id=user.id,
                caption=caption,
                url=upload_result["url"],
                file_type="video" if file.content_type.startswith("video") else "image",
                file_name=upload_result["name"]
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post  # Fixed typo: psot -> post
        
    except Exception as e:  # Fixed typo: execpt -> except
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        file.file.close()
            
        
        
@app.get("/feed")
async def get_feed(  # Fixed typo: get_fess -> get_feed
    session: AsyncSession = Depends(get_async_session),  # Added missing comma
    user: User = Depends(current_active_user)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]  # Fixed: users -> posts
    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    users_dict = {u.id: u for u in users}  # Fixed: user_dict -> users_dict
    
    
    post_data = []
    for post in posts:
        post_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name, 
                "created_at": post.created_at,
                "isowner": post.user_id == user.id,
                "email": users_dict.get(post.user_id).email if users_dict.get(post.user_id) else "Unknown"  # Fixed: user_dict -> users_dict
            }
        )
        
    return {"posts": post_data}



@app.delete("/post/{post_id}")
async def delete_post(
    post_id: str, 
    session: AsyncSession = Depends(get_async_session), 
    user: User = Depends(current_active_user)
):
    try:
        post_uuid = uuid.UUID(post_id)
        
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post Not Found")  # Fixed: details -> detail
        
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="YOU DON'T HAVE THE PERMISSION TO DELETE THIS POST")
                                
        await session.delete(post)
        await session.commit()
        
        return {"success": True, 'message': "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Removed extra closing parenthesis