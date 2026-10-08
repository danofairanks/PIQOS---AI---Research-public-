# Paste everything between the lines into a FRESH chat (ChatGPT; a fresh Claude chat; an incognito Claude chat). No memory, no prior context. Return the JSON verbatim in a code block.
------------------------------------------------------------
You will formalise 9 short software-documentation sentences as SMT-LIB 2 definitions. Each has the sentence, a short context that defines its variables and what `spec` means, and a fixed argument list. Rules:
1. For each sentence give exactly one form: (define-fun spec <args> Bool <body>) using exactly the argument list given. Plain Int arithmetic only (+ - * mod, comparisons, and/or/not/=>/ite). Do not use abs, xor or any other function. No other commands. Check that every parenthesis is balanced.
2. Resolve any ambiguity the way you judge best. Do not ask questions.
3. For each sentence also return "ambiguity": "no", or "yes: <one sentence naming the alternative reading you did not choose>".
4. Reply with ONLY a JSON object {"L01": {"smt": "...", "ambiguity": "..."}, ... "L10": {...}}. Escape any double quote inside a string value as \" so the JSON is valid.

Sentences (id: text | context | spec arguments):
L01: "Raises ValueError if amount is not a number between zero and max_rate, inclusive." | spec is true when amount is accepted (no ValueError is raised). | (define-fun spec ((amount Int) (max_rate Int)) Bool ...)
L02: "Allow up to max_rate / time_period acquisitions before blocking." | n is the number of acquisitions of amount 1 made within one time period; spec is true when all n acquisitions proceed without blocking. | (define-fun spec ((n Int) (max_rate Int)) Bool ...)
L03: "True if cost could be deducted from the rate limit without exceeding it." | limit is the limit; used is the amount already consumed in the current window; cost is the amount requested; spec is true when the call returns True. | (define-fun spec ((limit Int) (used Int) (cost Int)) Bool ...)
L04: "The entire number of tokens requested must be available in the bucket to be conforming." | requested is the number of tokens requested; available is the number of tokens currently in the bucket; spec is true when the request is conforming. | (define-fun spec ((requested Int) (available Int)) Bool ...)
L05: "Maximum function invocations allowed within a time period." | calls is that maximum; k is the number of invocations made within one period; spec is true when all k invocations are allowed. | (define-fun spec ((k Int) (calls Int)) Bool ...)
L07: "Returns None when the item can never fit (the weight exceeds the rate limit)." | weight is the item weight; limit is the rate limit (the maximum weight per interval); spec is true when the item can never fit. | (define-fun spec ((weight Int) (limit Int)) Bool ...)
L08: "limit: Number of requests allowed within interval." | limit is that number; n is the number of unit-weight requests made within one interval; spec is true when all n requests are allowed. | (define-fun spec ((n Int) (limit Int)) Bool ...)
L09: "Acquire an entry if the weighted count of the current and previous windows is less than or equal to the limit." | existing is the weighted count already recorded; amount is the amount requested by this call; limit is the limit; the previous window is empty; spec is true when the entry is acquired. | (define-fun spec ((existing Int) (amount Int) (limit Int)) Bool ...)
L10: "capacity (int): Maximum number of tokens that the bucket can hold." | capacity is that maximum; n is the number of tokens requested from a freshly created, full bucket; spec is true when that request is conforming. | (define-fun spec ((n Int) (capacity Int)) Bool ...)
------------------------------------------------------------
