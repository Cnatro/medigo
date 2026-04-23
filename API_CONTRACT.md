# API CONTRACT

## 1. Authentication

### POST /auth/register

Register new user
Roles: PATIENT, DOCTOR
Request:

````json
{
  "full_name": "string",
  "email": "string",
  "password": "string",
  "role": "PATIENT | DOCTOR",
  "profile": {}
}
````

````json PATIENT
{
  "full_name": "string",
  "email": "string",
  "password": "string",
  "role": "PATIENT | DOCTOR",
  "profile": {
    "date_of_birth": "2000-01-01",
    "gender": "MALE"

  }
}
````
```json DOCTOR
{
  "full_name": "string",
  "email": "string",
  "password": "string",
  "role": "PATIENT | DOCTOR",
   "profile": {
    "bio": "Cardiologist",
    "experience_years": 10,
    "clinic_id": "uuid-123"
  }

}
````

Response: `201 Created`

---

### POST /auth/login

Login user
Request:

```json
{
  "email": "string",
  "password": "string"
}
```

Response: `200 OK (JWT token)`

---

### POST /auth/refresh-token

Refresh JWT token

---

### POST /auth/logout

Logout user

---

## 2. User

### GET /users/me

Get current user info (JWT required)
Response: `200 OK`

---

## 3. Doctor & Clinic

### GET /doctors

Search doctors
Query:

    specialty_id
    name
    clinic_id
    page, size

---

### GET /doctors/{doctor_id}

Get doctor profile

---

### GET /doctors/{doctor_id}/schedules

Get working schedule by date range

---

### GET /clinics

Search clinics (name, location)

---

### GET /clinics/{clinic_id}

Get clinic details

---

## 4. Specialty & Symptom

### GET /specialties

List all specialties

---

### GET /symptoms

List all symptoms

---

## 5. Appointment

### POST /appointments

Role: PATIENT
Book appointment
Request:

```json
{
  "doctor_id": 1,
  "time_slot_id": 10,
  "reason": "string"
}
```

Constraints:

    Time slot must be available
    Cannot book past time
    Cannot overlap appointments

---

### GET /appointments

Role: PATIENT / DOCTOR
Query:

    patient_id
    doctor_id
    date
    status
    page, size

---

### GET /appointments/{appointment_id}

Get appointment details

---

### PATCH /appointments/{appointment_id}

Update appointment
Request:

```json
{
  "status": "PENDING | CONFIRMED | CANCELLED | COMPLETED",
  "time_slot_id": 10
}
```

---

### PATCH /appointments/{appointment_id}/cancel

Cancel appointment

---

### PATCH /appointments/{appointment_id}/confirm

Confirm appointment (Doctor)

---

## 6. Schedule Management (Doctor)

### GET /doctor-schedules/me

Role: DOCTOR
Get own schedules

---

### POST /doctor-schedules

Create schedule
Request:

```json
{
  "day_of_week": "MONDAY",
  "start_time": "08:00",
  "end_time": "17:00",
  "is_active": true
}
```

---

### PATCH /doctor-schedules/{schedule_id}

Update schedule

---

### GET /time-slots

Query:

    doctor_id
    date
    is_available

---

## 7. Review & Rating

### POST /reviews

Role: PATIENT
Review doctor

```json
{
  "doctor_id": 1,
  "rating": 5,
  "comment": "Good doctor"
}
```

---

### GET /reviews

Query:

    doctor_id

---

## 8. Suggestion & Chatbot

### POST /doctor-suggestions

Suggest doctors based on:

    symptoms
    specialty
    rating
    availability

---

### POST /chatbot/symptom-classify

Classify symptoms

```json
{
  "description": "I have headache and fever"
}
```

---

### POST /chatbot/chat

Chat with AI bot

```json
{
  "message": "I feel chest pain"
}
```

---

## 9. Order & Payment

### POST /orders

Create order

---

### PATCH /orders/{order_id}/cancel

Cancel/refund order

---

### POST /orders/momo/callback

Payment callback from MoMo

---

## 10. Notification (Optional)

### GET /notifications

Get user notifications

---

## 11. Status Definitions

### Appointment Status:

PENDING
CONFIRMED
CANCELLED
COMPLETED

---

## 12. Roles

PATIENT
DOCTOR
ADMIN (optional)

---

## 13. Notes

All protected APIs require JWT
Pagination: `page`, `size`
Standard response format recommended:

```json
{
  "success": true,
  "data": {},
  "message": ""
}
```
