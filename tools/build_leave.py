"""연차관리대장: 기존 아티팩트 HTML에서
   (1) Firebase 버전 (site/leave/index.html)
   (2) 백업 내보내기만 추가한 기존 버전 (old_with_export.html)
   을 만들어요."""
import sys, pathlib

src = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
out_new = pathlib.Path(sys.argv[2])
out_old = pathlib.Path(sys.argv[3])

def rep(s, a, b, count=1):
    n = s.count(a)
    assert n == count, (n, a[:80])
    return s.replace(a, b)

BK_CSS = '''  /* backup */
  .bk-h{font-size:13px;font-weight:700;margin:6px 0 4px;}
  .bk-p{font-size:12px;color:var(--ink-soft);margin:0 0 8px;line-height:1.6;}
  .bk-text{width:100%;min-height:64px;font-family:var(--mono);font-size:11px;padding:8px 10px;border:1px solid var(--line-strong);border-radius:var(--radius);background:var(--white);color:var(--ink);resize:vertical;margin-bottom:8px;}
  .bk-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:14px;}
  .bk-row span{font-size:12px;color:var(--stamp-green);}
'''

EXPORT_JS = '''  // ---------- 백업 코드 내보내기 ----------
  function backupObj(){
    return {app:'연차관리대장', exportedAt:new Date().toISOString(), data:{
      settings:state.settings, overrides:state.overrides, holidays:state.holidays,
      holidaysJP:state.holidaysJP, scenarios:state.scenarios, activeScenario:state.activeScenario
    }};
  }
  async function copyBackup(){
    const box = document.getElementById('backupText');
    box.value = JSON.stringify(backupObj());
    box.hidden = false; box.focus(); box.select();
    let ok = false;
    try{ await navigator.clipboard.writeText(box.value); ok = true; }catch(_){
      try{ ok = document.execCommand('copy'); }catch(__){}
    }
    const n = state.scenarios.reduce((s,x)=>s+((x.entries||[]).length),0);
    document.getElementById('backupMsg').textContent = ok
      ? `시나리오 ${state.scenarios.length}개 · 사용 내역 ${n}건을 복사했어요.`
      : '아래 상자의 내용을 전부 선택해서 복사해주세요.';
  }
  document.getElementById('copyBackupBtn').addEventListener('click', copyBackup);

'''

FOOTER_ANCHOR = '      <div class="footer-note">8H = 연차 1개'
INIT_ANCHOR = '  // ---------- Init ----------'

# ================= (2) 기존 아티팩트 + 내보내기 =================
OLD_PANEL = '''      <details class="panel">
        <summary>📦 백업 코드 내보내기</summary>
        <div class="panel-body">
          <p class="bk-p">지금 기록 전체(시나리오, 사용 내역, 부여 규칙, 공휴일)를 코드로 복사해요. 새 연차관리대장의 <b>📦 백업 · 가져오기</b>에 붙여넣으면 그대로 옮겨져요.</p>
          <div class="bk-row"><button class="btn" id="copyBackupBtn">백업 코드 복사</button><span id="backupMsg"></span></div>
          <textarea id="backupText" class="bk-text" readonly hidden></textarea>
        </div>
      </details>

'''
old = src
old = rep(old, '</style>', BK_CSS + '</style>')
old = rep(old, FOOTER_ANCHOR, OLD_PANEL + FOOTER_ANCHOR)
old = rep(old, INIT_ANCHOR, EXPORT_JS + INIT_ANCHOR)
out_old.write_text(old, encoding='utf-8')

# ================= (1) Firebase 버전 =================
NEW_CSS = BK_CSS + '''  [hidden]{display:none!important;}
  .auth-box{max-width:460px;margin:30px auto;background:var(--paper-2);border:1px solid var(--line-strong);border-radius:var(--radius);padding:30px 22px;text-align:center;}
  .auth-box h3{font-family:var(--serif);font-size:19px;margin:0 0 8px;}
  .auth-box p{font-size:13px;color:var(--ink-soft);line-height:1.7;margin:0 0 18px;}
  .auth-box .btn{padding:10px 22px;font-size:14px;}
  .auth-msg{margin:14px 0 0!important;color:var(--stamp-red)!important;font-size:12px!important;min-height:1em;}
  .auth-warn{border:1px solid var(--stamp-red-dim);border-radius:var(--radius);padding:10px 12px;font-size:12px!important;color:var(--ink)!important;text-align:left;}
  .acct{margin-top:6px;}
  .link-btn{border:0;background:transparent;color:inherit;font:inherit;text-decoration:underline;text-underline-offset:3px;cursor:pointer;padding:0;}
  .link-btn:hover{color:var(--ink);}
  /* 휴대폰에서 오른쪽이 잘리던 문제 */
  @media(max-width:640px){
    .layout>.book{min-width:0;padding:16px 12px;}
    .cal-nav{flex-wrap:wrap;gap:8px;}
    table.ledger{display:block;overflow-x:auto;}
    .hday-add{flex-wrap:wrap;}
  }
'''

AUTH_BOX = '''  <div class="auth-box" id="authBox" hidden>
    <h3>내 연차관리대장 열기</h3>
    <p>기록은 내 구글 계정으로만 열 수 있어요.<br>처음 한 번 로그인하면 이 기기에서는 계속 로그인돼 있어요.</p>
    <p class="auth-warn" id="inAppWarn" hidden>카카오톡·네이버 같은 앱 안에서 열면 구글 로그인이 막혀요. 오른쪽 위 메뉴의 <b>다른 브라우저로 열기</b>로 크롬이나 사파리에서 열어주세요.</p>
    <button class="btn" id="loginBtn">Google 계정으로 로그인</button>
    <p class="auth-msg" id="authMsg" aria-live="polite"></p>
  </div>

'''

NEW_PANEL = '''      <details class="panel" id="backupPanel">
        <summary>📦 백업 · 가져오기</summary>
        <div class="panel-body">
          <div class="bk-h">기존 연차관리대장에서 옮겨오기</div>
          <p class="bk-p">기존 연차관리대장(Claude) 맨 아래 <b>📦 백업 코드 내보내기 → 백업 코드 복사</b>를 누른 뒤, 여기에 붙여넣고 가져오기를 눌러주세요. 지금 화면의 기록은 가져온 내용으로 바뀌어요.</p>
          <textarea id="importText" class="bk-text" placeholder="여기에 백업 코드 붙여넣기"></textarea>
          <div class="bk-row"><button class="btn" id="importBtn">가져오기</button><span id="importMsg" aria-live="polite"></span></div>
          <div class="bk-h">백업해 두기</div>
          <p class="bk-p">지금 기록 전체를 코드로 복사해요. 메모장 등에 붙여넣어 보관하면 돼요.</p>
          <div class="bk-row"><button class="btn ghost" id="copyBackupBtn">백업 코드 복사</button><span id="backupMsg" aria-live="polite"></span></div>
          <textarea id="backupText" class="bk-text" readonly hidden></textarea>
        </div>
      </details>

'''

STORAGE_START = '  // ---------- Storage layer ----------'
STORAGE_END = '  function grantForYear(year){'

NEW_STORAGE = r'''  // ---------- Storage layer (Firebase) ----------
  // 기록은 Firestore의 users/{내 계정}/apps/leave 문서 하나에 저장돼요 (기존 아티팩트와 같은 구조).
  // 보안 규칙으로 내 구글 계정만 읽고 쓸 수 있어요.
  let fb = null, user = null, docRef = null, unsub = null, loaded = false;
  let docCache = {};
  let fbResolve, fbReject;
  const fbReady = new Promise((res, rej)=>{ fbResolve = res; fbReject = rej; });
  window.__fbLoaded = api => fbResolve(api);
  window.__fbFailed = () => fbReject(new Error('load'));
  if(window.__fbApi) fbResolve(window.__fbApi);
  const IN_APP = /KAKAOTALK|NAVER|Instagram|FBAN|FBAV|Line\/|DaumApps|everytimeApp/i.test(navigator.userAgent);
  const DEFAULT_SCENARIOS = [{id:uid(), name:'안1', entries:[]}, {id:uid(), name:'안2', entries:[]}];
  const FIELDS = ['settings','overrides','holidays','holidaysJP','scenarios','activeScenario'];

  function todayLocal(){ const d = new Date(); return `${d.getFullYear()}-${pad2(d.getMonth()+1)}-${pad2(d.getDate())}`; }

  function fbErrText(e){
    const c = (e && e.code) || '';
    if(c==='auth/popup-blocked') return '로그인 창이 막혔어요. 브라우저에서 이 사이트의 팝업을 허용한 뒤 다시 눌러주세요.';
    if(c==='auth/popup-closed-by-user' || c==='auth/cancelled-popup-request') return '로그인 창이 닫혔어요. 다시 눌러주세요.';
    if(c==='auth/unauthorized-domain') return 'Firebase 승인된 도메인에 bae4021.github.io가 없어요.';
    if(c==='auth/network-request-failed' || c==='unavailable') return '인터넷 연결을 확인해주세요.';
    if(c==='permission-denied') return '이 계정은 열 수 없거나, Firestore 보안 규칙이 아직 바뀌지 않았어요. 로그인한 계정과 보안 규칙을 확인해주세요.';
    return (e && e.message) || String(e || '알 수 없는 오류');
  }

  function storeGet(key, fallback){
    return (docCache && key in docCache) ? docCache[key] : fallback;
  }
  // 화면은 바로 바뀌고, 저장은 뒤에서 해요. 인터넷이 끊겨 있으면 연결되는 대로 저장돼요.
  function storeSet(key, val){
    docCache[key] = val;
    if(!docRef){ setSaveStatus('error'); return Promise.resolve(); }
    setSaveStatus('saving');
    fb.setDoc(docRef, {[key]: val}, {mergeFields:[key]})
      .then(()=>setSaveStatus('ok'))
      .catch(e=>{ console.error('save failed', key, e); setSaveStatus('error', e); });
    return Promise.resolve();
  }

  function setSaveStatus(kind, err){
    const el = document.getElementById('saveStatus');
    if(!el) return;
    if(kind==='error'){
      el.textContent = '⚠ 저장 실패 — ' + (err ? fbErrText(err) : '로그인 상태를 확인해주세요');
      el.className = 'save-status warn';
    } else if(kind==='saving'){
      el.textContent = navigator.onLine ? '☁ 저장 중...' : '⏸ 오프라인 · 연결되면 자동으로 저장돼요';
      el.className = 'save-status warn';
    } else if(kind==='loading'){
      el.textContent = '불러오는 중...'; el.className = 'save-status warn';
    } else if(kind==='login'){
      el.textContent = '로그인이 필요해요'; el.className = 'save-status warn';
    } else if(kind==='fatal'){
      el.textContent = '⚠ ' + err; el.className = 'save-status warn';
    } else {
      el.textContent = '☁ 계정에 자동 저장됨'; el.className = 'save-status ok';
    }
  }

  function applyState(){
    state.settings = storeGet('settings', DEFAULT_SETTINGS);
    state.overrides = storeGet('overrides', {});
    state.holidays = storeGet('holidays', DEFAULT_HOLIDAYS);
    state.holidaysJP = storeGet('holidaysJP', DEFAULT_HOLIDAYS_JP);
    state.scenarios = storeGet('scenarios', DEFAULT_SCENARIOS);
    if(!Array.isArray(state.scenarios) || !state.scenarios.length) state.scenarios = DEFAULT_SCENARIOS;
    state.scenarios.forEach(s=>{ if(!Array.isArray(s.entries)) s.entries = []; });
    state.activeScenario = storeGet('activeScenario', state.scenarios[0].id);
    if(!state.scenarios.find(s=>s.id===state.activeScenario)) state.activeScenario = state.scenarios[0].id;
  }

  function showApp(on){
    document.getElementById('appLayout').hidden = !on;
    document.getElementById('authBox').hidden = on;
    document.querySelector('.year-picker').style.visibility = on ? '' : 'hidden';
  }
  function renderAccount(){
    const el = document.getElementById('acct');
    el.innerHTML = user
      ? `${(user.email||'').replace(/[<>&"]/g,'')} 계정에 저장돼요 · <button class="link-btn" id="logoutBtn">로그아웃</button>`
      : '';
  }
  // 입력 중인 칸이 있으면 다른 기기에서 온 변경으로 화면을 다시 그리지 않아요
  function isEditing(){
    const a = document.activeElement;
    return !!(a && (a.classList.contains('tab-name-input') || (a.closest && a.closest('.rule-grid, #overrideBody'))));
  }

  async function login(){
    const msg = document.getElementById('authMsg');
    msg.textContent = '';
    if(!fb){ msg.textContent = '아직 준비 중이에요. 잠시 후 다시 눌러주세요.'; return; }
    try{
      const p = new fb.GoogleAuthProvider();
      p.setCustomParameters({prompt:'select_account'});
      await fb.signInWithPopup(fb.auth, p);
    }catch(e){ console.error(e); msg.textContent = fbErrText(e); }
  }

  function startStore(){
    fb.onAuthStateChanged(fb.auth, u=>{
      if(unsub){ unsub(); unsub = null; }
      user = u || null; loaded = false; docRef = null; docCache = {};
      renderAccount();
      if(!user){ showApp(false); setSaveStatus('login'); return; }
      document.getElementById('authBox').hidden = true;
      document.getElementById('authMsg').textContent = '';
      setSaveStatus('loading');
      docRef = fb.doc(fb.db, 'users', user.uid, 'apps', 'leave');
      unsub = fb.onSnapshot(docRef, snap=>{
        if(loaded && snap.metadata.hasPendingWrites) return; // 방금 내가 바꾼 내용 (화면엔 이미 반영됨)
        docCache = snap.exists() ? (snap.data() || {}) : {};
        applyState();
        if(!loaded){
          loaded = true;
          selectedYear = new Date().getFullYear();
          selectedMonth = new Date().getMonth();
          document.getElementById('fDate').value = todayLocal();
          showApp(true);
          setSaveStatus('ok');
          render();
          return;
        }
        if(!isEditing()) render();
      }, err=>{
        console.error('snapshot error', err);
        loaded = false;
        showApp(false);
        document.getElementById('authMsg').textContent = fbErrText(err);
        setSaveStatus('error', err);
      });
    });
  }

  // ---------- 백업 · 가져오기 ----------
  function backupObj(){
    return {app:'연차관리대장', exportedAt:new Date().toISOString(), data:{
      settings:state.settings, overrides:state.overrides, holidays:state.holidays,
      holidaysJP:state.holidaysJP, scenarios:state.scenarios, activeScenario:state.activeScenario
    }};
  }
  async function copyBackup(){
    const box = document.getElementById('backupText');
    box.value = JSON.stringify(backupObj());
    box.hidden = false; box.focus(); box.select();
    let ok = false;
    try{ await navigator.clipboard.writeText(box.value); ok = true; }catch(_){
      try{ ok = document.execCommand('copy'); }catch(__){}
    }
    const n = state.scenarios.reduce((s,x)=>s+((x.entries||[]).length),0);
    document.getElementById('backupMsg').textContent = ok
      ? `시나리오 ${state.scenarios.length}개 · 사용 내역 ${n}건을 복사했어요.`
      : '아래 상자의 내용을 전부 선택해서 복사해주세요.';
  }
  let importArmed = false, importTimer = null;
  async function importBackup(){
    const btn = document.getElementById('importBtn'), msg = document.getElementById('importMsg');
    const raw = document.getElementById('importText').value.trim();
    if(!docRef){ msg.textContent = '먼저 로그인해주세요.'; return; }
    if(!raw){ msg.textContent = '기존 연차관리대장에서 복사한 백업 코드를 붙여넣어주세요.'; return; }
    let data;
    try{
      const obj = JSON.parse(raw);
      data = (obj && obj.data) ? obj.data : obj;
      if(!data || !Array.isArray(data.scenarios)) throw 0;
    }catch(_){ msg.textContent = '백업 코드 형식이 아니에요. 처음부터 끝까지 다 붙여넣었는지 확인해주세요.'; return; }
    const haveNow = ('scenarios' in docCache) && state.scenarios.some(s=>(s.entries||[]).length);
    if(haveNow && !importArmed){
      importArmed = true;
      btn.textContent = '덮어쓰기';
      msg.textContent = '지금 기록이 있어요. 한 번 더 누르면 가져온 내용으로 바뀌어요.';
      clearTimeout(importTimer);
      importTimer = setTimeout(()=>{ importArmed = false; btn.textContent = '가져오기'; }, 6000);
      return;
    }
    importArmed = false; clearTimeout(importTimer); btn.textContent = '가져오기';
    const clean = {};
    FIELDS.forEach(k=>{ if(data[k] !== undefined) clean[k] = data[k]; });
    docCache = clean; applyState(); render();
    const n = state.scenarios.reduce((s,x)=>s+(x.entries||[]).length,0);
    btn.disabled = true;
    msg.textContent = '저장 중...';
    try{
      const saved = await Promise.race([fb.setDoc(docRef, clean).then(()=>true), new Promise(r=>setTimeout(()=>r(false), 15000))]);
      msg.textContent = saved
        ? `시나리오 ${state.scenarios.length}개 · 사용 내역 ${n}건을 가져왔어요 ✓`
        : '가져왔어요. 인터넷이 느려서 저장이 늦어지고 있어요 — 연결되면 자동으로 저장돼요.';
      document.getElementById('importText').value = '';
      setSaveStatus('ok');
    }catch(e){
      console.error(e); msg.textContent = '가져오지 못했어요. ' + fbErrText(e);
    }finally{ btn.disabled = false; }
  }

'''

new = src
new = rep(new, '</style>', NEW_CSS + '</style>')
new = rep(new, '  <div class="layout">', AUTH_BOX + '  <div class="layout" id="appLayout" hidden>')
new = rep(new, FOOTER_ANCHOR, NEW_PANEL + FOOTER_ANCHOR)
new = rep(new, '      <div class="save-status" id="saveStatus"></div>',
               '      <div class="save-status" id="saveStatus"></div>\n      <div class="save-status acct" id="acct" style="color:var(--ink-soft);"></div>')
a = new.index(STORAGE_START); b = new.index(STORAGE_END)
new = new[:a] + NEW_STORAGE + new[b:]
# 한국 시간 기준 '오늘' (기존엔 오전 9시 전에 하루 전으로 표시되던 문제)
new = rep(new, "const todayStr = new Date().toISOString().slice(0,10);", "const todayStr = todayLocal();")
INIT_OLD = new[new.index(INIT_ANCHOR):new.index('})();\n</script>')]
INIT_NEW = '''  // ---------- Init ----------
  document.getElementById('loginBtn').addEventListener('click', login);
  document.getElementById('acct').addEventListener('click', ev=>{ if(ev.target.id==='logoutBtn' && fb) fb.signOut(fb.auth); });
  document.getElementById('importBtn').addEventListener('click', importBackup);
  document.getElementById('copyBackupBtn').addEventListener('click', copyBackup);
  window.addEventListener('online', ()=>{ if(loaded) setSaveStatus('ok'); });
  (async function init(){
    if(IN_APP) document.getElementById('inAppWarn').hidden = false;
    document.querySelector('.year-picker').style.visibility = 'hidden';
    setSaveStatus('loading');
    try{
      fb = await Promise.race([fbReady, new Promise((_,rej)=>setTimeout(()=>rej(new Error('timeout')), 20000))]);
    }catch(e){
      setSaveStatus('fatal', '저장소 프로그램을 불러오지 못했어요. 인터넷 연결을 확인하고 새로고침해주세요.');
      return;
    }
    startStore();
  })();
'''
new = new.replace(INIT_OLD, INIT_NEW)
new = rep(new, '<script>\n(function(){', '<script src="../fb.js" defer onerror="window.__fbFailed&&window.__fbFailed()"></script>\n<script>\n(function(){')
new = rep(new, '저장 상태는 상단을 확인하세요', '기록은 내 구글 계정으로 보호돼요')
for bad in ['window.claude', 'window.storage', 'storageMode', 'loadAll']:
    assert bad not in new, bad
out_new.parent.mkdir(parents=True, exist_ok=True)
out_new.write_text(new, encoding='utf-8')
print('ok', len(old), len(new))
