# CST8919 Assignment 1 – Securing and Monitoring an Authenticated Flask App

## Student Information

**Name:** Jingjing Duan

**Course:** CST8919 – DevOps - Security and Compliance

---

# Project Overview

This assignment extends the Flask application developed in Lab 1 by integrating authentication, monitoring, and security logging in Microsoft Azure.

The application uses Auth0 for user authentication and is deployed to Azure App Service. User activities are logged and collected by Azure Monitor. Log Analytics and Kusto Query Language (KQL) are used to detect suspicious behavior, and Azure Alert Rules are configured to notify administrators when abnormal activities are detected.

---

# YouTube Demo Link


---

# Technologies Used

- Python 3.11
- Flask
- Auth0
- Azure App Service
- Azure Monitor
- Log Analytics Workspace
- Kusto Query Language (KQL)
- GitHub Actions

---

# Application Features

## Authentication

The application uses Auth0 to authenticate users.

Authenticated users can:

- Log in securely
- Access the protected page
- Log out

Unauthenticated users attempting to access the protected route are redirected to the login page.

---

## Security Logging

The application records the following security events:

### Login Success

When a user successfully logs in, the application logs:

- User ID
- Email address
- Timestamp

Example:

```json
{
  "event":"LOGIN_SUCCESS",
  "user_id":"auth0|xxxx",
  "email":"user@example.com"
}
```

---

### Protected Route Access

Whenever an authenticated user accesses `/protected`, the application records:

- User ID
- Email
- Route

Example:

```json
{
  "event":"PROTECTED_ACCESS",
  "user_id":"auth0|xxxx",
  "email":"user@example.com",
  "path":"/protected"
}
```

---

### Unauthorized Access

If an unauthenticated user attempts to access `/protected`, the application records:

- Event type
- Client IP address
- Requested path

Example:

```json
{
  "event":"UNAUTHORIZED_ACCESS",
  "path":"/protected",
  "ip_address":"127.0.0.1"
}
```

---

# Azure Deployment

The application is deployed to Azure App Service using GitHub Actions.

Deployment includes:

- Automatic build
- Automatic deployment
- Environment variables stored in Azure App Service
- Auth0 configuration

---

# Monitoring

Azure Monitor is configured to collect application logs.

Diagnostic Settings send the following logs to Log Analytics Workspace:

- App Service Console Logs
- App Service Application Logs
- HTTP Logs
- Platform Logs

---

# KQL Query

The following KQL query detects users who access the protected route excessively within a five-minute period.

```kusto
AppServiceConsoleLogs
| where ResultDescription contains "PROTECTED_ACCESS"
| extend UserId = extract('"user_id": "([^"]+)"', 1, ResultDescription)
| summarize AccessCount = count() by UserId, bin(TimeGenerated, 5m)
| where AccessCount >= 5
```

---

# Alert Rule

An Azure Alert Rule is configured using the KQL query above.

Alert configuration:

- Evaluation Frequency: 5 minutes
- Time Window: 5 minutes
- Threshold: Greater than 0 results

The alert is triggered when a user accesses the protected route five or more times within five minutes.

---

# Screenshots

## Azure App Service

![alt text](screenshots/image0.png)

---

## Successful Authentication

![alt text](screenshots/image.png)

---

## Protected Route

![alt text](screenshots/image2.png)

---

## Diagnostic Settings

![alt text](screenshots/image3.png)

---

## Log Analytics Query

![alt text](screenshots/image4.png)

---

## Alert Rule

![alt text](screenshots/image5.png)

---

# Conclusion

This assignment demonstrates how authentication, application logging, Azure monitoring, and alerting can be integrated to improve the security and observability of a cloud-hosted Flask application.

The solution provides centralized monitoring of user activities and enables administrators to detect suspicious behavior using Azure Monitor and Kusto Query Language.