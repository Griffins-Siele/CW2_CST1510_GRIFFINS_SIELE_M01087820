"""Minimal AI helper utilities for Streamlit app.

This module supplies small helper functions expected by the pages in
`Week_10_Lab/pages`. The functions are implemented with a safe fallback when
the OpenAI client is not installed or the API key is not configured to avoid
raising import/runtime errors during development.
"""
from __future__ import annotations
from typing import Tuple, Optional
import os
import json

# Load .env early so os.environ gets populated when developers paste keys in .env
try:
    from dotenv import load_dotenv
    load_dotenv()  # safe no-op if .env doesn't exist
except Exception:
    # python-dotenv may not be installed; the helper falls back to env variables
    pass

def get_openai_api_key() -> Optional[str]:
    """Return the OpenAI API key, checking multiple sources in order:

    1. OS environment variable OPENAI_API_KEY
    2. Streamlit secrets at st.secrets["OPENAI_API_KEY"] (if running under streamlit)
    3. None
    """
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    try:
        # avoid importing streamlit globally; import only when needed
        import streamlit as st
        return st.secrets.get("OPENAI_API_KEY") if isinstance(st.secrets, dict) or hasattr(st.secrets, "get") else None
    except Exception:
        return None


def is_openai_configured() -> bool:
    """Return True if an OpenAI key is available from any supported source."""
    return get_openai_api_key() is not None


def explain_statistics(text: str) -> Tuple[bool, str]:
    """Analyze a plain-text summary and return (success, advice).

    If OpenAI is configured and client is installed, an API call is attempted.
    Otherwise we fall back to a basic heuristic summary that is still
    helpful during offline development.
    """
    # Avoid importing openai during development unless we need it
    api_key = get_openai_api_key()
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            prompt = (
                "You are a helpful analytics assistant. Analyze the following: \n\n"
                + text
                + "\n\nProvide a short analysis and top 3 bullet point recommendations."
            )
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512
            )
            answer = resp.choices[0].message.content.strip()
            return True, answer
        except Exception as e:
            # If the API call fails, fall back to the heuristic analysis below
            # but include a short note in the response.
            heuristic_success, heuristic_resp = _explain_statistics_fallback(text)
            note = f"(OpenAI error: {str(e)}; providing a heuristic fallback)\n"
            return heuristic_success, note + heuristic_resp

    # Fallback heuristic: produce a tiny analysis from the summary
    # Local heuristic fallback
    return _explain_statistics_fallback(text)


def _explain_statistics_fallback(text: str) -> Tuple[bool, str]:
    try:
        # Look for simple stats and generate a human-readable response
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        summary = [l for l in lines if ":" in l]
        insights = []
        for s in summary:
            key, val = s.split(":", 1)
            key = key.strip().lower()
            val = val.strip()
            if "high priority" in key or "high priority" in s.lower():
                insights.append(f"High priority tickets: {val}. Consider increasing resources.")
            elif "open" in key or "open" in s.lower():
                insights.append(f"Open tickets: {val}. Ensure triage process is active.")
        if not insights:
            insights = ["No obvious trends detected from the summary; consider providing more context."]
        # Return a simple JSON-friendly response for UI
        resp_text = "\n".join([f"• {i}" for i in insights])
        return True, resp_text
    except Exception as e:
        return False, f"Error analyzing text: {str(e)}"


def get_security_advice(incident_text: str) -> Tuple[bool, str]:
    """Produce security advice for an incident. Uses OpenAI if configured,
    otherwise returns rule-based advice.
    """
    api_key = get_openai_api_key()
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            prompt = (
                "You are a cybersecurity incident response assistant. Given the incident:\n\n"
                + incident_text
                + "\n\nProvide a short, clear remediation checklist and prioritised next steps."
            )
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512
            )
            answer = resp.choices[0].message.content.strip()
            return True, answer
        except Exception as e:
            # If the OpenAI call fails, log the error and fall back to rules
            # to avoid failing the entire page.
            fallback_success, fallback_resp = _get_security_advice_fallback(incident_text)
            note = f"(OpenAI error: {str(e)}; providing a heuristic fallback)\n"
            return fallback_success, note + fallback_resp

    # Fallback rules
    text = incident_text.lower()
    adv = []
    if "malware" in text:
        adv.append("Isolate affected endpoints and run anti-malware scans.")
        adv.append("Preserve logs and evidence; consider rebuilding compromised hosts.")
        adv.append("Change passwords for affected accounts and review access logs.")
    if "phishing" in text or "spear" in text:
        adv.append("Block sender and reported URLs; verify any data exfiltration.")
        adv.append("Force password resets for potentially compromised accounts.")
    if "ddos" in text or "denial" in text:
        adv.append("Work with network provider to filter or rate-limit traffic.")
        adv.append("Implement traffic shaping and mitigation rules.")
    if "ransom" in text or "ransomware" in text:
        adv.append("Isolate networks; do not pay ransom. Restore from backups after validation.")

    if not adv:
        adv = [
            "Follow standard incident response: contain, eradicate, recover.",
            "Preserve evidence and notify stakeholders according to policy."
        ]

    return True, "\n".join([f"• {a}" for a in adv])


def _get_security_advice_fallback(incident_text: str) -> Tuple[bool, str]:
    text = incident_text.lower()
    adv = []
    if "malware" in text:
        adv.append("Isolate affected endpoints and run anti-malware scans.")
        adv.append("Preserve logs and evidence; consider rebuilding compromised hosts.")
        adv.append("Change passwords for affected accounts and review access logs.")
    if "phishing" in text or "spear" in text:
        adv.append("Block sender and reported URLs; verify any data exfiltration.")
        adv.append("Force password resets for potentially compromised accounts.")
    if "ddos" in text or "denial" in text:
        adv.append("Work with network provider to filter or rate-limit traffic.")
        adv.append("Implement traffic shaping and mitigation rules.")
    if "ransom" in text or "ransomware" in text:
        adv.append("Isolate networks; do not pay ransom. Restore from backups after validation.")

    if not adv:
        adv = [
            "Follow standard incident response: contain, eradicate, recover.",
            "Preserve evidence and notify stakeholders according to policy."
        ]
    return True, "\n".join([f"• {a}" for a in adv])


def streamlit_ai_chat(*args, **kwargs):
    """Simple wrapper placeholder for a streamlit-based AI chat UI.

    The pages import this symbol though it may not be used directly. We keep
    it as a no-op to avoid breaking imports.
    """
    return None
