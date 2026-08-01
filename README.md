# cst8919-assignment1 - # Securing and Monitoring anAuthenticated Flask App


## Objective

This project demonstrates how to integrate Auth0 authentication into a Flask web application. Users can log in and log out using Auth0, and authenticated users can access a protected page.

The app supports:

- Login with Auth0
- Logout
- A protected page that only authenticated users can access
  
## Demo Video

YouTube demo link:
https://youtu.be/atKJ5kunEu8


## Technologies Used

- Python
- Flask
- Auth0
- Authlib
- OpenID Connect (OIDC)
- python-dotenv
- HTML

## Auth0 Configuration

In Auth0, create a Regular Web Application and configure:

Allowed Callback URLs:

```text
http://localhost:3000/callback
```

Allowed Logout URLs:

```text
http://localhost:3000
```

Allowed Web Origins:
```text
http://localhost:3000
```

## Environment Variables
Create a .env file in the project root:
```env
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret
AUTH0_DOMAIN=your_auth0_domain
APP_SECRET_KEY=your_app_secret_key
```

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd Auth0-Python-Web-App-Integration
```

## Install Dependencies
```bash
python -m pip install -r requirements.txt
```

## Run the App
```bash
python server.py
```

Then open:
```text
http://localhost:3000
```

## Protected Route
The app includes a custom route:
```text
http://localhost:3000/protected
```
If the user is not logged in, they are redirected to the Auth0 login page.

## What I Learned
I learned how to integrate Auth0 with a Flask web application. Auth0 acts as the Identity Provider (IdP), while my Flask application acts as the Service Provider (SP). I learned how authentication works using OpenID Connect and how to manage user sessions in Flask. I also implemented a protected route that redirects unauthenticated users to the login page.
=======
