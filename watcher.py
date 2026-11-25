import csv,gzip,json,re,os,sys
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import urlopen,Request
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'
SOURCES={'stripe':'Stripe','brex':'Brex','ramp':'Ramp','robinhood':'Robinhood','coinbase':'Coinbase','affirm':'Affirm','chime':'Chime','plaid':'Plaid','sofi':'SoFi','betterment':'Betterment','wealthfront':'Wealthfront','clearstreet':'Clear Street','public':'Public','imc':'IMC','janestreet':'Jane Street','twosigma':'Two Sigma','point72':'Point72','acadianassetmanagement':'Acadian Asset Management','flowtraders':'Flow Traders','hudsonrivertrading':'Hudson River Trading'}
FIELDS='posting_id source source_id employer title location department posted_date url in_role first_run first_seen last_seen status removed_date'.split()
def role(title):
 return bool(re.search(r'\banalyst\b',title,re.I) and re.search(r'investment bank|capital markets|corporate finance|financial analyst|equity research|valuation|investment analyst|mergers|acquisitions',title,re.I))
def normalize(source,job):
 title=job['title']; sid=str(job['id']); loc=job.get('location') or {}; deps=job.get('departments') or []
 return dict(posting_id=source+':'+sid,source=source,source_id=sid,employer=SOURCES[source],title=title,location=loc.get('name',''),department=', '.join(x['name'] for x in deps),posted_date=(job.get('first_published') or '')[:10],url=job.get('absolute_url',''),in_role=str(role(title)).lower())
def build(data=DATA):
 rows={}; seen=set(); dates=[]
 for folder in sorted((data/'raw').glob('*')):
  files=sorted(folder.glob('*.json.gz'))
  if not files: continue
  day=folder.name; dates.append(day)
  for f in files:
   source=f.name.removesuffix('.json.gz'); first=source not in seen; seen.add(source)
   with gzip.open(f,'rt',encoding='utf-8') as h: jobs=json.load(h)['jobs']
   current=set()
   for job in jobs:
    row=normalize(source,job); key=row['posting_id']; current.add(key); old=rows.get(key)
    row.update(first_run=old['first_run'] if old else str(first).lower(),first_seen=old['first_seen'] if old else day,last_seen=day,status='open',removed_date=''); rows[key]=row
   for key,row in rows.items():
    if row['source']==source and key not in current and row['status']=='open': row.update(status='removed',removed_date=day)
 data.mkdir(exist_ok=True)
 with (data/'history.csv').open('w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=FIELDS); w.writeheader(); w.writerows(rows[k] for k in sorted(rows))
 return list(rows.values()),dates

def run():
 now=datetime.now(timezone.utc); day=now.date().isoformat(); folder=DATA/'raw'/day; folder.mkdir(parents=True,exist_ok=True); results=[]
 for source in SOURCES:
  path=folder/(source+'.json.gz'); path.unlink(missing_ok=True)
  try:
   with urlopen(Request(f'https://boards-api.greenhouse.io/v1/boards/{source}/jobs?content=false',headers={'User-Agent':'JobWatcher/1.0'}),timeout=20) as r: raw=r.read()
   jobs=json.loads(raw)['jobs']; assert isinstance(jobs,list)
   if len(jobs)>5000: raise ValueError('Board exceeds 5000 postings; replace source')
   for job in jobs: normalize(source,job)
   path.write_bytes(gzip.compress(raw,mtime=0)); results.append(dict(name=source,ok=True,count=len(jobs)))
  except Exception as e: print(source,e); results.append(dict(name=source,ok=False,count=0))
 rows,dates=build(); new=[r for r in rows if r['first_seen']==day and r['first_run']=='false']; removed=[r for r in rows if r['removed_date']==day]
 status=dict(run_time=now.isoformat(),first_run_date=dates[0] if dates else None,days_with_success=len(dates),open=sum(r['status']=='open' for r in rows),new_today=len(new),removed_today=len(removed),sources=results)
 (DATA/'status.json').write_text(json.dumps(status,indent=2)+'\n'); (DATA/'issue.md').write_text('\n'.join(['## New postings',*[f"- [{r['employer']}: {r['title']}]({r['url']})" for r in new],'## Removed postings',*[f"- [{r['employer']}: {r['title']}]({r['url']})" for r in removed]])+'\n')
if __name__=='__main__':
 if '--build' in sys.argv: build()
 else: run()
