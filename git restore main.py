[1mdiff --git a/main.py b/main.py[m
[1mindex 3ff0f87..270f7c5 100644[m
[1m--- a/main.py[m
[1m+++ b/main.py[m
[36m@@ -6,8 +6,10 @@[m [mfrom fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse[m
 from pydantic import BaseModel[m
 from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK[m
 from db_manager import DataManager[m
[32m+[m[32mimport auth[m
 [m
 app = FastAPI()[m
[32m+[m[32mapp.include_router(auth.router)[m
 [m
 templates = Jinja2Templates(directory="templates")[m
 [m
[36m@@ -33,6 +35,9 @@[m [masync def index(request: Request):[m
     }[m
     return templates.TemplateResponse("index.html", context=context)[m
 [m
[32m+[m[32m@app.get("/register", response_class=HTMLResponse)[m
[32m+[m
[32m+[m
 [m
 @app.get("/user/{user_id}")[m
 async def user_home(user_id: int, request: Request):[m
[36m@@ -54,7 +59,7 @@[m [masync def create_user(user_data: User):[m
     users = data_manager.get_all_users()[m
 [m
     for user in users:[m
[31m-        if user.name == user_data.username:[m
[32m+[m[32m        if user.username == user_data.username:[m
             return JSONResponse([m
                 status_code=HTTP_400_BAD_REQUEST,[m
                 content={"error": "User exists already"}[m
