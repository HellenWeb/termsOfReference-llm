from enum import StrEnum


class GenerationStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class CreditTransactionType(StrEnum):
    WELCOME = "welcome"
    REFERRAL = "referral"
    PROMO = "promo"
    PURCHASE = "purchase"
    GENERATION_DEBIT = "generation_debit"
    REFUND = "refund"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
