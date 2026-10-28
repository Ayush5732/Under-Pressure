"""Generate an owner-only map from authored rules and executed reference paths."""
import itertools,json
from pathlib import Path
from scenarios import stage,PEOPLE
import learning,engine
from test_engine import play,start
ROOT=Path(__file__).resolve().parent

def build():
 inventory={};questions={}
 for hire,event,pressure in itertools.product(('maya','jordan','sam'),('stable','cut','removal','scope'),('supportive','critical','hard')):
  for n in range(1,16):
   s=dict(step=n,staff=hire,flags=dict(event=event,pressure=pressure,absent=event=='removal',rule=True,data=True,tests=True,people_support=True,capable=True))
   spec=stage(s)
   for o in spec['options']:
    key=(n,o['key']);item=inventory.setdefault(key,dict(step=n,key=o['key'],title=spec['title'],variants=[],requires=sorted(learning.GATES.get(o['key'],[]))))
    v=dict(text=o['text'],cost=engine.required_cost(s,o),days=engine.required_days(s,o))
    if v not in item['variants']:item['variants'].append(v)
   for q in learning.questions(s):questions.setdefault((n,q['fact']),dict(step=n,fact=q['fact'],who=q['who'],text=q['text']))
 routes=[]
 for hire,event,pressure in itertools.product(('maya','jordan','sam'),('stable','cut','removal','scope'),('supportive','critical','hard')):
  s=play(hire,event,pressure)
  routes.append(dict(hire=hire,event=event,pressure=pressure,style='Investigate all available original questions; first feasible commitment',delivered=s['result']['delivered'],category=s['result']['category'],special=s['result']['special'],cost=s['spent'],days=s['day'],steps=[dict(step=h['step'],reply=h['reply'],key=h['key'],facts=h['facts']) for h in s['history']]))
 for hire,mode,bad,investigate in [('maya','lean',False,True),('jordan','full',True,True),('jordan','recover',True,True),('sam','full',False,False)]:
  s=play(hire,mode=mode,bad=bad,investigate=investigate)
  routes.append(dict(hire=hire,event='stable',pressure='supportive',style=f'{mode}; alternative management choices={bad}; investigate={investigate}',delivered=s['result']['delivered'],category=s['result']['category'],special=s['result']['special'],cost=s['spent'],days=s['day'],steps=[dict(step=h['step'],reply=h['reply'],key=h['key'],facts=h['facts']) for h in s['history']]))
 data=dict(inventory=list(inventory.values()),questions=list(questions.values()),routes=routes,categories=engine.CATEGORIES)
 (ROOT/'branch_analysis.json').write_text(json.dumps(data,indent=2))
 template=(ROOT/'branch_map_template.html').read_text();(ROOT/'Branch_Map.html').write_text(template.replace('__DATA__',json.dumps(data).replace('</','<\\/')))
 print(json.dumps(dict(main_reply_branches=len(inventory),information_branches=len(questions),reference_paths=len(routes),successful_paths=sum(r['delivered'] for r in routes),failed_paths=sum(not r['delivered'] for r in routes))))
if __name__=='__main__':build()
