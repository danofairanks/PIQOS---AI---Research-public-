# Arithmetic on numbers printed in arXiv 2611.10463v1 (typed from the PDF tables). E1 = recomputed here.
import math
print("== Table 1: Avg = mean(H-Avg, RULER)? H-Avg = mean of the five shown categories (Recall, RAG, ICL, Rank, LongQA)?")
rows={ # name: (Avg, HAvg, Recall, RAG, ICL, Rank, LongQA, RULER)
 "Llama3-8B zero-shot":(15.14,12.48,18.00,12.68,13.60,7.74,10.38,17.80),
 "Llama NExtLong":(70.15,58.80,82.56,60.91,81.76,31.47,37.30,81.50),
 "Llama RRSI":(39.67,46.02,28.19,64.63,83.45,22.18,31.65,33.32),
 "Qwen RRSI":(38.46,44.83,39.11,56.88,79.47,21.15,27.55,32.09),
 "Llama LongCapHarness":(79.32,64.01,100.00,59.70,83.85,39.67,36.84,94.62),
 "Qwen LongCapHarness":(78.73,63.18,100.00,56.33,76.84,56.28,26.45,94.28)}
for k,(avg,h,rec,rag,icl,rk,lq,ru) in rows.items():
    h5=round((rec+rag+icl+rk+lq)/5,2); a=round((h+ru)/2,2)
    print(f"{k:22s} H-Avg printed {h:5.2f} vs mean of 5 shown {h5:5.2f} | Avg printed {avg:5.2f} vs mean(H-Avg,RULER) {a:5.2f}")
print("Qwen NExtLong/PolicyLong rows (dashes for categories): Avg=(HAvg+RULER)/2:",round((50.26+74.87)/2,2),"(NExtLong; printed 62.56)",round((51.53+76.67)/2,2),"(PolicyLong; printed 64.10)")
print("Citation and Summarization are in the split (Table 6: test 970 and 700 records) but have no column in Table 1; H-Avg excludes them. Test records: HELMET shown categories =",1930+9555+12425+405+1050,"of 27,035 HELMET test; unshown =",970+700)
print("RULER share of all test records:",round(32388/59826*100,1),"% ; RULER weight in Avg: 50%")
print("== Text claims vs table")
print("Llama: LCH-base",round(79.32-15.14,2),"printed 64.18 | -NExtLong",round(79.32-70.15,2),"printed 9.17 | -RRSI",round(79.32-39.67,2),"printed 39.65")
print("Qwen: -base",round(78.73-61.91,2),"printed 16.82 | -PolicyLong",round(78.73-64.10,2),"printed 14.63 | -RRSI",round(78.73-38.46,2),"printed 40.27")
print("Recall margin over RRSI: Llama",round(100-28.19,2),"printed 71.81; Qwen",round(100-39.11,2),"printed 60.89 (text 60.89 written as 60.89?)")
print("HELMET-only margin (H-Avg): Llama vs NExtLong",round(64.01-58.80,2),"; Qwen vs PolicyLong",round(63.18-51.53,2),"; RULER-only: Llama vs NExtLong",round(94.62-81.50,2),"; Qwen vs PolicyLong",round(94.28-76.67,2))
print("Semantic categories (RAG, LongQA) vs best baseline: Llama RAG",round(59.70-64.63,2),"vs RRSI; LongQA",round(36.84-37.30,2),"vs NExtLong; Qwen RAG",round(56.33-56.88,2),"vs RRSI; LongQA",round(26.45-27.55,2),"vs RRSI")
print("== Table 3 (reranking RSI trajectory) vs Table 1 Rank column")
t3={"V0 BM25+sort (both)":[53.26,45.44,39.52,34.66,28.85],"Llama V1":[65.51,51.88,36.50,22.95,17.89],"Llama V2":[57.79,47.48,36.70,30.85,25.51],"Qwen V1":[68.14,55.13,37.06,25.12,17.08],"Qwen V2":[71.76,64.48,55.50,45.85,43.83]}
for k,v in t3.items(): print(f"  {k:20s} mean {sum(v)/5:6.2f}")
print("  Table 1 Rank: Llama 39.67, Qwen 56.28 -> equal to the V2 means of Table 3 (39.67 and 56.28)")
print("  Llama: V2 mean 39.67 vs V0 (BM25+sort, no LLM) 40.35 =",round(39.67-40.35,2),"; Qwen V2 vs V0 =",round(56.28-40.35,2))
print("  Table 3 says the runs use '500 records, 100 per length'; Table 6 has 405 re-rank test + 210 dev = 615 total ->",500-405,"at least that many of the 500 are not test records")
print("== Table 4 cost checks")
print("NExtLong 960 GPU-h x $3.85 =",round(960*3.85,2),"(printed 3,696.00); PolicyLong 482.81 x 3.85 =",round(482.81*3.85,2),"(printed 1,858.82)")
for name,i,o,ri,ro,pr in [("Inference Llama RRSI",236.05,89.55,0.02,0.04,8.30),("Inference Llama LCH",408.00,1.87,0.02,0.04,8.23),("Inference Qwen RRSI",285.61,8.33,0.10,0.10,29.39),("Inference Qwen LCH",535.08,2.34,0.10,0.10,53.74)]:
    print(f"  {name:22s} recomputed {i*ri+o*ro:7.2f} printed {pr}")
print("Development (rates $4 input, $0.40 cache-read input, $20 output per M):")
for name,i,o,pr in [("RRSI",52.42,3.87,331.56),("LongCapHarness",814.11,3.35,541.47)]:
    lo=i*0.40+o*20; hi=i*4+o*20
    print(f"  {name:15s} printed ${pr}; minimum at stated rates ${lo:7.2f} (all input cached), maximum ${hi:7.2f} (all input ordinary) -> printed within range: {lo<=pr<=hi}")
print("  RRSI: even with ALL input at the ordinary $4 rate the stated rates give $",round(52.42*4+3.87*20,2),"< printed $331.56")
print("  LongCapHarness implied ordinary-priced input (M tokens) if rest cached:",round((541.47-3.35*20-814.11*0.4)/3.6,1))
print("Ratios: dev cost / PolicyLong training",round(541.47/1858.82,3),"; / NExtLong",round(541.47/3696,3),"| dev input tokens ratio LCH/RRSI",round(814.11/52.42,1))
print("Total cost for the test set: dev + inference (Llama) LCH",round(541.47+8.23,2),"vs RRSI",round(331.56+8.30,2),"; Qwen LCH",round(541.47+53.74,2),"vs RRSI",round(331.56+29.39,2))
print("== LongBench-v2 (Qwen): Medium 34.47 v PolicyLong 27.10 =",round(34.47-27.10,2),"; Long 27.85 v 31.50 =",round(27.85-31.50,2),"; non-code test records 403 + dev 50 = 453 (full benchmark minus code domain)")
print("   binomial SE at p=0.3: n=100 ->",round(100*math.sqrt(.3*.7/100),1),"points; n=150 ->",round(100*math.sqrt(.3*.7/150),1),"points (illustrative; per-length counts are not given)")
