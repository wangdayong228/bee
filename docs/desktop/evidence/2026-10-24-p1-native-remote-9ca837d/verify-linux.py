import pathlib,json,hashlib,re,sys
base=pathlib.Path('.cache/qa/p1-native-remote-9ca837d')
rev='9ca837d902fbf026be9931f796a3d1289e33dad3'
run='39941148651'
tee='a687f86d781e825c04c1d84d75b41bba5d862254'
tee_hash='4bc9caad3ad2ce5de01b9983a750cee6380098fc308333c30c098fbf8e7bad38'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v,e):
 if not v:raise RuntimeError(e)
for row in sys.argv[1:]:
 root=base/'linux'/row; ev=root/'checks/desktop-ci-evidence'
 arm=row.endswith('-arm');target=('aarch64' if arm else 'x86_64')+'-unknown-linux-gnu';arch='arm64' if arm else 'x64';goarch='arm64' if arm else 'amd64'
 n=read(ev/'native.json')
 check(n['revision']==rev and str(n['runId'])==run and n['target']==target and n['platform']=='linux' and n['arch']==arch,f'{row} native identity mismatch: {n}')
 check(n['ok'] and all(c['ok'] for c in n['checks']),f'{row} native checks failed: {n}')
 pkgs=list((root/'test').rglob('*.AppImage'));srcs=list((root/'test').rglob('*.source.json'))
 check(len(pkgs)==len(srcs)==1,f'{row} expected one AppImage/source, actual {pkgs}/{srcs}')
 pkg,src=pkgs[0],srcs[0];source=read(src);ph=sha(pkg);sh=sha(src)
 check(source['revision']==rev and source['teeRevision']==tee and source['target']==target and source['goos']=='linux' and source['goarch']==goarch,f'{row} source mismatch: {source}')
 check(tee_hash in (ev/'tee.log').read_text(),f'{row} TEE hash absent')
 smokes={}
 for mode in ['extract','fuse']:
  p=ev/f'smoke-{mode}/smoke.json'
  check(p.exists(),f'{row} {mode} smoke absent')
  s=read(p)
  check(s['ok'] and s['mode']==mode and s['target']==target and s['revision']==rev,f'{row} {mode} smoke identity/ok mismatch: {s}')
  check(s['package']['bytes']==pkg.stat().st_size and s['package']['sha256']==ph,f'{row} {mode} package bytes/hash mismatch')
  check(s['sourceSha256']==sh and s['provenance']['source']==source,f'{row} {mode} source mismatch')
  check(s['packagedBee']['sha256']==s['provenance']['binarySha256']==source['binarySha256'],f'{row} {mode} Bee hash mismatch')
  o=s['observation'];check(o['ok'] and o['observedMs']>=10000,f'{row} {mode} observation invalid: {o}')
  check(o['cleanup']['parentClosed'] and o['cleanup']['liveRemaining']==[],f'{row} {mode} cleanup live process: {o["cleanup"]}')
  resize=o['resize'];check(resize['requested']=={'width':860,'height':600},f'{row} {mode} wrong requested minimum size: {resize}')
  def dimensions(g):
   widths=re.findall(r'^WIDTH=(\d+)$',g,re.M);heights=re.findall(r'^HEIGHT=(\d+)$',g,re.M)
   check(len(widths)==len(heights)==1,f'{row} {mode} ambiguous geometry: {g}')
   return [int(widths[0]),int(heights[0])]
  check(dimensions(resize['geometry'])==[860,600],f'{row} {mode} resize geometry not 860x600')
  finals=[x for x in o['samples'] if x['phase']=='final'];check(len(finals)==1,f'{row} {mode} missing unique final sample')
  final=finals[0];check(dimensions(final['geometry'])==[860,600],f'{row} {mode} final geometry not 860x600')
  check(final['window']['id']==resize['window']['id']==o['window']['id'],f'{row} {mode} final window identity mismatch')
  check(final['window']['pid']==resize['window']['pid']==o['pid'],f'{row} {mode} owner PID mismatch')
  check(any(w['id']==final['window']['id'] and w['pid']==o['pid'] for w in o['lastWindows']),f'{row} {mode} final owned window absent from last probe')
  check(any(p['pid']==o['pid'] and not p['state'].startswith('Z') for p in o['processes']),f'{row} {mode} final parent liveness record absent')
  smokes[mode]={k:o[k] for k in ['ok','observedMs','exit','cleanup','scope']};smokes[mode]['minimumClientSize']={'requested':resize['requested'],'resizeGeometry':resize['geometry'],'finalGeometry':final['geometry'],'sameWindowId':final['window']['id']}

 logs={}
 for name,pattern in [('browser-e2e.log',r'(\d+) passed'),('cargo-test.log',r'test result: ok\. (\d+) passed; (\d+) failed; (\d+) ignored')]:
  text=(ev/name).read_text();matches=re.findall(pattern,text);check(matches,f'{row} {name} missing counts');logs[name]=matches
 raw=(base/f'linux-{row}-job.log').read_text()
 check('vite build --mode demo' in raw and tee_hash in raw,f'{row} raw log lacks demo/TEE')
 check('489 passed' in raw and '489 passed' in (ev/'browser-e2e.log').read_text(),f'{row} browser count not independently matched')
 check('36 passed; 0 failed; 0 ignored' in raw and '36 passed; 0 failed; 0 ignored' in (ev/'cargo-test.log').read_text(),f'{row} Rust count not independently matched')
 out={'row':row,'revision':rev,'runId':run,'target':target,'nativeOk':True,'package':{'path':str(pkg),'bytes':pkg.stat().st_size,'sha256':ph},'source':{'path':str(src),'sha256':sh,'content':source},'teeArchiveSha256':tee_hash,'downloadedLogCounts':logs,'smokes':smokes}
 (root/'verification-summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False))
