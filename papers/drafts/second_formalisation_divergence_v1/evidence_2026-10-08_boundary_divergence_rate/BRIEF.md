# Paste everything between the lines into a FRESH chat (ChatGPT, and separately a fresh Claude chat). No memory, no prior context. Return the JSON verbatim, in a code block.
------------------------------------------------------------
You will formalise 24 short English statements as SMT-LIB 2 definitions. Rules:
1. For each statement give exactly one form: (define-fun spec <args> Bool <body>) using exactly the argument list given for it. Plain Int arithmetic only (+ - * mod, comparisons, and/or/not, ite). No other commands (no declare-*, assert, check-sat, set-option).
2. Resolve any ambiguity the way you judge best. Do not ask questions.
3. For each statement also return "ambiguity": "no", or "yes: <one sentence naming the alternative reading you did not choose>".
4. Reply with ONLY a JSON object {"B01": {"smt": "...", "ambiguity": "..."}, ... "C06": {...}}. Escape any double quote inside a string value as \" so the JSON is valid.

Statements (id: text | spec argument list):
B01: "The integer x is between 5 and 20." | (define-fun spec ((x Int)) Bool ...)
B02: "The integers x and y are within 3 of each other." | (define-fun spec ((x Int) (y Int)) Bool ...)
B03: "The integer x is up to 10." | (define-fun spec ((x Int)) Bool ...)
B04: "The integer x is over 65." | (define-fun spec ((x Int)) Bool ...)
B05: "The integer x ranges from 1 to 10." | (define-fun spec ((x Int)) Bool ...)
B06: "The integer x is more than twice the integer y." | (define-fun spec ((x Int) (y Int)) Bool ...)
B07: "The integer x is less than half of the integer y." | (define-fun spec ((x Int) (y Int)) Bool ...)
B08: "The integer x is closer to 0 than the integer y is." | (define-fun spec ((x Int) (y Int)) Bool ...)
B09: "The integer x is positive and y is positive or z is positive." | (define-fun spec ((x Int) (y Int) (z Int)) Bool ...)
B10: "Either x or y is even." | (define-fun spec ((x Int) (y Int)) Bool ...)
B11: "At most two of the integers a, b and c are positive." | (define-fun spec ((a Int) (b Int) (c Int)) Bool ...)
B12: "The integers a, b and c are consecutive." | (define-fun spec ((a Int) (b Int) (c Int)) Bool ...)
B13: "The integer x is greater than the integer y by no more than 3." | (define-fun spec ((x Int) (y Int)) Bool ...)
B14: "The accepted requests with amounts q1, q2 and q3 together do not exceed the cap C. Amounts are integers and may be negative." | (define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool ...)
B15: "The integer x is below 0 or above 10." | (define-fun spec ((x Int)) Bool ...)
B16: "The integer x is not between 1 and 10." | (define-fun spec ((x Int)) Bool ...)
B17: "The integer x is a multiple of 3 between 1 and 20." | (define-fun spec ((x Int)) Bool ...)
B18: "The integer x exceeds the integer y by at least 2." | (define-fun spec ((x Int) (y Int)) Bool ...)
C01: "The integer x equals 7." | (define-fun spec ((x Int)) Bool ...)
C02: "The integer x is odd." | (define-fun spec ((x Int)) Bool ...)
C03: "The integer x is at least 5 and at most 10." | (define-fun spec ((x Int)) Bool ...)
C04: "The integer x is greater than 3 and less than 8." | (define-fun spec ((x Int)) Bool ...)
C05: "Neither x nor y exceeds 10." | (define-fun spec ((x Int) (y Int)) Bool ...)
C06: "The integer x is not less than 5 and not more than 8." | (define-fun spec ((x Int)) Bool ...)
------------------------------------------------------------
