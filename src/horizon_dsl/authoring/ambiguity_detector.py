from __future__ import annotations


def detect_ambiguities(intent_text: str) -> list[str]:
    ambiguities: list[str] = []
    lowered = intent_text.lower()

    if "merchant" in lowered and "merchant_id" not in lowered:
        ambiguities.append("Merchant identifier field is not explicit; assume `merchant_id` until clarified.")
    if "device" in lowered and "device_id" not in lowered:
        ambiguities.append("Device identifier field is not explicit; assume `device_id` until clarified.")
    if "score" in lowered and "inclusive" not in lowered:
        ambiguities.append("Score band boundaries are assumed inclusive but should be confirmed.")
    if "approve" in lowered and "below 800" not in lowered:
        ambiguities.append("Default approval path is inferred from the narrative and should be confirmed.")
    if "model" in lowered and "version" not in lowered:
        ambiguities.append("Model version is missing and needs clarification.")

    return ambiguities
