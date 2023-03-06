from fastapi import APIRouter
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_mail import MessageSchema, FastMail, MessageType

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from starlette.responses import RedirectResponse, JSONResponse

from app.schema import EmailSchema
from app.config import google_credentials, email_configuration, template_env

router = APIRouter()


# Google OAuth2 credentials
CLIENT_ID = google_credentials["web"]["client_id"]
CLIENT_SECRET = google_credentials["web"]["client_secret"]


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


@router.get("/google")
async def login_with_google():
    authorization_url, _ = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        state="Sr3tym0LFn1nT4FVyf3rJUaorkRPDH",
        include_granted_scopes="true",
    )
    return RedirectResponse(url=authorization_url)


@router.get("/google/callback")
async def login_with_google_callback(code: str):
    flow.fetch_token(code=code)
    credentials = flow.credentials
    user_info = get_user_info(credentials)
    return user_info


def get_user_info(credentials):
    service = build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()
    return user_info  # idinfo



@router.post("/email") # async
def email_send(email: EmailSchema) -> JSONResponse:
    html = """<h1>Hi this test mail, thanks for using Fastapi-mail</h1> """
    # template = template_env.get_template(email.template_name)
    # html = template.render(user_name=email.user_name, subject=email.subject)
    message = MessageSchema(
        subject="Test Mail", #email.subject,
        recipients=["lx.raval01@gmail.com"],#email.mail_to,  # email.dict().get("email"),
        body=html,
        subtype=MessageType.html,
    )
    fm = FastMail(email_configuration)
    fm.send_message(message) # await
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
