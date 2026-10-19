# Reproduction

"Reproduce Table 2 of paper Z", "rerun baseline B as published", "does paper Z's result hold?".

**Match the original exactly. Every deviation goes to the supervisor before it is used.**

1. **Targets.** From the full paper, write down each target as reported: paper version, table and cell, value, uncertainty, N. Propose a tolerance if none was given. If the paper versions, an erratum, or the code disagree on a target, the supervisor picks which counts. For a whole paper, list its experiments, mark which headline claims depend on each, and let the supervisor choose.
2. **The original.** Collect the code at the paper's commit, dependencies as they resolved at the paper's date, the data version, the evaluation stack (eval code, metric implementation, prompt format, chat template, decoding, test-set version), and the stated seeds and run count. Take settings from the full paper, appendix, captions, and code. A detail the paper calls "standard" or "default" and the released code does not pin is unspecified: list it, don't fill it. Where text, equations, config, and code disagree, find which produced the reported number and ask which to follow. If the code that produced the numbers is gone, say so and recommend the closest released code, labelled as such.
3. **Cost.** Estimate what the paper's setting costs from the paper or a measured step, with its basis and a ceiling. A budget in the request approves runs within it. Downscaling to fit is a deviation and needs consent.
4. **Run.** Use the released code as released. If you must reimplement, follow the full method and the reference code, and check that every essential component is present; agent code often runs while leaving part of the method out. A workaround to make the original run is a deviation: ask first.
5. **On a miss.** First find and correct your own departures from the original; that needs no question. Then check the evaluation stack. Ask before changing an original setting to test a cause. The original may itself be wrong (selection on the test set, leakage, a non-standard metric); report that as a finding. When the paper and code cannot settle a gap, draft a precise question to the authors for the supervisor to send.
6. **Hand back.** Judgment first: does the result hold? Then a table per target: paper version and cell, paper value, our value, difference, status (matched, near, trend only, not reproduced, not run), and any departure. "The code runs" is not "the numbers match". State what was not regenerated in this session.

**Reply:** the judgment, the target table, deviations with their consent, and open questions for the authors.

Sources: SOURCES.md entries `reclaim`, `vanmiltenburg-preregistering-nlp`, `ppo-37-details`, `independent-reproducibility`, `sacrebleu-clarity`, `olmes`, `researchcodebench`, `exp-bench`.
