"""Configuration management for export-geoconfirmed."""

from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    service_name: str = Field(..., alias="SERVICE_NAME")
    project_id: str = Field(..., alias="PROJECT_ID")
    region: str = Field(..., alias="REGION")
    runtime: str = Field(..., alias="RUNTIME")
    timeout: int = Field(..., alias="TIMEOUT")
    runtime_service_account_email: EmailStr = Field(..., alias="RUNTIME_SERVICE_ACCOUNT_EMAIL")

    # BigQuery settings
    bq_dataset: str = Field(default="geolocations", alias="BQ_DATASET")
    bq_table: str = Field(default="geoconfirmed_events", alias="BQ_TABLE")

    model_config = {
        "env_file": "project.env",
        "case_sensitive": False,
        "extra": "allow",
    }


settings = Settings()
