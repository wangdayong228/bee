import concurrent.futures,subprocess,json,datetime,pathlib
root=pathlib.Path(__file__).parent
config=json.loads((root/'runs.json').read_text())
def fetch(item):
 name,rid=item
 result={}
 for resource in ['','/jobs','/artifacts']:
  data=json.loads(subprocess.check_output(['gh','api',f'repos/wangdayong228/bee/actions/runs/{rid}{resource}'],text=True,timeout=40))
  (root/f'{name}-{resource.strip("/") or "run"}-latest.json').write_text(json.dumps(data,indent=2)+'\n')
  result[resource]=data
 run=result[''];assert run['head_sha']==config['source'],(name,run['head_sha'])
 return {'name':name,'runId':rid,'status':run['status'],'conclusion':run['conclusion'],'jobs':[{'id':j['id'],'name':j['name'],'status':j['status'],'conclusion':j['conclusion'],'active':[s['name'] for s in j.get('steps',[]) if s['status']=='in_progress']} for j in result['/jobs']['jobs']],'artifacts':len(result['/artifacts']['artifacts'])}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: rows=list(pool.map(fetch,config['runs'].items()))
output={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':rows}
(root/'snapshot-latest.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output))
