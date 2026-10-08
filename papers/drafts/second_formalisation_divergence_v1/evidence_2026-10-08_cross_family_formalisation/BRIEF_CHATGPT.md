# Paste everything between the lines into a FRESH ChatGPT session (no memory, no prior chat). Do not add context. Return its JSON reply to me verbatim.
------------------------------------------------------------
You will formalise six short English statements as SMT-LIB 2 definitions. Rules:
1. For each statement give exactly one form: (define-fun spec <args> Bool <body>) using only the argument list and the already-declared symbols given below. Use plain Int arithmetic and quantifiers where the statement needs them. No other commands (no declare-*, assert, check-sat, set-option).
2. Resolve any ambiguity the way you judge best. Do not ask questions.
3. For each statement also return "ambiguity": "no", or "yes: <one sentence naming the alternative reading you did not choose>".
4. Reply with ONLY a JSON object: {"S1": {"smt": "...", "ambiguity": "..."}, "S2": {...}, ... "S6": {...}}.

Already declared / argument lists:
S1: "The function f is bounded above by g plus a constant, using a single constant that works for every n."
    declared: (declare-fun f (Int) Int) (declare-fun g (Int) Int); spec takes no arguments: (define-fun spec () Bool ...)
S2: "The sequence a is increasing."
    declared: (declare-fun a (Int) Int); spec takes no arguments.
S3: "The total amount consumed by the three accepted requests never exceeds the cap C. The requests have amounts q1, q2, q3 and are processed in that order; amounts are integers and may be negative."
    spec takes arguments: (define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool ...)
S4: "Every student passed an exam."
    declared: (declare-fun passed (Int Int) Bool)   ; passed(student, exam); spec takes no arguments.
S5: "The integer x is between 1 and 10."
    spec takes arguments: (define-fun spec ((x Int)) Bool ...)
S6: "The integer x is a positive even number."
    spec takes arguments: (define-fun spec ((x Int)) Bool ...)
------------------------------------------------------------
