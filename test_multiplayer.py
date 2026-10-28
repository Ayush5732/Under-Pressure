import json,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from http.server import ThreadingHTTPServer
import engine,server
class MultiplayerTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();server.DB=Path(cls.tmp.name)/'rooms.db';server.LIVE_WAIT=2;cls.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.url='http://127.0.0.1:'+str(cls.http.server_port);threading.Thread(target=cls.http.serve_forever,daemon=True).start()
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.tmp.cleanup()
 def setUp(self):server.JOIN_FAILURES.clear()
 def request(self,path,body=None,token=None):
  headers={'Content-Type':'application/json'}
  if token:headers['Authorization']='Bearer '+token
  req=urllib.request.Request(self.url+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
  try:
   with urllib.request.urlopen(req,timeout=4) as r:return r.status,json.loads(r.read())
  except urllib.error.HTTPError as e:return e.code,json.loads(e.read())
 def create(self):return self.request('/api/create',{})[1]
 def test_join_normalized_code_only_mentor_role(self):
  r=self.create();self.assertEqual(len(r['code']),8);self.assertEqual(r['share_url'],self.url)
  code=r['code'].lower();status,j=self.request('/api/join',{'code':' '+code[:4]+'-'+code[4:]+' '});self.assertEqual(status,200);self.assertEqual(j['session'],r['partner']);self.assertNotIn('protagonist',j)
  _,v=self.request('/api/state',token=j['session']);self.assertEqual(v['role'],'partner');self.assertIn('project_report',v['state']);self.assertNotIn('history',v['state'])
  self.assertEqual(self.request('/api/action',dict(action='select',id='open',revision=0),j['session'])[0],403)
 def test_bad_code_and_invite_permissions(self):
  r=self.create();self.assertEqual(self.request('/api/join',{'code':'NO-SUCH-ROOM'})[0],404);self.assertEqual(self.request('/api/invite',token=r['partner'])[0],403)
  _,invite=self.request('/api/invite',token=r['protagonist']);self.assertEqual(invite['code'],r['code']);self.assertNotIn('partner',invite)
 def test_live_waits_then_delivers_chat(self):
  r=self.create();done=threading.Event();output=[]
  def listen():output.append(self.request('/api/live?since=0%3A1',token=r['partner']));done.set()
  t=threading.Thread(target=listen);t.start();self.assertFalse(done.wait(.1))
  self.request('/api/action',dict(action='chat',text='Review this delivery position.'),r['protagonist']);self.assertTrue(done.wait(2));t.join();status,result=output[0];self.assertEqual(status,200);self.assertEqual(result['state']['messages'][-1]['text'],'Review this delivery position.');self.assertNotIn('assessment',self.request('/api/state',token=r['protagonist'])[1]['state'])
 def test_mentor_change_reaches_player_without_reload(self):
  r=self.create();s=engine.new_game();s.update(opening=None,staff='sam',step=6,pending='operational')
  with server.LOCK,server.connect() as db:db.execute('UPDATE rooms SET state=? WHERE code=?',(json.dumps(s),r['code']))
  done=threading.Event();out=[]
  def listen():out.append(self.request('/api/live?since=0%3A1',token=r['protagonist']));done.set()
  t=threading.Thread(target=listen);t.start();self.assertFalse(done.wait(.1));self.request('/api/action',dict(action='intervene',kind='cut',reason='Company commitments changed.',revision=0),r['partner']);self.assertTrue(done.wait(2));t.join();v=out[0][1]['state'];self.assertEqual(v['budget']['authorization'],270000);self.assertIsNone(v['pending']);self.assertNotIn('assessment',v)
 def test_legacy_six_character_code_resumes(self):
  with server.LOCK,server.connect() as db:db.execute('INSERT INTO rooms VALUES (?,?,?,?)',('A10F5B','legacy-player','legacy-mentor',json.dumps(engine.new_game())))
  _,j=self.request('/api/join',{'code':'a10f5b'});self.assertEqual(j['session'],'legacy-mentor')
 def test_live_requires_valid_session(self):self.assertEqual(self.request('/api/live?since=0%3A1',token='wrong')[0],401)
if __name__=='__main__':unittest.main()
