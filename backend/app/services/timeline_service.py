from datetime import datetime,time
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.allergy import Allergy
from app.models.diagnosis import Diagnosis
from app.models.hospital_record import HospitalRecord
from app.models.lab_report import LabReport
from app.models.manual_entry import ManualEntry
from app.models.medication import Medication
from app.models.prescription import Prescription
from app.models.vaccination import Vaccination
from app.models.vital_sign import VitalSign
from app.models.wearable_data import WearableData

from app.schemas.timeline import TimelineEvent, TimelineResponse


class TimelineService:

    def get_timeline(
        self,
        db: Session,
        patient_id: UUID,
    ) -> TimelineResponse:

        events: list[TimelineEvent] = []

        events.extend(self._diagnosis_events(db, patient_id))
        events.extend(self._medication_events(db, patient_id))
        events.extend(self._allergy_events(db, patient_id))
        events.extend(self._hospital_record_events(db, patient_id))
        events.extend(self._prescription_events(db, patient_id))
        events.extend(self._lab_report_events(db, patient_id))
        events.extend(self._vaccination_events(db, patient_id))
        events.extend(self._vital_sign_events(db, patient_id))
        events.extend(self._wearable_events(db, patient_id))
        events.extend(self._manual_entry_events(db, patient_id))

        events.sort(
            key=lambda event: event.event_date,
            reverse=True,
        )

        return TimelineResponse(events=events)

    def _create_event(
        self,
        *,
        id: UUID,
        event_type: str,
        title: str,
        event_date: datetime,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> TimelineEvent:

        return TimelineEvent(
            id=id,
            event_type=event_type,
            title=title,
            description=description,
            event_date=event_date,
            metadata=metadata or {},
        )
    


    def _diagnosis_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        diagnoses = (
            db.query(Diagnosis)
            .filter(Diagnosis.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for diagnosis in diagnoses:

            event_date = (
                datetime.combine(diagnosis.diagnosis_date, time.min)
                if diagnosis.diagnosis_date
                else diagnosis.created_at
            )

            events.append(
                self._create_event(
                    id=diagnosis.id,
                    event_type="Diagnosis",
                    title=diagnosis.diagnosis_name,
                    description=diagnosis.notes,
                    event_date=event_date,
                    metadata={
                        "severity": diagnosis.severity,
                        "status": diagnosis.status,
                        "doctor": diagnosis.diagnosed_by,
                        "icd10": diagnosis.icd10_code,
                        "source": diagnosis.source,
                    },
                )
            )

        return events


    def _medication_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        medications = (
            db.query(Medication)
            .filter(Medication.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for medication in medications:

            event_date = (
                datetime.combine(medication.start_date, time.min)
                if medication.start_date
                else medication.created_at
            )

            events.append(
                self._create_event(
                    id=medication.id,
                    event_type="Medication",
                    title=f"Started {medication.medication_name}",
                    description=medication.indication or medication.notes,
                    event_date=event_date,
                    metadata={
                        "generic_name": medication.generic_name,
                        "brand_name": medication.brand_name,
                        "dosage": medication.dosage,
                        "dosage_form": medication.dosage_form.value,
                        "route": medication.route.value,
                        "frequency": medication.frequency.value,
                        "start_date": medication.start_date,
                        "end_date": medication.end_date,
                        "is_active": medication.is_active,
                    },
                )
            )

        return events


    def _allergy_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        allergies = (
            db.query(Allergy)
            .filter(Allergy.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for allergy in allergies:

            event_date = (
                datetime.combine(allergy.diagnosed_date, time.min)
                if allergy.diagnosed_date
                else allergy.created_at
            )

            events.append(
                self._create_event(
                    id=allergy.id,
                    event_type="Allergy",
                    title=f"Diagnosed Allergy: {allergy.allergy_name}",
                    description=allergy.reaction or allergy.notes,
                    event_date=event_date,
                    metadata={
                        "type": allergy.allergy_type.value,
                        "severity": allergy.severity.value,
                        "is_active": allergy.is_active,
                        "diagnosed_date": allergy.diagnosed_date,
                    },
                )
            )

        return events
    
    def _hospital_record_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        records = (
            db.query(HospitalRecord)
            .filter(HospitalRecord.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for record in records:

            event_date = datetime.combine(
                record.visit_date,
                time.min,
            )

            events.append(
                self._create_event(
                    id=record.id,
                    event_type="Hospital Visit",
                    title=f"Visited {record.hospital_name}",
                    description=record.summary,
                    event_date=event_date,
                    metadata={
                        "doctor": record.doctor_name,
                        "record_type": record.record_type,
                        "source_file": record.source_file,
                        "extracted_by_ai": record.extracted_by_ai,
                        "extraction_status": record.extraction_status,
                    },
                )
            )

        return events


    def _prescription_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        prescriptions = (
            db.query(Prescription)
            .filter(Prescription.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for prescription in prescriptions:

            event_date = datetime.combine(
                prescription.prescription_date,
                time.min,
            )

            events.append(
                self._create_event(
                    id=prescription.id,
                    event_type="Prescription",
                    title=f"Prescription by Dr. {prescription.doctor_name}",
                    description=prescription.instructions or prescription.notes,
                    event_date=event_date,
                    metadata={
                        "doctor": prescription.doctor_name,
                        "diagnosis": prescription.diagnosis,
                        "status": prescription.status.value,
                        "number_of_medicines": len(prescription.items),
                        "hospital_record_id": (
                            str(prescription.hospital_record_id)
                            if prescription.hospital_record_id
                            else None
                        ),
                    },
                )
            )

        return events


    def _lab_report_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        reports = (
            db.query(LabReport)
            .filter(LabReport.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for report in reports:

            event_date = datetime.combine(
                report.report_date,
                time.min,
            )

            events.append(
                self._create_event(
                    id=report.id,
                    event_type="Lab Report",
                    title=report.report_name,
                    description=report.notes,
                    event_date=event_date,
                    metadata={
                        "category": report.category.value,
                        "status": report.status.value,
                        "laboratory": report.laboratory_name,
                        "doctor": report.doctor_name,
                        "number_of_results": len(report.results),
                        "hospital_record_id": (
                            str(report.hospital_record_id)
                            if report.hospital_record_id
                            else None
                        ),
                    },
                )
            )

        return events
    
    def _vaccination_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        vaccinations = (
            db.query(Vaccination)
            .filter(Vaccination.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for vaccination in vaccinations:

            event_date = datetime.combine(
                vaccination.administered_date,
                time.min,
            )

            events.append(
                self._create_event(
                    id=vaccination.id,
                    event_type="Vaccination",
                    title=f"{vaccination.vaccine_name} Vaccination",
                    description=vaccination.notes,
                    event_date=event_date,
                    metadata={
                        "manufacturer": vaccination.manufacturer,
                        "dose_number": vaccination.dose_number,
                        "administered_by": vaccination.administered_by,
                        "batch_number": vaccination.batch_number,
                        "status": vaccination.status,
                        "next_due_date": vaccination.next_due_date,
                    },
                )
            )

        return events


    def _vital_sign_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        vitals = (
            db.query(VitalSign)
            .filter(VitalSign.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for vital in vitals:

            summary = []

            if vital.heart_rate is not None:
                summary.append(f"HR: {vital.heart_rate} bpm")

            if (
                vital.systolic_bp is not None
                and vital.diastolic_bp is not None
            ):
                summary.append(
                    f"BP: {vital.systolic_bp}/{vital.diastolic_bp} mmHg"
                )

            if vital.body_temperature is not None:
                summary.append(f"Temp: {vital.body_temperature}°C")

            if vital.oxygen_saturation is not None:
                summary.append(f"SpO₂: {vital.oxygen_saturation}%")

            description = ", ".join(summary) if summary else vital.notes

            events.append(
                self._create_event(
                    id=vital.id,
                    event_type="Vital Sign",
                    title="Vital Signs Recorded",
                    description=description,
                    event_date=vital.recorded_at,
                    metadata={
                        "source": vital.source,
                        "device_name": vital.device_name,
                        "heart_rate": vital.heart_rate,
                        "systolic_bp": vital.systolic_bp,
                        "diastolic_bp": vital.diastolic_bp,
                        "respiratory_rate": vital.respiratory_rate,
                        "body_temperature": vital.body_temperature,
                        "oxygen_saturation": vital.oxygen_saturation,
                        "height_cm": vital.height_cm,
                        "weight_kg": vital.weight_kg,
                        "bmi": vital.bmi,
                        "notes": vital.notes,
                    },
                )
            )

        return events


    def _wearable_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        wearables = (
            db.query(WearableData)
            .filter(WearableData.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for wearable in wearables:

            summary = []

            if wearable.steps is not None:
                summary.append(f"{wearable.steps} steps")

            if wearable.calories_burned is not None:
                summary.append(f"{wearable.calories_burned} kcal")

            if wearable.sleep_hours is not None:
                summary.append(f"{wearable.sleep_hours} hrs sleep")

            if wearable.distance_km is not None:
                summary.append(f"{wearable.distance_km} km")

            description = ", ".join(summary) if summary else wearable.notes

            events.append(
                self._create_event(
                    id=wearable.id,
                    event_type="Wearable Data",
                    title=f"{wearable.source.value} Sync",
                    description=description,
                    event_date=wearable.recorded_at,
                    metadata={
                        "device_name": wearable.device_name,
                        "source": wearable.source.value,
                        "steps": wearable.steps,
                        "calories_burned": wearable.calories_burned,
                        "distance_km": wearable.distance_km,
                        "active_minutes": wearable.active_minutes,
                        "sleep_hours": wearable.sleep_hours,
                        "resting_heart_rate": wearable.resting_heart_rate,
                        "heart_rate_variability": wearable.heart_rate_variability,
                        "vo2_max": wearable.vo2_max,
                        "stress_level": wearable.stress_level,
                        "notes": wearable.notes,
                    },
                )
            )

        return events


    def _manual_entry_events(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[TimelineEvent]:

        entries = (
            db.query(ManualEntry)
            .filter(ManualEntry.patient_id == patient_id)
            .all()
        )

        events: list[TimelineEvent] = []

        for entry in entries:

            description = (
                f"{entry.metric_value} {entry.unit}"
                if entry.unit
                else str(entry.metric_value)
            )

            events.append(
                self._create_event(
                    id=entry.id,
                    event_type="Manual Entry",
                    title=entry.metric_name,
                    description=description,
                    event_date=entry.recorded_at,
                    metadata={
                        "category": entry.category,
                        "notes": entry.notes,
                    },
                )
            )

        return events
    
timeline_service = TimelineService()