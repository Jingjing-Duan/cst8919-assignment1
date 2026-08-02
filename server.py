import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import logging
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
app.logger.setLevel(logging.INFO)

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{env.get('AUTH0_DOMAIN')}/.well-known/openid-configuration",
)


def write_log(level, event, **details):
    log_data = {
        "event": event,
        **details,
    }

    message = json.dumps(log_data)

    if level == "warning":
        app.logger.warning(message)
    else:
        app.logger.info(message)


@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    user_info = token.get("userinfo", {})

    write_log(
        "info",
        "LOGIN_SUCCESS",
        user_id=user_info.get("sub", "unknown"),
        email=user_info.get("email", "unknown"),
    )

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()

    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/protected")
def protected():
    if "user" not in session:
        write_log(
            "warning",
            "UNAUTHORIZED_ACCESS",
            path=request.path,
            ip_address=request.remote_addr,
        )

        return redirect("/login")

    user_info = session["user"].get("userinfo", {})

    write_log(
        "info",
        "PROTECTED_ACCESS",
        user_id=user_info.get("sub", "unknown"),
        email=user_info.get("email", "unknown"),
        path=request.path,
    )

    return render_template("protected.html", user=session["user"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)