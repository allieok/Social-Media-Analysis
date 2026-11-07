"""Contract for a future provider; no live adapter is implemented or selected."""

from typing import Protocol

from jet_social.models import FeatureEvent


class VideoFeatureProvider(Protocol):
    name: str
    model_version: str

    def extract(self, approved_media_path: str, duration_ms: int) -> list[FeatureEvent]: ...
