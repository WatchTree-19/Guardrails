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
| `self_check_input` | covered | N/A | N/A | none | migrated to `RailOutcome`; block path preserves mask event |
| `self_check_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome` |
| `self_check_facts` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; threshold preserved in accuracy metadata |
| `alignscore_check_facts` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; fallback and threshold preserved |
| `hf_classifier_input` | covered | N/A | N/A | none | migrated to `RailOutcome` |
| `hf_classifier_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome` |
| `hf_classifier_retrieval` | covered | N/A | N/A | output_data | migrated to `RailOutcome.transform`; retrieval clear is a transform, not an output bypass block |
| `llama_guard_input` | covered | N/A | N/A | none | migrated to `RailOutcome`; fail-closed unparseable case pinned |
| `llama_guard_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; bypass reads outcome directly |
| `policyai_input` | covered | N/A | N/A | none | migrated to `RailOutcome` |
| `policyai_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; metadata preserves exception message |
| `regex_input` | covered | N/A | N/A | none | migrated to `RailOutcome`; same action has block and transform consequences |
| `regex_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; same action has block and transform consequences |
| `regex_retrieval` | covered | N/A | N/A | output_data | migrated to `RailOutcome.transform`; retrieval clear is a transform, not an output bypass block |
| `privateai_detect_input` | covered | N/A | N/A | none | migrated to `RailOutcome` |
| `privateai_detect_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome` |
| `privateai_mask_input` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `privateai_mask_output` | covered | N/A: default bypass replaced | direct RailOutcome covered | text | migrated to `RailOutcome.transform`; streaming transform application remains unsupported |
| `privateai_mask_retrieval` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `gliner_detect_input` | covered | N/A | N/A | none | migrated to `RailOutcome` |
| `gliner_detect_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome` |
| `gliner_mask_input` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `gliner_mask_output` | covered | N/A: default bypass replaced | direct RailOutcome covered | text | migrated to `RailOutcome.transform`; streaming transform application remains unsupported |
| `gliner_mask_retrieval` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `sensitive_data_detect_input` | covered | N/A | N/A | none | migrated to `RailOutcome` |
| `sensitive_data_detect_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome` |
| `sensitive_data_mask_input` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `sensitive_data_mask_output` | covered | N/A: default bypass replaced | direct RailOutcome covered | text | migrated to `RailOutcome.transform`; streaming transform application remains unsupported |
| `sensitive_data_mask_retrieval` | covered | N/A | N/A | output_data | transform only; no output mapping path |
| `content_safety_input` | covered | N/A | N/A | none | migrated to `RailOutcome` |
| `content_safety_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; bypass reads outcome directly |
| `topic_safety_input` | covered | N/A | N/A | none | none |
| `jailbreak_heuristics_input` | covered | N/A | N/A | none | none |
| `jailbreak_model_input` | covered | N/A | N/A | none | none |
| `pangea_input` | covered | N/A | N/A | output_data | migrated to plural `RailOutcome.transform`; rewrites both user and bot targets |
| `pangea_output` | covered | N/A: mapping deleted | direct RailOutcome covered | text | migrated to plural `RailOutcome.transform`; streaming transform application remains unsupported |
| `crowdstrike_aidr_input` | covered | N/A | N/A | output_data | migrated to `RailOutcome`; transform rewrites both user and bot targets |
| `crowdstrike_aidr_output` | covered | N/A: default bypass replaced | direct RailOutcome covered | text | migrated to `RailOutcome`; streaming transform application remains unsupported |
| `prompt_security_input` | covered | N/A | N/A | output_data | migrated to `RailOutcome`; transform rewrites the user target |
| `prompt_security_output` | covered | N/A: mapping deleted | direct RailOutcome covered | text | migrated to `RailOutcome`; streaming transform application remains unsupported |
| `autoalign_input` | covered | N/A | N/A | output_data | block wins over PII transform |
| `autoalign_output` | covered | N/A: mapping deleted | direct RailOutcome covered | text | migrated to `RailOutcome`; streaming transform application remains unsupported |
| `autoalign_groundedness_output_api` | N/A: flow does not gate on mapping verdict | covered | gap: unit only | none | mapping blocks on score while flow only calls action -> owner decision pending |
| `autoalign_factcheck_output_api` | N/A: flow does not gate on mapping verdict | covered | gap: unit only | none | mapping blocks on score while flow only calls action -> owner decision pending |
| `injection_detection_reject` | covered | N/A: default bypass replaced | direct RailOutcome covered | text | migrated to `RailOutcome`; reject blocks injections and transforms non-injection rewrites |
| `injection_detection_omit` | covered | N/A: default bypass replaced | direct RailOutcome covered | text | migrated to `RailOutcome.transform`; streaming transform application remains unsupported |
| `clavata_input` | covered | N/A | N/A | none | migrated to `RailOutcome` |
| `clavata_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; default boolean inversion removed |
| `fiddler_user_safety` | covered | N/A | N/A | none | migrated to `RailOutcome` |
| `fiddler_bot_safety` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; default boolean inversion removed |
| `fiddler_bot_faithfulness` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; default boolean inversion removed |
| `activefence_input` | covered | N/A | N/A | none | migrated to `RailOutcome`; simple threshold mode pinned |
| `activefence_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; simple output threshold preserved |
| `activefence_input_detailed` | covered | N/A | N/A | none | migrated to `RailOutcome`; detailed threshold evidence preserved in metadata |
| `gcp_moderation_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; simple output threshold preserved |
| `gcp_moderation_output_detailed` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; detailed threshold evidence preserved in metadata |
| `guardrails_ai_input` | covered | N/A | N/A | none | mapping polarity bug was output-only |
| `guardrails_ai_output` | covered | covered | gap: unit only | none | mapping polarity fixed to match flow |
| `patronus_lynx_output` | covered | covered | gap: unit only | none | none |
| `patronus_api_output` | covered | covered | gap: unit only | none | missing flow abort fixed; failed checks now block |
| `self_check_hallucination` | covered | covered | gap: unit only | none | blocking flow covered |
| `hallucination_warning` | separate render flow | N/A | N/A | none | same action has warning-only and blocking consequences -> interpreter must be flow-aware |
| `trend_micro_input` | covered | N/A | N/A | none | migrated to `RailOutcome`; reason preserved for exception rendering |
| `trend_micro_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; reason preserved for exception rendering |
| `cleanlab_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; score preserved in trustworthiness metadata |
| `ai_defense_input` | covered | N/A | N/A | none | migrated to `RailOutcome`; fail-open/fail-closed fallback pinned |
| `ai_defense_output` | covered | N/A: mapping deleted | direct RailOutcome covered | none | migrated to `RailOutcome`; fail-open/fail-closed fallback pinned |

## Phase Status

The normal Colang flow decision source is covered for the current library gate
rails, including block/allow and transform. Legacy output mapping is covered at
unit level, including tuple unwrapping and transform lossiness. The streaming
and parallel bypass helpers now read `RailOutcome` directly before falling back
to legacy `output_mapping`, with focused runtime coverage for both bypass sites.

The transform queue is migrated for the target -> text rewrite rails: pangea,
PII masking, HF retrieval clearing, regex retrieval clearing, CrowdStrike AIDR,
Prompt Security, AutoAlign PII rewrites, and injection omit/rewrite. The
remaining equivalence gap is runtime coverage for the actual streaming/parallel
bypass path for each legacy raw-return fallback that still has an output
mapping. Transform-on-streaming is explicitly unsupported in this phase:
streaming bypasses observe transform outcomes as non-blocking and do not apply
rewrites.
