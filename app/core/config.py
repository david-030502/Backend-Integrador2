from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str = Field(default="", validation_alias="DB_NAME")
    db_user: str = Field(default="postgres", validation_alias="DB_USER")
    db_password: str = Field(default="", validation_alias="DB_PASSWORD")
    db_host: str = Field(default="localhost", validation_alias="DB_HOST")
    db_port: int = Field(default=5432, validation_alias="DB_PORT")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class JwtSettings(BaseSettings):
    secret: str = Field(validation_alias="JWT_SECRET")
    algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    expire_minutes: int = Field(default=60, validation_alias="JWT_EXPIRE_MINUTES")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("secret")
    @classmethod
    def validar_secret(cls, valor: str) -> str:
        if not valor or not valor.strip():
            raise ValueError("JWT_SECRET no puede estar vacío")
        if len(valor) < 32:
            raise ValueError("JWT_SECRET debe tener al menos 32 caracteres")
        return valor


class HmacSettings(BaseSettings):
    secret: str = Field(validation_alias="SENAVI_HMAC_SECRET")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("secret")
    @classmethod
    def validar_secret(cls, valor: str) -> str:
        if not valor or not valor.strip():
            raise ValueError("SENAVI_HMAC_SECRET no puede estar vacío")
        return valor


settings = Settings()
jwt_settings = JwtSettings()
configuracion_hmac = HmacSettings()
