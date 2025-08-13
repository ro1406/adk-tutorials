"""
Author: Rohan Mitra (rohanmitra8@gmail.com)
tools.py (c) 2025
Desc: Tools for the ADK agent to book a doctor's appointment
Created:  2025-08-12T20:32:25.091Z
Modified: 2025-08-13T14:10:00.562Z
"""

from typing import Any, Dict, List, Optional
import uuid


def make_appointment(
    patient_full_name: str,
    date_of_birth: str,
    doctor_or_specialty: str,
    reason_for_visit: str,
    appointment_type: str,
    consent: bool,
    contact_phone: Optional[str] = None,
    contact_email: Optional[str] = None,
    location_preference: Optional[str] = None,
    preferred_dates: Optional[List[str]] = None,
    preferred_time_windows: Optional[List[str]] = None,
    timezone: Optional[str] = "GMT+4 Dubai",
    insurance_provider: Optional[str] = "",
    insurance_member_id: Optional[str] = "",
    urgency: Optional[str] = "",
    accessibility_notes: Optional[str] = "",
    additional_notes: Optional[str] = "",
) -> Dict[str, Any]:
    """Tool to book a doctor's appointment.

    Accepts explicit appointment details, prints them for visibility, and
    returns a success payload with a generated confirmation ID. This is a
    stub and does not integrate with any external scheduling system.

    Returns
    -------
    Dict[str, Any]
        A dictionary indicating success and containing a confirmation ID
        and an echo of the received details.
    """

    #For now just prints the appointment details to the console
    #Can be changed to integrate with an external scheduling system
    #Eg: Check Google Calendar for availability and book the appointment

    
    received: Dict[str, Any] = {
        "patient_full_name": patient_full_name,
        "date_of_birth": date_of_birth,
        "doctor_or_specialty": doctor_or_specialty,
        "reason_for_visit": reason_for_visit,
        "appointment_type": appointment_type,
        "consent": consent,
        "contact_phone": contact_phone,
        "contact_email": contact_email,
        "location_preference": location_preference,
        "preferred_dates": preferred_dates,
        "preferred_time_windows": preferred_time_windows,
        "timezone": timezone,
        "insurance_provider": insurance_provider,
        "insurance_member_id": insurance_member_id,
        "urgency": urgency,
        "accessibility_notes": accessibility_notes,
        "additional_notes": additional_notes,
    }
    
    print("[make_appointment] Received appointment request:")
    for key in sorted(received.keys()):
        value = received[key]
        if value:
            print(f"  - {key}: {value}")

    confirmation_id = str(uuid.uuid4())
    print(f"[make_appointment] Mock booking created with confirmation_id={confirmation_id}")

    return {
        "success": True,
        "confirmation_id": confirmation_id,
        "message": "Appointment booked.",
    }
