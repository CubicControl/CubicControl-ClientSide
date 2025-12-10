<p align="center">
  <img src="static/resources/ClientSideLogo.png" alt="CubicControl Logo" width="500"/>
</p>
<br>

# CubicControl ClientSide

CubicControl ClientSide is the **remote web interface** for the CubicControl ecosystem.  
It works together with the **[CubicControl-Launcher](https://github.com/CubicControl/CubicControl-Launcher)** — the dedicated Windows control panel designed for running Minecraft servers on a spare or dedicated PC.

ClientSide gives you (and your friends) the ability to safely **wake**, **start**, **stop**, and **monitor** your Minecraft server from anywhere, without exposing your local machine.  
Deploying it on Render’s free tier makes the server fully remote-ready while keeping all sensitive services private.

<p align="center">
  <a href="https://cubiccontrol.github.io/">
    <img src="https://img.shields.io/badge/Full%20Guide-brightgreen?style=for-the-badge"/>
  </a>
</p>

---

## 📝 Overview

CubicControl ClientSide is a lightweight Flask + Socket.IO application that exposes a **secure, minimal remote UI** for your CubicControl-powered Minecraft server.

It is built for:

- Allowing friends to start the server anytime  
- Keeping the host PC asleep when idle  
- Avoiding exposing the full launcher interface to the internet  
- Zero-cost hosting powered by Render’s free tier  

---

## ⚠️ Disclaimer

**I am not a professional developer.**  
CubicControl began as a personal project that I chose to share publicly. While it works well, some parts may not follow perfect coding standards.  
Improvements and fixes will continue over time.

---

## 🚀 Features

- Remote **wake**, **start**, **stop**, and **restart** controls  
- Live server status updates via WebSockets  
- Secure login with customizable username/password  
- Environment-based permission flags (`ALLOW_*`)  
- Sends Wake-on-LAN packets directly to your host PC  
- Works seamlessly with CubicControl-Launcher via shared `AUTH_KEY`  
- Simple, free deployment using Render  

---

# 🌐 Deploy to Render (Recommended)

1. Create a new **Web Service** on Render (free tier is enough).  
2. Use this repository URL as the source.  
3. Set:
   - **Environment:** Python  
   - **Build Command:** `pip install -r requirements.txt`  
   - **Start Command:** `python app.py`  
4. Add the required environment variables (see tables below).  
5. Ensure `AUTHKEY_SERVER_WEBSITE` matches the `AUTH_KEY` from CubicControl-Launcher.  
6. Set `TARGET_IP_ADDRESS_SERVER` to your public domain/IP (from your Caddy proxy).  
7. Deploy and log in using your configured `LOGIN_USERNAME` / `LOGIN_PASSWORD`.

# 💻 Run Locally

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
# Set environment variables manually or using envvars.env
python app.py
```

## Open

➡️ http://localhost:5000

Then log in using `LOGIN_USERNAME` / `LOGIN_PASSWORD`.

---

## 🔑 Environment Variables

### **Required**

| Variable                    | Description                                                                        |
|-----------------------------|------------------------------------------------------------------------------------|
| `AUTHKEY_SERVER_WEBSITE`    | Shared secret used in Authorization headers; must match Launcher's `AUTH_KEY`.     |
| `TARGET_MAC_ADDRESS_SERVER` | MAC address of the host PC (`AA:BB:CC:DD:EE:FF`).                                  |
| `TARGET_IP_ADDRESS_SERVER`  | Public domain or IP where the Launcher/Caddy API can be reached.                   |
| `LOGIN_USERNAME`            | Username for logging into ClientSide.                                              |
| `LOGIN_PASSWORD`            | Password for logging into ClientSide.                                              |
| `SERVER_NAME`               | Display name shown in the UI.                                                      |

### **Optional / Feature Toggles**

| Variable         | Description                                                                |
|------------------|----------------------------------------------------------------------------|
| `ALLOW_WAKE`     | Enable/disable wake button (`true/false/1/0/yes/no`).                      |
| `ALLOW_START`    | Enable/disable start button.                                               |
| `ALLOW_STOP`     | Enable/disable stop button.                                                |
| `ALLOW_RESTART`  | Enable/disable restart button.                                             |
| `SECRET_KEY`     | Optional Flask session secret; auto-generated if missing.                  |

---

## 📘 Full Installation & Setup Guide

A complete, step-by-step guide — covering Wake-on-LAN setup, port forwarding, Caddy, Launcher configuration, ClientSide deployment, and best practices — is available here:

➡️ **https://cubiccontrol.github.io/**

This is the recommended starting point for all new users.

---

## 💡 Tips

- Never share your `AUTH_KEY`. Anyone with it can control the backend.  
- If remote actions fail, re-check Wake-on-LAN settings (BIOS → Windows network adapter → router).  
- Render’s free tier sleeps when inactive; your site may take a few seconds to wake up.
