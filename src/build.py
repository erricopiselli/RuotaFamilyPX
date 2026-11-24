import json,sys,unicodedata,re
W=[12,14,14,12]
SETS={1:[[1]],2:[[1,2]],3:[[0,1,2],[1,2,3]],4:[[0,1,2,3]]}
def fits(ph):
    words=ph.split()
    for k in (1,2,3,4):
        for rows in SETS[k]:
            lines=[];cur='';ri=0;ok=True
            for w in words:
                if ri>=len(rows): ok=False;break
                cand=(cur+' '+w).strip()
                if len(cand)<=W[rows[ri]]: cur=cand
                else:
                    if not cur: ok=False;break
                    lines.append(cur);ri+=1;cur=w
                    if ri>=len(rows) or len(w)>W[rows[ri]]: ok=False;break
            if ok and cur and ri<len(rows): return True
    return False
STOP=set("IL LO LA I GLI LE L UN UNA UNO DI DEL DELLA DELL DEI DEGLI DELLE A AL ALLA AI DA DAL IN NEL NELLA CON SU SUL PER E O D CHE TRA FRA".split())
def _w(s): return [w for w in re.split(r"[ ']",''.join(c for c in unicodedata.normalize('NFD',s.upper()) if c.isalpha() or c in " '")) if w and w not in STOP]
def _st(w): return w[:5] if len(w)>5 else w
def leak(h,p):  # la frase non può contenere parole dell'indizio
    hw={_st(w) for w in _w(h)}; return any(_st(w) in hw for w in _w(p))
MINL=22         # almeno 22 lettere: frasi su più righe, niente risposte banali
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.upper()) if c.isalpha() and ord(c)<128)
out=[];seen=set();bad=0
for fn in sys.argv[1:-1]:
    for line in open(fn,encoding='utf-8'):
        line=line.strip()
        if not line or '|' not in line: continue
        h,p=[x.strip() for x in line.split('|',1)]
        p=p.upper()
        if re.search(r"[^A-ZÀÈÉÌÒÙ' ]",p): print('CHARS',p);bad+=1;continue
        if not fits(p): print('FIT',p);bad+=1;continue
        if len(norm(p))<MINL: print('CORTA',p);bad+=1;continue
        if leak(h,p): print('INDIZIO',h,p);bad+=1;continue
        k=norm(p)
        if k in seen: print('DUP',p);bad+=1;continue
        seen.add(k);out.append([h,p])
json.dump(out,open(sys.argv[-1],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('ok',len(out),'bad',bad)
