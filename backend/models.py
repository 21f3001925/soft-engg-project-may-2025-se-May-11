from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import enum
import secrets
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class AlertType(enum.Enum):
    missed_medication = "missed_medication"
    emergency = "emergency"


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.String(36), db.ForeignKey("user.user_id")),
    db.Column("role_id", db.String(36), db.ForeignKey("role.id")),
)


class ReferenceType(enum.Enum):
    medication = "medication"
    appointment = "appointment"
    event = "event"


class Role(db.Model, RoleMixin):  # type: ignore
    __tablename__ = "role"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship("User", secondary=roles_users, back_populates="roles")


class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = "user"
    user_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        default=lambda: secrets.token_urlsafe(32),
    )
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    roles = db.relationship("Role", secondary=roles_users, back_populates="users")
    senior_citizen = db.relationship(
        "SeniorCitizen",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    caregiver = db.relationship(
        "Caregiver", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    alerts = db.relationship(
        "Alert", back_populates="recipient", cascade="all, delete-orphan"
    )
    name = db.Column(db.String)
    avatar_url = db.Column(db.String)


class SeniorCitizen(db.Model):  # type: ignore
    __tablename__ = "seniorcitizen"
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    font_size = db.Column(db.String)
    theme = db.Column(db.String)

    user = relationship("User", back_populates="senior_citizen")
    appointments = relationship(
        "Appointment", back_populates="senior", cascade="all, delete-orphan"
    )
    medications = relationship(
        "Medication", back_populates="senior", cascade="all, delete-orphan"
    )
    emergency_contacts = relationship(
        "EmergencyContact", back_populates="senior", cascade="all, delete-orphan"
    )
    caregiver_assignments = relationship(
        "CaregiverAssignment", back_populates="senior", cascade="all, delete-orphan"
    )
    event_attendance = relationship(
        "EventAttendance", back_populates="senior", cascade="all, delete-orphan"
    )


class Caregiver(db.Model):  # type: ignore
    __tablename__ = "caregiver"
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )

    user = relationship("User", back_populates="caregiver")
    assignments = relationship(
        "CaregiverAssignment", back_populates="caregiver", cascade="all, delete-orphan"
    )


class CaregiverAssignment(db.Model):  # type: ignore
    __tablename__ = "caregiver_assignment"
    caregiver_id = db.Column(
        db.String(36),
        db.ForeignKey("caregiver.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    senior_id = db.Column(
        db.String(36),
        db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE"),
        primary_key=True,
    )

    caregiver = relationship("Caregiver", back_populates="assignments")
    senior = relationship("SeniorCitizen", back_populates="caregiver_assignments")


class Appointment(db.Model):  # type: ignore
    __tablename__ = "appointment"
    appointment_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title = db.Column(db.String)
    date_time = db.Column(db.DateTime)
    location = db.Column(db.String)
    senior_id = db.Column(
        db.String(36), db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE")
    )
    reminder_task_id = db.Column(db.String(36), nullable=True)

    senior = relationship("SeniorCitizen", back_populates="appointments")


class Medication(db.Model):  # type: ignore
    __tablename__ = "medication"
    medication_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String)
    dosage = db.Column(db.String)
    time = db.Column(db.DateTime)
    isTaken = db.Column(db.Boolean, default=False)
    senior_id = db.Column(
        db.String(36), db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE")
    )

    senior = relationship("SeniorCitizen", back_populates="medications")


class EmergencyContact(db.Model):  # type: ignore
    __tablename__ = "emergency_contact"
    contact_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String)
    relation = db.Column(db.String)
    phone = db.Column(db.String)
    senior_id = db.Column(
        db.String(36), db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE")
    )

    senior = relationship("SeniorCitizen", back_populates="emergency_contacts")


class Feedback(db.Model):  # type: ignore
    __tablename__ = "news"
    news_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    api_article_id = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    url = db.Column(db.String)
    source = db.Column(db.String)
    category = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class ServiceProvider(db.Model):  # type: ignore
    __tablename__ = "service_provider"
    service_provider_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String, nullable=False)
    contact_email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)
    services_offered = db.Column(db.String)
    events = relationship(
        "Event", back_populates="service_provider", cascade="all, delete-orphan"
    )


class Event(db.Model):  # type: ignore
    __tablename__ = "event"
    event_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String)
    date_time = db.Column(db.DateTime)
    location = db.Column(db.String)
    description = db.Column(db.Text)
    service_provider_id = db.Column(
        db.String(36),
        db.ForeignKey("service_provider.service_provider_id", ondelete="CASCADE"),
    )

    service_provider = relationship("ServiceProvider", back_populates="events")
    attendance = relationship(
        "EventAttendance", back_populates="event", cascade="all, delete-orphan"
    )


class EventAttendance(db.Model):  # type: ignore
    __tablename__ = "event_attendance"
    senior_id = db.Column(
        db.String(36),
        db.ForeignKey("seniorcitizen.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    event_id = db.Column(
        db.String(36),
        db.ForeignKey("event.event_id", ondelete="CASCADE"),
        primary_key=True,
    )

    senior = relationship("SeniorCitizen", back_populates="event_attendance")
    event = relationship("Event", back_populates="attendance")


class Alert(db.Model):  # type: ignore
    __tablename__ = "alert"
    alert_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    recipient_user_id = db.Column(
        db.String(36), db.ForeignKey("user.user_id", ondelete="CASCADE")
    )
    alert_type = db.Column(db.Enum(AlertType))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    reference_type = db.Column(db.Enum(ReferenceType))
    reference_id = db.Column(db.String(36))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    recipient = relationship("User", back_populates="alerts")
