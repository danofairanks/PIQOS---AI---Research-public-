# E1 arithmetic on Table 3 / Table 5 / Table 4 of arXiv 2609.19644v1 (values transcribed from the PDF text; page numbers in README).
# (venue, n, scholarpeer_mean, scholarpeer_accept, stanford_mean, stanford_accept)
human=[('ICLR2026',5,6.8,60.0,5.2,60.0),('NeurIPS2025',38,6.2,65.8,5.5,76.3),('ICML2026sp',64,6.9,79.7,6.1,96.9)]
ai   =[('ICLR2026',4,7.0,100.0,5.4,75.0),('NeurIPS2025',33,7.3,87.9,5.6,75.8),('ICML2026sp',49,7.6,93.9,5.7,69.4)]
def wavg(rows,i):
    n=sum(r[1] for r in rows); return sum(r[1]*r[i] for r in rows)/n
print('n human',sum(r[1] for r in human),'n AI',sum(r[1] for r in ai),'(AI papers are the successful subset of the same 107 problems)')
for name,i in (('ScholarPeer mean',2),('ScholarPeer accept %',3),('Stanford mean',4),('Stanford accept %',5)):
    print('%-22s human(weighted) %.3f   AI(weighted) %.3f   AI-human %+.3f'%(name,wavg(human,i),wavg(ai,i),wavg(ai,i)-wavg(human,i)))
print('Per venue, held-out reviewer (Stanford), AI minus human mean / accept-rate:')
for h,a in zip(human,ai): print('  %-12s mean %+.1f   accept %+.1f pts   (AI n=%d, human n=%d)'%(h[0],a[4]-h[4],a[5]-h[5],a[1],h[1]))
print('Success rate 86/107 = %.1f%%; failures 21 (excluded from the AI review averages)'%(100*86/107))
print('Table 5 (ICML49): Stanford accept by review round: 49.0 -> 73.5 -> 69.4 (round 2 lower than round 1); ScholarPeer 46.9 -> 79.6 -> 93.9')
print('Table 7 integrity audit denominators: 49-50 papers (the ICML 49-task set), headline success count is 86')
