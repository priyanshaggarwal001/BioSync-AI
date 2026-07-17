from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.patient_profiles import PatientProfile
from app.models.vital_sign import VitalSign
from app.schemas.vital_sign import (
    VitalSignCreate,
    VitalSignUpdate,
)

class VitalSignService(BaseService[VitalSign]):
    def __init__(self):
        super().__init__(VitalSign) 
    

    def create_vital_sign(
        self,
        db: Session,
        patient: PatientProfile,
        vital_sign_data: VitalSignCreate,
    ) -> VitalSign:

        vital_sign = VitalSign(
            patient_id=patient.id,
            **vital_sign_data.model_dump(),
        )

        return self.create(
            db,
            vital_sign,
        )



    def update_vital_sign(
            self,
            db: Session,
            vital_sign: VitalSign,
            vital_sign_data: VitalSignUpdate,
    ) -> VitalSign:
        
        return self.update(
            db,
            vital_sign,
            vital_sign_data.model_dump(exclude_unset=True),
        )
    
    def get_patient_vital_sign(
        self,
        db: Session,
        patient_id,
        vital_sign_id,
    ) -> VitalSign | None:

        statement = (
            select(VitalSign)
            .where(
                VitalSign.id == vital_sign_id,
                VitalSign.patient_id == patient_id,
            )
        )

        return db.scalar(statement)
    
    def get_patient_vital_signs(
        self,
        db: Session,
        patient_id,
    ) -> list[VitalSign]:

        statement = (
            select(VitalSign)
            .where(
                VitalSign.patient_id == patient_id,
            )
        )

        return db.scalars(statement).all()
    
    
vital_sign_service = VitalSignService()