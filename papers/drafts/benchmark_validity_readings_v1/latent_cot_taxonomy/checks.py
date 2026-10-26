rows={ # content-used cells from Table 1: (C0, C1, donor delta)
"GPT2 COCONUT GSM8k":(0.333,0.103,-0.307),"GPT2 CODI GSM8k":(0.430,0.263,-0.380),"GPT2 SIMCOT GSM8k":(0.360,0.080,-0.333),
"GPT2 SIMCOT ProsQA":(0.993,0.800,-0.077),"GPT2 SIMCOT PrOntoQA":(1.000,0.827,-0.507),
"Llama COCONUT GSM8k":(0.370,0.253,-0.080),"Llama CODI GSM8k":(0.553,0.360,-0.373),"Llama SIMCOT GSM8k":(0.390,0.307,-0.087)}
print("C1 donor vs deletion on the eight content-used cells (paper: five worse, one milder, two undetermined)")
for k,(c0,c1,d) in rows.items():
    dele=c1-c0; print(f"  {k:22s} deletion {dele:+.3f} donor {d:+.3f} diff {d-dele:+.3f}")
leaf={"carrier":5,"empty":2,"bare placeholder":1,"laid-out placeholder":1,"assembling":2,"unstructured":6,"inert unprofiled":2,"unclassified (unresolved)":2}
print("C2 leaf census from Table 16 (hand-tallied), total =",sum(leaf.values()),"; per leaf:",leaf)
