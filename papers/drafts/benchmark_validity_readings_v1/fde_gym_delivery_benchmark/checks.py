rows = {  # name: (S, lo, hi, U, C, resolved) from Table 3
 "Opus 5.5":(0.56,0.50,0.62,0.70,0.14,14),"Sonnet 5.5":(0.49,0.43,0.55,0.67,0.18,15),
 "GPT-6 Astra":(0.38,0.30,0.46,0.60,0.22,9),"GPT-6.1 Sol":(0.37,0.28,0.44,0.57,0.20,7),
 "GLM-5.3 Flash":(0.22,0.11,0.31,0.40,0.18,8),"DeepSeek V4.1 Flash":(0.21,0.10,0.30,0.38,0.18,9),
 "Gemini 3.8 Flash":(0.19,0.09,0.28,0.45,0.26,4),"Qwen 3.8 Flash":(0.07,-0.03,0.17,0.27,0.21,4),
 "GPT-5.5":(0.03,-0.05,0.11,0.11,0.08,0),"GPT-6 Luna":(-0.12,-0.20,-0.05,0.00,0.12,0),
 "Mistral Small 4":(-0.32,-0.41,-0.23,-0.31,0.01,0),"Haiku 4.5":(-0.33,-0.42,-0.24,-0.23,0.09,0),
 "Haiku 4.5 (thinking)":(-0.35,-0.44,-0.26,-0.27,0.08,0)}
print("C1 S vs U-C")
for n,(s,lo,hi,u,c,r) in rows.items(): print(f"  {n:22s} S={s:+.2f} U-C={u-c:+.2f} resid={s-(u-c):+.2f} {'OK' if abs(s-(u-c))<=0.011 else 'FAIL'}")
print("C2 contact-cost share of L0->L1 drop (range endpoints)")
lo_rise, hi_rise = 0.18-0.10, 0.24-0.07
print(f"  rise range {lo_rise:.2f}-{hi_rise:.2f}; share of 0.28: {lo_rise/0.28:.2f}-{hi_rise/0.28:.2f}")
print("C3 implied U for S>=0.8 at mean C")
for n in ("Opus 5.5","Sonnet 5.5","GPT-6 Astra"):
    c=rows[n][4]; print(f"  {n:12s} C={c:.2f} -> U>={0.8+c:.2f}")
print("C4 CI overlap (adjacent)")
names=list(rows)
for a,b in zip(names,names[1:]):
    print(f"  {a} vs {b}: {'overlap' if rows[a][1]<=rows[b][2] else 'separate'}")
print("  Opus vs Astra:", 'overlap' if rows['Opus 5.5'][1]<=rows['GPT-6 Astra'][2] else 'separate')
