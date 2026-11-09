*Copied from the evaluator's working note. Written after seeing only the first two pages (title, abstract, start of the introduction) and before reading the body; that order is the evaluator's own record (the repository history is not an independent timestamp).*

---

# Predictions fixed before reading the body (2026-11-09)
- P1 (0.8): the simulated user is a language model with a partial fidelity check; no live human users in the main experiment.
- P2 (0.7): the multi-turn versus single-turn gap is not fully attributable to chatbot path dependence; simulated-user behaviour and the format difference account for part, acknowledged in the discussion.
- P3 (0.7): re-presenting facts explains a large share of the gap: (20.3-12.1)/(20.3-5.6) = 56% would be removed; the paper states this fraction or an equivalent.
- P4 (0.65): a forced provisional disposition on every turn could itself produce anchoring; the paper discusses this or tests a version without it (0.4).
- P5 (0.7): the number of emergency cases is small (tens); conversations are clustered by case and chatbot; intervals or mixed models are reported (0.65).
- P6 (0.6): endpoints differ widely; the headline average hides a range.
- P7 (0.55): the clinician comparison for context-seeking is on fixed transcripts, not live conversations.
- P8 (0.5): mitigations are proposed but not all tested.
- P9 (0.55): coupling between inference and context-seeking rests on association or lagged analyses, not on an intervention that severs it.
- P10 (0.6): over-triage costs are reported or discussed.
- P11 (0.5): models from the assisting model's developer are among the chatbots; an author-affiliated developer's assistant is among them (0.5); versions, access dates and system prompts are listed.
- P12 (0.5): data and case files are partly withheld; code or simulator prompts are released (0.5).
- P13 (0.6): the title and abstract use causal wording ("lead chatbots to miss"); the strongest design for it is the single-message re-presentation contrast.

# Scored after reading (added later; not part of the preregistration)
P1 met (a language model plays the user; realism rests on a citation). P2 partial (the format confound is not discussed). P3 missed (only 12.1% is reported; the 56% is the reader's arithmetic). P4 missed (the design keeps provisional dispositions out of the context, so the concern moves to input overlap). P5 partial (28 emergency cases; mixed models in most analyses; the headline exact test treats 354 pairs as independent). P6 met (3.6% to 82.1%). P7 met. P8 met. P9 met. P10 met. P11 partial (models from the assisting model's developer are among the chatbots and the whole instrument; versions, dates and decoding settings are listed; no assistant of the affiliated company is tested). P12 met (promised at publication). P13 met. 8 held, 3 partial, 2 missed.
- `checks.py` was written after reading the paper; it is not preregistered. It uses numbers typed from the paper's text and tables.
