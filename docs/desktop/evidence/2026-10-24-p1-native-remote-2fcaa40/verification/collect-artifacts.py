import concurrent.futures,subprocess,json,hashlib,zipfile,pathlib,datetime,shutil,sys
root=pathlib.Path(__file__).parent
config=json.loads((root/'runs.json').read_text()); archive=root/'artifact-zips';extract=root/'artifacts';archive.mkdir(exist_ok=True);extract.mkdir(exist_ok=True)
items=[]
wanted={int(value) for value in sys.argv[1:]}
for name,rid in config['runs'].items():
 data=json.loads((root/f'{name}-artifacts-latest.json').read_text())
 for a in data['artifacts']:
  assert config['source'] in a['name'],(name,a['name'])
  assert not a['expired'],a['id']
  assert a['workflow_run']['head_sha']==config['source'],a['workflow_run']
  if not wanted or a['id'] in wanted:items.append((name,rid,a))
def collect(item):
 name,rid,a=item;aid=str(a['id']);dest=archive/(aid+'.zip');record=archive/(aid+'-verification.json')
 if record.exists():
  old=json.loads(record.read_text());assert old['artifact']==a['name'];assert hashlib.sha256(dest.read_bytes()).hexdigest()==old['sha256'];return {'id':a['id'],'name':a['name'],'cached':True}
 part=dest if dest.exists() else archive/(aid+'.part')
 if not part.exists() or part.stat().st_size != a['size_in_bytes']:
  # Keep auth in process memory/stdin; never emit tokens or signed redirect URLs.
  token=subprocess.check_output(['gh','auth','token'],text=True,timeout=15).strip()
  quote=lambda value: '"'+value.replace('\\','\\\\').replace('"','\\"')+'"'
  curl_config_text='url = '+quote(f'https://api.github.com/repos/wangdayong228/bee/actions/artifacts/{aid}/zip')+'\nheader = '+quote('Authorization: Bearer '+token)+'\n'
  redirect=subprocess.run(['curl','--silent','--show-error','--dump-header','-','--output','/dev/null','--config','-'],input=curl_config_text,text=True,capture_output=True,timeout=45)
  assert redirect.returncode==0,(aid,'redirect transport exit',redirect.returncode)
  locations=[line.split(':',1)[1].strip() for line in redirect.stdout.splitlines() if line.lower().startswith('location:')]
  assert len(locations)==1 and locations[0].startswith('https://'),(aid,'HTTPS redirect absent')
  download=subprocess.run(['curl','--fail','--silent','--show-error','--location','--continue-at','-','--max-time','900','--retry','3','--retry-delay','1','--output',str(part),'--config','-'],input='url = '+quote(locations[0])+'\n',text=True,capture_output=True,timeout=950)
  assert download.returncode==0,(aid,'resumable transfer exit',download.returncode)
 blob=part.read_bytes();digest=hashlib.sha256(blob).hexdigest();assert a.get('digest')=='sha256:'+digest,(aid,a.get('digest'),digest)
 dest_size=len(blob);assert dest_size==a['size_in_bytes'],(aid,dest_size,a['size_in_bytes'])
 if part!=dest:part.rename(dest)
 target=extract/aid;target.mkdir(exist_ok=True)
 files=[]
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None,aid
  for info in z.infolist():
   path=pathlib.PurePosixPath(info.filename);assert not path.is_absolute() and '..' not in path.parts,info.filename
   if info.is_dir():continue
   content=z.read(info);out=target.joinpath(*path.parts);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(content)
   files.append({'path':info.filename,'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest()})
 out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runId':rid,'source':config['source'],'id':a['id'],'artifact':a['name'],'reportedBytes':a['size_in_bytes'],'downloadedBytes':dest_size,'githubDigest':a['digest'],'sha256':digest,'zipCRCValid':True,'files':files}
 record.write_text(json.dumps(out,indent=2)+'\n');assert dest_size==a['size_in_bytes'],(aid,dest_size,a['size_in_bytes'])
 return {'id':a['id'],'name':a['name'],'files':len(files),'bytes':dest_size,'sha256':digest}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(collect,items))
print(json.dumps({'collected':results}))
