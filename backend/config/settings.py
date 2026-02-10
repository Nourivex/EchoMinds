"""
Configuration management untuk EchoMinds Backend
Menggunakan Pydantic Settings untuk type-safe config
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings dengan environment variable support"""
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_reload: bool = Field(default=True, env="API_RELOAD")
    debug: bool = Field(default=True, env="DEBUG")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:5173"],
        env="CORS_ORIGINS"
    )
    
    # LLM Configuration
    llm_provider: str = Field(default="ollama", env="LLM_PROVIDER")  # ollama or llamacpp
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    default_model: str = Field(default="llama3.2:3b", env="DEFAULT_MODEL")
    
    # Resource Allocation
    cpu_threads: int = Field(default=4, env="CPU_THREADS")
    gpu_layers: int = Field(default=0, env="GPU_LAYERS")  # 0=CPU, -1=all GPU, N=first N layers
    context_length: int = Field(default=4096, env="CONTEXT_LENGTH")
    max_tokens: int = Field(default=512, env="MAX_TOKENS")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    
    # Vector Database
    vector_db_path: Path = Field(default=Path("../data/vectorstore"), env="VECTOR_DB_PATH")
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        env="EMBEDDING_MODEL"
    )
    collection_prefix: str = Field(default="echominds_", env="COLLECTION_PREFIX")
    
    # Storage Paths
    character_data_path: Path = Field(
        default=Path("../data/characters"),
        env="CHARACTER_DATA_PATH"
    )
    conversation_data_path: Path = Field(
        default=Path("../data/conversations"),
        env="CONVERSATION_DATA_PATH"
    )
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Path = Field(default=Path("logs/echominds.log"), env="LOG_FILE")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
        self.character_data_path.mkdir(parents=True, exist_ok=True)
        self.conversation_data_path.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
