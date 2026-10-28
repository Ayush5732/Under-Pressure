#!/usr/bin/env python3
"""Persistent two-device rooms with authenticated live state subscriptions."""
import argparse,json,os,secrets,socket,sqlite3,threading,time,webbrowser
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
import engine
ROOT=Path(__file__).resolve().parent;DB=Path(os.environ.get('STATE_DIRECTORY',str(ROOT)))/'saves-v3.sqlite3';LOCK=threading.Lock();CHANGED=threading.Condition(LOCK)
SHARE_URL=None;JOIN_FAILURES={};LIVE_WAIT=20

def connect():
 DB.parent.mkdir(parents=True,exist_ok=True)
 c=sqlite3.connect(DB);c.execute('CREATE TABLE IF NOT EXISTS rooms (code TEXT PRIMARY KEY,player TEXT,partner TEXT,state TEXT)');return c

def lan_addresses():
 found=set()
 try:
  for item in socket.getaddrinfo(socket.gethostname(),None,socket.AF_INET):found.add(item[4][0])
 except OSError:pass
 # Route selection uses a private network destination; no packets are sent.
 try:
  with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as probe:
   probe.connect(('192.168.255.254',1));found.add(probe.getsockname()[0])
 except OSError:pass
 return sorted(x for x in found if not x.startswith(('127.','0.')))

class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def respond(self,status,data):
  b=json.dumps(data).encode()
  try:
   self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(b)
  except (BrokenPipeError,ConnectionResetError):pass
 def token(self):return self.headers.get('Authorization','').removeprefix('Bearer ')
 def lookup(self,db):
  t=self.token()
  if not t:raise PermissionError('Session not found. Open your saved role link or join with the room code.')
  row=db.execute('SELECT * FROM rooms WHERE player=? OR partner=?',(t,t)).fetchone()
  if not row:raise PermissionError('Session not found. Open your saved role link or join with the room code.')
  return row,'protagonist' if secrets.compare_digest(t,row[1]) else 'partner'
 def public_origin(self):
  configured=os.environ.get('PUBLIC_ORIGIN') or os.environ.get('RENDER_EXTERNAL_URL')
  if configured:
   value=configured.rstrip('/');u=urlparse(value)
   if u.scheme not in ('http','https') or not u.netloc or u.path or u.query or u.fragment:raise ValueError('Invalid public origin configuration.')
   return value
  return None
 def share_url(self):
  if self.public_origin():return self.public_origin()
  host=self.headers.get('Host','127.0.0.1:8765')
  return SHARE_URL if SHARE_URL and host.split(':')[0] in ('localhost','127.0.0.1') else 'http://'+host
 def state(self,row,role):return dict(code=row[0],role=role,state=engine.view(json.loads(row[3]),role))
 def do_GET(self):
  parsed=urlparse(self.path);route=parsed.path
  if route=='/health':return self.respond(200,dict(status='ok'))
  if route in ('/api/state','/api/live','/api/invite'):
   try:
    if route=='/api/live':
     since=parse_qs(parsed.query).get('since',[''])[0];deadline=time.monotonic()+LIVE_WAIT
     with CHANGED:
      while True:
       with connect() as db:row,role=self.lookup(db)
       s=json.loads(row[3]);cursor=f"{s['revision']}:{s['chat_revision']}"
       if cursor!=since:break
       left=deadline-time.monotonic()
       if left<=0:return self.respond(200,dict(unchanged=True))
       CHANGED.wait(left)
     return self.respond(200,self.state(row,role))
    with LOCK,connect() as db:row,role=self.lookup(db)
    if route=='/api/invite':
     if role!='protagonist':return self.respond(403,dict(error='Only the project host can open the invitation panel.'))
     return self.respond(200,dict(code=row[0],share_url=self.share_url()))
    return self.respond(200,self.state(row,role))
   except PermissionError as e:return self.respond(401,dict(error=str(e)))
   except Exception:return self.respond(500,dict(error='Could not load the saved project.'))
  files={'/':('index.html','text/html'),'/app.js':('app.js','text/javascript'),'/style.css':('style.css','text/css')}
  if route not in files:return self.respond(404,dict(error='Not found'))
  name,mime=files[route];b=(ROOT/'web'/name).read_bytes();self.send_response(200);self.send_header('Content-Type',mime+'; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(b)
 def do_POST(self):
  origin=self.headers.get('Origin')
  if origin and origin!=(self.public_origin() or f'http://{self.headers.get("Host")}'):return self.respond(403,dict(error='Cross-origin requests are not allowed.'))
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length<0 or length>32768:return self.respond(413,dict(error='Request too large.'))
   body=json.loads(self.rfile.read(length) or '{}')
   if not isinstance(body,dict):raise ValueError('Invalid request.')
   route=urlparse(self.path).path;status=200
   with CHANGED:
    with connect() as db:
     if route=='/api/create':
      alphabet='ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
      while True:
       code=''.join(secrets.choice(alphabet) for _ in range(8))
       if not db.execute('SELECT 1 FROM rooms WHERE code=?',(code,)).fetchone():break
      p=secrets.token_urlsafe(24);m=secrets.token_urlsafe(24);db.execute('INSERT INTO rooms VALUES (?,?,?,?)',(code,p,m,json.dumps(engine.new_game())));status=201;result=dict(code=code,protagonist=p,partner=m,share_url=self.share_url())
     elif route=='/api/join':
      ip=self.client_address[0];now=time.monotonic();failed=[t for t in JOIN_FAILURES.get(ip,[]) if now-t<60];JOIN_FAILURES[ip]=failed
      if len(failed)>=12:return self.respond(429,dict(error='Too many incorrect room codes. Wait a minute and retry.'))
      code=body.get('code','')
      if not isinstance(code,str):raise ValueError('Enter the room code supplied by Alex.')
      code=''.join(c for c in code.upper() if c not in ' -\t\n\r')
      row=db.execute('SELECT * FROM rooms WHERE code=?',(code,)).fetchone() if 1<=len(code)<=16 else None
      if not row:failed.append(now);return self.respond(404,dict(error='Room not found. Check the code and make sure you opened the host’s game address.'))
      result=dict(code=row[0],session=row[2],role='partner')
     else:
      row,role=self.lookup(db);s=json.loads(row[3])
      if route!='/api/action':return self.respond(404,dict(error='Unknown action.'))
      action=body.get('action')
      if action not in ('chat','read') and body.get('revision')!=s['revision']:return self.respond(409,dict(error='The project changed. Review the latest state and retry.'))
      if action=='intervene' and role!='partner':return self.respond(403,dict(error='Only the live mentor controls interventions.'))
      if action in ('select','note','restore','read','candidates') and role!='protagonist':return self.respond(403,dict(error='Only Alex can perform this action.'))
      s=engine.act(s,role,action,body);db.execute('UPDATE rooms SET state=? WHERE code=?',(json.dumps(s),row[0]));result=dict(code=row[0],role=role,state=engine.view(s,role))
    CHANGED.notify_all() # The database commit is complete before clients wake.
   self.respond(status,result)
  except PermissionError as e:self.respond(401,dict(error=str(e)))
  except (ValueError,TypeError,KeyError) as e:self.respond(400,dict(error=str(e)))
  except Exception:self.respond(500,dict(error='Could not save this action. Refresh and retry.'))
def main():
 global DB,SHARE_URL
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=int(os.environ.get('PORT','8765')));p.add_argument('--host',default='0.0.0.0',help='0.0.0.0 permits other devices on the local network; use 127.0.0.1 for this computer only.');p.add_argument('--no-browser',action='store_true');p.add_argument('--db',type=Path);a=p.parse_args()
 if a.db:DB=a.db
 connect().close()
 try:http=ThreadingHTTPServer((a.host,a.port),Handler)
 except OSError as e:p.exit(1,f'{e}\nClose the old server or use --port 8766.\n')
 local=f'http://127.0.0.1:{a.port}';addresses=lan_addresses() if a.host=='0.0.0.0' else ([a.host] if a.host!='127.0.0.1' else [])
 SHARE_URL=f'http://{addresses[0]}:{a.port}' if addresses else local
 print(f'Under Pressure — live rooms\nThis computer: {local}\nMentor joins on the same network: {SHARE_URL}\nShare the game address and the room code shown after creating a project.\nKeep Terminal open. Saves: {DB}',flush=True)
 if not addresses:print('No network address detected. Check Wi-Fi or use a local interface address.',flush=True)
 if not a.no_browser:webbrowser.open(local)
 try:http.serve_forever()
 except KeyboardInterrupt:print('Progress saved.')
 finally:http.server_close()
if __name__=='__main__':main()
