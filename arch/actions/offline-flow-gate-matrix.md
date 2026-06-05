# Offline Flow Gate Audit

This is the credential-free proof plan for the actions decoupling migration.
No vendor credentials are required. VCR replay is optional coverage only when a
recorded cassette already exists and is stable.

## Test Policy

- The normal Colang flow gate is the current source of truth.
- The new interpreter must derive `RailOutcome` from synthetic raw action
  returns.
- For rails with legacy `output_mapping`, the sweep is three-way:
  `flow gate == output_mapping == RailOutcome`.
- A three-way disagreement is an adjudication point, not a reason to preserve
  the wrong side.
- Exception handling, refusal intents, multilingual text, and Jinja messages are
  rendering. They are tested with stubbed actions and config flags, but they do
  not define the verdict.
- Tuple unwrapping must be pinned for the output bypass path because
  `is_output_blocked` currently maps `result[0]`.

## Fixture Families

Use these families to generate per-rail synthetic raw returns.

| Family | Raw returns | Expected verdict |
| --- | --- | --- |
| `rail_outcome` | `RailOutcome.allow(...)`, `RailOutcome.block(...)` | allow, block |
| `bool_allowed` | `True`, `False` | allow, block |
| `bool_flag` | `False`, `True` | allow, block |
| `score_min_0_5` | `0.49`, `0.5`, `0.51` | block, allow, allow |
| `score_min_0_6` | `0.59`, `0.6`, `0.61` | block, allow, allow |
| `threshold_gt(T)` | `T`, `T + 0.01` | allow, block |
| `dict_flag(K)` | `{K: False}`, `{K: True}`, `{}`, `None` | allow, block, adjudicate, adjudicate |
| `dict_allowed` | `{"allowed": True}`, `{"allowed": False}`, `{}` | allow, block, adjudicate |
| `transform_text` | no-op, transform-only, block+transform | allow, transform, block |
| `api_error_fallback` | vendor fallback object with `blocked=False` and `transformed=False` | allow |

## Flow Gate Audit

| Library | Flow gate | Existing mapping | Category | Synthetic fixture rows |
| --- | --- | --- | --- | --- |
| `content_safety` | `not response.is_blocked` gates input and output. Multilingual only changes rendered refusal. | Output maps `RailOutcome.is_blocked`. | Clean `RailOutcome`. | `rail_outcome` with empty and non-empty `policy_violations`; multilingual on/off render cases. |
| `topic_safety` | `not response.is_blocked` gates input. | None. | Clean `RailOutcome`. | `rail_outcome`. |
| `jailbreak_detection` | `response.is_blocked` gates heuristics and model input rails. | None. | Clean `RailOutcome`. | `rail_outcome`; cached raw `{jailbreak: true/false}` parser cases. |
| `self_check/input_check` | `not allowed` gates input. | None. | Clean boolean allowed. | `bool_allowed`. |
| `self_check/output_check` | `not allowed` gates output. | `lambda value: not value`. | Clean boolean allowed. | `bool_allowed`, plus tuple-wrapped results. |
| `self_check/facts` | `accuracy < 0.5` gates output when `$check_facts` is true. | `result < 0.5`. | Clean score threshold. | `score_min_0_5`; `$check_facts` false render no-op. |
| `factchecking/align_score` | `accuracy < 0.5` gates output when `$check_facts` is true. | `result < 0.5`. | Clean score threshold. | `score_min_0_5`; `$check_facts` false render no-op. |
| `hallucination` | `self check hallucination` blocks on `is_hallucination`; `hallucination warning` only renders a warning on the same boolean. | `lambda value: value`. | Flow-specific consequence. | `bool_flag`; include one block flow case and one warning-only flow case. |
| `hf_classifier` | `not allowed` gates input/output; retrieval clears chunks on not allowed. | Output maps `not result`. | Clean boolean allowed plus retrieval transform. | `bool_allowed`; retrieval `False -> relevant_chunks=""`. |
| `llama_guard` | `not response["allowed"]` gates input/output. | Output maps `not allowed`, default missing key to allowed. | Clean dict allowed with edge cases. | `dict_allowed` with `policy_violations`; missing key adjudication. |
| `privateai` | `has_pii` gates input/output/retrieval; mask flows rewrite text. | Detect maps identity. | Boolean flag plus transform. | `bool_flag`; mask input/output/retrieval with changed and unchanged text. |
| `gliner` | `has_pii` gates input/output/retrieval; mask flows rewrite text. | Detect maps identity. | Boolean flag plus transform. | `bool_flag`; mask input/output/retrieval with changed and unchanged text. |
| `sensitive_data_detection` | `has_sensitive_data` gates input/output/retrieval; mask flows rewrite text. | Detect maps identity. | Boolean flag plus transform. | `bool_flag`; mask input/output/retrieval with changed and unchanged text. |
| `regex` | `result["is_match"]` gates input/output; retrieval match clears chunks. | `result.get("is_match", False)`. | Dict flag plus retrieval transform. | `dict_flag("is_match")`; retrieval match -> `relevant_chunks=""`; missing key adjudication. |
| `policyai` | `result.assessment == "UNSAFE"` gates input/output. | Same comparison with missing default `SAFE`. | Clean dict enum with edge cases. | `{"assessment": "SAFE"}`, `{"assessment": "UNSAFE", "category": "x"}`, missing assessment adjudication. |
| `trend_micro` | `result.blocked` gates input/output and API errors fail open except missing API key returns block. | `result.action.lower() == "block"`. | Clean object flag with API fallback. | `GuardResult(action="Allow")`, `GuardResult(action="Block")`, API error allow fallback, missing key block fallback. |
| `cleanlab` | `trustworthiness_score < 0.6` gates output. | Same threshold with missing default `1`. | Clean score threshold. | `score_min_0_6`; missing score adjudication. |
| `ai_defense` | `result["is_blocked"]` gates prompt/response. | `None` or missing `is_blocked` fail closed. | Dict flag with fail-closed divergence. | `dict_flag("is_blocked")`; explicit `None` and missing key adjudication. |
| `prompt_security` | `is_blocked` blocks; else `is_modified` rewrites prompt/response. | Missing `is_blocked` defaults to block. | Block or transform. | `is_blocked=false/is_modified=false`; `is_blocked=true`; `is_blocked=false/is_modified=true`; both true means block wins; missing key adjudication. |
| `autoalign` | `guardrails_triggered` blocks; else `pii.guarded` rewrites input/output. Groundedness and factcheck flows call actions but do not gate on score. | Output maps `guardrails_triggered`; groundedness and factcheck mappings block on score `< 0.5`. | Block or transform, plus score divergence. | `guardrails_triggered=false/pii.guarded=false`; `guardrails_triggered=true`; `guardrails_triggered=false/pii.guarded=true`; score `0.49/0.5/0.51` must be adjudicated because flow does not block. |
| `activefence` | Simple input/output block on `max_risk_score > 0.7`; detailed input blocks on per-category thresholds. | Mapping checks max risk and all detailed thresholds. | Threshold matrix with simple-vs-detailed divergence. | `threshold_gt(0.7)` for max risk; each detailed threshold boundary; adult content `0.31` with max risk below `0.7` exposes output mapping vs simple flow divergence. |
| `gcp_moderate_text` | Simple flow blocks on `max_risk_score > 0.8`; detailed flow blocks on per-category thresholds. | Mapping checks max risk and all detailed thresholds. | Threshold matrix with simple-vs-detailed divergence. | `threshold_gt(0.8)` for max risk; each detailed threshold boundary; category above threshold with max risk below `0.8` exposes simple flow vs mapping divergence. |
| `guardrails_ai` | `not result["valid"]` gates input/output. | Mapping currently returns `valid`, which reverses output bypass polarity. | Latent bug. | `validation_passed=True -> flow allow, mapping block`; `validation_passed=False -> flow block, mapping allow`; new outcome should follow flow after owner adjudication. |
| `patronusai` | Lynx blocks on `hallucination`; API blocks on `not pass` but currently lacks `abort`. | Lynx maps hallucination; API maps `not pass`. | Clean dict flags plus known flow bug. | Lynx `hallucination=false/true`; API `pass=true/false`; API block must expect abort after bug fix. |
| `pangea` | `blocked` blocks; else `transformed` rewrites user/output message; API errors fail open. | None, so default mapping allows objects. | Block or transform, output bypass divergence. | `blocked=false/transformed=false`; `blocked=true`; `blocked=false/transformed=true`; API error fallback allow; block wins if both true. |
| `crowdstrike_aidr` | `blocked` blocks; else `transformed` rewrites user/output message; API errors fail open. | None, so default mapping allows objects. | Block or transform, output bypass divergence. | `blocked=false/transformed=false`; `blocked=true`; `blocked=false/transformed=true`; API error fallback allow; block wins if both true. |
| `injection_detection` | `is_injection` plus config action: `reject` blocks, `omit`/`sanitize` rewrites output, otherwise rewrites output to response text. | None, so default mapping allows dicts. | Config-dependent block or transform. | `is_injection=false` with text rewrite; `is_injection=true/action=reject`; `is_injection=true/action=omit`; `is_injection=true/action=sanitize`; exception branch needs render characterization. |
| `clavata` | `is_match` blocks active input/output flow. | None, so default boolean mapping would invert output bypass polarity. | Boolean flag with output bypass divergence. | `False -> allow`, `True -> block`; tuple-wrapped result; output bypass divergence must be adjudicated. |
| `fiddler` | Safety actions return true for detected hazard; faithfulness returns true for low faithfulness despite `$is_faithful` variable name. | None, so default boolean mapping inverts output bypass polarity. | Boolean flag with output bypass divergence. | Safety `False/True`; faithfulness `False/True`; no endpoint fallback allow. |

## Known Adjudication Points

1. `guardrails_ai_validation_mapping` polarity is reversed relative to the
   normal flow gate and its own docstring. The new outcome should follow the
   flow, and the mapping should be fixed or deleted.
2. `patronus api check output` is missing `abort`; the owner ruling says to fix
   it and treat `pass=false` as a hard block.
3. `autoalign_groundedness_output_api` and `autoalign_factcheck_output_api`
   mappings block on score, but the current flows do not gate on the score.
   Decide whether the mappings are dead behavior or the flows are incomplete.
4. `fiddler`, `clavata`, `pangea`, `crowdstrike_aidr`, and
   `injection_detection` have output rail shapes where default output mapping
   does not match the flow gate. The sweep should expose this, not preserve it.
5. `activefence` and `gcp_moderate_text` have simple flows and detailed
   mappings that can disagree when a category threshold is crossed but the
   simple max-risk threshold is not.
6. `hallucination` uses one action for both warning-only rendering and blocking.
   The interpreter must be tied to the configured flow consequence, not just the
   action name.

## First Test Slice

Start with rails where the decision is clean and the fixture count is small:

1. `content_safety`, `topic_safety`, `jailbreak_detection`
2. `self_check/output_check`, `self_check/facts`, `factchecking/align_score`
3. `privateai`, `gliner`, `sensitive_data_detection`, `regex`
4. `llama_guard`, `hf_classifier`, `policyai`, `trend_micro`

After those pass, add the transform rails:

1. `pangea`, `crowdstrike_aidr`, `prompt_security`
2. `autoalign`
3. `injection_detection`
4. retrieval transforms from `regex` and `hf_classifier`

Keep the adjudication cases as explicit expected failures until the owner
decides which side represents intended behavior.
