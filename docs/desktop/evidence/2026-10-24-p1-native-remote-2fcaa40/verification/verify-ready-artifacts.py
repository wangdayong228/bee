import pathlib,json,re,hashlib,datetime
root=pathlib.Path(__file__).parent;config=json.loads((root/'runs.json').read_text());rows=[]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def unique(paths,label):
 paths=list(paths);assert len(paths)==1,(label,[str(p) for p in paths]);return paths[0]
def logcounts(base):
 out={}
 for name in ['browser-e2e.log','cargo-test.log','signed-app.log','go-test.log','tooling.log','bridge.log']:
  paths=list(base.rglob(name))
  if not paths:continue
  assert len(paths)==1,(name,paths)
  text=re.sub(r'\x1b\[[0-9;]*m','',paths[0].read_text(encoding='utf-8-sig'))
  if name=='browser-e2e.log':out[name]=re.findall(r'(?m)^\s*([0-9]+) (passed|failed)(?: \(([^)]+)\))?\s*$',text)
  elif name in ['cargo-test.log','signed-app.log']:out[name]=re.findall(r'test result: ([^\n]+)',text)
  elif name=='go-test.log':out[name]={'okPackages':len(re.findall(r'(?m)^ok\s',text))}
  else:out[name]={k:int(v) for k,v in re.findall(r'(?m)^[ℹ#] (tests|pass|fail|skipped) ([0-9]+)',text)}
 return out
for f in sorted((root/'artifact-zips').glob('*-verification.json')):
 record=load(f);base=root/'artifacts'/str(record['id']);name=record['artifact']
 assert record['source']==config['source']
 row={'id':record['id'],'name':name,'counts':logcounts(base)}
 if '-test-' in name:
  sourcepath=unique(base.rglob('*.source.json'),name+' source');source=load(sourcepath);assert source['revision']==config['source'];assert source['teeRevision']=='a687f86d781e825c04c1d84d75b41bba5d862254'
  row['source']=source;row['sourceSHA256']=hashfile(sourcepath)
  packages=[p for p in base.rglob('*') if p.is_file() and p.suffix in ['.exe','.dmg','.AppImage']];package=unique(packages,name+' package');row['package']={'name':package.name,'bytes':package.stat().st_size,'sha256':hashfile(package)}
  reports=list(base.rglob('packages.json'))
  if reports:
   report=load(unique(reports,name+' manifest'));assert report['revision']==config['source'];pm=unique(report['packages'],name+' packages list');assert pm['bytes']==row['package']['bytes'];assert pm['sha256']==row['package']['sha256']
   if 'sidecar' in report:assert source==report['sidecar']['source'];assert row['sourceSHA256']==report['sidecar']['sourceSha256']
   if 'source' in report:assert source==report['source'];assert row['sourceSHA256']==report['sourceFile']['sha256']
 for p in base.rglob('smoke.json'):
  s=load(p);assert s['revision']==config['source'];assert s['ok'] is True;assert s['observation']['ok'] is True
  row.setdefault('smoke',[]).append({'mode':s['mode'],'package':s['package'],'sourceSha256':s['sourceSha256'],'packagedBeeSHA256':s['packagedBee']['sha256'],'observedMs':s['observation']['observedMs'],'finalGeometry':s['observation']['finalGeometry']['actual'],'cleanup':s['observation']['cleanup'],'smokeFile':str(p.relative_to(root))})
 rows.append(row)
# Cross-artifact checks bind runner reports to the actual downloaded package and source bytes.
for row in rows:
 if not row.get('smoke'):continue
 prefix=row['name'].replace('-checks-','-test-');package=unique([r for r in rows if r['name']==prefix],prefix)
 for s in row['smoke']:
  assert s['package']['bytes']==package['package']['bytes'];assert s['package']['sha256']==package['package']['sha256'];assert s['sourceSha256']==package['sourceSHA256'];assert s['packagedBeeSHA256']==package['source']['binarySha256'];assert s['observedMs']>=10000;assert s['finalGeometry']=={'width':860,'height':600};assert not s['cleanup']['liveRemaining'];assert s['cleanup']['parentClosed']
output={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':config['source'],'artifacts':rows}
(root/'artifact-validation-latest.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output))
