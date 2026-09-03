from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Float,
)

from sqlalchemy.orm import declarative_base

from datetime import datetime

import os

from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# ============================================================
# BASE
# ============================================================

Base = declarative_base()


# ============================================================
# CANDIDATE
# ============================================================

class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    candidate_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
    )

    password_hash = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


# ============================================================
# INTERVIEW
# ============================================================

class Interview(Base):

    __tablename__ = "interviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    candidate_id = Column(
        String,
        nullable=False,
    )

    role = Column(
        String,
        nullable=False,
    )

    difficulty = Column(
        String,
        nullable=False,
    )

    interview_type = Column(
        String,
        nullable=False,
    )

    max_rounds = Column(
        Integer,
        nullable=False,
    )

    status = Column(
        String,
        default="in_progress",
    )

    final_report = Column(
        Text,
        nullable=True,
    )

    # ========================================================
    # VIDEO ANALYSIS
    # ========================================================

    video_path = Column(
        Text,
        nullable=True,
    )

    video_duration_seconds = Column(
        Float,
        nullable=True,
    )

    video_fps = Column(
        Float,
        nullable=True,
    )

    video_width = Column(
        Integer,
        nullable=True,
    )

    video_height = Column(
        Integer,
        nullable=True,
    )

    video_analyzed_frames = Column(
        Integer,
        nullable=True,
    )

    face_detected_frames = Column(
        Integer,
        nullable=True,
    )

    face_visibility_percentage = Column(
        Float,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


# ============================================================
# INTERVIEW ANSWER
# ============================================================

class InterviewAnswer(Base):

    __tablename__ = "interview_answers"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    interview_id = Column(
        Integer,
        ForeignKey("interviews.id"),
        nullable=False,
    )

    round = Column(
        Integer,
        nullable=False,
    )

    question = Column(
        Text,
        nullable=False,
    )

    answer = Column(
        Text,
        nullable=False,
    )

    feedback = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )