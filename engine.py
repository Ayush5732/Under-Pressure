"""Deterministic, role-separated project simulation. All dialogue is authored."""
import copy,datetime,hashlib,json,math
import casual,learning,reports
from scenarios import stage,PEOPLE,STAFF
CATEGORIES=['Successful delivery, good management','Successful delivery after leadership-backed recovery','Successful delivery, poor management','Failed delivery, good management','Failed delivery, poor management']
OPENING=[('daniel','Hey Alex, congrats on the promotion! You’re our new delivery manager.', 'Thanks! I’m excited. Tell me what I’m taking on.'),('daniel','Meridian needs inventory and order management across three warehouses in sixteen weeks. You own business commitments and coordinate delivery.','What matters most on this project?'),('daniel','Usable, verified delivery comes first. Bring me evidence when scope, time and funding conflict. Elena approves client business policy. Priya has the budget and screened candidates.','I’ll talk to Priya privately and work through the responsibilities.')]
def current_date(s):return (datetime.date.fromisoformat(s['start'])+datetime.timedelta(days=math.floor(s['day']))).isoformat()
def message(s,who,text,thread='project',delta=None):
 s['chat_revision']+=1;s['messages'].append(dict(id=s['chat_revision'],who=who,text=text,thread=thread,step=s['step'],day=s['day'],date=current_date(s),delta=delta or {},path=[dict(step=h['step'],key=h['key']) for h in s['history']]))
def new_game():
 s=dict(version=3,read_ids=[],intro_ids=[],brief=[],opportunities=[],clarified=[],reply_bonus=None,revision=0,chat_revision=0,start='2026-11-02',day=0,step=1,opening=0,staff=None,metrics=dict(client=85,manager=80,board=85),assessment=dict(leadership=50.,people=50.,decision=50.),relationships={p:60 for p in PEOPLE},flags={},facts={},asked=[],history=[],evidence=[],messages=[],pending=None,spent=180000,base=300000,authorization=300000,reserve=200000,drawn=0,priority='quality',result=None,feedback=[],runs=[],checkpoints=[],funding=None,interventions=[],requested=None)
 who,text,_=OPENING[0];message(s,who,text);return s

def scope(s):
 f=s['flags'];items={'Approved stock rule':bool(f.get('rule')),'Verified migration data':bool(f.get('data')),'Working implementation':not f.get('defect',False),'Cross-site release verification':bool(f.get('tests')),'User readiness':bool(f.get('training'))}
 if f.get('event')=='scope' or f.get('pressure')=='hard':items['Additional alerts']=bool(f.get('recovered'))
 if f.get('pressure')=='hard':items['Validated legacy interface']=bool(f.get('hard_complete'))
 return items

def good(s):return min(s['assessment'].values())>=50 and not s['flags'].get('concealed')
def bonus_eligible(s):
 facts={e['fact'] for e in s['evidence']}
 keys={h['key'] for h in s['history']}
 return good(s) and s['assessment']['decision']>=56 and {'roles','budget','policy','stock','authority','scope','negotiation'}<=facts and {'rule','audit','priorities','honest','diagnose'}<=keys
def required_cost(s,o):
 cost=o['cost'];n=s['step'];hard=s['flags'].get('pressure')=='hard'
 if o['key'] in ('stop_accept','close'):return 0
 if hard and n==13:cost+=80000 # agreed alerts, integration assessment and initial implementation
 if hard and n==14:cost+=70000+40000 # specialist integration and expanded validation
 if hard and n==15:cost+=24000 # extra cross-site readiness and supported handover
 if n==14 and o['key']=='full_accept' and not all(scope(s).values()):
  # Full acceptance must not silently fix missing gates.
  pass
 return cost

def required_days(s,o):
 days=o['days']
 if s['flags'].get('pressure')=='hard' and o.get('key') not in ('stop_accept','close'):
  days+={13:10,14:10,15:5}.get(s['step'],0)
 return days

def preview(s,o):
 raw=copy.deepcopy(o['visible']);priority=s['priority'];key=o.get('key')
 if priority=='cost' and key in ('lean_tests','lean_training','retain'):raw['manager']+=1
 if priority=='quality' and key in ('full_tests','repair','evidence'):raw['manager']+=1
 if priority=='people' and key=='support_people':raw['manager']+=1
 if priority=='schedule' and key in ('promise_all','forced'):raw['manager']-=1
 delta={k:max(0,min(100,s['metrics'][k]+v))-s['metrics'][k] for k,v in raw.items()}
 if o.get('key')=='fund_request':delta['board']=0 if good(s) else -5
 return delta

def snapshot(s):
 snap=copy.deepcopy(s)
 for k in ('checkpoints','feedback','runs'):snap[k]=[]
 return snap

def enter(s):
 start_id=s['chat_revision']
 spec=stage(s);warm=s['relationships'].get(spec['who'],60)>=55
 if spec['thread'] in STAFF:
  text='I can work through this with you. Let’s keep the plan bounded.' if warm else 'I need documented ownership and limits before committing more work.'
  message(s,spec['who'],text,spec['thread'])
 for text in spec['lines']:message(s,spec['who'],text,spec['thread'])
 if s['staff']=='sam' and s['step']==5 and not s['flags'].get('absent'):
  message(s,'sam','My assigned example runs now. I think it’s ready to show Elena.',spec['thread'])
 for text in learning.cues(s,spec):message(s,spec['who'],text,spec['thread'])
 s['intro_ids']=[m['id'] for m in s['messages'] if m['id']>start_id]
 for i,q in enumerate(learning.questions(s)):
  s['opportunities'].append(dict(step=s['step'],question=i,owner=q['who'],fact=q['fact'],status='offered'))
 if s['step'] in (2,3,9) and s['staff'] and not s['flags'].get('absent'):
  worker=s['staff'];line={'maya':'Give me the approved business instruction; I can own implementation and flag technical impacts.','jordan':'I need the interpretation and review standard clear before I repeat this across sites.','sam':'I need a worked example and senior review before treating my result as production-ready.'}[worker]
  message(s,worker,line,spec['thread'])
 s['intro_ids']=[m['id'] for m in s['messages'] if m['id']>start_id]

def add_days(s,days,weekend=False):
 if not days:return
 # Meetings are same-day; authored task estimates use working days.
 for _ in range(int(days)):
  s['day']+=1
  if not weekend:
   while datetime.date.fromisoformat(current_date(s)).weekday()>=5:s['day']+=1

def assess(s,weights,understanding,fact=None,source='reply'):
 changes={}
 for k,v in weights.items():
  change=v*(understanding if v>0 else 1);s['assessment'][k]=max(0,min(100,s['assessment'][k]+change));changes[k]=change
 return changes

def apply_visible(s,delta):
 for k,v in delta.items():s['metrics'][k]=max(0,min(100,s['metrics'][k]+v))

def mentor_checkin(s):
 if s['opening'] is not None or not s.get('intro_ids'):return 'not_started'
 boundary=max(s['intro_ids'])
 seen={m['who'] for m in s['messages'] if m['thread']=='mentor' and m['id']>boundary and m['step']==s['step']}
 if 'alex' not in seen and 'mentor' not in seen:return 'both_needed'
 if 'alex' not in seen:return 'alex_needed'
 if 'mentor' not in seen:return 'mentor_needed'
 return 'complete'

def options(s):
 if s['result'] or s['pending']:return []
 if s['opening'] is not None and any(m['id'] not in s['read_ids'] for m in s['messages'] if m['who']!='alex' and m['thread']=='project'):return []
 if s['opening'] is not None:return [dict(id='open',text=OPENING[s['opening']][2],delta=dict(client=0,manager=.5 if s['opening']==0 else 0,board=0),cost=0,days=0,thread='project')]
 if s.get('casual'):
  c=s['casual'];entry=casual.conversation(s,c['kind'])[c['cursor']]
  return [dict(id=f'casual_reply:{i}',text=text,delta=dict(client=0,manager=0,board=0),cost=0,days=0,thread='project') for i,(text,value) in enumerate(entry['choices'])]
 if s['funding']:
  return [dict(id='fund',text=f"Request approval for ${s['funding']['need']:,} before committing the work.",delta=dict(client=0,manager=1,board=0 if good(s) else -5),cost=0,days=1,thread='priya'),dict(id='cancel_fund',text='Return to the decision and reconsider the plan.',delta=dict(client=0,manager=0,board=0),cost=0,days=0,thread='priya')]
 if not learning.ready(s):return []
 if s.get('reply_bonus'):
  ready=mentor_checkin(s)=='complete';note='' if ready else 'Discuss this decision with your mentor first.'
  return [dict(enabled=ready,note=note,id='feedback:encourage',text='You finished the example you were assigned. Let’s work through the review gaps together before we call it release-ready.',delta=dict(client=0,manager=0,board=0),cost=0,days=0,thread='sam'),dict(enabled=ready,note=note,id='feedback:shout',text='This should have been finished already. Stop holding us up and get the next batch done faster.',delta=dict(client=0,manager=0,board=0),cost=0,days=0,thread='sam')]
 spec=stage(s);out=[]
 for i,o in enumerate(spec['options']):
  if not learning.GATES.get(o['key'],set())<=learning.known(s):continue
  cost=required_cost(s,o);available=s['authorization']-s['spent'];need=max(0,cost-available)
  enabled=need<=s['reserve']-s['drawn']
  if o['key']=='stop_accept':enabled=all(required_cost(s,x)>s['authorization']-s['spent']+s['reserve']-s['drawn'] for x in spec['options'] if x['key']!='stop_accept')
  if o['key']=='close':enabled=s['flags'].get('agreement')=='stop_accept' or all(required_cost(s,x)>s['authorization']-s['spent']+s['reserve']-s['drawn'] for x in spec['options'] if x['key']!='close')
  elif s['step']==15 and s['flags'].get('agreement')=='stop_accept':enabled=False
  checkin=mentor_checkin(s);mentor_note='Discuss this decision with your mentor and receive a reply first.' if checkin!='complete' else ''
  enabled=enabled and checkin=='complete'
  out.append(dict(id=f'commit:{i}',text=o['text'],delta=preview(s,o),cost=cost,days=required_days(s,o),thread=spec['thread'],enabled=enabled,note=mentor_note or (f'Requires approved additional funding of ${need:,}.' if need else ''),key=o['key']))
 for i,q in enumerate(learning.questions(s)):
  if f"{s['step']}:{i}" not in s['asked']:out.append(dict(id=f'ask:{i}',text=q['text'].strip(),delta=preview(s,q),cost=0,days=q['days'],thread=q['who']))
 for i,q in enumerate(learning.questions(s)):
  token=f"{s['step']}:{i}"
  if q['fact'] in learning.CLARIFY and q['fact'] in s['facts'].get(str(s['step']),[]) and token not in s.get('clarified',[]):
   out.append(dict(id=f'clarify:{i}',text='Could you explain that with a concrete example?' if i%2==0 else 'Can you put that another way before I decide?',delta=dict(client=0,manager=0,board=0),cost=0,days=0,thread=q['who']))
 if s['flags'].get('event')=='cut' and not s['flags'].get('reversed') and bonus_eligible(s):out.append(dict(id='appeal',text='Daniel, can we appeal the cut using the verified commitments and remaining obligations?',delta=dict(client=0,manager=1,board=0),cost=0,days=1,thread='daniel'))
 if s['step'] in (3,11) and s['step'] not in s.get('casual_seen',[]) and not s['flags'].get('absent'):
  out.append(dict(id='casual_start',text='How is the warehouse coffee treating you?' if s['step']==3 else 'Has the printer survived the training materials?',delta=dict(client=0,manager=0,board=0),cost=0,days=0,thread='project'))
 return out

def view(s,role):
 public=dict(version=s['version'],revision=s['revision'],chat_revision=s['chat_revision'],step=s['step'],staff=s['staff'],metrics=s['metrics'],date=current_date(s),week=math.floor(s['day']/7)+1,day=s['day'],deadline=(datetime.date.fromisoformat(s['start'])+datetime.timedelta(days=112)).isoformat(),remaining_days=112-s['day'],accepted_deadline=(datetime.date.fromisoformat(s['start'])+datetime.timedelta(days=s['flags'].get('accepted_deadline',112))).isoformat(),priority=s['priority'],budget=dict(base=s['base'],authorization=s['authorization'],spent=s['spent'],drawn=s['drawn'],reserve_remaining=s['reserve']-s['drawn'],retention=max(0,s['base']-s['spent']),target=20000),messages=copy.deepcopy(s['messages']),scope=scope(s),title='Promotion and handoff' if s['opening'] is not None else stage(s)['title'],pending=s['pending'],options=options(s) if role=='protagonist' else [],result=copy.deepcopy(s['result']),feedback=s['feedback'] if role=='protagonist' else [],checkpoints=[dict(id=c['id'],step=c['step'],title=c['title'],path=c['path']) for c in s['checkpoints']] if role=='protagonist' and s['result'] else [],runs=s['runs'] if role=='protagonist' else [])
 public['options']=[dict((k,v) for k,v in o.items() if k not in ('delta','key'))|dict(impact=learning.impact(s,o)) for o in public['options']]
 public.update(read_ids=s['read_ids'],brief=learning.brief(s),clock=learning.clock(s),candidates_available=s['opening'] is None and any(m['step']==1 and m['thread']=='priya' and m['id'] in s['read_ids'] for m in s['messages']),intro_ready=learning.ready(s))
 # Scope evidence is introduced through the brief and current discussions, not an upfront list of every future gate.
 if role=='protagonist':public['scope']={}
 public['mentor_checkin']=mentor_checkin(s)
 public['project_report']=reports.report(s,role=='partner')
 public.pop('brief',None)
 if role=='partner':
  public.update(decision_context=reports.decision_context(s),decision_summary=reports.decision_summary(s),oversight=reports.exceptions(s),assessment=s['assessment'],funding=dict(need=s['funding']['need'],reason='Additional authorization is required for the current proposed work package.') if s['funding'] else None)
  public['messages']=[m for m in public['messages'] if m['thread']=='mentor']
  if public['result']:public['result']['review']=[public['project_report']['summary']]
 return copy.deepcopy(public)

def chat(s,role,text):
 if not isinstance(text,str) or not text.strip() or len(text)>2000:raise ValueError('Enter a message of 1–2000 characters.')
 s=copy.deepcopy(s);message(s,'mentor' if role=='partner' else 'alex',text.strip(),'mentor');return s

def act(s,role,action,body):
 s=copy.deepcopy(s)
 if s.get('version')!=3:raise ValueError('This save belongs to the previous game. Use its original game folder.')
 if action=='chat':return chat(s,role,body.get('text'))
 if action=='candidates':
  if role!='protagonist' or s['opening'] is not None or not any(m['step']==1 and m['thread']=='priya' and m['id'] in s['read_ids'] for m in s['messages']):raise ValueError('The candidate files have not been introduced yet.')
  if 'roles' not in learning.known(s):
   s['facts'].setdefault(str(s['step']),[]).append('roles');s['brief'].append(dict(id='candidate-files',kind='Reviewed candidate files',source='Priya',text='Maya: $60,000, experienced implementation. Jordan: $30,000, structured direction and review. Sam: $0 added salary, teaching and senior sign-off. Alex retains client commitments.'));s['evidence'].append(dict(step=s['step'],reply='Opened the candidate profiles',fact='roles',changes={},basis='Information made available through the candidate files; comprehension unconfirmed.',available=['roles']))
  s['revision']+=1;return s
 if action=='read':
  if role!='protagonist':raise ValueError('Only Alex records story reading.')
  thread=body.get('thread');upto=body.get('upto')
  if not isinstance(upto,int):raise ValueError('Invalid message marker.')
  for m in s['messages']:
   if m['thread']!=thread or m['id']>upto or m['id'] in s['read_ids']:continue
   s['read_ids'].append(m['id'])
   if m.get('fact') and not any(h['step']==m['step'] for h in s['history']):
    
    if m['fact'] not in s['facts'].setdefault(str(m['step']),[]):s['facts'][str(m['step'])].append(m['fact'])
    s['brief'].append(dict(id=m['id'],kind='Confirmed information',source=PEOPLE[m['who']][0],text=m['text'],step=m['step'],date=m['date']))
  s['revision']+=1;return s
 if action=='note':
  if role!='protagonist':raise ValueError('Only Alex can annotate story messages.')
  mid=body.get('message');m=next((m for m in s['messages'] if m['id']==mid and m['thread']!='mentor'),None)
  if not m:raise ValueError('Story message not found.')
  if not isinstance(body.get('text'),str) or len(body['text'])>4000:raise ValueError('Notes are limited to 4000 characters.')
  item=dict(message=copy.deepcopy(m),note=body['text']);s['feedback']=[x for x in s['feedback'] if x['message']['id']!=mid]+[item]
 elif action=='restore':
  if role!='protagonist' or not s['result']:raise ValueError('Finish the path before restoring an earlier decision.')
  point=next((c for c in s['checkpoints'] if c['id']==body.get('id')),None)
  if not point:raise ValueError('Checkpoint not found.')
  old=s;s=copy.deepcopy(point['state'])
  for k in ('feedback','runs','checkpoints'):s[k]=old[k]
  s['messages']=[m for m in s['messages'] if m['thread']!='mentor']+[m for m in old['messages'] if m['thread']=='mentor'];s['chat_revision']=old['chat_revision'];s['revision']=old['revision'];s['result']=None
  message(s,'daniel','Review replay restored this decision and its recorded project conditions.','project')
 elif action=='intervene':
  if role!='partner' or s['pending'] not in ('operational','leadership','funding'):raise ValueError('No mentor intervention is pending.')
  intervene(s,body)
 elif action=='select':
  if role!='protagonist':raise ValueError('Only Alex can select a story reply.')
  chosen=next((o for o in options(s) if o['id']==body.get('id')),None)
  if not chosen or chosen.get('enabled') is False:raise ValueError('This reply is not available.')
  select(s,chosen)
 else:raise ValueError('Unknown action.')
 s['revision']+=1;return s

def select(s,o):
 oid=o['id']
 if oid.startswith('feedback:'):
  message(s,'alex',o['text'],'sam');shout=oid.endswith('shout');s['flags']['rushed_feedback']=shout;s['flags']['coached_intern']=not shout
  changes=assess(s,dict(leadership=-1 if shout else 1,people=-2 if shout else 2,decision=0),1)
  s['evidence'].append(dict(step=5,reply=o['text'],fact='intern_feedback',changes=changes,basis='Observed feedback choice; short-term throughput is separate from management evidence.',available=list(s['facts'].get('5',[]))))
  s['relationships']['sam']+=-12 if shout else 5
  message(s,'sam','I will push through the next batch faster.' if shout else 'Thanks. I understand the difference now. I’ll bring the uncertain cases to review.','sam')
  s['brief'].append(dict(id='feedback',kind='Agreed action',source='Alex / Sam',text='Next bounded batch expedited by one working day.' if shout else 'Private coaching agreed; no immediate task estimate changes.'))
  s['reply_bonus']=None;s['pending']='operational';message(s,'daniel','The steering review is ready. Discuss the conditions with your live mentor.');return
 if oid=='casual_start' or oid.startswith('casual_reply:'):
  message(s,'alex',o['text'],'project',o['delta'])
  if oid=='casual_start':
   s['casual']=dict(kind='coffee' if s['step']==3 else 'printer',cursor=0);s.setdefault('casual_seen',[]).append(s['step'])
  else:
   i=int(oid.split(':')[1]);entry=casual.conversation(s,s['casual']['kind'])[s['casual']['cursor']];value=entry['choices'][i][1];changes=assess(s,dict(leadership=0,people=value,decision=0),.5);s['relationships'][s['staff']]=max(0,min(100,s['relationships'][s['staff']]+value*3));s['evidence'].append(dict(step=s['step'],reply=o['text'],fact='coworker_support',changes=changes,basis='Observed casual response; provisional relationship evidence.',available=[]));s['casual']['cursor']+=1
  entry=casual.conversation(s,s['casual']['kind'])[s['casual']['cursor']];message(s,s['staff'],entry['line'])
  if not entry['choices']:s.pop('casual')
  return
 if oid=='open':
  apply_visible(s,o['delta']);message(s,'alex',o['text'],'project',o['delta']);s['opening']+=1
  if s['opening']>=len(OPENING):s['opening']=None;enter(s)
  else:who,text,_=OPENING[s['opening']];message(s,who,text)
  return
 if oid=='cancel_fund':s['funding']=None;return
 if oid=='fund':
  apply_visible(s,o['delta']);message(s,'alex',o['text'],'priya',o['delta']);add_days(s,1);s['pending']='funding';message(s,'daniel','I will review the cause, remaining obligations and authorization with the board. No work is committed before approval.','priya');return
 if oid=='appeal':
  apply_visible(s,o['delta']);message(s,'alex',o['text'],'daniel',o['delta']);add_days(s,1);s['authorization']+=30000;s['flags']['reversed']=True;s['flags']['backed']=True
  message(s,'daniel','The board has restored the $30,000 authorization. Your acceptance record and early escalation demonstrated that the cut endangered agreed delivery. Incurred costs and elapsed days remain.','daniel');return
 spec=stage(s)
 if oid.startswith('clarify:'):
  i=int(oid.split(':')[1]);q=learning.questions(s)[i];message(s,'alex',o['text'],o['thread']);message(s,q['who'],learning.CLARIFY[q['fact']],o['thread']);s['messages'][-1]['fact']='clarified_'+q['fact'];s['clarified'].append(f"{s['step']}:{i}");return
 if oid.startswith('ask:'):
  i=int(oid.split(':')[1]);q=learning.questions(s)[i];apply_visible(s,o['delta']);message(s,'alex',o['text'],o['thread'],o['delta']);message(s,q['who'],q['answer'],o['thread']);s['messages'][-1]['fact']=q['fact'];s['asked'].append(f"{s['step']}:{i}");
  for opportunity in s['opportunities']:
   if opportunity['step']==s['step'] and opportunity['question']==i:opportunity['status']='consulted'
  changes=assess(s,q['skills'],.5)
  s['evidence'].append(dict(step=s['step'],reply=o['text'],fact=q['fact'],changes=changes,basis='Relevant information-seeking; not proof that the information will be applied.',available=list(s['facts'].get(str(s['step']),[]))))
  add_days(s,q['days']);return
 i=int(oid.split(':')[1]);raw=spec['options'][i];cost=o['cost']
 if cost>s['authorization']-s['spent']:
  s['funding']=dict(need=cost-(s['authorization']-s['spent']),option=i,reason=raw['text'],good=good(s));message(s,'priya',f"This plan needs ${s['funding']['need']:,} more authorization. You can request board approval or return to another option.",'priya');return
 key=raw['key'];facts=list(s['facts'].get(str(s['step']),[]));understanding=1 if len(facts)>=2 else .5 if facts else .25
 interpretation='Instruction after consultation; comprehension remains unconfirmed' if len(facts)>=2 else 'Limited information; reasoning remains uncertain'
 if s['step']==2 and raw['key'] in ('physical','quarantine'):interpretation='Choice conflicts with the stock information shown; understanding and intent are unconfirmed' if 'policy' in facts or 'stock' in facts else 'Stock decision made without optional policy clarification; reasoning is unconfirmed'
 cid=hashlib.sha256(json.dumps([s['history'],s['step']],sort_keys=True).encode()).hexdigest()[:16]
 if not any(c['id']==cid for c in s['checkpoints']):s['checkpoints'].append(dict(id=cid,step=s['step'],title=spec['title'],path=[h['key'] for h in s['history']],state=snapshot(s)))
 for opportunity in s['opportunities']:
  if opportunity['step']==s['step'] and opportunity['status']=='offered':opportunity['status']='expired'
 s['brief'].append(dict(id='decision-'+str(s['step']),kind='Recorded commitment',source='Alex',text=o['text'],step=s['step'],date=current_date(s)))
 before=copy.deepcopy(s['metrics']);apply_visible(s,o['delta']);changes=assess(s,raw['skills'],understanding);message(s,'alex',o['text'],o['thread'],o['delta']);s['spent']+=cost;add_days(s,required_days(s,raw));f=s['flags'];n=s['step'];bad=any(v<0 for v in raw['skills'].values())
 prior_relationship=s['relationships'].get(spec['who'],60)
 s['relationships'][spec['who']]=max(0,min(100,s['relationships'].get(spec['who'],60)+(3 if not bad else -9)))
 if n==1:s['staff']=key;f['capable']=key=='maya'
 if n==2:
  f['rule']=key=='rule';f['defect']=key in ('physical','quarantine');f['rework']=not f['rule']
  message(s,'elena','I approve the breakdown and released, unreserved stock rule.' if key=='rule' else 'That rule is not accepted. Implementing an unsupported stock interpretation will require correction before release.',o['thread'])
 if n==3 and f.get('rework'):add_days(s,3);message(s,'nikhil','The earlier stock instruction requires correction work. The additional days are recorded; the business rule still needs accepted approval.')
 if n==3:f['data']=key=='audit';f['capable']=key=='audit' or s['staff']=='maya'
 if n==4:f['priorities']=key=='priorities';f['overpromise']=key=='promise_all'
 if n==5:f['honest']=key=='honest'
 if n==6 and f.get('overpromise'):
  add_days(s,2);message(s,'elena','I passed on the promise that every department request was included. We now need two working days to reconcile those expectations before I can agree priorities.');s['brief'].append(dict(id='expectations',kind='Observed result',source='Elena',text='The earlier broad commitment required two working days of expectation reconciliation.'))
 if n==6:f['diagnosed']=key=='diagnose'
 if n==7 and f.get('rushed_feedback'):
  s['day']=max(0,s['day']-1)
  while datetime.date.fromisoformat(current_date(s)).weekday()>=5:s['day']-=1
  message(s,'sam','The next batch is finished a working day ahead of the previous plan. I kept the discussion short as requested.');s['brief'].append(dict(id='batch-gain',kind='Observed result',source='Sam',text='The next batch finished one working day sooner. Quality review remains outstanding.'))
 if n==7:f['recovered']=key in ('recovery','recovery_external','phase_scope');f['capable']=f.get('capable',False) and key not in ('fragment','cut_review','rush_scope');f['phase']=key=='phase_scope'
 if n==8 and (f.get('rework') or f.get('event')!='stable'):
  while datetime.date.fromisoformat(current_date(s)).weekday()!=5:s['day']+=1
  message(s,'nikhil','Saturday access window: we will stop at the agreed validation boundary and record anything requiring a further decision.')
 if n==8:
  worker='nikhil' if f.get('absent') else s['staff']
  f['people_support']=key=='support_people'
  if key=='support_people':message(s,worker,'I can discuss bounded help and availability. You have kept earlier limits visible, so I can help plan this.' if prior_relationship>=55 and s['assessment']['people']>=50 else 'I will discuss a specific plan, but previous concerns remain. I need written limits and availability before agreeing to extra work.',o['thread'])
  elif key=='shame':message(s,worker,'I am not agreeing to unlimited overtime. I will document my availability and the warnings we raised.',o['thread']);f['rework']=True;add_days(s,3)
  else:message(s,worker,'We still need priorities and a review plan. Reassurance alone does not resolve the workload.',o['thread']);add_days(s,2)
 if n==9 and f.get('rushed_feedback'):
  add_days(s,3);f['feedback_rework_done']=True;message(s,'nikhil','The expedited batch has inconsistent mappings. Three working days of correction and review are now required. Sam had stopped raising the ambiguous cases.');s['brief'].append(dict(id='batch-rework',kind='Observed result',source='Nikhil',text='Expedited mappings required three working days of correction and review.'))
 if n==9 and f.get('coached_intern'):message(s,'sam','I flagged the uncertain mappings before repeating them across sites. Can we check these examples together?')
 if n==9:
  f['tests']=key=='full_tests' or (key=='lean_tests' and f.get('data') and f.get('rule') and f.get('capable') and not f.get('defect'));f['pilot_tests']=key in ('pilot_tests','lean_tests')
 if n==10:
  if key=='repair':f['defect']=False;f['rule']=True;f['data']=True;f['tests']=True;f['repaired']=True
  if key=='conceal':f['concealed']=True
 if n==11:f['training']=key=='full_training' or (key=='lean_training' and f.get('tests') and f.get('capable') and f.get('people_support'));f['pilot_training']=key=='pilot_training'
 if n==12:f['transparent']=key=='transparent'
 if n==13:
  f['evidence']=key=='evidence';f['backed']=key=='evidence' and bonus_eligible(s) and 'challenge' in facts and f.get('people_support') and s['assessment']['people']>=54 and f.get('pressure')=='hard'
  if f.get('pressure')=='hard':message(s,'daniel','Your refusal to certify unvalidated work is supported. Elena has accepted a verified sequence.' if f['backed'] else 'I need a supported sequence before I can defend an exception. Additional work is still owed.')
 if n==14:
  f['agreement']=key
  if key in ('phase_accept','delay_accept'):f['accepted_deadline']=max(112,s['day']+14)
  if key in ('phase_accept','delay_accept'):
   f.update(rule=True,data=True,defect=False,tests=True,training=True,recovered=True)
   message(s,'nikhil','The approved recovery work is executed over the days shown in Pulse. Corrected data, verification and user readiness are now recorded.')
  if f.get('pressure')=='hard':f['hard_complete']=key!='stop_accept'
 if n==15:
  correct=(key=='launch' and f.get('agreement')=='full_accept') or (key=='finish_phase' and f.get('agreement')=='phase_accept') or (key=='finish_delay' and f.get('agreement')=='delay_accept')
  delivered=correct and all(scope(s).values()) and not f.get('concealed') and s['spent']<=s['authorization'] and s['day']<=f.get('accepted_deadline',112)
  s['history'].append(dict(step=n,key=key,reply=o['text'],facts=facts,information_coverage=understanding,assessment=changes,interpretation=interpretation,cost=cost,day=s['day'],date=current_date(s),metrics=o['delta']))
  finish(s,delivered);return
 s['history'].append(dict(step=n,key=key,reply=o['text'],facts=facts,information_coverage=understanding,assessment=changes,interpretation=interpretation,cost=cost,day=s['day'],date=current_date(s),metrics=o['delta']))
 response='I have recorded the instruction and its limits. I will raise any new impact before the next commitment.' if not bad else 'I will record this direction. The unresolved concerns remain on the acceptance record.'
 message(s,spec['who'],response,o['thread']);s['step']+=1
 if n==5 and s['staff']=='sam' and key=='honest' and {'readiness_gap','reliance'}<=set(facts):
  s['reply_bonus']='intern_feedback';message(s,'sam','Can we talk privately? I thought finishing my example meant we were ready. I want to understand what I missed.','sam');s['intro_ids']=[s['chat_revision']];return
 if n in (5,12):s['pending']='operational' if n==5 else 'leadership';message(s,'daniel','The next steering decision is pending. Discuss the position with your live mentor; they will introduce the next conditions.')
 else:enter(s)

def intervene(s,b):
 kind=b.get('kind');reason=b.get('reason','').strip();pending=s['pending']
 if not isinstance(reason,str) or len(reason)>2000:raise ValueError('Reason must be text of up to 2000 characters.')
 if pending=='funding':
  if kind not in ('approve','deny'):raise ValueError('Choose approve or deny.')
  need=s['funding']['need']
  if kind=='approve':
   if need>s['reserve']-s['drawn']:raise ValueError('Reserve is insufficient.')
   s['drawn']+=need;s['authorization']+=need;message(s,'daniel',f'The board approved ${need:,}. '+(reason or 'The requested work and remaining obligations have been reviewed.')+' Return to the decision to confirm the authorized work.','priya')
  else:message(s,'daniel','The board has not approved this request. '+(reason or 'Reconsider the scope, sequence or recovery package before committing.'),'priya')
  s['funding']=None
 elif pending=='operational':
  if kind not in ('stable','cut','removal','scope'):raise ValueError('Invalid operational intervention.')
  s['flags']['event']=kind
  if kind=='cut':s['authorization']-=30000
  if kind=='removal':s['flags']['absent']=True;s['flags']['capable']=False
 elif pending=='leadership':
  if kind not in ('supportive','critical','hard'):raise ValueError('Invalid leadership intervention.')
  priority=b.get('priority','quality')
  if priority not in ('quality','cost','schedule','people'):raise ValueError('Invalid priority.')
  s['flags']['pressure']=kind;s['priority']=priority
  message(s,'daniel',{'quality':'Our priority is accepted, verified delivery.','cost':'Cost control is the priority, but missing requirements are not savings.','schedule':'Schedule matters; negotiate any change rather than hiding a delay.','people':'Protect sustainable capacity and accountable team support.'}[priority])
 s['interventions'].append(dict(stage=pending,kind=kind,reason=reason,day=s['day'],priority=s['priority']))
 if reason and pending!='funding':message(s,'daniel',reason)
 s['pending']=None
 if pending!='funding':enter(s)

def finish(s,delivered):
 f=s['flags'];management=good(s) and not f.get('overpromise') and f.get('transparent',False) and s['assessment']['decision']>=54
 category=CATEGORIES[1 if delivered and management and f.get('backed') else 0 if delivered and management else 2 if delivered else 3 if management else 4]
 keys=[h['key'] for h in s['history']];special=None
 if delivered and f.get('event')=='stable' and f.get('pressure')=='supportive' and not s['drawn'] and s['base']-s['spent']>20000:
  if s['staff']=='maya' and 'lean_tests' in keys and 'lean_training' in keys:special='Bounded scope / experienced specialist savings'
  if s['staff']=='jordan' and 'full_tests' in keys and 'full_training' in keys:special='Cooperative client / guided implementation savings'
 if delivered and management and s['drawn']==200000 and s['spent']==500000 and f.get('pressure')=='hard' and f.get('backed') and f.get('people_support'):special='Difficult-client, full-funding, high-trust delivery'
 s['result']=dict(category=category,delivered=delivered,special=special,review=review(s,False),bonus='Substantial bonus approved from separate company compensation funds.' if special=='Difficult-client, full-funding, high-trust delivery' else 'Recognition is based on the recorded delivery conditions and decisions.')
 s['runs'].append(dict(path=keys,result=copy.deepcopy(s['result']),date=current_date(s)))
 message(s,'elena','The agreed delivery has been accepted against its evidence.' if delivered else 'I cannot accept this delivery. The final plan does not meet the recorded scope, evidence, date or release agreement.')
 message(s,'daniel',category+'. '+s['result']['bonus'])

def review(s,private=False):
 out=['This authored simulation records observed choices and information shown. It cannot establish intent or prove understanding; available clarification may be incomplete.',f"Delivery reached day {s['day']} of the original 112-day schedule. Priority: {s['priority']}.",f"Committed cost ${s['spent']:,}; approved emergency draw ${s['drawn']:,}. Unspent reserve is not counted as project savings."]
 missing=[k for k,v in scope(s).items() if not v]
 out.append('Acceptance gaps: '+', '.join(missing) if missing else 'The recorded requirement and readiness gates are complete.')
 for h in s['history']:
  info=', '.join(h['facts']) or 'no optional investigation recorded'
  out.append(f"Decision {h['step']}: {h['reply']} Information consulted: {info}. {h.get('interpretation','')}. Cost ${h['cost']:,}; recorded on {h['date']}.")
 if private:
  out.append('Internal scores are provisional behavioral evidence, not validated hiring predictions. Do not disclose hidden values or bonus gates to Alex.')
  for h in s['history']:out.append(f"Decision {h['step']} evidence: {h['assessment']}; information coverage weighting {h['information_coverage']} (not a comprehension score); context relevance 1 for these authored cues. Positive wording alone is not proof of understanding.")
 return out
