from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.config import settings, google_credentials, email_configuration, template_env
from app.schema import EmailSchema
from app.routers import api_router
from app.models import create_tables

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from starlette.responses import RedirectResponse, JSONResponse
from fastapi_mail import MessageSchema, FastMail, MessageType


# Google OAuth2 credentials
# CLIENT_ID = google_credentials.get(
#     "client_id",
#     "1059122565838-ssslohu20habg3ie5g66ov750jo7dq0p.apps.googleusercontent.com",
# )
# CLIENT_SECRET = google_credentials.get(
#     "client_secret", "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"
# )
# REDIRECT_URI = google_credentials.get("redirect_uris")
# SCOPES = ["openid", "email", "profile"]


# OAuth2 authorization code flow
flow = Flow.from_client_config(
    client_config=google_credentials,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
)

flow.redirect_uri = "http://127.0.0.1:8008/login/google/callback"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=google_credentials.get("web").get("auth_uri"),
    tokenUrl=google_credentials.get("web").get("token_uri"),
)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.include_router(api_router)
    # configure_static(app)
    # create_tables()  # new
    return app


app = start_application()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "hello laxminarayan"}


@app.get("/login/google")
async def login_with_google():
    authorization_url, _ = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        state="Sr3tym0LFn1nT4FVyf3rJUaorkRPDH",
        include_granted_scopes="true",
    )
    return RedirectResponse(url=authorization_url)


@app.get("/login/google/callback")
async def login_with_google_callback(code: str):
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return {"access_token": credentials.token}


@app.get("/me")
async def get_user_info(credentials: Credentials = Depends(oauth2_scheme)):
    # Use the credentials to get the user's information
    # Here is an example of using the Google API to get the user's email and name:
    from google.oauth2 import id_token
    from google.auth.transport import requests

    token = id_token.verify_oauth2_token(
        credentials.token, requests.Request(), google_credentials.get("web").get("client_id")
    )
    return {"email": token["email"], "name": token["name"]}


@app.post("/email")
async def email_send(email: EmailSchema) -> JSONResponse:
    html = """<h1>Hi this test mail, thanks for using Fastapi-mail</h1> """
    # template = template_env.get_template(email.template_name)
    # html = template.render(user_name=email.user_name, subject=email.subject)
    message = MessageSchema(
        subject=email.subject,
        recipients=email.mail_to,  # email.dict().get("email"),
        body=html,
        subtype=MessageType.html,
    )
    fm = FastMail(email_configuration)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
