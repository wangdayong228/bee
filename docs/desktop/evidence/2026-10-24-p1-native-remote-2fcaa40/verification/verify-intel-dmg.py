import pathlib,subprocess,json,hashlib,plistlib,re,datetime
root=pathlib.Path(__file__).parent;config=json.loads((root/'runs.json').read_text());reports=[]
for f in (root/'artifact-zips').glob('*-verification.json'):
 r=json.loads(f.read_text())
 if r['artifact'].startswith('bee-macos15-intel-test-'):reports.append(r)
assert len(reports)==1,len(reports)
r=reports[0];base=root/'artifacts'/str(r['id']);dmgs=list(base.rglob('*.dmg'));assert len(dmgs)==1;dmg=dmgs[0]
pkgs=list(base.rglob('packages.json'));assert len(pkgs)==1;report=json.loads(pkgs[0].read_text());assert report['revision']==config['source']
checks=[]
def run(args,label):
 p=subprocess.run(args,capture_output=True,timeout=60);entry={'label':label,'args':list(map(str,args)),'exit':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')};checks.append(entry);assert p.returncode==0,entry;return p.stdout
run(['hdiutil','verify',str(dmg)],'DMG checksum')
entities=plistlib.loads(run(['hdiutil','attach','-readonly','-nobrowse','-noautoopen','-plist',str(dmg)],'Read-only no-browse mount'))['system-entities'];mounts=[e['mount-point'] for e in entities if 'mount-point'in e];assert len(mounts)==1;mount=pathlib.Path(mounts[0]);dev=next(e['dev-entry'] for e in entities if e.get('mount-point')==str(mount))
try:
 apps=list(mount.glob('*.app'));assert len(apps)==1;app=apps[0]
 run(['codesign','--verify','--deep','--strict',str(app)],'App seal')
 info=plistlib.loads((app/'Contents/Info.plist').read_bytes());assert info['CFBundleIdentifier']=='dev.tokhive.bee';assert info['LSMinimumSystemVersion']=='13.0';assert 'Downloads' in info['NSDownloadsFolderUsageDescription']
 for name in ['bee-desktop','bee']:
  binary=app/'Contents/MacOS'/name;file=run(['file',str(binary)],name+' architecture').decode();assert 'x86_64' in file and 'arm64' not in file
  commands=run(['otool','-l',str(binary)],name+' Mach-O load commands').decode();assert re.search(r'^\s*minos 13\.0\s*$',commands,re.M)
  if name=='bee':assert hashlib.sha256(binary.read_bytes()).hexdigest()==report['signedBundledBee']['sha256'];assert binary.stat().st_size==report['signedBundledBee']['bytes']
finally:
 run(['hdiutil','detach',dev],'Detach image')
# Fresh inventory verifies no mounted copy of this exact image remains.
inventory=plistlib.loads(run(['hdiutil','info','-plist'],'Mount inventory after detach'));assert all(pathlib.Path(i.get('image-path','')).resolve()!=dmg.resolve() for i in inventory['images'])
checks[-1].pop('stdout');checks[-1]['filteredResult']={'matchingImageAfterDetach':False};checks[-1]['filter']='Only the tested DMG match result is retained from the mount inventory.'
output={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':config['source'],'scope':'Read-only package validation; no Intel code execution or GUI/macOS13 acceptance','artifactId':r['id'],'appInfo':{k:info[k] for k in ['CFBundleIdentifier','LSMinimumSystemVersion','NSDownloadsFolderUsageDescription']},'checks':checks,'unmounted':True}
(root/'intel-dmg-verification.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'checks':len(checks),'unmounted':True,'source':config['source']}))
