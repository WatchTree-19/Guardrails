# Actions Decoupling Execution Plan

This is the working plan for finishing the actions decoupling work phase by
phase. It supersedes the older static gate-sweep wording for day-to-day
execution, while keeping the same north star: one vendor implementation per
rail, with `RailOutcome` as the single Python decision result.

## Operating Rules

- Work one phase at a time.
- Each phase should end with focused tests and a focused commit.
- Do not use vendor credentials as the correctness bar.
- VCR replay is nice extra coverage only where stable cassettes already exist.
- Parser and action unit tests stay separate from runtime flow equivalence.
- Streaming and parallel output bypass tests stay separate because they do not
  run the normal Colang flow path.
- Adjudication cases are made explicit. Do not hide divergence by preserving the
  wrong path.

## Correctness Split

There are two different legacy paths, so they get two different proof surfaces.

| Surface | What it proves | Comparison |
| --- | --- | --- |
| Runtime flow oracle | The normal Colang library flow decision still matches the new interpreter. | Real flow execution with stubbed action raw return equals `RailOutcome` decision. |
| Output bypass | The streaming and parallel bypass path stops using legacy boolean mapping as a separate decision source. | Legacy `output_mapping`, where it actually runs today, equals `RailOutcome` until the mapping is deleted. |

Input rails never consult `output_mapping`, so input runtime tests must not
compare against it. Output mapping is only relevant for output-rail bypasses.

## Phase 0: Baseline And Matrix

Status: mostly complete.

Deliverables:

- Audit library rail flow gates.
- Sort rails into clean boolean, clean `RailOutcome`, threshold, dict flag,
  transform, and adjudication families.
- Record known divergences as owner decisions, not hidden test assumptions.

Artifacts:

- `arch/actions/offline-flow-gate-matrix.md`
- `tests/test_output_mapping_rail_outcome_equivalence.py`
- `tests/test_runtime_flow_gate_equivalence.py`

Gate:

- Matrix is committed.
- Existing focused equivalence tests pass offline.

## Phase 1: Runtime Flow Oracle Harness

Status: in progress.

Goal:

Run real Colang library flows as the oracle while replacing only the action
implementation with a stub that returns synthetic raw values.

Deliverables:

- Reusable `RailSpec` table with flow name, direction, action name, model type,
  task, parser, and rail config.
- Minimal `RailsConfig.from_content(config=...)` builder.
- `TestChat` plus `LLMRails` execution with registered stub actions.
- Two-layer classification:
  - Observable rendering: allow, refusal, exception, transform.
  - Decision: allow, block, transform.
- `enable_rails_exceptions` parametrized as rendering, not a separate verdict.

Already covered:

- `self check input`
- `self check output`
- `self check facts`
- `alignscore check facts`
- `hf classifier check input`
- `hf classifier check output`
- `llama guard check input`
- `llama guard check output`
- `policyai moderation on input`
- `policyai moderation on output`
- `regex check input`
- `regex check output`
- `detect pii on input`
- `detect pii on output`
- `gliner detect pii on input`
- `gliner detect pii on output`
- `detect sensitive data on input`
- `detect sensitive data on output`
- `mask pii on input`
- `mask pii on output`
- `mask pii on retrieval`
- `gliner mask pii on input`
- `gliner mask pii on output`
- `gliner mask pii on retrieval`
- `mask sensitive data on input`
- `mask sensitive data on output`
- `mask sensitive data on retrieval`
- `pangea ai guard input`
- `pangea ai guard output`
- `crowdstrike aidr guard input`
- `crowdstrike aidr guard output`
- `protect prompt`
- `protect response`
- `content safety check output`
- `topic safety check input`
- `jailbreak detection heuristics`
- `jailbreak detection model`

Next tasks:

1. Add remaining transform rails after that.

Gate:

- Focused runtime flow tests pass offline.
- `ruff`, `ruff format`, and `pyright` pass for touched tests.

## Phase 2: Output Bypass Equivalence

Status: started.

Goal:

Pin the legacy output bypass behavior before replacing `output_mapping`.

Deliverables:

- Keep `tests/test_output_mapping_rail_outcome_equivalence.py` separate from
  runtime flow tests.
- Assert tuple unwrapping for output bypass explicitly.
- Compare `output_mapping` to `RailOutcome` only for rails where the bypass path
  actually uses it.
- Mark known divergences as explicit adjudication cases.

Next tasks:

1. Add explicit divergence rows for guardrails_ai, clavata, and
   injection_detection.

Gate:

- Output bypass tests document the intended delete path for every mapping.
- No input rail test compares against `output_mapping`.

## Phase 3: Parser And Action Unit Coverage

Status: in progress.

Goal:

Keep raw vendor parsing and action behavior covered without mixing that coverage
with flow gate proof.

Deliverables:

- Parser tests for raw vendor payloads into action raw returns or
  `RailOutcome`.
- Action tests for fail-open, fail-closed, fallback, and metadata behavior.
- No live credentials.
- No runtime Colang assertions in these tests.

Next tasks:

1. Add parser rows for jailbreak cached raw values.
2. Add parser rows for content safety policy violations.
3. Add parser rows for llama guard missing and malformed values.
4. Add action fallback tests for API-error rails.

Gate:

- Parser/action tests explain raw return shapes used by the runtime fixture
  matrix.

## Phase 4: Expand To Transform Rails

Status: not started.

Goal:

Prove rails where the verdict can be transform, not just allow or block.

Rails:

- `pangea`
- `crowdstrike_aidr`
- `prompt_security`
- `autoalign`
- `injection_detection`
- mask flows from `privateai`, `gliner`, and `sensitive_data_detection`
- retrieval transforms from `regex` and `hf_classifier`

Deliverables:

- `RailOutcome.transform(...)` fixture rows.
- Runtime classifier that observes transformed input, output, or context vars
  without relying only on assistant content.
- Block wins over transform when both are present.
- API fallback rows where vendors fail open.

Gate:

- Runtime flow oracle can distinguish allow, block, and transform.
- Output bypass tests document where bool mapping cannot express transform.

## Phase 5: Implement Or Tighten Interpreters

Status: started for clean rails, incomplete overall.

Goal:

Make `RailOutcome` derivation the Python decision source for each rail.

Deliverables:

- Interpreter coverage for clean rails first.
- Threshold and dict interpreters next.
- Transform interpreters after runtime transform classification is proven.
- Adjudication cases either fixed or explicitly accepted by the owner.

Order:

1. Existing `RailOutcome` rails: content safety, topic safety, jailbreak.
2. Boolean allowed rails: self-check, hf_classifier.
3. Score threshold rails: facts, align score, cleanlab.
4. Dict flag rails: llama guard, regex, policyai.
5. Vendor object rails: trend_micro, activefence, gcp_moderate_text.
6. Transform rails.

Gate:

- Each interpreter is covered by runtime flow oracle tests or by an explicit
  bypass/adjudication test where normal Colang is not the path.

## Phase 6: Remove `output_mapping`

Status: not started.

Goal:

Delete the second decision path from output rail streaming and parallel bypass.

Code seams:

- `nemoguardrails/rails/llm/llmrails.py`
- `nemoguardrails/colang/v1_0/runtime/runtime.py`

Deliverables:

- Replace `output_mapping` and `default_output_mapping` decisions with
  `RailOutcome` interpretation.
- Preserve tuple unwrapping where the bypass currently depends on it, or prove
  it is unnecessary.
- Remove mapping registration once every caller has moved.

Gate:

- Runtime flow tests stay green.
- Output bypass tests stay green.
- Streaming and parallel bypass tests cover block and allow.

## Phase 7: Fix Known Bugs And Adjudication Points

Status: not started.

Known points:

- `guardrails_ai_validation_mapping` polarity is reversed relative to the normal
  flow gate.
- `patronus api check output` is missing `abort`; owner ruling says to fix it.
- `autoalign_groundedness_output_api` and `autoalign_factcheck_output_api`
  mappings block on scores while current flows do not.
- `activefence` and `gcp_moderate_text` simple flows can disagree with detailed
  mapping thresholds.
- `hallucination` uses one action for block and warning-only flows, so the
  interpreter must be tied to configured consequence.

Gate:

- Every divergence has a test and an owner decision.
- Bug fixes include characterization before and after where useful.

## Phase 8: IORails Consolidation

Status: planned, later.

Goal:

Delete forked IORails rail implementations and drive IORails through the same
library actions and `RailOutcome` decisions.

Deliverables:

- Route IORails rail execution through the shared action dispatcher and
  executor.
- Apply block outcomes via IORails `BlockSpec`.
- Defer transform application until a transform rail is supported in IORails, or
  implement it explicitly.
- Retire forked rail action classes after the shared path is proven.

Gate:

- Recorded IORails behavior is preserved where cassettes exist.
- Unit tests cover shared action dispatch and outcome application.

## Phase 9: Optional Flow Simplification

Status: optional.

Goal:

Once Python owns all verdicts, simplify Colang flows so they render outcomes
instead of hand-interpreting raw returns.

Scope:

- Keep multilingual text rendering in flows.
- Keep NLU-mapped refusal intents in flows.
- Keep vendor-specific Jinja refusal text in flows.
- Do not force every flow into one identical shape if metadata-driven rendering
  needs per-rail branches.

Gate:

- This phase is reversible per flow.
- No behavior change unless backed by runtime characterization tests.

## Immediate Next Phase

Continue Phase 1 and Phase 2 together for the next small slice:

1. Add remaining runtime transform rows for `autoalign` and
   `injection_detection`.
2. Add output bypass divergence rows for the remaining known divergent mappings.
3. Run the focused test files.
4. Commit that slice before moving to the next rail family.
