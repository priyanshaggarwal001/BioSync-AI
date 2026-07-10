from enum import Enum


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer Not To Say"


class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class AllergyType(str, Enum):
    DRUG = "Drug"
    FOOD = "Food"
    ENVIRONMENTAL = "Environmental"
    INSECT = "Insect"
    LATEX = "Latex"
    OTHER = "Other"


class AllergySeverity(str, Enum):
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    LIFE_THREATENING = "Life Threatening"
from enum import Enum


class LabReportCategory(str, Enum):
    BLOOD = "Blood"
    URINE = "Urine"
    IMAGING = "Imaging"
    GENETIC = "Genetic"
    PATHOLOGY = "Pathology"
    OTHER = "Other"


class LabReportStatus(str, Enum):
    NORMAL = "Normal"
    ABNORMAL = "Abnormal"
    CRITICAL = "Critical"
    PENDING = "Pending"

class LabResultStatus(str, Enum):
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    CRITICAL = "Critical"
from enum import Enum


class MedicationDosageForm(str, Enum):
    TABLET = "Tablet"
    CAPSULE = "Capsule"
    SYRUP = "Syrup"
    INJECTION = "Injection"
    CREAM = "Cream"
    DROPS = "Drops"
    INHALER = "Inhaler"
    OTHER = "Other"


class MedicationRoute(str, Enum):
    ORAL = "Oral"
    IV = "IV"
    IM = "IM"
    SUBCUTANEOUS = "Subcutaneous"
    TOPICAL = "Topical"
    INHALATION = "Inhalation"
    OTHER = "Other"


class MedicationFrequency(str, Enum):
    ONCE_DAILY = "Once Daily"
    TWICE_DAILY = "Twice Daily"
    THREE_TIMES_DAILY = "Three Times Daily"
    FOUR_TIMES_DAILY = "Four Times Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    AS_NEEDED = "As Needed"


class PrescriptionStatus(str, Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    
class DataSource(str, Enum):
    MANUAL = "manual"
    HOSPITAL = "hospital"
    LAB = "lab"
    APPLE_HEALTH = "apple_health"
    GOOGLE_FIT = "google_fit"
    FITBIT = "fitbit"
    GARMIN = "garmin"
    SAMSUNG_HEALTH = "samsung_health"
    WHOOP = "whoop"
    API = "api"
    OTHER = "other"