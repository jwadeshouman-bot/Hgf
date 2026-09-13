# M7MAD_FF AI v4.0 - Full API + Viewer + Red/Black Theme
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for, Response
import requests
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "M7MAD_AI_SECRET_2026_NEVER_CHANGE"

# ====== AI Server ======
AI_BASE = "http://51.75.118.171:20085"

# ====== المستخدمين ======
users = {"admin": {"password": "1234", "name": "M7MAD_FF", "role": "admin"}}


# ============================================================
# دوال الاتصال بالـ API
# ============================================================
def _safe_request(method, endpoint, **kwargs):
    try:
        url = f"{AI_BASE}{endpoint}"
        kwargs.setdefault('timeout', 60)
        if method == 'POST':
            r = requests.post(url, **kwargs)
        elif method == 'GET':
            r = requests.get(url, **kwargs)
        elif method == 'DELETE':
            r = requests.delete(url, **kwargs)
        else:
            return {"error": "Invalid method"}
        try:
            return r.json()
        except:
            return {"response": r.text}
    except Exception as e:
        return {"error": str(e)}


def api_chat(user_id, message):
    return _safe_request('POST', '/chat', json={"user_id": user_id, "message": message})


def api_chat_form(user_id, message):
    return _safe_request('POST', '/chat/form', data={"user_id": user_id, "message": message})


def api_ask(question):
    return _safe_request('GET', '/ask', params={"question": question})


def api_ask_text(question):
    try:
        r = requests.get(f"{AI_BASE}/ask/text", params={"question": question}, timeout=60)
        return r.text
    except Exception as e:
        return f"Error: {e}"


def api_create_session(user_id):
    return _safe_request('POST', '/session', json={"user_id": user_id})


def api_reset(user_id):
    return _safe_request('POST', '/reset', json={"user_id": user_id})


def api_session_info(user_id):
    return _safe_request('GET', f'/session/{user_id}')


def api_delete_session(user_id):
    return _safe_request('DELETE', f'/session/{user_id}')


def api_health():
    return _safe_request('GET', '/health')


def api_info():
    return _safe_request('GET', '/api')


def api_version():
    return _safe_request('GET', '/version')


# ============================================================
# CSS مشترك
# ============================================================
BASE_CSS = """
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{font-family:'Segoe UI',Tahoma,sans-serif;background:#0a0a0a;
    background-image:radial-gradient(circle at 20% 50%,rgba(255,0,64,0.1) 0%,transparent 50%),
                      radial-gradient(circle at 80% 80%,rgba(255,23,68,0.08) 0%,transparent 50%);
    color:#fff;min-height:100vh}
input,textarea,button{font-family:inherit}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:#1a1a1a}
::-webkit-scrollbar-thumb{background:#ff0040;border-radius:3px}
</style>
"""


# ============================================================
# LOGIN
# ============================================================
LOGIN_HTML = BASE_CSS + """
<!DOCTYPE html><html dir="rtl" lang="ar"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>M7MAD_FF AI</title>
<style>
body{display:flex;justify-content:center;align-items:center;padding:20px;overflow:hidden}
.bg{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;overflow:hidden;pointer-events:none}
.bg span{position:absolute;display:block;background:rgba(255,0,64,0.25);border-radius:50%;animation:floatUp 15s linear infinite;bottom:-150px}
@keyframes floatUp{0%{transform:translateY(0) rotate(0);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translateY(-1000px) rotate(720deg);opacity:0}}
.box{position:relative;z-index:1;background:linear-gradient(145deg,#1a1a1a,#0f0f0f);border:1px solid rgba(255,0,64,0.3);border-radius:25px;padding:40px 30px;width:100%;max-width:420px;box-shadow:0 25px 80px rgba(255,0,64,0.2);animation:slideUp 0.6s ease}
@keyframes slideUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.logo{text-align:center;margin-bottom:30px}
.logo-icon{font-size:60px;margin-bottom:10px;animation:pulse 2s ease infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.1)}}
.logo h1{font-size:26px;font-weight:bold;background:linear-gradient(135deg,#ff0040,#ff1744,#ff5252);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.logo p{color:rgba(255,255,255,0.5);font-size:13px;margin-top:5px}
.field{margin-bottom:18px}
.field label{display:block;color:#ff5252;font-size:13px;margin-bottom:8px;font-weight:bold}
.field input{width:100%;padding:15px 18px;background:#0a0a0a;border:2px solid #2a2a2a;border-radius:15px;color:#fff;font-size:15px;outline:none;transition:all 0.3s}
.field input:focus{border-color:#ff0040;background:#111;box-shadow:0 0 0 3px rgba(255,0,64,0.15)}
.btn{width:100%;padding:16px;background:linear-gradient(135deg,#ff0040,#d50000);color:#fff;border:none;border-radius:15px;font-size:16px;font-weight:bold;cursor:pointer;margin-top:10px;box-shadow:0 8px 25px rgba(255,0,64,0.4);transition:all 0.3s}
.btn:hover{transform:translateY(-2px);box-shadow:0 12px 35px rgba(255,0,64,0.6)}
.error{background:rgba(255,0,64,0.15);border:1px solid rgba(255,0,64,0.4);color:#ff5252;padding:12px;border-radius:12px;margin-bottom:20px;text-align:center;font-size:14px}
.footer{text-align:center;color:rgba(255,255,255,0.4);font-size:12px;margin-top:25px}
.footer a{color:#ff5252;text-decoration:none}
</style></head><body>
<div class="bg">
<span style="left:10%;animation-delay:0s;width:15px;height:15px"></span>
<span style="left:25%;animation-delay:2s;width:25px;height:25px"></span>
<span style="left:40%;animation-delay:4s;width:10px;height:10px"></span>
<span style="left:55%;animation-delay:6s;width:20px;height:20px"></span>
<span style="left:70%;animation-delay:8s;width:18px;height:18px"></span>
<span style="left:85%;animation-delay:10s;width:22px;height:22px"></span>
</div>
<div class="box">
<div class="logo"><div class="logo-icon">🤖</div><h1>M7MAD_FF AI</h1><p>سجل دخولك</p></div>
{% if error %}<div class="error">❌ {{ error }}</div>{% endif %}
<form method="POST" action="/login">
<div class="field"><label>👤 اسم المستخدم</label>
<input type="text" name="username" placeholder="username" required autofocus></div>
<div class="field"><label>🔒 كلمة المرور</label>
<input type="password" name="password" placeholder="••••••••" required></div>
<button type="submit" class="btn">🚀 دخول</button></form>
<div class="footer">Powered by <a href="#">M7MAD_FF</a> © 2026</div>
</div></body></html>
"""


# ============================================================
# CHAT
# ============================================================
CHAT_HTML = """
<!DOCTYPE html><html dir="rtl" lang="ar"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>M7MAD_FF AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%;overflow:hidden}
body{font-family:'Segoe UI',Tahoma,sans-serif;background:#0a0a0a;
    background-image:radial-gradient(circle at 20% 50%,rgba(255,0,64,0.08) 0%,transparent 50%),
                      radial-gradient(circle at 80% 80%,rgba(255,23,68,0.06) 0%,transparent 50%);
    color:#fff}
input,textarea,button{font-family:inherit}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-thumb{background:#ff0040;border-radius:3px}

.app{display:flex;flex-direction:column;height:100vh;height:100dvh;overflow:hidden}

/* HEADER */
.header{background:linear-gradient(135deg,#ff0040,#d50000,#ff1744);
    background-size:300% 300%;animation:gradientMove 5s ease infinite;
    padding:12px 15px;display:flex;justify-content:space-between;align-items:center;
    box-shadow:0 4px 20px rgba(255,0,64,0.4);flex-shrink:0;z-index:10;gap:10px}
@keyframes gradientMove{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.header-info h1{font-size:17px;font-weight:bold;text-shadow:0 2px 10px rgba(0,0,0,0.3)}
.header-info p{font-size:10px;opacity:0.9;margin-top:1px}
.header-actions{display:flex;align-items:center;gap:6px}
.icon-btn{background:rgba(0,0,0,0.25);border:none;color:white;width:36px;height:36px;
    border-radius:50%;cursor:pointer;font-size:16px;display:flex;align-items:center;
    justify-content:center;transition:all 0.3s;flex-shrink:0}
.icon-btn:hover{background:rgba(0,0,0,0.5);transform:scale(1.1)}
.icon-btn:active{transform:scale(0.95)}
.user-badge{background:rgba(255,255,255,0.15);padding:6px 12px;border-radius:20px;
    font-size:11px;font-weight:bold;white-space:nowrap}

/* STATUS */
.status{padding:5px 15px;text-align:center;font-size:11px;font-weight:bold;
    background:rgba(76,175,80,0.2);color:#4caf50;flex-shrink:0;transition:all 0.3s}
.status.busy{background:rgba(255,193,7,0.2);color:#ffc107}
.status.error{background:rgba(244,67,54,0.2);color:#f44336}

/* CHAT */
.chat{flex:1;padding:15px;overflow-y:auto;background:rgba(0,0,0,0.2);
    display:flex;flex-direction:column;gap:10px}
.msg{padding:10px 16px;border-radius:18px;max-width:80%;word-wrap:break-word;
    line-height:1.5;animation:fadeIn 0.3s ease;font-size:14px;
    box-shadow:0 2px 10px rgba(0,0,0,0.3);position:relative}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.user{background:linear-gradient(135deg,#ff0040,#d50000);color:white;margin-left:auto;
    border-bottom-right-radius:5px;box-shadow:0 4px 15px rgba(255,0,64,0.3)}
.bot{background:#1a1a1a;border:1px solid #2a2a2a;color:#e0e0e0;margin-right:auto;
    border-bottom-left-radius:5px}
.bot b{color:#ff5252}
.msg-actions{position:absolute;top:5px;left:5px;display:none;gap:4px}
.msg:hover .msg-actions{display:flex}
.msg-action{background:rgba(0,0,0,0.7);border:none;color:white;width:24px;height:24px;
    border-radius:50%;cursor:pointer;font-size:11px;display:flex;align-items:center;
    justify-content:center;transition:all 0.2s}
.msg-action:hover{background:#ff0040}

/* TOOLS TOGGLE */
.tools-toggle{position:fixed;bottom:90px;left:15px;width:50px;height:50px;
    background:linear-gradient(135deg,#ff0040,#d50000);border:none;border-radius:50%;
    cursor:pointer;font-size:22px;color:white;box-shadow:0 5px 20px rgba(255,0,64,0.5);
    z-index:100;transition:all 0.3s;display:flex;align-items:center;justify-content:center}
.tools-toggle:hover{transform:scale(1.1)}
.tools-toggle.active{transform:rotate(45deg);background:linear-gradient(135deg,#d50000,#8b0000)}

.tools-panel{position:fixed;bottom:150px;left:15px;
    background:linear-gradient(145deg,#1a1a1a,#0f0f0f);
    border:1px solid rgba(255,0,64,0.3);border-radius:20px;padding:12px;
    box-shadow:0 10px 40px rgba(0,0,0,0.8);z-index:99;
    display:grid;grid-template-columns:repeat(3,1fr);gap:8px;
    transform:scale(0);opacity:0;transition:all 0.3s;
    transform-origin:bottom left;max-width:290px;pointer-events:none}
.tools-panel.show{transform:scale(1);opacity:1;pointer-events:auto}
.tool{padding:10px 8px;background:linear-gradient(145deg,#0f0f0f,#0a0a0a);
    border:1px solid rgba(255,0,64,0.2);color:#e0e0e0;border-radius:12px;
    cursor:pointer;font-size:11px;font-weight:bold;transition:all 0.3s;
    display:flex;flex-direction:column;align-items:center;gap:4px;
    text-align:center;min-height:60px;justify-content:center}
.tool .emoji{font-size:20px;line-height:1}
.tool:hover{background:linear-gradient(135deg,#ff0040,#d50000);border-color:transparent;
    transform:translateY(-2px);box-shadow:0 5px 15px rgba(255,0,64,0.4)}
.tool:active{transform:scale(0.95)}

/* INPUT */
.input-area{display:flex;padding:12px 15px;background:linear-gradient(135deg,#1a1a1a,#0f0f0f);
    border-top:1px solid rgba(255,0,64,0.2);gap:10px;flex-shrink:0;
    padding-bottom:max(12px,env(safe-area-inset-bottom))}
.input-area input{flex:1;padding:14px 20px;background:#0a0a0a;border:2px solid #2a2a2a;
    border-radius:25px;color:white;font-size:15px;outline:none;transition:all 0.3s;min-width:0}
.input-area input:focus{border-color:#ff0040;background:#111;box-shadow:0 0 0 3px rgba(255,0,64,0.15)}
.send-btn{padding:14px 22px;background:linear-gradient(135deg,#ff0040,#d50000);
    color:white;border:none;border-radius:25px;font-size:15px;font-weight:bold;
    cursor:pointer;transition:all 0.3s;box-shadow:0 4px 15px rgba(255,0,64,0.4);
    flex-shrink:0;display:flex;align-items:center;justify-content:center;min-width:60px}
.send-btn:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(255,0,64,0.6)}
.send-btn:disabled{opacity:0.5;cursor:not-allowed}

/* TOAST */
.toast{position:fixed;bottom:80px;right:50%;transform:translateX(50%) translateY(100px);
    background:linear-gradient(135deg,#ff0040,#d50000);color:white;padding:12px 24px;
    border-radius:25px;font-size:14px;z-index:400;opacity:0;transition:all 0.3s;
    font-weight:bold;pointer-events:none;box-shadow:0 8px 30px rgba(255,0,64,0.5)}
.toast.show{transform:translateX(50%) translateY(0);opacity:1}

@media (max-width:768px){
    .msg{max-width:85%;font-size:13px}
    .header{padding:10px 12px}
    .header-info h1{font-size:15px}
    .user-badge{font-size:10px;padding:5px 8px}
    .icon-btn{width:32px;height:32px;font-size:14px}
    .tools-toggle{width:46px;height:46px;font-size:20px}
    .tools-panel{grid-template-columns:repeat(3,1fr);max-width:260px}
}
</style></head><body>
<div class="app">

<!-- HEADER -->
<div class="header">
    <div class="header-info">
        <h1>🤖 M7MAD_FF AI</h1>
        <p>مساعدك الذكي</p>
    </div>
    <div class="header-actions">
        <button class="icon-btn" onclick="window.open('/api-viewer', '_blank')" title="كل الـ API">🌐</button>
        <button class="icon-btn" onclick="window.open('http://51.75.118.171:20085/docs', '_blank')" title="Swagger">📖</button>
        <button class="icon-btn" onclick="window.open('http://51.75.118.171:20085/redoc', '_blank')" title="ReDoc">📚</button>
        <button class="icon-btn" onclick="downloadChat()" title="تحميل">💾</button>
        <div class="user-badge">👤 {{ username }}</div>
        <a href="/logout"><button class="icon-btn" title="خروج">🚪</button></a>
    </div>
</div>

<!-- STATUS -->
<div class="status" id="status">✅ جاهز</div>

<!-- CHAT -->
<div class="chat" id="chat">
<div class="msg bot"><b>أهلاً {{ username }}! 👋</b><br>أنا <b>M7MAD_FF AI</b><br><br>اسألني أي شي أو اضغط على الأزرار ⚡</div>
</div>

<!-- TOOLS TOGGLE -->
<button class="tools-toggle" id="toolsToggle" onclick="toggleTools()" title="الأوامر">⚡</button>

<!-- TOOLS PANEL -->
<div class="tools-panel" id="toolsPanel">
    <div class="tool" onclick="quick('مرحبا')"><span class="emoji">👋</span>مرحبا</div>
    <div class="tool" onclick="quick('شلونك')"><span class="emoji">💬</span>شلونك</div>
    <div class="tool" onclick="quick('منو انت')"><span class="emoji">🤖</span>منو انت</div>
    <div class="tool" onclick="quick('شكرا')"><span class="emoji">🌟</span>شكراً</div>
    <div class="tool" onclick="quick('قول لي نكتة')"><span class="emoji">😂</span>نكتة</div>
    <div class="tool" onclick="quick('ساعدني')"><span class="emoji">❓</span>ساعدني</div>
    <div class="tool" onclick="quick('معلومات API')"><span class="emoji">ℹ️</span>API</div>
    <div class="tool" onclick="quick('فحص الخدمة')"><span class="emoji">✅</span>فحص</div>
    <div class="tool" onclick="quick('الإصدار')"><span class="emoji">📌</span>الإصدار</div>
    <div class="tool" onclick="quick('معلومات جلستي')"><span class="emoji">📊</span>جلستي</div>
    <div class="tool" onclick="resetMemory()"><span class="emoji">🗑️</span>مسح</div>
    <div class="tool" onclick="deleteSession()"><span class="emoji">❌</span>حذف</div>
    <div class="tool" onclick="copyLast()"><span class="emoji">📋</span>نسخ</div>
    <div class="tool" onclick="clearChat()"><span class="emoji">🧹</span>تفريغ</div>
    <div class="tool" onclick="window.open('/api-viewer', '_blank')"><span class="emoji">🌐</span>API Viewer</div>
</div>

<!-- INPUT -->
<div class="input-area">
<input id="inp" placeholder="اكتب رسالتك..." autofocus autocomplete="off">
<button class="send-btn" id="btn" onclick="send()">➤</button>
</div>

</div>

<!-- TOAST -->
<div class="toast" id="toast"></div>

<script>
const chat = document.getElementById('chat');
const inp = document.getElementById('inp');
const btn = document.getElementById('btn');
const status = document.getElementById('status');
const toastEl = document.getElementById('toast');
const uid = '{{ username }}_' + Math.random().toString(36).substr(2,5);

let lastBotMsg = '';

inp.addEventListener('keypress', e => { if(e.key === 'Enter') send(); });

function toast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    setTimeout(() => toastEl.classList.remove('show'), 2000);
}

function setStatus(text, cls = '') {
    status.textContent = text;
    status.className = 'status ' + cls;
}

function toggleTools() {
    document.getElementById('toolsPanel').classList.toggle('show');
    document.getElementById('toolsToggle').classList.toggle('active');
}

function closeTools() {
    document.getElementById('toolsPanel').classList.remove('show');
    document.getElementById('toolsToggle').classList.remove('active');
}

function quick(t) {
    inp.value = t;
    send();
    closeTools();
}

async function send() {
    const m = inp.value.trim();
    if(!m) return;
    add(m, 'user');
    inp.value = '';
    btn.disabled = true;
    setStatus('⏳ جاري المعالجة...', 'busy');
    try {
        const r = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user_id: uid, message: m})
        });
        const d = await r.json();
        add(d.reply, 'bot');
        lastBotMsg = d.reply;
        setStatus('✅ جاهز');
    } catch(e) {
        add('❌ خطأ: ' + e, 'bot');
        setStatus('❌ خطأ', 'error');
    }
    btn.disabled = false;
    inp.focus();
}

function add(text, cls) {
    const d = document.createElement('div');
    d.className = 'msg ' + cls;
    d.innerHTML = '<div class="msg-actions"><button class="msg-action" onclick="copyMsg(this)" title="نسخ">📋</button></div>' + text;
    chat.appendChild(d);
    chat.scrollTop = chat.scrollHeight;
}

function copyMsg(btnEl) {
    const msg = btnEl.parentElement.parentElement;
    const text = msg.textContent.replace('📋', '').trim();
    navigator.clipboard.writeText(text).then(() => toast('✅ تم النسخ'));
}

function copyLast() {
    if(!lastBotMsg) { toast('❌ ما فيه رد'); return; }
    navigator.clipboard.writeText(lastBotMsg).then(() => toast('✅ تم النسخ'));
    closeTools();
}

function downloadChat() {
    const msgs = document.querySelectorAll('.msg');
    let text = '📱 M7MAD_FF AI - المحادثة\\n';
    text += '='.repeat(40) + '\\n';
    text += '📅 التاريخ: ' + new Date().toLocaleString('ar-EG') + '\\n';
    text += '👤 المستخدم: {{ username }}\\n';
    text += '='.repeat(40) + '\\n\\n';
    msgs.forEach(m => {
        const sender = m.classList.contains('user') ? '👤 أنت' : '🤖 AI';
        const content = m.textContent.replace('📋', '').trim();
        text += sender + ':\\n' + content + '\\n\\n';
    });
    const blob = new Blob([text], {type: 'text/plain;charset=utf-8'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'm7mad_chat_' + Date.now() + '.txt';
    a.click();
    toast('✅ تم التحميل');
}

function clearChat() {
    if(!confirm('متأكد من تفريغ الشات؟')) return;
    chat.innerHTML = '<div class="msg bot"><b>تم التفريغ! 🧹</b><br>ابدأ محادثة جديدة</div>';
    toast('✅ تم التفريغ');
    closeTools();
}

async function resetMemory() {
    try {
        await fetch('/api/reset', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user_id: uid})
        });
        add('🗑️ تم مسح الذاكرة!', 'bot');
        toast('✅ تم المسح');
    } catch(e) { toast('❌ فشل المسح'); }
    closeTools();
}

async function deleteSession() {
    if(!confirm('متأكد من حذف الجلسة؟')) return;
    try {
        await fetch('/api/delete-session', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user_id: uid})
        });
        add('❌ تم حذف الجلسة!', 'bot');
        toast('✅ تم الحذف');
    } catch(e) { toast('❌ فشل الحذف'); }
    closeTools();
}

document.addEventListener('click', e => {
    const panel = document.getElementById('toolsPanel');
    const toggle = document.getElementById('toolsToggle');
    if(panel && !panel.contains(e.target) && !toggle.contains(e.target)) {
        closeTools();
    }
});
</script>
</body></html>
"""


# ============================================================
# API VIEWER DATA
# ============================================================
API_ENDPOINTS = [
    {
        "category": "💬 المحادثة",
        "items": [
            {"method": "POST", "path": "/chat", "desc": "إرسال رسالة JSON",
             "body": '{"user_id":"123456","message":"مرحبا"}'},
            {"method": "POST", "path": "/chat/form", "desc": "إرسال رسالة Form Data",
             "body": "user_id=123456&message=مرحبا"},
            {"method": "GET", "path": "/ask?question=مرحبا", "desc": "سؤال مباشر (JSON)", "body": None},
            {"method": "GET", "path": "/ask/text?question=مرحبا", "desc": "سؤال مباشر (نص)", "body": None},
        ]
    },
    {
        "category": "🆕 الجلسات",
        "items": [
            {"method": "POST", "path": "/session", "desc": "إنشاء جلسة جديدة",
             "body": '{"user_id":"123456"}'},
            {"method": "POST", "path": "/reset", "desc": "مسح ذاكرة الجلسة",
             "body": '{"user_id":"123456"}'},
            {"method": "GET", "path": "/session/123456", "desc": "معلومات الجلسة", "body": None},
            {"method": "DELETE", "path": "/session/123456", "desc": "حذف الجلسة", "body": None},
        ]
    },
    {
        "category": "⚙️ النظام",
        "items": [
            {"method": "GET", "path": "/health", "desc": "فحص الخدمة", "body": None},
            {"method": "GET", "path": "/api", "desc": "معلومات الـ API", "body": None},
            {"method": "GET", "path": "/version", "desc": "إصدار الـ API", "body": None},
            {"method": "GET", "path": "/docs", "desc": "Swagger UI (تفاعلي)", "body": None},
            {"method": "GET", "path": "/redoc", "desc": "ReDoc (قراءة)", "body": None},
        ]
    }
]


# ============================================================
# Routes
# ============================================================
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template_string(CHAT_HTML, username=session['username'])


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            return render_template_string(LOGIN_HTML, error="أدخل البيانات كاملة")
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('home'))
        else:
            users[username] = {"password": password, "name": username, "role": "user"}
            session['username'] = username
            session['role'] = 'user'
            return redirect(url_for('home'))
    return render_template_string(LOGIN_HTML, error=None)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


# ============================================================
# Chat
# ============================================================
@app.route('/chat', methods=['POST'])
def chat():
    if 'username' not in session:
        return jsonify({'reply': '❌ لازم تسجل دخول'}), 401
    data = request.json
    user_id = data.get('user_id', 'default')
    message = data.get('message', '')
    
    cmd = handle_command(user_id, message)
    if cmd:
        return jsonify({'reply': cmd})
    
    result = api_chat(user_id, message)
    reply = result.get('response') or result.get('reply') or result.get('error') or "ما فهمت 🤔"
    return jsonify({'reply': reply})


def handle_command(user_id, message):
    msg = message.lower().strip()
    
    if any(w in msg for w in ["معلومات api", "api info"]):
        r = api_info()
        return f"📚 <b>معلومات الـ API:</b><br><pre style='white-space:pre-wrap;font-size:11px;background:#0a0a0a;padding:10px;border-radius:8px'>{str(r)[:500]}</pre>"
    
    if any(w in msg for w in ["فحص", "health"]):
        r = api_health()
        return f"✅ <b>فحص الخدمة:</b><br>📊 <code>{r}</code>"
    
    if "إصدار" in msg or "version" in msg:
        r = api_version()
        return f"📌 <b>الإصدار:</b><br><code>{r}</code>"
    
    return None


# ============================================================
# Proxy APIs
# ============================================================
@app.route('/api/chat-json', methods=['POST'])
def proxy_chat_json():
    return jsonify(api_chat(request.json.get('user_id'), request.json.get('message')))


@app.route('/api/chat-form', methods=['POST'])
def proxy_chat_form():
    return jsonify(api_chat_form(request.form.get('user_id'), request.form.get('message')))


@app.route('/api/ask', methods=['GET'])
def proxy_ask():
    return jsonify(api_ask(request.args.get('question', '')))


@app.route('/api/ask-text', methods=['GET'])
def proxy_ask_text():
    return Response(api_ask_text(request.args.get('question', '')), mimetype='text/plain')


@app.route('/api/create-session', methods=['POST'])
def proxy_create_session():
    return jsonify(api_create_session(request.json.get('user_id')))


@app.route('/api/reset', methods=['POST'])
def proxy_reset():
    return jsonify(api_reset(request.json.get('user_id')))


@app.route('/api/session-info/<user_id>', methods=['GET'])
def proxy_session_info(user_id):
    return jsonify(api_session_info(user_id))


@app.route('/api/delete-session', methods=['POST'])
def proxy_delete_session():
    return jsonify(api_delete_session(request.json.get('user_id')))


@app.route('/api/health')
def proxy_health():
    return jsonify(api_health())


@app.route('/api/info')
def proxy_info():
    return jsonify(api_info())


@app.route('/api/version')
def proxy_version():
    return jsonify(api_version())


# ============================================================
# API Viewer - يعرض كل الـ Endpoints
# ============================================================
@app.route('/api-viewer')
def api_viewer():
    html = """<!DOCTYPE html><html dir="rtl" lang="ar"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>API Viewer - M7MAD_FF AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,sans-serif;background:#0a0a0a;
    background-image:radial-gradient(circle at 20% 50%,rgba(255,0,64,0.08) 0%,transparent 50%),
                      radial-gradient(circle at 80% 80%,rgba(255,23,68,0.06) 0%,transparent 50%);
    color:#fff;padding:20px;min-height:100vh}
.container{max-width:900px;margin:0 auto}
h1{color:#ff5252;text-align:center;margin-bottom:10px;font-size:26px}
.subtitle{text-align:center;color:rgba(255,255,255,0.5);margin-bottom:30px;font-size:13px}
.base-url{background:linear-gradient(145deg,#1a1a1a,#0f0f0f);border:1px solid rgba(255,0,64,0.3);
    border-radius:15px;padding:15px 20px;margin-bottom:25px;display:flex;align-items:center;
    justify-content:space-between;flex-wrap:wrap;gap:10px}
.base-url code{color:#ff5252;font-weight:bold;font-size:13px;word-break:break-all}
.base-url button{background:linear-gradient(135deg,#ff0040,#d50000);color:white;border:none;
    padding:8px 16px;border-radius:10px;cursor:pointer;font-weight:bold;font-size:12px;transition:all 0.3s}
.base-url button:hover{transform:translateY(-2px);box-shadow:0 5px 15px rgba(255,0,64,0.4)}
.category{margin-bottom:30px}
.category-title{color:#ff5252;font-size:18px;font-weight:bold;margin-bottom:15px;
    padding-bottom:8px;border-bottom:2px solid rgba(255,0,64,0.2)}
.endpoint{background:linear-gradient(145deg,#1a1a1a,#0f0f0f);border:1px solid rgba(255,0,64,0.2);
    border-radius:15px;padding:15px;margin-bottom:12px;transition:all 0.3s}
.endpoint:hover{border-color:rgba(255,0,64,0.5);transform:translateX(-3px)}
.ep-header{display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap}
.method{padding:4px 12px;border-radius:8px;font-weight:bold;font-size:11px;letter-spacing:1px}
.get{background:#4caf50;color:white}
.post{background:#2196f3;color:white}
.delete{background:#f44336;color:white}
.path{font-family:monospace;color:#ff5252;font-weight:bold;font-size:13px;
    background:rgba(255,0,64,0.1);padding:4px 10px;border-radius:8px;word-break:break-all}
.desc{color:rgba(255,255,255,0.7);font-size:13px;margin-bottom:8px}
.body-box{background:#0a0a0a;border:1px solid #2a2a2a;border-radius:10px;padding:10px;
    font-family:monospace;font-size:12px;color:#e0e0e0;overflow-x:auto;margin-top:8px;
    position:relative;padding-left:70px}
.body-box code{color:#4caf50}
.copy-btn{position:absolute;top:8px;left:8px;background:rgba(255,0,64,0.2);border:none;
    color:#ff5252;padding:4px 10px;border-radius:6px;cursor:pointer;font-size:10px;transition:all 0.3s}
.copy-btn:hover{background:#ff0040;color:white}
.test-btn{background:linear-gradient(135deg,#ff0040,#d50000);color:white;border:none;
    padding:8px 16px;border-radius:10px;cursor:pointer;font-weight:bold;font-size:12px;
    margin-top:10px;transition:all 0.3s}
.test-btn:hover{transform:translateY(-2px);box-shadow:0 5px 15px rgba(255,0,64,0.4)}
.test-btn:disabled{opacity:0.5;cursor:not-allowed}
.response{background:#0a0a0a;border:1px solid #2a2a2a;border-radius:10px;padding:12px;
    font-family:monospace;font-size:12px;color:#4caf50;overflow-x:auto;margin-top:10px;
    white-space:pre-wrap;display:none;max-height:300px;overflow-y:auto}
.response.show{display:block}
.back-btn{display:inline-block;margin-bottom:20px;color:#ff5252;text-decoration:none;
    font-size:14px;padding:8px 16px;background:rgba(255,0,64,0.1);border-radius:10px;
    border:1px solid rgba(255,0,64,0.3);transition:all 0.3s}
.back-btn:hover{background:rgba(255,0,64,0.2)}
@media (max-width:600px){
    h1{font-size:20px}
    .path{font-size:11px}
    .body-box{font-size:11px;padding-left:60px}
}
</style></head><body>
<div class="container">
<a href="/" class="back-btn">← رجوع للتطبيق</a>
<h1>🔴 M7MAD_FF AI - API Viewer</h1>
<p class="subtitle">كل الـ Endpoints المتاحة — مع إمكانية التجربة</p>

<div class="base-url">
<code>📍 Base URL: http://51.75.118.171:20085</code>
<button onclick="copyBase()">📋 نسخ</button>
</div>
"""

    for idx, cat in enumerate(API_ENDPOINTS):
        html += f'<div class="category"><div class="category-title">{cat["category"]}</div>'
        for j, ep in enumerate(cat["items"]):
            method_lower = ep["method"].lower()
            body_html = ""
            if ep["body"]:
                body_html = f'''
                <div class="body-box">
                    <button class="copy-btn" onclick="copyBody(this)">📋</button>
                    <code>{ep["body"]}</code>
                </div>'''
            
            test_url = f'http://51.75.118.171:20085{ep["path"]}'
            resp_id = f'resp-{idx}-{j}'
            body_escaped = (ep["body"] or "").replace("'", "\\'").replace('"', '&quot;')
            
            html += f'''
            <div class="endpoint">
                <div class="ep-header">
                    <span class="method {method_lower}">{ep["method"]}</span>
                    <span class="path">{ep["path"]}</span>
                </div>
                <div class="desc">{ep["desc"]}</div>
                {body_html}
                <button class="test-btn" onclick="testEndpoint('{ep["method"]}', '{test_url}', this)">🧪 جرب</button>
                <div class="response" id="{resp_id}"></div>
            </div>'''
        html += '</div>'

    html += """
</div>
<script>
function copyBase() {
    navigator.clipboard.writeText('http://51.75.118.171:20085');
    showToast('✅ تم النسخ');
}
function copyBody(btn) {
    const code = btn.nextElementSibling.textContent;
    navigator.clipboard.writeText(code);
    showToast('✅ تم النسخ');
}
function showToast(msg) {
    const t = document.createElement('div');
    t.textContent = msg;
    t.style.cssText = 'position:fixed;bottom:20px;right:50%;transform:translateX(50%);background:linear-gradient(135deg,#ff0040,#d50000);color:white;padding:12px 24px;border-radius:25px;font-weight:bold;z-index:9999;box-shadow:0 8px 30px rgba(255,0,64,0.5)';
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 2000);
}
async function testEndpoint(method, url, btn) {
    const respEl = btn.nextElementSibling;
    respEl.classList.add('show');
    respEl.textContent = '⏳ جاري التنفيذ...';
    btn.disabled = true;
    
    try {
        const opts = {method: method};
        
        // لو POST أو PUT، لازم body
        if (method === 'POST' || method === 'PUT') {
            // جرب نلاقي body
            const bodyBox = btn.parentElement.querySelector('.body-box code');
            if (bodyBox) {
                const body = bodyBox.textContent.trim();
                if (body.startsWith('{')) {
                    opts.headers = {'Content-Type': 'application/json'};
                    opts.body = body;
                } else {
                    opts.headers = {'Content-Type': 'application/x-www-form-urlencoded'};
                    opts.body = body;
                }
            }
        }
        
        const r = await fetch(url, opts);
        const text = await r.text();
        let formatted = text;
        try { formatted = JSON.stringify(JSON.parse(text), null, 2); } catch(e) {}
        respEl.textContent = '✅ الرد (HTTP ' + r.status + '):\\n' + formatted;
    } catch(e) {
        respEl.textContent = '❌ خطأ: ' + e.message;
    }
    btn.disabled = false;
}
</script>
</body></html>"""
    return html


if __name__ == "__main__":
    print("="*55)
    print("🤖 M7MAD_FF AI v4.0")
    print("="*55)
    print(f"🌐 http://localhost:8000")
    print(f"🌐 API Viewer: http://localhost:8000/api-viewer")
    print("="*55)
    app.run(host='0.0.0.0', port=8000, debug=False)