import unittest,json
import engine,reports
from test_engine import start,choose,read_all,play
class ReportTests(unittest.TestCase):
 def test_start_is_not_completed_and_no_mistakes(self):
  s=start();r=reports.report(s,True);self.assertEqual(len(r['rows']),5);self.assertTrue(all(x['status']=='pending' for x in r['rows']));self.assertEqual(reports.exceptions(s)['findings'],[])
 def test_player_and_mentor_knowledge_differ(self):
  s=start();self.assertEqual(len(reports.report(s)['rows']),2);self.assertEqual(len(reports.report(s,True)['rows']),5)
  self.assertNotIn('Legacy',json.dumps(reports.report(s,True)));self.assertNotIn('forty-eight',reports.exceptions(s)['lookahead'])
 def test_report_is_not_transcript(self):
  s=choose(start(),2);r=reports.report(s);dump=json.dumps(r);self.assertNotIn(s['history'][0]['reply'],dump);self.assertNotIn('What would each person',dump);self.assertIn('Implementation staffing appointed',dump)
 def test_confirmed_error_distinct_from_missing_information(self):
  s=choose(start(),2);s=choose(s,1);f=reports.exceptions(s)['findings'];self.assertTrue(any(x['title']=='Stock allocation instruction' and x['status']=='issue' for x in f));self.assertTrue(any(x['kind']=='Information gap' and x['status']=='pending' for x in f));self.assertTrue(all('intent' in x['basis'] for x in f))
 def test_mentor_payload_report_only(self):
  s=start();s=engine.act(s,'partner','chat',{'text':'Please review the current requirements.'});v=engine.view(s,'partner');self.assertNotIn('history',v);self.assertNotIn('evidence',v);self.assertTrue(all(m['thread']=='mentor' for m in v['messages']));self.assertIn('oversight',v);self.assertIn('project_report',v)
 def test_view_does_not_mutate_stored_result(self):
  s=start();s['result']={'review':['Original review'],'delivered':False};before=json.dumps(s,sort_keys=True);engine.view(s,'partner');self.assertEqual(before,json.dumps(s,sort_keys=True))
 def test_no_oversight_in_player_payload(self):
  s=start();v=engine.view(s,'protagonist');self.assertNotIn('oversight',v);self.assertNotIn('assessment',v);self.assertNotIn('brief',v)
 def test_activated_scope_only(self):
  s=start();s['flags']['pressure']='hard';r=reports.report(s,True);self.assertEqual(len(r['rows']),7);self.assertEqual(len(reports.report(s)['rows']),2)
 def test_recovered_error_remains_historical(self):
  s=choose(start(),2);s=choose(s,1);s['flags']['rule']=True;f=reports.exceptions(s)['findings'];x=next(x for x in f if x['title']=='Stock allocation instruction');self.assertEqual(x['status'],'resolved')
if __name__=='__main__':unittest.main()
