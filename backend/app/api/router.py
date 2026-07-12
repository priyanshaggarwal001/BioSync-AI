from fastapi import APIRouter

from app.api.users import router as users_router
from app.api.patient_profiles import router as patient_profiles_router
from app.api.manual_entries import router as manual_entries_router
from app.api.diagnosis import router as diagnosis_router
from app.api.allergy import router as allergy_router
from app.api.medication import router as medication_router
from app.api.prescription import router as prescription_router
from app.api.prescripton import router as prescription_item_router

api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(patient_profiles_router)
api_router.include_router(manual_entries_router)
api_router.include_router(diagnosis_router)
api_router.include_router(allergy_router)
api_router.include_router(medication_router)
api_router.include_router(prescription_router)
api_router.include_router(prescription_item_router)