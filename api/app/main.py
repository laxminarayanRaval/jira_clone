from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.config import settings, google_credentials

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from starlette.responses import RedirectResponse


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

# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl=flow.authorization_url(),
#     tokenUrl=flow.token_url(),
# )


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
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


# @app.get("/me")
# async def get_user_info(credentials: Credentials = Depends(oauth2_scheme)):
#     # Use the credentials to get the user's information
#     # Here is an example of using the Google API to get the user's email and name:
#     from google.oauth2 import id_token
#     from google.auth.transport import requests

#     token = id_token.verify_oauth2_token(
#         credentials.token, requests.Request(), CLIENT_ID
#     )
#     return {"email": token["email"], "name": token["name"]}
