"""포지션 성격에 따른 capability / experience 가중치 매핑.

PROCESS.md 기준:
- Backend / Frontend (스킬 중심): capability 0.7, experience 0.3
- PL / PM (경험 중심):             capability 0.2, experience 0.8
- QA (균등):                       capability 0.5, experience 0.5
"""

from __future__ import annotations

# (capability_weight, experience_weight)
_POSITION_WEIGHTS: dict[str, tuple[float, float]] = {
    # 경험 중심
    "PL":   (0.2, 0.8),
    "PM":   (0.2, 0.8),
    "SA":   (0.3, 0.7),
    "TL":   (0.3, 0.7),
    "PO":   (0.2, 0.8),
    "기획자": (0.2, 0.8),
}

_ROLE_WEIGHTS: dict[str, tuple[float, float]] = {
    "DEVELOPER": (0.7, 0.3),
    "PUBLISHER": (0.7, 0.3),
    "PLANNER":   (0.2, 0.8),
    "QA":        (0.5, 0.5),
    "DESIGNER":  (0.4, 0.6),
}

_DEFAULT_WEIGHTS = (0.5, 0.5)


def get_weights(
    position: str,
    engineer_role: str = "",
    client_weights: dict[str, float] | None = None,
) -> tuple[float, float]:
    """포지션명 → (capability_weight, experience_weight) 반환.

    우선순위:
    1. position 이름으로 매핑 (PL, PM 등 경험 중심 포지션)
    2. engineer_role 로 매핑 (DEVELOPER, QA 등)
    3. client_weights (1depth 기본값 — 포지션/역할 매핑이 없을 때 폴백)
    4. 기본값 (0.5, 0.5)
    """
    upper_pos = position.upper().strip()
    if upper_pos in _POSITION_WEIGHTS:
        return _POSITION_WEIGHTS[upper_pos]

    upper_role = engineer_role.upper().strip()
    if upper_role in _ROLE_WEIGHTS:
        return _ROLE_WEIGHTS[upper_role]

    if client_weights:
        cap = client_weights.get("capability", 0.5)
        exp = client_weights.get("experience", 0.5)
        return (cap, exp)

    return _DEFAULT_WEIGHTS
