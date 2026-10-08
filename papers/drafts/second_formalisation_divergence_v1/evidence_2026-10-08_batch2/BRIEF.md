# Paste everything between the lines into a FRESH chat (ChatGPT; a fresh Claude chat; an incognito Claude chat). No memory, no prior context. Return the JSON verbatim in a code block.
------------------------------------------------------------
You will formalise 18 short statements as SMT-LIB 2 definitions. Each has the statement text, a short context that defines its variables, and a fixed argument list. Rules:
1. For each statement give exactly one form: (define-fun spec <args> Bool <body>) using exactly the argument list given. Plain Int arithmetic only (+ - * mod, comparisons, and/or/not/=>/ite). Do not use abs, xor or any other function. No other commands.
2. Resolve any ambiguity the way you judge best. Do not ask questions.
3. For each statement also return "ambiguity": "no", or "yes: <one sentence naming the alternative reading you did not choose>".
4. Reply with ONLY a JSON object {"E01": {"smt": "...", "ambiguity": "..."}, ... "K5": {...}}. Escape any double quote inside a string value as \" so the JSON is valid.

Statements (id: text | context | spec arguments):
E01: "SPIFFE trust bundles MUST rotate at least every 90 days." | d is the number of days between two consecutive rotations of one bundle. | (define-fun spec ((d Int)) Bool ...)
E02: "verify the identity of the user for any transaction amount greater than 1000 USD." | amt is the transaction amount in whole USD; v is 1 if the user's identity was verified for this transaction and 0 otherwise. | (define-fun spec ((amt Int) (v Int)) Bool ...)
E03: "must be a valid decimal number with at most 2 decimal places for fiat currencies." | dp is the number of digits after the decimal point of the amount. | (define-fun spec ((dp Int)) Bool ...)
E04: "Critical CVE → patch within 24h, High → 7 days, Medium → 30 days." | sev is 3 for Critical, 2 for High and 1 for Medium; h is the time taken to patch, in hours. | (define-fun spec ((sev Int) (h Int)) Bool ...)
E05: "age within the reconciler TTL, and at most 5 s of future skew." | age and ttl are in seconds; skew is the number of seconds the timestamp lies in the future. | (define-fun spec ((age Int) (ttl Int) (skew Int)) Bool ...)
E06: "Bounds: pool 2, reserve 1, fence epoch ≤ 4, at most one stale failover." | pool, reserve, epoch and stale are the observed values of those four quantities. | (define-fun spec ((pool Int) (reserve Int) (epoch Int) (stale Int)) Bool ...)
E07: "commit a transaction if the reported latency exceeds 200ms." | lat is the reported latency in milliseconds; c is 1 if the transaction is committed and 0 otherwise. | (define-fun spec ((lat Int) (c Int)) Bool ...)
E08: "Zero governance bypasses during Redis outage; full recovery within 5 minutes." | b is the number of governance bypasses during the outage; r is the recovery time in seconds. | (define-fun spec ((b Int) (r Int)) Bool ...)
E09: "Uses WATCH/MULTI/EXEC optimistic locking with up to 5 retries for concurrent write safety." | attempts is the total number of times the transaction was tried, including the first try. | (define-fun spec ((attempts Int)) Bool ...)
E10: "if Slack alert not acknowledged within 4h, page on-call via PagerDuty." | t is the whole number of hours the alert has gone unacknowledged; p is 1 if on-call is paged and 0 otherwise. | (define-fun spec ((t Int) (p Int)) Bool ...)
C11: "at most one stale failover." | n is the number of stale failovers. | (define-fun spec ((n Int)) Bool ...)
C12: "at most 5 s of future skew." | skew is the number of seconds the timestamp lies in the future. | (define-fun spec ((skew Int)) Bool ...)
K0: "The three accepted requests with amounts q1, q2 and q3 together do not exceed the cap C. Amounts are integers and may be negative." | C is the cap; q1, q2 and q3 are the integer amounts of the three accepted requests, in that order. | (define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool ...)
K1: "The capacity consumed by the three accepted requests with amounts q1, q2 and q3 never exceeds the cap C. Amounts are integers and may be negative." | C is the cap; q1, q2 and q3 are the integer amounts of the three accepted requests, in that order. | (define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool ...)
K2: "The capacity consumed by the three accepted requests with amounts q1, q2 and q3 never exceeds the cap C. Consumed capacity is never given back. Amounts are integers and may be negative." | C is the cap; q1, q2 and q3 are the integer amounts of the three accepted requests, in that order. | (define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool ...)
K3: "The capacity consumed by the three accepted requests with amounts q1, q2 and q3 never exceeds the cap C. A negative amount restores no capacity. Amounts are integers and may be negative." | C is the cap; q1, q2 and q3 are the integer amounts of the three accepted requests, in that order. | (define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool ...)
K4: "The sum of q1, q2 and q3 does not exceed the cap C. Amounts are integers and may be negative." | C is the cap; q1, q2 and q3 are the integer amounts of the three accepted requests, in that order. | (define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool ...)
K5: "The sum of the positive amounts among q1, q2 and q3 does not exceed the cap C. Amounts are integers and may be negative." | C is the cap; q1, q2 and q3 are the integer amounts of the three accepted requests, in that order. | (define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool ...)
------------------------------------------------------------
