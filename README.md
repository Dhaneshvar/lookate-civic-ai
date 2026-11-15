# LookAte Civic Plus

AI-powered civic incident reporting and tracking for Bengaluru and India.

LookAte Civic Plus lets citizens capture live photos with GPS, upload multiple existing photos, or describe civic issues by voice or text. Azure OpenAI analyzes the evidence, compares the image with the description, classifies risk, identifies the responsible department and prepares a report for citizen confirmation.

## Core workflow

```text
Photo / voice / text
        ↓
GPS or manual map pin
        ↓
Azure OpenAI evidence analysis
        ↓
Issue, risk, confidence and evidence-match preview
        ↓
Citizen selects Confirm & Send
        ↓
State-aware department routing
        ↓
Incident number, map marker and WhatsApp update
```

The app never sends a report or WhatsApp notification during preview. The citizen confirms the AI-generated report first.

## Features

- Live camera mode with continuous GPS tracking
- Upload mode for up to five existing photos
- Manual map pin selection
- Reverse geocoding for area, city, state and pincode
- Azure OpenAI vision classification
- Evidence comparison between the image and user description
- Issue type, risk level and confidence chips
- State-aware civic authority and department routing
- Dynamic incident numbers such as `PY-20261116-ABC123` and `KA-20261116-ABC123`
- Issue-specific map markers and clickable incident details
- WhatsApp report and status notifications through Twilio
- Public incident tracking links
- Officer view with city-wise counts and status updates
- Civic AI chat for safety guidance, nearby incidents and safer routes
- Installable mobile PWA with camera, microphone and GPS support

## Architecture

```text
React + Leaflet PWA
  ├─ Civic AI chat
  ├─ Civic Plus reporting form
  ├─ GPS, camera and map pin
  ├─ Incident map and officer view
  └─ WhatsApp tracking links
             │
             ▼
Flask civic orchestration API
  ├─ Azure OpenAI vision and classification
  ├─ Reverse geocoding
  ├─ State and department router
  ├─ Preview and Confirm & Send workflow
  ├─ Incident timeline and status API
  └─ Twilio WhatsApp adapter
             │
             ├─ OpenStreetMap / Nominatim
             ├─ SerpAPI Maps and Directions
             ├─ Twilio WhatsApp
             └─ Government portal or email adapter
```

## Technology

- React, TypeScript, Vite, Tailwind CSS and Leaflet
- Python, Flask and Flask-CORS
- Azure OpenAI vision-capable deployment
- SerpAPI, OpenStreetMap, Nominatim and OSRM
- Twilio WhatsApp REST API
- Web App Manifest and service worker
- IBM Bob development copilot

## Local setup

Requirements: Python 3.10+, Node 18+, Azure OpenAI credentials and SerpAPI credentials.

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

Health check: `http://localhost:5000/api/health`

### Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Environment variables

Never commit `backend/.env` or expose secret values.

```env
SERPAPI_KEY=your_serpapi_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_DEPLOYMENT=your_vision_capable_deployment
AZURE_OPENAI_API_VERSION=2025-01-01-preview

# Optional Twilio WhatsApp notifications
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+919876543210
LOOKATE_PUBLIC_URL=https://your-public-lookate-url
```

## Important endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Check Azure and SerpAPI configuration |
| `POST /api/chat` | Civic AI assistant and safer route guidance |
| `POST /api/civic/report` | Analyze, preview or confirm a civic report |
| `GET /api/civic/incidents` | Load incident board and map data |
| `POST /api/civic/incidents/{id}/status` | Officer status update |
| `POST /api/civic/escalate` | Queue phone escalation |

## State-aware routing

The backend reverse-geocodes the submitted coordinates instead of trusting a stale frontend label. It derives the actual state, city, area and pincode, then selects the relevant civic authority metadata.

Examples include Karnataka and BBMP services, Puducherry local administration, Tamil Nadu civic services and a national grievance fallback for other locations. Direct government submission requires an official API, approved webhook or configured email integration. The prototype prepares the correct state-specific report and portal link without falsely claiming external acceptance.

## WhatsApp updates

After confirmation, the citizen can receive the incident number, report time, location, issue, risk, department, status, next action, safety advice, progress link and state portal link.

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python send_whatsapp.py --incident PY-20261116-ABC123
```

The recipient must join the Twilio Sandbox during testing. Production requires an approved WhatsApp sender and message templates.

## Public tracking

After deployment, a citizen can open:

```text
https://your-public-lookate-url/?incident=PY-20261116-ABC123
```

The app displays the incident details and progress timeline. Production deployments should replace the local JSON store with durable database storage.

## Demo flow

1. Open Civic Plus and select Live camera + GPS or Upload photos.
2. Capture a pothole, garbage, flood or water-leak image.
3. Confirm or adjust the map pin and add a description.
4. Select Analyse & preview.
5. Review issue, risk, confidence and evidence-match chips.
6. Select Confirm & Send.
7. Show the incident number and map marker.
8. Show the WhatsApp report.
9. Open Officer view and change the status.
10. Show the status-update WhatsApp message.

## IBM Bob build story

See [IBM_BOB_BUILD_STORY.md](IBM_BOB_BUILD_STORY.md) for the Bob prompts, development journey, feature traceability and demo narration. Bob supported repository analysis, civic schema design, Azure vision integration, routing, dashboard development, WhatsApp readiness and testing.

## Testing

```powershell
cd backend
python -m py_compile app.py send_whatsapp.py
python tests/test_agent_tools.py
python tests/test_azure_sdk_path.py
```

## Safety and limitations

- AI classification assists human review, especially for high-risk cases.
- The app does not claim government acceptance without an official integration response.
- Real phone calls require a verified telephony provider and department number.
- Camera, microphone and GPS require permission and HTTPS on deployed devices.
- The local JSON incident store is suitable for a prototype; production needs durable storage.

## IBM Bobathon positioning

**LookAte Civic Plus turns a citizen’s photo or voice observation into a verified, location-aware and trackable civic action.**

Built for IBM Bobathon: **Smarter Streets, Better Living**.
