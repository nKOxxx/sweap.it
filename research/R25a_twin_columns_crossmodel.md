# R25a: TWIN-COLUMN DUPLICATION - CROSS-MODEL ON ONE HOST
Date: 2026-10-17. Follow-up to R25's 26 MB mirror finding. Question: is the
reasoning/reasoning_content twin pattern model-specific?

## METHOD
Per-model audit of the Hermes store (read-only), joining messages to
sessions.model. Plus a Claude Code store check (thinking field layout).

## RESULT: 100% TWIN RATE ON EVERY MODEL THAT WRITES REASONING

model                              w/reason   twins   reas_MB   twin_MB
glm-4.6                               7,934    7,934    22.12     22.12
deepseek-ai/DeepSeek-V4-Flash-0731    1,470    1,470     3.79      3.79
MiniMaxAI/MiniMax-M2.7                   51       51     0.13      0.13
glm-4.7                                   1        1     0.00      0.00

Every assistant row with reasoning on every model family (paid glm lane,
free DeepSeek lane, free MiniMax lane) carries byte-identical twins. The
duplication is a STORE-LAYER behavior, not a model behavior: whichever
model produces the thinking, the store writes it twice.

## CROSS-STORE CHECK (kills the universal claim honestly)

Claude Code transcript store (same machine): thinking blocks live INSIDE
content as {type:thinking} blocks, stored ONCE; the row has NO
reasoning/reasoning_content fields. So the twin pattern is Hermes-store-
schema-specific, not universal to AI stores.

## COPY LAW (binding on all published claims)

- TRUE and publishable: "on the Hermes store, every thinking blob is
  stored twice, across all models tested (9,456 rows, 26.04 MB)."
- NOT publishable: "AI stores carry everything twice." Claude Code does
  not. The accurate frame: SOME store schemas duplicate spent thinking;
  sweap's weigh-in detects which pattern YOUR store has.
- Second-host check (different machine, same Hermes schema) still owed
  before any universal Hermes-claim; this round only proves cross-MODEL
  on one host.
