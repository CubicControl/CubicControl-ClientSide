<p align="center">
  <img src="static/resources/ClientSideLogo.png" alt="CubicControl Logo" width="450"/>
</p>
<br>

CubicControl ClientSide is a lightweight Flask + Socket.IO web UI that talks to the [CubicControl-Launcher](https://github.com/CubicControl/CubicControl-Launcher) so friends can wake, start, stop, and restart your Minecraft server remotely. Deploy it on Render's free tier to keep your home machine private while exposing only the control surface.

> ⚠️ **Disclaimer**
>
> **I am not a professional developer.** CubicControl started as a personal project that I decided to share in case others find it useful or enjoyable. While I have done my best to ensure the code is functional and free of major bugs, there may be inconsistencies or coding issues present.  
> **This is an ongoing project, and improvements or fixes will continue over time.**


## How it works
- Proxies start/stop/restart/status requests to the launcher backend using a shared AUTH key for Authorization: Bearer headers.
- Sends Wake-on-LAN magic packets directly to your host MAC/IP when allowed.
- UI buttons are shown/enabled based on ALLOW_* env flags and live status updates streamed over WebSocket.
- Session-based login protects the panel; a static SECRET_KEY prevents session churn across restarts.

## Deploy to Render (recommended)
1. Create a new Web Service on Render (free tier is fine) and put this repository url as source.
2. Set Environment to Python; Build command: `pip install -r requirements.txt`; Start command: `python app.py`.
3. Add the environment variables from `envvars.env` (see table below). Set `AUTHKEY_SERVER_WEBSITE` to the same value as the AUTH_KEY configured in CubicControl-Launcher/ServerSide.
4. Point `TARGET_IP_ADDRESS_SERVER` at the public domain/IP where the launcher (and its Caddy proxy) is reachable.
5. Deploy. Visit the Render URL, log in with `LOGIN_USERNAME` / `LOGIN_PASSWORD`, and use the buttons to wake/start/stop/restart the server.

## Run locally
- `python -m venv .venv && .venv\Scripts\activate`
- `pip install -r requirements.txt`
- Set the env vars (you can copy `envvars.env` and export the keys), then `python app.py`.
- Open http://localhost:5000 and log in.

## Environment variables
- `AUTHKEY_SERVER_WEBSITE` (alias `AUTH_KEY` in envvars.env): Shared secret used for Authorization: Bearer when calling ServerSide; must match the AUTH_KEY configured in CubicControl-Launcher.
- `TARGET_MAC_ADDRESS_SERVER` (alias `TARGET_MAC_ADDRESS`): MAC address of the host PC for Wake-on-LAN (format `AA:BB:CC:DD:EE:FF`).
- `TARGET_IP_ADDRESS_SERVER` (alias `TARGET_IP_ADDRESS`): Public domain or IP (plus optional port) where the ServerSide/Caddy endpoint is reachable, used to build https://TARGET/status and other calls.
- `LOGIN_USERNAME`: Username required to sign in to this web UI.
- `LOGIN_PASSWORD`: Password for the UI.
- `SERVER_NAME`: Display name shown in the header of the UI; defaults to "Jean-mIcHeL GamIng" if unset.
- `ALLOW_WAKE`, `ALLOW_START`, `ALLOW_STOP`, `ALLOW_RESTART`: Per-button toggles; accepts true/false/1/0/yes/no/on/off; unset uses defaults (wake/start true, stop/restart false).
- `SECRET_KEY` (optional): Static Flask secret for sessions; if omitted, a key is generated and persisted under `instance/secret_key`.

## Tips
- Make sure the Render service can reach your launcher host (open firewall/ports as needed).
- If you deploy on a different domain, update the allowed origin in `app.py` or set a matching Render custom domain.
- Keep the AUTH key private; anyone with it can issue backend commands.
