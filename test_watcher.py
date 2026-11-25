import gzip,json
import pytest
from watcher import SOURCES,normalize,role,build
@pytest.mark.parametrize('source',SOURCES)
def test_conversion(source):
 r=normalize(source,{'id':1,'title':'Investment Banking Analyst','location':{'name':'NY'},'absolute_url':'https://example.com'})
 assert r['posting_id']==source+':1' and r['location']=='NY' and r['in_role']=='true' and r['posted_date']==''
def test_role():
 assert role('Investment Banking Analyst') and not role('Software Engineer') and not role('Investment Banking Associate')
def test_history(tmp_path):
 def snap(day,ids):
  p=tmp_path/'raw'/day;p.mkdir(parents=True);(p/'stripe.json.gz').write_bytes(gzip.compress(json.dumps({'jobs':[{'id':i,'title':'Analyst'} for i in ids]}).encode()))
 snap('2026-01-01',[1]);snap('2026-01-03',[2]);snap('2026-01-04',[1,2]);snap('2026-01-05',[1]);rows,dates=build(tmp_path);r={x['source_id']:x for x in rows};assert r['1']['first_seen']=='2026-01-01' and r['1']['last_seen']=='2026-01-05' and r['1']['status']=='open' and r['1']['first_run']=='true';assert r['2']['removed_date']=='2026-01-05' and r['2']['last_seen']=='2026-01-04' and r['2']['first_run']=='false';before=(tmp_path/'history.csv').read_bytes();build(tmp_path);assert before==(tmp_path/'history.csv').read_bytes()
