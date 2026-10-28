"""Authored discovery, knowledge gates and operational previews. No text inference."""
import datetime, math
from scenarios import PEOPLE,stage,STAFF,question
GATES={'rule':{'stock','policy'},'priorities':{'scope'},'honest':{'demo'},'lean_tests':{'reuse'},'lean_training':{'champions'},'evidence':{'challenge'},'retain':{'finding'}}
TOPICS={1:{'priya':'Priya has the candidate responsibilities and budget commitments.','daniel':'Daniel set the delivery priorities; he can explain how those shape this hire.','nikhil':'Nikhil will provide senior cover if the new hire needs specialist support.'},2:{'marcus':'Marcus asked for the sales view; he can explain what his team needs to see.','rosa':'Rosa controls warehouse allocations and releases.','elena':'Elena signs off the business rule across departments.','daniel':'Daniel can clarify which decisions belong to us and which need client approval.'},3:{'nikhil':'Nikhil found the duplicate records and can explain the release risk.'},4:{'elena':'Elena can rank what her departments actually need for acceptance.','daniel':'Daniel needs to approve any change in delivery commitments.'},5:{'elena':'Elena is taking this demonstration to her steering group. It matters what she will use it to claim.'},6:{'priya':'Priya has the commitments still payable under the new conditions.','elena':'Elena can discuss what the client needs in the first usable delivery.'},7:{'nikhil':'Nikhil has the technical checks and handover requirements.'},8:{'daniel':'Daniel owns the deadline escalation; he can discuss the limits we can negotiate.'},9:{'elena':'Elena will accept the warehouse rollout; she can clarify the coverage her teams require.'},10:{'elena':'Elena decides whether an optional feature can be deferred.'},11:{'rosa':'Rosa knows which warehouse users can rehearse the workflow.'},13:{'elena':'Elena owns the new acceptance demand; she can explain the scope.','nikhil':'Nikhil has the specialist integration assessment.'},14:{'nikhil':'Nikhil can explain the remaining work in a funded completion plan.'},15:{'nikhil':'Nikhil holds the final verification record.'}}
CLARIFY={
 'roles':'Think of this as buying different kinds of capacity: Maya handles complex implementation, Jordan needs structured direction, and Sam needs teaching and senior sign-off. None takes over your client commitments.',
 'budget':'The $180,000 is already committed. Hiring, checks and training come from what remains of the $300,000 authorization. The separate $200,000 reserve needs board approval before use.',
 'stock':'Start with 100 physically present. Remove 30 already reserved and 10 still quarantined: 60 can be promised to a new order. A physical-stock display can still show the full breakdown.',
 'policy':'Elena approves the business rule. You recommend it and the hire implements it. Displaying 100 physical units does not authorize selling all 100.',
 'demo':'A demonstration shows working behavior. It does not prove that migrated data, every warehouse workflow and user training are complete.',
 'reliance':'Elena wants to report progress to her steering group. Label the demonstration accurately so her report does not become an unintended promise that production is finished.',
 'readiness_gap':'Sam finished the example he was assigned. Nikhil has not yet checked reservation and quarantine behavior. Sam can be finished with his task while the project still needs that review.'}
def known(s):return {f for facts in s['facts'].values() for f in facts}
def ready(s):return all(mid in s.get('read_ids',[]) for mid in s.get('intro_ids',[]))
def questions(s):
 qs=stage(s)['questions']
 if s['staff']=='sam' and s['step']==5 and not s['flags'].get('absent'):
  qs=qs+[question('Have you signed off Sam’s demonstration for release?','nikhil','Sam completed his assigned happy-path example. Reservation and quarantine cases are not signed off. Keep this a demonstration and review those cases before certifying release.','readiness_gap',(1,1,1))]
 return qs

def cues(s,spec):
 out=[];owners={q['who'] for q in questions(s)}
 for owner in sorted(owners):
  if owner==spec['thread']:continue
  text=TOPICS.get(s['step'],{}).get(owner)
  if not text:
   if owner==s['staff']:text=f'{PEOPLE[owner][0].split()[0]} has the implementation and review notes for this work.'
   elif owner=='nikhil':text='Nikhil has the independent technical review for this work.'
   else:text=f'{PEOPLE[owner][0].split()[0]} is the person who can confirm their part of this plan.'
  if owner=='nikhil' and s['staff']=='sam' and s['step']==5:text='Nikhil has not yet sent me the independent sign-off. He may have a different view of what is ready.'
  if owner==spec['who']:text={'elena':'I have the client acceptance details; message me directly if you want to work through them.','nikhil':'My review notes are available privately if you want to examine the technical checks.','daniel':'We can discuss the decision boundaries privately before you commit.'}.get(owner,'I can talk through my implementation and review notes privately before you decide.')
  out.append(text)
 return out

def impact(s,o):
 if o['id'].startswith(('ask:','clarify:')):return 'Same-day discussion · no new spending commitment'
 if o['id']=='feedback:encourage':return 'No immediate productivity gain · time for a private coaching conversation'
 if o['id']=='feedback:shout':return 'Finish the next bounded batch 1 working day sooner · no reduction in required checks'
 if o['id']=='fund':return 'Seek board authorization · allow 1 working day for review'
 if o['id']=='cancel_fund':return 'No new commitment · reconsider the plan'
 if o['id']=='appeal':return '1 working day to review authorization with Daniel'
 if not o['id'].startswith('commit:'):return 'Conversation only · no new project spending'
 text=f"Commit ${o['cost']:,} · plan {o['days']} working day"+('s' if o['days']!=1 else '')
 context={'full_tests':'cross-site verification capacity funded','minimum_tests':'no added verification capacity','pilot_tests':'coverage limited to a pilot','lean_tests':'focused checks reuse existing evidence','full_training':'three-site rehearsal capacity funded','minimum_training':'standard handover only','shame':'availability and stopping point not agreed','promise_all':'all requests treated as a delivery commitment','overstate':'a stronger progress claim with less review time'}
 if o.get('key') in context:text+=' · '+context[o['key']]
 if o.get('note'):text+=' · '+o['note']
 return text

def brief(s):
 entries=[dict(id='initial',kind='Initial brief',source='Daniel',text='Deliver inventory and order management for three warehouses within sixteen weeks. Base authorization $300,000; emergency funding requires approval.')]
 entries+=s.get('brief',[])
 # Unknowns are only current topics already introduced, never a map of future surprises.
 open_items=[]
 if s['opening'] is None and ready(s) and not s['result'] and not s.get('pending'):
  for i,q in enumerate(questions(s)):
   if q['fact'] not in known(s):open_items.append(dict(owner=q['who'],text=q['text']))
 return dict(entries=entries,open=open_items)

def clock(s):
 remaining=s['flags'].get('accepted_deadline',112)-s['day'];work=0
 # Reference estimate from currently introduced staffing and already-agreed conditions.
 # Future mentor conditions are deliberately not forecast here.
 from scenarios import stage
 import copy
 if not s['result']:
  for n in range(s['step'],16):
   t=dict(s);t['step']=n
   base=stage(t)['options'][0]['days'];work+=base
  if s['flags'].get('pressure')=='hard':work+=sum(v for n,v in {13:10,14:10,15:5}.items() if n>=s['step'])
  if s['flags'].get('rushed_feedback') and not s['flags'].get('feedback_rework_done'):work+=3
 calendar=math.ceil(work*7/5);slack=remaining-calendar
 status='red' if remaining<0 or slack<0 else 'yellow' if slack<14 else 'green'
 if s['result'] and remaining>=0:status='green' if s['result']['delivered'] else 'yellow'
 return dict(status=status,label={'red':'Schedule critical','yellow':'Limited schedule margin','green':'Schedule has margin'}[status],remaining=remaining,estimated_workdays=work,estimated_calendar_days=calendar,slack=slack,elapsed=s['day'],total=s['flags'].get('accepted_deadline',112),basis='Reference forecast from the current scope and staffing. Future changes and unresolved information can change it.')
