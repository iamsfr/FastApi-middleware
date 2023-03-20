import time
from fastapi import Depends, FastAPI,Request,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

origins = [ 
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def handle_email_background(email:str,data:str):
    for i in range(100):
        print(i)
        time.sleep(0.1)

@app.get('/users/email')
async def handle_email(email:str,background_task: BackgroundTasks):
    background_task.add_task(handle_email_background,email,"this sample background task")
    return {"user":"safeer","message":"mail sent"}


@app.post('/token')
async def get_token(form_data:OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username,"token_type":'bearer'}


@app.get('/')
def home():
    return {"hello": "world"}


@app.get('/selfie')
async def selfie(token: str = Depends(oauth_scheme)):
    return {"yes": token}
    
    
@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    response = await call_next(request)

    # Add a custom header to the response
    response.headers["X-Custom-Header"] = "Hello, World!"

    return response