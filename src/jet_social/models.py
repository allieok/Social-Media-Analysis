"""Versioned pilot contracts. Metric windows and missingness stay explicit."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Consent(Contract):
    consent_id: UUID
    status: Literal["active", "withdrawn"]
    purposes: list[Literal["analysis", "review", "planning", "posters"]]
    expires_at: AwareDatetime
    external_model_processing: bool = False


class MetricSnapshot(Contract):
    observed_at: AwareDatetime
    window_hours: int = Field(gt=0)
    source: Literal["owner_export", "permitted_api", "synthetic"]
    reach: int | None = Field(default=None, ge=0)
    saves: int | None = Field(default=None, ge=0)
    shares: int | None = Field(default=None, ge=0)
    missing_reason: str | None = None

    @model_validator(mode="after")
    def explain_missing(self):
        if any(v is None for v in (self.reach, self.saves, self.shares)):
            if not self.missing_reason or not self.missing_reason.strip():
                raise ValueError("Missing metrics require a missing_reason")
        return self


class FeatureEvent(Contract):
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    kind: Literal["hook", "value", "proof", "cta", "person_presence", "screen_text"]
    value: str = Field(min_length=1)
    source: Literal["human", "synthetic", "asr", "ocr", "vlm", "rule"]
    confidence: float | None = Field(default=None, ge=0, le=1)

    @model_validator(mode="after")
    def ordered(self):
        if self.end_ms <= self.start_ms:
            raise ValueError("Feature interval must have positive duration")
        return self


class Post(Contract):
    post_id: UUID
    account_id: UUID
    consent: Consent
    platform: Literal["instagram_reels", "tiktok"]
    published_at: AwareDatetime
    duration_ms: int = Field(gt=0, le=180000)
    purpose: Literal["event", "community", "education", "entertainment"]
    campaign_id: UUID | None = None
    paid: bool | None = None
    collaboration: bool | None = None
    follower_snapshot: int | None = Field(default=None, ge=0)
    metrics: MetricSnapshot
    features: list[FeatureEvent] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_times(self):
        if self.metrics.observed_at < self.published_at:
            raise ValueError("Metric observation precedes publication")
        elapsed = (self.metrics.observed_at - self.published_at).total_seconds()
        if elapsed < self.metrics.window_hours * 3600:
            raise ValueError("Observation does not cover the declared metric window")
        if any(f.end_ms > self.duration_ms for f in self.features):
            raise ValueError("Feature interval exceeds video duration")
        return self


class Dataset(Contract):
    schema_version: Literal["1.0"] = "1.0"
    synthetic: bool
    posts: list[Post] = Field(min_length=1)

    @model_validator(mode="after")
    def check_identity_and_source(self):
        ids = [p.post_id for p in self.posts]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate post_id")
        for post in self.posts:
            if (post.metrics.source == "synthetic") != self.synthetic:
                raise ValueError("Synthetic status and metric source must agree")
            if not self.synthetic and any(f.source == "synthetic" for f in post.features):
                raise ValueError("Real datasets cannot contain synthetic features")
        return self

    def authorize(self, now: datetime) -> None:
        for post in self.posts:
            consent = post.consent
            if consent.status != "active" or consent.expires_at <= now:
                raise ValueError("Processing blocked: consent withdrawn or expired")
            if "analysis" not in consent.purposes:
                raise ValueError("Processing blocked: analysis not authorized")
