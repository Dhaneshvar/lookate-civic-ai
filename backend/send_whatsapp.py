"""Send a LookAte Civic incident update over WhatsApp using Twilio.

Usage:
    python send_whatsapp.py --incident BLR-20261116-ABC123 --to +919876543210

The script reads the incident from static/civic_incidents.json and sends only
when the Twilio WhatsApp variables are configured in backend/.env.
"""
import argparse
import base64
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')


def find_incident(incident_id):
    path = ROOT / 'static' / 'civic_incidents.json'
    if not path.exists():
        raise SystemExit(f'Incident store not found: {path}')
    incidents = json.loads(path.read_text(encoding='utf-8'))
    return next((item for item in incidents if item.get('id') == incident_id), None)


def send_whatsapp(incident, recipient):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID', '').strip()
    auth_token = os.getenv('TWILIO_AUTH_TOKEN', '').strip()
    sender = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886').strip()
    if not account_sid or not auth_token:
        raise SystemExit('Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in backend/.env first.')
    recipient = recipient if recipient.startswith('whatsapp:') else f'whatsapp:{recipient}'
    reported_at = incident.get('reported_at') or incident.get('created_at', '')
    progress_url = (incident.get('progress_url') or os.getenv('LOOKATE_PUBLIC_URL', 'http://localhost:5173') + '/?incident=') + incident['id']
    body = (
        f"LOOKATE CIVIC PLUS — REPORT RECEIVED\n\n"
        f"Incident number: {incident['id']}\n"
        f"Reported: {reported_at}\n"
        f"Location: {incident['address']}\n"
        f"Issue: {incident['issue_label']}\n"
        f"Risk: {incident['risk'].upper()}\n"
        f"Department: {incident['department']}\n"
        f"State authority portal: {incident.get('civic_portal', 'Not available')}\n"
        f"Status: {incident['status']}\n\n"
        f"What we detected: {incident['summary']}\n"
        f"What happens next: {incident.get('next_action', 'The department will review and assign the incident.')}\n\n"
        f"Safety advice: {incident['safety_advice']}\n\n"
        f"Track progress: {progress_url}\n"
        f"Reply FOLLOW UP {incident['id']} for an update."
    )
    token = base64.b64encode(f'{account_sid}:{auth_token}'.encode()).decode()
    response = requests.post(
        f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json',
        headers={'Authorization': f'Basic {token}'},
        data={'From': sender, 'To': recipient, 'Body': body},
        timeout=20,
    )
    if not response.ok:
        raise SystemExit(f'Twilio rejected the message ({response.status_code}): {response.text[:500]}')
    result = response.json()
    print(json.dumps({'success': True, 'message_sid': result.get('sid'), 'status': result.get('status')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a civic incident WhatsApp notification')
    parser.add_argument('--incident', required=True, help='Incident number, e.g. BLR-20261116-ABC123')
    parser.add_argument('--to', help='Recipient phone in E.164 format; defaults to TWILIO_WHATSAPP_TO')
    args = parser.parse_args()
    recipient = args.to or os.getenv('TWILIO_WHATSAPP_TO', '').strip()
    if not recipient:
        raise SystemExit('Provide --to or set TWILIO_WHATSAPP_TO in backend/.env.')
    incident = find_incident(args.incident)
    if not incident:
        raise SystemExit(f'Incident not found: {args.incident}')
    send_whatsapp(incident, recipient)
