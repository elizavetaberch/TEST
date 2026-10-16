import struct, sys, collections, json

class R:
    def __init__(s, b, p=0): s.b=b; s.p=p
    def u8(s): v=s.b[s.p]; s.p+=1; return v
    def i32(s): v=struct.unpack_from('<i',s.b,s.p)[0]; s.p+=4; return v
    def u16(s): v=struct.unpack_from('<H',s.b,s.p)[0]; s.p+=2; return v
    def f32(s): v=struct.unpack_from('<f',s.b,s.p)[0]; s.p+=4; return v
    def cstr(s):
        e=s.b.index(b'\0',s.p); v=s.b[s.p:e].decode('latin1'); s.p=e+1; return v
    def lua(s):
        t=s.u8()
        if t==0: return s.f32()
        if t==1: return s.cstr()
        if t==2: return None
        if t==3: return bool(s.u8())
        if t==4:
            d={}
            while s.b[s.p]!=5:
                k=s.lua(); d[k if not isinstance(k,float) else int(k)]=s.lua()
            s.p+=1; return d
        raise ValueError('lua type %d at %d'%(t,s.p-1))

def header(r):
    h={}
    h['game']=r.cstr(); r.cstr()
    h['replay'],h['map']=r.cstr().split('\r\n')[:2]
    r.cstr()
    r.i32(); h['mods']=r.lua()
    r.i32(); h['scenario']=r.lua()
    n=r.u8(); h['sources']=[]
    for _ in range(n):
        name=r.cstr(); pid=r.i32(); h['sources'].append((name,pid))
    h['cheats']=r.u8()
    na=r.u8(); h['armies']={}
    for _ in range(na):
        r.i32(); pd=r.lua(); src=r.u8()
        h['armies'][src]=pd
        if src!=255: r.u8()
    h['seed']=r.i32()
    return h

def ops(r):
    while r.p+3<=len(r.b):
        t=r.u8(); ln=r.u16()
        data=r.b[r.p:r.p+ln-3]; r.p+=ln-3
        yield t,data

def parse_cmd(d):
    r=R(d); n=r.i32(); ents=[r.i32() for _ in range(n)]
    cid=r.i32(); r.i32(); ctype=r.u8(); r.i32()
    tt=r.u8(); tgt=None
    if tt==1: tgt=('ent',r.i32())
    elif tt==2: tgt=('pos',r.f32(),r.f32(),r.f32())
    r.u8(); fm=r.i32()
    if fm!=-1: [r.f32() for _ in range(5)]
    bp=r.cstr()
    return dict(ents=ents,cid=cid,ctype=ctype,tgt=tgt,bp=bp)

def events(path):
    b=open(path,'rb').read(); r=R(b); h=header(r)
    tick=0; src=None; ev=[]
    for t,d in ops(r):
        if t==0: tick+=struct.unpack('<i',d)[0]; continue
        if t==1: src=d[0]; continue
        ev.append((tick,src,t,d))
    return h,ev,tick

# --- CLI: python3 sc2rp.py <replay.SC2ReplayDLC> [minutes_of_build_order] ---
FACTIONS = {1: 'UEF', 2: 'Cybran', 3: 'Illuminate/Aeon'}
OP_ISSUE, OP_FACTORY, OP_RESEARCH, OP_CALLBACK = 15, 16, 18, 28  # empirically identified

def fmt(t): return '%d:%02d' % (t // 600, (t // 10) % 60)  # 10 sim ticks per second

def summary(path, bo_minutes=6):
    h, ev, total = events(path)
    names = {k: v['PlayerName'].encode('latin1').decode('utf8', 'replace') for k, v in h['armies'].items()}
    print('%s | %s | map %s | duration %s' % (h['game'], h['replay'], h['map'], fmt(total)))
    print('options:', {k: v for k, v in h['scenario'].get('Options', {}).items() if k != 'RestrictedCategories'})
    builds = collections.defaultdict(list); research = collections.defaultdict(list); acts = collections.Counter()
    for tick, src, t, d in ev:
        if t in (OP_ISSUE, OP_FACTORY, 17, 25, OP_CALLBACK): acts[src] += 1
        if t in (OP_ISSUE, OP_FACTORY):
            c = parse_cmd(d)
            if c['ctype'] in (9, 10) and c['bp']: builds[src].append((tick, c['bp']))
        elif t == OP_RESEARCH:
            research[d[3]].append((tick, int.from_bytes(d[9:11], 'little')))
    for s, a in sorted(h['armies'].items()):
        print('\n== %s | %s | team %d | actions %d (~%.0f APM) | research picks %d' % (
            names[s], FACTIONS.get(int(a['Faction']), a['Faction']), a['Team'], acts[s],
            acts[s] / max(total / 600, 1), len(research[s])))
        cnt = collections.Counter(bp for _, bp in builds[s])
        print('   orders total:', ', '.join('%s x%d' % kv for kv in cnt.most_common()))
        print('   first %d min:' % bo_minutes, ' | '.join('%s %s' % (fmt(t), bp) for t, bp in builds[s] if t < bo_minutes * 600))
        print('   research ids:', ' '.join('%s#%d' % (fmt(t), r) for t, r in research[s]))

if __name__ == '__main__':
    summary(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 6)
