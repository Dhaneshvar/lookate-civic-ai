# IBM Bob Build Story

## Project

**LookAte Civic — Bengaluru's AI Civic Copilot**

LookAte Civic helps residents report potholes, garbage overflow, water leaks, flooding, broken streetlights, traffic hazards and blocked footpaths using a photo or natural-language description.

The application classifies the issue, estimates risk, routes it to the responsible department, generates a trackable incident number and displays the incident on a Civic Pulse dashboard.

## How IBM Bob was used

IBM Bob was used as the development copilot throughout the transformation of LookAte from a travel assistant into a civic-response platform.

### 1. Understanding the existing codebase

Prompt used with Bob:

> Inspect this React and Flask repository. Explain the current architecture, identify the existing AI, image-upload, map, routing and API flows, and recommend the smallest safe change that would convert the travel assistant into a Bengaluru civic-issue reporting application.

Bob helped identify the reusable building blocks:

- React application shell and tab navigation
- Flask API and Azure OpenAI integration
- Existing image upload and vision input
- Location-aware map and routing
- Structured AI tool-calling flow
- Existing SerpAPI search integration

### 2. Designing the civic domain model

Prompt used with Bob:

> Design a civic incident schema for Bengaluru. It must support issue classification, risk level, confidence, responsible department, location, status timeline, incident number, safety advice and phone escalation state. Keep it compatible with the existing Flask application.

Bob guided the addition of the civic classification and routing model in `backend/app.py`.

The supported issue categories are:

- Pothole
- Road damage
- Garbage
- Water leak
- Flooding
- Streetlight failure
- Traffic hazard
- Blocked footpath
- Other civic issue

### 3. Building multimodal AI triage

Prompt used with Bob:

> Add an Azure OpenAI vision workflow that receives a citizen image and optional description, returns strict JSON classification, assigns a risk level and recommends a department. Do not invent an address or claim physical verification. Add a safe fallback for demo mode when the AI is unavailable.

Bob helped implement:

- Azure OpenAI vision classification
- Strict JSON parsing
- Risk and confidence fields
- Safety advice
- Department routing
- Deterministic fallback classification for offline demos

### 4. Creating the incident workflow

Prompt used with Bob:

> Add an API endpoint that converts a civic classification into a submitted incident. Generate a unique Bengaluru incident number, save the incident, include a status timeline, and return the department and incident number to the citizen.

This resulted in the civic endpoints:

- `POST /api/civic/report`
- `GET /api/civic/incidents`
- `POST /api/civic/escalate`

### 5. Building the Civic Pulse dashboard

Prompt used with Bob:

> Create a responsive React Civic Pulse dashboard. It should allow a citizen to take or upload a photo, add a description, submit the report, show the generated incident number, and display all incidents with risk, department, status and address.

Bob helped create `frontend/src/components/CivicDashboard.tsx` and connect it to the Flask API.

The dashboard includes:

- Photo capture/upload
- Optional natural-language description
- Browser location capture
- AI triage status
- Incident number display
- Incident counts
- Risk indicators
- Department routing
- Incident list
- Phone escalation action

### 6. Adding phone escalation readiness

Prompt used with Bob:

> Add a safe phone escalation workflow. It should create a call brief for the responsible civic department, add the escalation to the incident timeline, and clearly indicate that a verified telephony provider is required before placing a real call.

The current prototype queues the escalation and generates a call brief. The endpoint is ready to connect to Twilio or IBM voice services after credentials and verified department numbers are added.

## Bob-to-feature traceability

| IBM Bob contribution | Result in the prototype |
|---|---|
| Repository analysis | Reused existing map, voice, image and Azure flows |
| Civic schema design | Structured incidents with risk, department and timeline |
| Vision workflow prompt | Photo-based issue classification |
| API implementation prompt | Incident creation and incident numbers |
| UI generation prompt | Civic Pulse dashboard |
| Integration/debugging prompts | Connected React dashboard to Flask endpoints |
| Safety prompt | No fabricated address or false government confirmation |
| Telephony design prompt | Provider-ready phone escalation queue |

## Suggested Bob evidence to attach

Add screenshots or a short screen recording of the following Bob interactions to the submission:

1. Bob inspecting the original LookAte repository.
2. Bob proposing the civic incident schema.
3. Bob generating or modifying the Azure vision classification flow.
4. Bob creating the Civic Pulse dashboard.
5. Bob running the application and fixing an integration issue.
6. Bob reviewing the final civic workflow for safety and feasibility.

> Replace this section's placeholders with actual screenshots from your IBM Bob session. The screenshots should show the prompt, Bob's response or code change, and the resulting feature in the running application.

## Two-minute Bob story for the video

> We started with LookAte, a voice and image-based travel assistant. We used IBM Bob to inspect the existing architecture and identify what could be reused for a Bengaluru civic solution.
>
> We then asked Bob to design a civic incident model, add Azure OpenAI vision triage, classify issues by type and risk, route each report to the responsible department, and generate a trackable incident number.
>
> Bob helped us build the Civic Pulse dashboard and connect it to the Flask backend. The citizen can now upload a photo, receive an AI classification, see the department responsible, and track the incident.
>
> Finally, we used Bob to design a safe phone escalation workflow. The prototype generates a call brief and queues the request, while real calls require a verified telephony provider and department number.
>
> IBM Bob was not just used to generate code. It helped us understand the repository, make architecture decisions, implement the workflow, test integrations and turn a travel product into a civic-response platform for Bengaluru.

## Validation checklist

- [ ] Capture Bob workspace screenshots.
- [ ] Show the same feature working in the running application.
- [ ] Demonstrate one pothole report from photo to incident number.
- [ ] Demonstrate one garbage, water or flooding classification.
- [ ] Show the Civic Pulse dashboard after submission.
- [ ] Show the phone escalation call brief.
- [ ] Add the final IBM Bob demo recording link to the submission form.
