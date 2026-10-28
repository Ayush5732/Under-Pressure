import unittest,copy
import engine,learning
from test_engine import start,read_all,choose,checkin
class DiscoveryTests(unittest.TestCase):
 def ask(self,s,i):return read_all(engine.act(s,'protagonist','select',{'id':f'ask:{i}'}))
 def test_opening_and_candidate_reveal(self):
  s=engine.new_game();self.assertEqual(engine.options(s),[]);self.assertFalse(engine.view(s,'protagonist')['candidates_available'])
  with self.assertRaises(ValueError):engine.act(s,'protagonist','select',{'id':'open'})
  s=start();self.assertTrue(engine.view(s,'protagonist')['candidates_available'])
 def test_candidate_files_are_observed_without_retroactive_credit(self):
  s=start();s=engine.act(s,'protagonist','candidates',{});self.assertIn('roles',learning.known(s));self.assertEqual(s['step'],1)
  s=choose(start(),2);s=engine.act(s,'protagonist','candidates',{});self.assertNotIn('roles',s['history'][0]['facts']);self.assertIn('roles',s['facts']['2'])
 def test_information_requires_display_ack(self):
  s=start();s=engine.act(s,'protagonist','select',{'id':'ask:0'});self.assertNotIn('roles',learning.known(s));s=read_all(s);self.assertIn('roles',learning.known(s));self.assertIn('Maya',s['brief'][-1]['text'])
 def test_knowledge_gate_and_character_thread(self):
  s=choose(start(),2);self.assertFalse(any(o['id']=='commit:0' for o in engine.options(s)))
  self.assertTrue(all(o['thread']!='project' for o in engine.options(s) if o['id'].startswith('ask:')))
  s=self.ask(s,1);s=self.ask(s,2);self.assertTrue(any(o['id']=='commit:0' for o in engine.options(s)))
 def test_expired_information_cannot_backfill_decision(self):
  s=checkin(choose(start(),2));s=engine.act(s,'protagonist','select',{'id':'ask:2'});s=read_all(engine.act(s,'protagonist','select',{'id':'commit:1'}))
  # The pending answer was not read at commitment. The historical evidence remains unchanged.
  self.assertNotIn('policy',s['history'][-1]['facts']);self.assertNotIn('policy',learning.known(s))
  self.assertTrue(any(o['status']=='expired' for o in s['opportunities'] if o['step']==2))
 def test_no_trust_scores_on_public_choices(self):
  v=engine.view(start(),'protagonist');self.assertTrue(all('delta' not in o and 'impact' in o for o in v['options']));self.assertNotIn('assessment',v)
 def test_clarification_is_scoped_once(self):
  s=self.ask(start(),0);o=next(o for o in engine.options(s) if o['id']=='clarify:0');self.assertEqual(o['thread'],'priya');s=read_all(engine.act(s,'protagonist','select',{'id':o['id']}));self.assertFalse(any(o['id']=='clarify:0' for o in engine.options(s)))
 def bonus_state(self):
  s=choose(start(),2)
  for i in (1,2):s=self.ask(s,i)
  s=choose(s,0);s=choose(s,0);s=self.ask(s,0);s=choose(s,0)
  for i in (0,1,2):s=self.ask(s,i)
  return checkin(choose(s,0))
 def test_intern_bonus_requires_evidence(self):
  s=self.bonus_state();self.assertEqual(s['reply_bonus'],'intern_feedback');self.assertTrue(all(o['thread']=='sam' for o in engine.options(s)))
  a=engine.act(s,'protagonist','select',{'id':'feedback:encourage'});b=engine.act(s,'protagonist','select',{'id':'feedback:shout'});self.assertEqual(a['day'],b['day']);self.assertEqual(a['spent'],b['spent']);self.assertGreater(a['assessment']['people'],b['assessment']['people'])
 def test_feedback_speed_then_rework(self):
  states=[]
  for key in ('encourage','shout'):
   s=engine.act(self.bonus_state(),'protagonist','select',{'id':'feedback:'+key});s=read_all(engine.act(s,'partner','intervene',{'kind':'stable'}));s=choose(s,0);s=choose(s,0);gain=s['day'];s=choose(s,0);s=choose(s,0);states.append((gain,s))
  self.assertLess(states[1][0],states[0][0]);self.assertTrue(states[1][1]['flags']['feedback_rework_done']);self.assertTrue(any('inconsistent mappings' in m['text'] for m in states[1][1]['messages']))
 def test_clock_and_brief_no_future_scope_list(self):
  s=start();v=engine.view(s,'protagonist');self.assertEqual(v['scope'],{});self.assertEqual(len(v['project_report']['rows']),2);self.assertEqual(v['clock']['status'],'green');s['day']=111;self.assertEqual(learning.clock(s)['status'],'red');s['flags']['accepted_deadline']=300;self.assertEqual(learning.clock(s)['status'],'green')
if __name__=='__main__':unittest.main()
