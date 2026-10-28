import copy,json,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from http.server import ThreadingHTTPServer
import engine,server

def read_all(s):
 for t in {m['thread'] for m in s['messages'] if m['thread']!='mentor' and m['id'] not in s['read_ids']}:
  s=engine.act(s,'protagonist','read',{'thread':t,'upto':s['chat_revision']})
 return s

def checkin(s):
 if s['opening'] is None and engine.mentor_checkin(s)!='complete':
  s=engine.act(s,'protagonist','chat',{'text':'Let us discuss this decision.'});s=engine.act(s,'partner','chat',{'text':'Consider the facts and make your decision.'})
 return s

def start():
 s=engine.new_game()
 for _ in range(3):s=read_all(s);s=engine.act(s,'protagonist','select',{'id':'open'})
 return checkin(read_all(s))

def choose(s,i):return read_all(engine.act(checkin(read_all(s)),'protagonist','select',{'id':f'commit:{i}'}))
def play(staff='maya',event='stable',pressure='supportive',mode='full',bad=False,investigate=True):
 s=start();count=0
 while not s['result']:
  s=read_all(s)
  if not s['pending']:s=checkin(s)
  count+=1
  if count>100:raise RuntimeError('Route loop')
  if s['pending']:
   kind={'operational':event,'leadership':pressure,'funding':'approve'}[s['pending']];s=engine.act(s,'partner','intervene',dict(kind=kind,reason='Documented circumstances and required work.'));continue
  if s.get('reply_bonus'):
   s=engine.act(s,'protagonist','select',{'id':'feedback:encourage'});continue
  if s['funding']:s=engine.act(s,'protagonist','select',{'id':'fund'});continue
  if investigate:
   for o in list(engine.options(s)):
    if o['id'].startswith('ask:'):s=read_all(engine.act(s,'protagonist','select',{'id':o['id']}))
  n=s['step'];i=0
  if n==1:i={'maya':0,'jordan':1,'sam':2}[staff]
  if bad and n in (2,3,4,5,6,7,8,10,12,13):i=1 if n in (2,4,5,6,7,8) else 2
  if mode=='lean':
   if n in (9,11):i=3
   if n==10:i=1
  if mode=='recover':
   if n in (14,15):i=1
   if n in (10,12):i=0
  if not any(o['id']==f'commit:{i}' and o.get('enabled',True) for o in engine.options(s)):
   commits=[o for o in engine.options(s) if o['id'].startswith('commit:') and o.get('enabled',True)]
   if not commits:raise RuntimeError('No viable or orderly-stop reply')
   i=int(commits[0]['id'].split(':')[1])
  s=choose(s,i)
 return s
class EngineTests(unittest.TestCase):
 def test_36_conditions_have_an_ending(self):
  import itertools
  for args in itertools.product(('maya','jordan','sam'),('stable','cut','removal','scope'),('supportive','critical','hard')):
   s=play(*args);self.assertIn(s['result']['category'],engine.CATEGORIES);self.assertLessEqual(s['spent'],s['authorization']);self.assertLessEqual(s['drawn'],200000)
 def test_three_staff_routes(self):
  for staff in ('maya','jordan','sam'):
   s=play(staff);self.assertTrue(s['result']['delivered'],s['result']);self.assertEqual(len(s['history']),15)
 def test_two_savings_routes(self):
  for s in (play(mode='lean'),play('jordan')):self.assertIsNotNone(s['result']['special']);self.assertEqual(s['drawn'],0)
  self.assertIsNone(play('sam',mode='lean')['result']['special'])
 def test_high_cost_perfect_route(self):
  s=play(pressure='hard');self.assertEqual(s['drawn'],200000);self.assertEqual(s['spent'],500000);self.assertTrue(s['result']['delivered']);self.assertEqual(s['result']['special'],'Difficult-client, full-funding, high-trust delivery')
 def test_success_with_poor_management(self):
  s=play(mode='recover',bad=True);self.assertTrue(s['result']['delivered']);self.assertEqual(s['result']['category'],engine.CATEGORIES[2])
 def test_two_failure_categories(self):
  s=play();s['result']=None;s['flags']['training']=False;engine.finish(s,False);self.assertEqual(s['result']['category'],engine.CATEGORIES[3])
  s=play(bad=True);self.assertFalse(s['result']['delivered']);self.assertEqual(s['result']['category'],engine.CATEGORIES[4])
 def test_casual_exchange_returns_without_cost_or_major_decision(self):
  s=start();s=choose(s,0)
  for i in (1,2):s=read_all(engine.act(s,'protagonist','select',{'id':f'ask:{i}'}))
  s=choose(s,0);before=(s['step'],s['spent'],len(s['history']))
  s=engine.act(s,'protagonist','select',{'id':'casual_start'})
  for _ in range(2):s=engine.act(s,'protagonist','select',{'id':'casual_reply:0'})
  self.assertEqual(before,(s['step'],s['spent'],len(s['history'])));self.assertFalse(any(o['id']=='casual_start' for o in engine.options(s)));self.assertGreater(s['assessment']['people'],50)
 def test_priorities_change_exact_trust_preview(self):
  s=start();s['opening']=None;s['staff']='maya';s['step']=9;s['facts']['9']=['reuse'];s['flags'].update(rule=True,data=True,capable=True)
  s['priority']='cost';a=next(o for o in engine.options(s) if o['id']=='commit:3')['delta']['manager'];s['priority']='quality';b=next(o for o in engine.options(s) if o['id']=='commit:3')['delta']['manager'];self.assertEqual(a,b+1)
 def test_no_softlock_when_final_hard_work_exceeds_all_funding(self):
  s=play('maya','scope','hard');self.assertFalse(s['result']['delivered']);self.assertIn(s['result']['category'],engine.CATEGORIES);self.assertLessEqual(s['spent'],s['authorization'])
 def test_information_rejoins_and_cannot_repeat(self):
  s=start();s=read_all(engine.act(s,'protagonist','select',{'id':'ask:0'}));self.assertEqual(s['step'],1);self.assertEqual(len(s['history']),0);self.assertEqual(s['facts']['1'],['roles'])
  with self.assertRaises(ValueError):engine.act(s,'protagonist','select',{'id':'ask:0'})
 def test_previews(self):
  s=start()
  for o in engine.options(s):
   after=engine.act(s,'protagonist','select',{'id':o['id']});self.assertEqual({k:after['metrics'][k]-s['metrics'][k] for k in s['metrics']},o['delta'])
 def test_understanding_evidence(self):
  a=choose(start(),0);b=start()
  for i in (0,1):b=read_all(engine.act(b,'protagonist','select',{'id':f'ask:{i}'}))
  b=choose(b,0);self.assertEqual(a['history'][0]['information_coverage'],.25);self.assertEqual(b['history'][0]['information_coverage'],1)
 def test_role_privacy(self):
  s=play(pressure='hard');v=engine.view(s,'protagonist');self.assertNotIn('assessment',v);self.assertNotIn('evidence',v);self.assertNotIn('understanding',v);self.assertNotIn('assessment',json.dumps(v['checkpoints']));self.assertNotIn('state',json.dumps(v['checkpoints']));self.assertIn('assessment',engine.view(s,'partner'))
 def test_funding_authorization(self):
  s=start();s['authorization']=200000;s=choose(s,0);self.assertEqual(s['spent'],180000);self.assertEqual(s['funding']['need'],40000);s=engine.act(s,'protagonist','select',{'id':'fund'})
  with self.assertRaises(ValueError):engine.act(s,'protagonist','intervene',{'kind':'approve'})
  s=engine.act(s,'partner','intervene',{'kind':'approve'});s=choose(s,0);self.assertEqual(s['spent'],240000)
 def test_appeal_gate(self):
  s=start();self.assertFalse(any(o['id']=='appeal' for o in engine.options(s)));s['flags'].update(event='cut',diagnosed=True);s['assessment'].update(leadership=65,people=65,decision=65);s['evidence']=[{'fact':f} for f in ('roles','budget','policy','stock','authority','scope','negotiation')];s['history']=[{'step':i+1,'key':k} for i,k in enumerate(('rule','audit','priorities','honest','diagnose'))];old=s['authorization'];s=engine.act(s,'protagonist','select',{'id':'appeal'});self.assertEqual(s['authorization'],old+30000);self.assertFalse(any(o['id']=='appeal' for o in engine.options(s)))
 def test_restore_feedback(self):
  s=play();s=engine.act(s,'protagonist','note',{'message':1,'text':'Opening note'});s=engine.act(s,'protagonist','restore',{'id':s['checkpoints'][0]['id']});self.assertEqual(s['step'],1);self.assertEqual(s['spent'],180000);self.assertEqual(len(s['runs']),1);self.assertEqual(s['feedback'][0]['note'],'Opening note')
 def test_persistence_and_chat(self):
  s=start();rev=s['revision'];s=engine.act(s,'partner','chat',{'text':'Consider the trade-off.'});self.assertEqual(s['revision'],rev);self.assertEqual(s['messages'][-1]['thread'],'mentor');self.assertEqual(engine.view(json.loads(json.dumps(s)),'protagonist'),engine.view(s,'protagonist'))
 def test_workload_reaction(self):
  a=play();b=play(bad=True);self.assertGreater(a['day'],0);self.assertTrue(any('unlimited overtime' in m['text'] for m in b['messages']))
class ApiTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();server.DB=Path(cls.tmp.name)/'save.db';cls.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.url='http://127.0.0.1:'+str(cls.http.server_port);threading.Thread(target=cls.http.serve_forever,daemon=True).start()
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.tmp.cleanup()
 def req(self,path,body=None,token=None,origin=None):
  headers={'Content-Type':'application/json'}
  if token:headers['Authorization']='Bearer '+token
  if origin:headers['Origin']=origin
  req=urllib.request.Request(self.url+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
  try:
   with urllib.request.urlopen(req) as r:return r.status,json.loads(r.read())
  except urllib.error.HTTPError as e:return e.code,json.loads(e.read())
 def test_roles_revision_persistence(self):
  status,r=self.req('/api/create',{});self.assertEqual(status,201);p=r['protagonist'];m=r['partner'];self.assertEqual(self.req('/api/state',token='bad')[0],401);self.assertEqual(self.req('/api/action',dict(action='select',id='open',revision=0),m)[0],403)
  self.req('/api/action',dict(action='read',thread='project',upto=1),p)
  status,d=self.req('/api/action',dict(action='select',id='open',revision=1),p);self.assertEqual(status,200);self.assertEqual(self.req('/api/action',dict(action='select',id='open',revision=0),p)[0],409);self.assertEqual(d['state'],self.req('/api/state',token=p)[1]['state'])
 def test_origin(self):self.assertEqual(self.req('/api/create',{},origin='https://evil.example')[0],403)
if __name__=='__main__':unittest.main()
