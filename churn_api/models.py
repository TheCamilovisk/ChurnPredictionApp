from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Gender(str, Enum):
    male = "Male"
    female = "Female"


class BooleanMeta(str, Enum):
    no = "No"
    yes = "Yes"


class InternetService(str, Enum):
    no = "No"
    fiber_optic = "Fiber optic"
    dsl = "DSL"


class PhoneDependentService(str, Enum):
    no_service = "No phone service"
    no = "No"
    yes = "Yes"


class InternetDependentService(str, Enum):
    no_service = "No internet service"
    no = "No"
    yes = "Yes"


class Contract(str, Enum):
    monthly = "Month-to-month"
    yealy = "One year"
    two_year = "Two year Contract"


class PaymentMethod(str, Enum):
    electronic = "Electronic check"
    mailed = "Mailed check"
    bank_transfer = "Bank transfer (automatic)"
    credit_card = "Credit card (automatic)"


class Payload(BaseModel):
    customerID: Optional[str]
    gender: Gender
    SeniorCitizen: BooleanMeta
    Partner: BooleanMeta
    Dependents: BooleanMeta
    tenure: int
    PhoneService: BooleanMeta
    MultipleLines: PhoneDependentService
    InternetService: InternetService
    OnlineSecurity: InternetDependentService
    OnlineBackup: InternetDependentService
    DeviceProtection: InternetDependentService
    TechSupport: InternetDependentService
    StreamingTV: InternetDependentService
    StreamingMovies: InternetDependentService
    Contract: Contract
    PaperlessBilling: BooleanMeta
    PaymentMethod: PaymentMethod
    MonthlyCharges: float
    TotalCharges: float
