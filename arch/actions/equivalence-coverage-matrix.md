# Equivalence Coverage Matrix

This matrix records which current decision sources are pinned offline against
`RailOutcome`. Runtime flow means the normal Colang path in
`tests/test_runtime_flow_gate_equivalence.py`. Output mapping means the legacy
streaming/parallel bypass decision in
`tests/test_output_mapping_rail_outcome_equivalence.py`.

`Streaming bypass` is marked as a gap when the mapping is unit-pinned but the
actual per-chunk or parallel bypass runtime path is not yet equivalence-pinned.

| Rail | Runtime Flow | Output Mapping | Streaming Bypass | Transform Observed | Known Divergence -> Resolution |
| --- | --- | --- | --- | --- | --- |
| `self_check_input` | covered | N/A | N/A | none | none |
| `self_check_output` | covered | covered | gap: unit only | none | none |
| `self_check_facts` | covered | covered | gap: unit only | none | none |
| `alignscore_check_facts` | covered | covered | gap: unit only | none | none |
| `hf_classifier_input` | covered | N/A | N/A | none | none |
| `hf_classifier_output` | covered | covered | gap: unit only | none | none |
| `hf_classifier_retrieval` | covered | N/A | N/A | output_data | retrieval clear is a transform, not an output bypass block |
| `llama_guard_input` | covered | N/A | N/A | none | none |
| `llama_guard_output` | covered | covered | gap: unit only | none | none |
| `policyai_input` | covered | N/A | N/A | none | none |
| `policyai_output` | covered | covered | gap: unit only | none | none |
| `regex_input` | covered | N/A | N/A | none | none |
| `regex_output` | covered | covered | gap: unit only | none | none |
| `regex_retrieval` | covered | N/A | N/A | output_data | retrieval clear is a transform, not an output bypass block |
| `privateai_detect_input` | covered | N/A | N/A | none | none |
| `privateai_detect_output` | covered | covered | gap: unit only | none | none |
| `privateai_mask_input` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `privateai_mask_output` | covered | default covered | gap: unit only | text | default string mapping cannot express transform -> replace with `RailOutcome` |
| `privateai_mask_retrieval` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `gliner_detect_input` | covered | N/A | N/A | none | none |
| `gliner_detect_output` | covered | covered | gap: unit only | none | none |
| `gliner_mask_input` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `gliner_mask_output` | covered | default covered | gap: unit only | text | default string mapping cannot express transform -> replace with `RailOutcome` |
| `gliner_mask_retrieval` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `sensitive_data_detect_input` | covered | N/A | N/A | none | none |
| `sensitive_data_detect_output` | covered | covered | gap: unit only | none | none |
| `sensitive_data_mask_input` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `sensitive_data_mask_output` | covered | default covered | gap: unit only | text | default string mapping cannot express transform -> replace with `RailOutcome` |
| `sensitive_data_mask_retrieval` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `content_safety_input` | covered | N/A | N/A | none | none |
| `content_safety_output` | covered | covered | behavioral covered; equivalence gap | none | none |
| `topic_safety_input` | covered | N/A | N/A | none | none |
| `jailbreak_heuristics_input` | covered | N/A | N/A | none | none |
| `jailbreak_model_input` | covered | N/A | N/A | none | none |
| `pangea_input` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `pangea_output` | covered | default covered | gap: unit only | text | default object mapping allows block and transform -> replace with `RailOutcome` |
| `crowdstrike_aidr_input` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `crowdstrike_aidr_output` | covered | default covered | gap: unit only | text | default object mapping allows block and transform -> replace with `RailOutcome` |
| `prompt_security_input` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `prompt_security_output` | covered | covered | gap: unit only | text | mapping covers block but cannot express transform -> replace with `RailOutcome` |
| `autoalign_input` | covered | N/A | N/A | output_data | block wins over PII transform |
| `autoalign_output` | covered | covered | gap: unit only | text | mapping covers block but cannot express transform -> replace with `RailOutcome` |
| `autoalign_groundedness_output_api` | N/A: flow does not gate on mapping verdict | covered | gap: unit only | none | mapping blocks on score while flow only calls action -> owner decision pending |
| `autoalign_factcheck_output_api` | N/A: flow does not gate on mapping verdict | covered | gap: unit only | none | mapping blocks on score while flow only calls action -> owner decision pending |
| `injection_detection_reject` | covered | default covered | gap: unit only | text | default dict mapping allows block and transform -> replace with `RailOutcome` |
| `injection_detection_omit` | covered | default covered | gap: unit only | text | default dict mapping allows transform -> replace with `RailOutcome` |
| `clavata_input` | covered | N/A | N/A | none | none |
| `clavata_output` | covered | default covered | gap: unit only | none | default boolean mapping inverts flow polarity -> replace with `RailOutcome` |
| `fiddler_user_safety` | covered | N/A | N/A | none | none |
| `fiddler_bot_safety` | covered | default covered | gap: unit only | none | default boolean mapping inverts flow polarity -> replace with `RailOutcome` |
| `fiddler_bot_faithfulness` | covered | default covered | gap: unit only | none | default boolean mapping inverts flow polarity -> replace with `RailOutcome` |
| `activefence_input` | covered | N/A | N/A | none | none |
| `activefence_output` | covered | covered | gap: unit only | none | detailed category mapping can block when simple output flow allows -> owner decision pending |
| `activefence_input_detailed` | covered | N/A | N/A | none | none |
| `gcp_moderation_output` | covered | covered | gap: unit only | none | detailed category mapping can block when simple output flow allows -> owner decision pending |
| `gcp_moderation_output_detailed` | covered | covered | gap: unit only | none | detailed flow and mapping agree on category thresholds |
| `guardrails_ai_input` | covered | N/A | N/A | none | mapping polarity bug was output-only |
| `guardrails_ai_output` | covered | covered | gap: unit only | none | mapping polarity fixed to match flow |
| `patronus_lynx_output` | covered | covered | gap: unit only | none | none |
| `patronus_api_output` | covered | covered | gap: unit only | none | missing flow abort fixed; failed checks now block |
| `self_check_hallucination` | covered | covered | gap: unit only | none | blocking flow covered |
| `hallucination_warning` | separate render flow | N/A | N/A | none | same action has warning-only and blocking consequences -> interpreter must be flow-aware |
| `trend_micro_input` | covered | N/A | N/A | none | none |
| `trend_micro_output` | covered | covered | gap: unit only | none | none |
| `cleanlab_output` | covered | covered | gap: unit only | none | none |
| `ai_defense_input` | covered | N/A | N/A | none | none |
| `ai_defense_output` | covered | covered | gap: unit only | none | mapping fail-closed defaults are pinned |

## Phase Status

The normal Colang flow decision source is covered for the current library gate
rails, including block/allow and transform. Legacy output mapping is covered at
unit level, including tuple unwrapping and transform lossiness.

The remaining equivalence gap is runtime coverage for the actual
streaming/parallel bypass path. Phase 6 should close that gap while replacing
`output_mapping` with `RailOutcome`.
