"""Arithmetic/structure checks on arXiv 2610.29968v1 (CulturalRiddles). POST-HOC. Inputs = numbers printed in the paper (E2);
outputs recomputed (E1). Table 5 columns were transcribed from the PDF text layer; ambiguous single-number rows are treated as writers-only
(consistent with 57 human-evaluated of 61 benchmarked communities)."""
# --- Fig 4 / Table 3 reconciliation
resp=28*6090
rules,native,jury=32171,100769,37580
scores=dict(c3=52777,c2=9442,c1=1106,c0=104161,unscored=3034)
print("responses 28x6090:",resp,"| pipeline sum:",rules+native+jury,"| score sum:",sum(scores.values()))
print("rules+human:",rules+native,"(printed 132,940)")
t3=[9195,20661,32161,8705,7,2475,736,1062,1554,4328,1997,653,28049,12636,8187,515,19]
print("Table 3 rows sum:",sum(t3))
inc=[9195,20661,32161,8705,7,2475,736]
print("incorrect rows (score 0) in rule+human:",sum(inc),"| hallucinated share of those:",round(32161/sum(inc)*100,1),"% (paper headline: 24.19% of ALL rule+human responses)")
print("EM share of all:",round(28049/resp*100,2),"% (printed 16.45) | EM share of correct:",round(28049/scores['c3']*100,1),"% => misses",round(100-28049/scores['c3']*100,1),"% (printed ~47%)")
print("accuracy printed-denominator (scored only):",round(scores['c3']/(resp-scores['unscored'])*100,2),"%")
lo=scores['c3']/resp*100; hi=(scores['c3']+scores['unscored'])/resp*100
print("accuracy bound if the 1.78% unscored were all wrong / all right:",round(lo,2),"to",round(hi,2))
# --- translation gap
print("translation: +10.3pp of gap (69-22.1) =",round(10.3/(69-22.1)*100,1),"% (printed 'about a fifth')")
# --- Table 5 (writers / evaluators), rows read directly from the PDF text for the communities of interest only.
# An attempt to transcribe the full column and sum it gave 173 / 117 vs printed 167 / 109: the text layer of Table 5 is ambiguous for rows with a
# single number, so NO aggregate from the transcription is reported. Per-row values below were read from unambiguous "writers evaluators" pairs.
rows={"Buginese (IDN)":(1,1),"Lumasaba (UGA)":(1,1),"Mongondow (IDN)":(1,1),"Luganda (UGA)":(1,1)}
for k,(w,e) in rows.items(): print(f"hardest-group community {k}: writers={w}, evaluators={e}")
print("printed totals: 167 writers, 109 evaluators; 19 communities have a second annotator (H2) out of 57 human-evaluated")
