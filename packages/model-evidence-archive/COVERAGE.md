# Coverage

Date of this note: 2026-11-08.

| Item | State |
|---|---|
| Frozen probes | 12, in `probes/panel_v1.json`, frozen 2026-10-23. Not revised. |
| Authentic provider records in git | 0 |
| OpenAI adapter | Implemented. Used only when `OPENAI_API_KEY` is set and collection is `--live`. |
| Anthropic adapter | Not implemented. A present secret is reported as `ADAPTER_NOT_IMPLEMENTED`. |
| Google adapter | Not implemented. Same rule. |
| Weekly workflow | Dry-run unless a secret is configured. Artifacts are not commits. |

Gate A in `KILL_CRITERIA.md` is not met. No public run has shown a real provider call.

A later commit that adds files under `records/public/` must leave the captured `raw_response` bytes as collected. This file should be updated in that same commit with the count, the models, and the dates. Do not backdate this table.
