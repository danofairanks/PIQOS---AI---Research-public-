# Values transcribed by hand from the paper's text-extracted Tables 3, 4, 10-12, 15-17 (pdftotext).
meme={ # ER Agg Tr Del Cas Abs Overall
"4omini":{"RAW":(97,19,78,26,4.27,11.54,39.30),"MemMachine":(98,9,73,29,4.88,8.46,37.06),"EMem":(48,36,63,37,6.71,12.31,33.84),"Memora":(93,11,58,23,6.10,10.00,33.52)},
"DSV4f":{"RAW":(100,21,87,29,3.66,18.46,43.19),"MemMachine":(100,11,85,48,7.32,16.92,44.71),"EMem":(48,36,87,38,6.10,15.38,38.41),"Memora":(92,2,57,38,9.15,20.00,36.36)}}
tasks=("ER","Agg","Tr","Del","Cas","Abs")
print("C1 MEME per-task: RAW-RAG minus best of {MemMachine, EMem, Memora} (lower bound on the best baseline; other baselines omitted)")
for rd,d in meme.items():
    for i,t in enumerate(tasks):
        best=max((v[i],k) for k,v in d.items() if k!="RAW")
        print(f"  {rd:7s} {t:3s} RAW {d['RAW'][i]:6.2f} best {best[1]:10s} {best[0]:6.2f} diff {d['RAW'][i]-best[0]:+6.2f}")
mab={"4omini":{"RAW":(67.85,47.68,31.74,46.00,48.32),"Memora":(68.78,47.77,26.82,32.00,43.84)},
     "DSV4f":{"RAW":(75.78,50.39,33.48,54.00,53.41),"Memora":(75.05,50.72,31.76,34.00,47.88)}}
print("C2 MemoryAgentBench: RAW-RAG minus Memora by capability (AR, TTL, LRU, CR); share of overall lead from CR")
for rd,d in mab.items():
    diffs=[a-b for a,b in zip(d['RAW'][:4],d['Memora'][:4])]; tot=sum(diffs)/4
    print(f"  {rd:7s} {[round(x,2) for x in diffs]} mean {tot:.2f} (reported {d['RAW'][4]-d['Memora'][4]:.2f}); CR share {diffs[3]/4/tot:.0%}")
print("C3 LoCoMo / LongMemEval: main-table (mixed settings) vs matched-setting leads")
print("  Table 3: 4o-mini",round(89.07-88.12,2),"(vs MemMachine); 4.1-mini",round(93.70-93.05,2),"(vs EverMemOS, Qwen3-setting published score)")
print("  Table 10 (text-emb, matched): 4o-mini vs MemMachine",round(89.07-88.12,2),"; 4.1-mini vs MemMachine",round(93.70-91.69,2))
print("  Table 11 (Qwen3, matched): 4o-mini vs EverMemOS",round(89.13-86.76,2),"; 4.1-mini vs EverMemOS",round(94.55-93.05,2))
print("  LongMemEval: Table 15 vs Memora (policy retriever, published)",round(87.53-87.40,2),"; Table 16 (Qwen3) vs EverMemOS",round(89.93-83.00,2))
print("  LongMemEval non-abstention (Table 17): vs EMem/EMem-G textemb",round(87.80-83.00,2),round(87.80-84.90,2),"; Qwen3",round(90.57-83.00,2),round(90.57-84.90,2))
print("  Unchanged-context rerun variability on LoCoMo (A.4.4): +0.281 points; main-table lead 0.65-0.95; matched leads 0.95-2.37")
print("C4 Independent LoCoMo reproduction (second-hand, README via fetch): 88.68 / 93.48 -> deltas vs paper",round(88.68-89.07,2),round(93.48-93.70,2),"; leads over best compared",round(88.68-88.12,2),round(93.48-93.05,2))
print("C5 Short-answer LoCoMo (Table 12) RAW-RAG(minimal) minus Nemori")
print("  GPT-4.1-mini: J",round(90.87-79.40,2),"F1",round(49.57-53.40,2),"B1",round(41.35-45.60,2))
print("  GPT-4o-mini : J",round(85.78-74.40,2),"F1",round(52.58-49.50,2),"B1",round(44.50-38.50,2))
print("C6 Mem0 published LoCoMo, category-weighted (841/282/321/96):",round((67.13*841+51.15*282+55.51*321+72.93*96)/(841+282+321+96),2),"vs published aggregate 66.88")
print("C7 PersonaMem-v2 gaps vs RAW-RAG 49.62: EverMemOS",round(53.25-49.62,2),"MemOS",round(50.72-49.62,2),"; binomial SE at n=5000, p=0.5:",round(100*(0.25/5000)**0.5,2),"pp each")
