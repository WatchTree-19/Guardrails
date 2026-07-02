# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The rich, structured outcome of a single rail check.

``RailOutcome`` is the canonical result a rail produces, superseding three
narrower encodings that exist today:

- ``RailResult(is_safe, reason)`` on the IORails path,
- the lossy ``output_mapping`` boolean consulted on the streaming and
  parallel bypass paths, and
- the raw heterogeneous return values (bool, str, dict, vendor models) that
  Colang flows interpret by hand.

It carries the full outcome spectrum observed across the rail library so a
single implementation per rail can drive both the Colang runtime and the
IORails engine without either side losing information.

This module is additive: nothing consumes ``RailOutcome`` yet. Adapters on
each engine are introduced in later phases.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RailDecision(Enum):
    """The three mutually exclusive things a rail can decide."""

    ALLOW = "allow"
    BLOCK = "block"
    TRANSFORM = "transform"


class TransformTarget(Enum):
    """The conversation variable a transform rewrites."""

    USER_MESSAGE = "user_message"
    BOT_MESSAGE = "bot_message"
    RELEVANT_CHUNKS = "relevant_chunks"


@dataclass(frozen=True, slots=True)
class BlockSpec:
    """How a BLOCK decision is carried out.

    ``abort`` records whether the flow stops the turn (hard block) or emits a
    message and continues (soft block). It is recorded from the rail's actual
    behavior, never inferred: the ``patronus api check output`` flow blocks
    without aborting, and that distinction must survive.

    A block may name a typed ``exception_type`` (used when
    ``enable_rails_exceptions`` is set), a dialog ``refusal_intent`` resolved
    by the NLU layer (e.g. ``refuse to respond``), or an already-resolved
    literal ``refusal_message`` with its ``language`` (multilingual refusal).
    """

    abort: bool = True
    exception_type: str | None = None
    refusal_intent: str | None = None
    refusal_message: str | None = None
    language: str | None = None


@dataclass(frozen=True, slots=True)
class TransformSpec:
    """A rewrite of a single conversation variable."""

    target: TransformTarget
    text: str


@dataclass(frozen=True, slots=True)
class RailOutcome:
    """The structured verdict of one rail check.

    ``block`` is set if and only if ``decision`` is BLOCK; ``transform`` is set
    if and only if ``decision`` is TRANSFORM. ``metadata`` holds side data that
    flows expose as globals (policy violations, scores, categories, reasoning
    traces) and is never load-bearing for the decision itself. ``events`` and
    ``context_updates`` preserve the Colang ``ActionResult`` channels so the
    Colang adapter loses nothing.
    """

    decision: RailDecision
    reason: str | None = None
    block_spec: BlockSpec | None = None
    transform_spec: TransformSpec | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    events: tuple[dict[str, Any], ...] = ()
    context_updates: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if (self.block_spec is not None) != (self.decision is RailDecision.BLOCK):
            raise ValueError("block_spec must be set if and only if decision is BLOCK")
        if (self.transform_spec is not None) != (self.decision is RailDecision.TRANSFORM):
            raise ValueError("transform_spec must be set if and only if decision is TRANSFORM")

    @property
    def is_blocked(self) -> bool:
        """Single source the streaming and parallel bypass paths read."""
        return self.decision is RailDecision.BLOCK

    @classmethod
    def allow(cls, *, reason: str | None = None, **metadata: Any) -> "RailOutcome":
        return cls(decision=RailDecision.ALLOW, reason=reason, metadata=dict(metadata))

    @classmethod
    def block(
        cls,
        *,
        abort: bool = True,
        exception_type: str | None = None,
        refusal_intent: str | None = None,
        refusal_message: str | None = None,
        language: str | None = None,
        reason: str | None = None,
        **metadata: Any,
    ) -> "RailOutcome":
        return cls(
            decision=RailDecision.BLOCK,
            reason=reason,
            block_spec=BlockSpec(
                abort=abort,
                exception_type=exception_type,
                refusal_intent=refusal_intent,
                refusal_message=refusal_message,
                language=language,
            ),
            metadata=dict(metadata),
        )

    @classmethod
    def transform(
        cls,
        target: TransformTarget,
        text: str,
        *,
        reason: str | None = None,
        **metadata: Any,
    ) -> "RailOutcome":
        return cls(
            decision=RailDecision.TRANSFORM,
            reason=reason,
            transform_spec=TransformSpec(target=target, text=text),
            metadata=dict(metadata),
        )
