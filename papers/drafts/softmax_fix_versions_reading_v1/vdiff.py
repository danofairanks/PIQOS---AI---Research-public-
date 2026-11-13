# Sentence-level diff of two PDF text layers (pdftotext output files). Run: python3 -I vdiff.py DIR   where DIR holds v1.txt and v3.txt (pdftotext of the two PDFs; the PDFs are not stored here).
import re,difflib,unicodedata,sys
d=sys.argv[1]
def load(p):
    t=open(p,encoding='utf8').read()
    t=unicodedata.normalize('NFKC',t).replace('“','"').replace('”','"').replace('’',"'").replace('‘',"'")
    t=re.sub(r'-\n(?=[a-z])','',t)
    t=re.sub(r'\n(?!\n)',' ',t)
    t=re.sub(r'[ \t]+',' ',t)
    paras=[p.strip() for p in t.split('\n\n') if len(p.strip())>40]
    sents=[]
    for p in paras:
        for s in re.split(r'(?<=[.!?]) (?=[A-Z])',p):
            s=s.strip()
            if len(s.split())>=6: sents.append(s)
    return sents
a=load(d+'/v1.txt'); b=load(d+'/v3.txt')
print(len(a),'v1 sentences;',len(b),'v3 sentences')
n=lambda s:re.sub(r'\W+',' ',s.lower()).strip()
na=[n(s) for s in a]; nb=[n(s) for s in b]
sm=difflib.SequenceMatcher(None,na,nb,autojunk=False)
eq=sum(i2-i1 for t,i1,i2,j1,j2 in sm.get_opcodes() if t=='equal')
print('identical sentences:',eq,'| ratio',round(sm.ratio(),3))
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal': continue
    print('\n['+tag+']')
    for s in a[i1:i2]: print('  v1:',s[:360])
    for s in b[j1:j2]: print('  v3:',s[:360])
