/* Audit journey: charts, models, tabs, stage nav, questions. Plain JS + the casebook kit (window.K). */
(function(){
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const inr=v=>'₹'+Math.round(v).toLocaleString('en-IN');
const L=v=>v>=1e5?'₹'+(v/1e5).toFixed(2)+' L':inr(v);
const NS='http://www.w3.org/2000/svg';
function el(t,a,txt){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;return e;}
function svgIn(id,W,H,label){const h=document.getElementById(id);if(!h)return null;const s=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':label||''});h.appendChild(s);return s;}
let tip;function showTip(html,x,y){if(!tip){tip=document.createElement('div');tip.className='tip';document.body.appendChild(tip);}tip.innerHTML=html;tip.hidden=false;tip.style.left=Math.min(x+14,innerWidth-275)+'px';tip.style.top=(y+16)+'px';}
function hideTip(){if(tip)tip.hidden=true;}
function bind(node,html){node.setAttribute('tabindex','0');node.addEventListener('mousemove',e=>showTip(html,e.clientX,e.clientY));node.addEventListener('mouseleave',hideTip);node.addEventListener('focus',()=>{const r=node.getBoundingClientRect();showTip(html,r.left,r.top);});node.addEventListener('blur',hideTip);}
const J=window.J||{};
const time=v=>{const h=Math.floor(v),m=Math.round((v-h)*60);return (h>12?h-12:h)+(m?':'+String(m).padStart(2,'0'):'')+' pm';};

function charts(){
  $$('.chart').forEach(c=>c.innerHTML='');
  if(window.K){
    K.hbar('c-reviews',{rows:J.reviews,vfmt:v=>v.toLocaleString('en-IN'),labelW:190,rowH:24,aria:'Google review counts for 18 salons'});
    K.hbar('c-hours',{rows:J.hours,vfmt:time,labelW:210,rowH:26,max:22,aria:'Closing time per salon'});
    K.hbar('c-score',{rows:J.score.map(r=>({label:r.label,value:r.value,color:r.value>=4?'flow':r.value<=1?'leak':r.value<=2?'est':'move'})),vfmt:v=>v+' / 5',max:5,labelW:170,aria:'Scorecard'});
    K.hbar('c-shap',{rows:[{label:'Return rate 35% → 50%',value:30.9,color:'move'},{label:'Visits a year 6 → 8',value:29.2,color:'move'},{label:'New clients 60 → 75',value:27.1,color:'flow'},{label:'Average bill ₹1,800 → ₹2,000',value:12.9,color:'est'}],vfmt:v=>v.toFixed(0)+'% of uplift',labelW:210,aria:'Share of revenue uplift by lever'});
  }
  matrix();retention();gantt();
}
function matrix(){
  const h=document.getElementById('c-matrix');if(!h)return;const W=Math.max(320,Math.min(620,h.clientWidth||620)),H=Math.round(W*0.72),P=38;
  const s=svgIn('c-matrix',W,H,'Impact versus effort for 14 actions');const x=v=>P+(W-P-12)*(v-0.5)/5,y=v=>H-P-(H-P-12)*(v-0.5)/5;
  const mx=x(2.5),my=y(3.5);
  s.append(el('rect',{x:P,y:12,width:mx-P,height:my-12,class:'q-win'}));
  [['Quick wins',P+8,28],['Big projects',mx+8,28],['Fill-ins',P+8,H-P-8],['Later',mx+8,H-P-8]].forEach(([t,a,b])=>s.append(el('text',{x:a,y:b,class:'qlab'},t)));
  s.append(el('line',{x1:mx,x2:mx,y1:12,y2:H-P,class:'grid'}));s.append(el('line',{x1:P,x2:W-12,y1:my,y2:my,class:'grid'}));
  s.append(el('line',{x1:P,x2:W-12,y1:H-P,y2:H-P,class:'base'}));s.append(el('line',{x1:P,x2:P,y1:12,y2:H-P,class:'base'}));
  s.append(el('text',{x:W-12,y:H-12,'text-anchor':'end',class:'ax'},'Effort →'));
  const t=el('text',{x:14,y:my,class:'ax',transform:`rotate(-90 14 ${my})`,'text-anchor':'middle'},'Impact →');s.append(t);
  const phc=['','flow','move','est'];
  (J.acts||[]).forEach(a=>{const g=el('g',{class:'dot'});const cx=x(a.f),cy=y(a.i);
    g.append(el('circle',{cx,cy,r:13,style:`fill:var(--${phc[a.p]})`}));g.append(el('text',{x:cx,y:cy+4,'text-anchor':'middle',class:'dn'},a.n));
    bind(g,`<div><b>${a.n}. ${a.t}</b></div><div>Phase ${a.p} · ${a.pr}</div>`);s.append(g);});
}
function retention(){
  const h=document.getElementById('c-ret');if(!h||!J.ret)return;const W=Math.max(320,Math.min(1100,h.clientWidth||900)),L=Math.min(220,W*.38),R=16,rowH=34,T=10,H=T+rowH*J.ret.length+30;
  const s=svgIn('c-ret',W,H,'Return windows by service in weeks');const x=v=>L+(W-L-R)*v/24;
  for(let w=0;w<=24;w+=4){s.append(el('line',{x1:x(w),x2:x(w),y1:T,y2:H-26,class:'grid'}));s.append(el('text',{x:x(w),y:H-8,'text-anchor':'middle',class:'ax'},w+'w'));}
  J.ret.forEach((r,i)=>{const y0=T+i*rowH;const g=el('g',{});
    g.append(el('text',{x:L-10,y:y0+rowH/2+4,'text-anchor':'end',class:'lbl2'},r.label));
    g.append(el('rect',{x:x(r.a),y:y0+9,width:Math.max(4,x(r.b)-x(r.a)),height:rowH-18,rx:3,style:'fill:var(--move)'}));
    g.append(el('text',{x:x(r.b)+8,y:y0+rowH/2+4,class:'val'},r.a+'–'+r.b+' weeks'));
    bind(g,`<div>${r.label}</div><div><b>Reminder at ${r.a}–${r.b} weeks</b></div>`);s.append(g);});
}
function gantt(){
  const h=document.getElementById('c-gantt');if(!h||!J.acts)return;const hw=h.clientWidth||1000,nar=hw<640;
  const W=Math.max(320,Math.min(1160,hw)),L=nar?4:Math.min(300,W*.42),R=6,rowH=nar?42:26,T=26,H=T+rowH*J.acts.length+6;
  const s=svgIn('c-gantt',W,H,'90-day plan');const x=w=>L+(W-L-R)*w/12;
  [['Weeks 1–4',0],['5–8',4],['9–12',8]].forEach(([t,w],i)=>{s.append(el('rect',{x:x(w),y:0,width:x(4)-x(0),height:H,class:i%2?'band2':'band1'}));s.append(el('text',{x:x(w)+6,y:16,class:'ax'},t));});
  const ph={1:[0,4],2:[4,8],3:[8,12]},col={1:'flow',2:'move',3:'est'};
  J.acts.forEach((a,i)=>{const y0=T+i*rowH;const g=el('g',{});const [s0,e0]=ph[a.p];const by=nar?y0+20:y0+6,bh=nar?16:rowH-12;
    if(nar)g.append(el('text',{x:s0>=8?x(12)-4:x(s0)+4,y:y0+14,'text-anchor':s0>=8?'end':'start',class:'lbl2'},a.n+'. '+a.t));
    else g.append(el('text',{x:L-10,y:y0+rowH/2+4,'text-anchor':'end',class:'lbl2'},a.n+'. '+a.t));
    g.append(el('rect',{x:x(s0)+3,y:by,width:x(e0)-x(s0)-6,height:bh,rx:3,style:`fill:var(--${col[a.p]});opacity:${a.pr==='P1'?1:.55}`}));
    g.append(el('text',{x:x(s0)+10,y:by+bh/2+4,class:'gl'},a.pr));
    bind(g,`<div><b>${a.n}. ${a.t}</b></div><div>Weeks ${s0+1}–${e0} · ${a.pr}</div>`);s.append(g);});
}
/* budget explorer */
function budget(){const B=+$('#bb').value,c=+$('#bc').value,r=+$('#br').value/100,v=+$('#bv').value,k=+$('#bk').value/100;
  $('#bbO').textContent=inr(B);$('#bcO').textContent=inr(c);$('#brO').textContent=Math.round(r*100)+'%';$('#bvO').textContent=inr(v);$('#bkO').textContent=Math.round(k*100)+'%';
  const enq=B/c,bk=enq*r,cpb=bk?B/bk:0,first=bk*v,yr=bk*(1-k)*v+bk*k*6*v;
  $('#bOut').innerHTML=`<div class="fun">${[['Spend',inr(B),100],['Enquiries',Math.round(enq),70],['Bookings',Math.round(bk),45],['First-visit revenue',L(first),30]].map(([a,b,w])=>`<div style="--w:${w}%"><span>${a}</span><b>${b}</b></div>`).join('')}</div>
  <div class="kpis"><div><small>Cost per booking</small><b>${inr(cpb)}</b></div><div><small>First-visit revenue per ₹1</small><b>${(first/B).toFixed(2)}×</b></div><div><small>12-month value of these clients*</small><b class="flow">${L(yr)}</b></div></div>
  <p class="cap">*Returners assumed at 6 visits a year. ${first<B?'<b class="leak">First visits alone don\'t pay back this spend.</b> Retention is what makes paid media profitable for a salon.':'First visits pay back the spend before any return visit.'}</p>`;}
['bb','bc','br','bv','bk'].forEach(id=>{const i=document.getElementById(id);if(i)i.addEventListener('input',budget);});

/* revenue model */
const SH={n:27.1,r:30.9,v:29.2,b:12.9};
function rev(){const n=+$('#m1').value,r=+$('#m2').value/100,v=+$('#m3').value,b=+$('#m4').value;
  $('#m1O').textContent=n;$('#m2O').textContent=Math.round(r*100)+'%';$('#m3O').textContent=v;$('#m4O').textContent=inr(b);
  const val=(n*r*v+n*(1-r))*b,base=(60*.35*6+60*.65)*1800;
  $('#mOut').innerHTML=`<div class="eq"><span><small>New</small>${n}</span>×<span><small>Return</small>${Math.round(r*100)}%</span>×<span><small>Visits</small>${v}</span>×<span><small>Bill</small>${inr(b)}</span></div>
  <div class="kpis"><div><small>Yearly value of one month's new clients</small><b class="flow">${L(val)}</b></div><div><small>vs today (assumed ₹2.97 L)</small><b>${(val/base).toFixed(1)}×</b></div><div><small>Visits from one month's clients</small><b>${Math.round(n*r*v+n*(1-r))}</b></div></div>
  <p class="cap">Formula: (new × return rate × visits a year + new who don't return) × average bill. Illustrative inputs only.</p>`;}
['m1','m2','m3','m4'].forEach(id=>{const i=document.getElementById(id);if(i)i.addEventListener('input',rev);});
$$('[data-rv]').forEach(b=>b.addEventListener('click',()=>{const p=b.dataset.rv==='after'?[75,50,8,2000]:[60,35,6,1800];['m1','m2','m3','m4'].forEach((id,i)=>$('#'+id).value=p[i]);rev();}));

/* marketing share */
function attr(){const R=+$('#aR').value,V=+$('#aV').value,Bv=+$('#aB').value;$('#aRo').textContent=R+'%';$('#aVo').textContent=V+'%';$('#aBo').textContent=Bv+'%';
  const m=SH.n+SH.r*R/100+SH.v*V/100+SH.b*Bv/100,o=100-m;
  $('#aOut').innerHTML=`<div class="big2"><b class="flow">${Math.round(m)}%</b><span>of the modelled growth is marketing's at these settings</span></div>
  <div class="stackbar" role="img" aria-label="Marketing ${Math.round(m)} percent, salon floor ${Math.round(o)} percent"><i class="mk" style="width:${m}%"><span>Marketing ${Math.round(m)}%</span></i><i class="op" style="width:${o}%"><span>Salon floor ${Math.round(o)}%</span></i></div>
  <ul class="legend3"><li><b>New clients</b> ${SH.n}% · all marketing</li><li><b>Return rate</b> ${SH.r}% · ${R}% marketing (reminders, win-back)</li><li><b>Visits a year</b> ${SH.v}% · ${V}% marketing (reminders vs membership terms)</li><li><b>Average bill</b> ${SH.b}% · ${Bv}% marketing (offers vs chair consultation)</li></ul>
  <p class="cap">Cautious → about 45%. Generous → about 75%. The rest needs the salon floor.</p>`;}
['aR','aV','aB'].forEach(id=>{const i=document.getElementById(id);if(i)i.addEventListener('input',attr);});
$$('[data-pre]').forEach(b=>b.addEventListener('click',()=>{const p={low:[40,30,0],mid:[60,50,20],high:[85,80,40]}[b.dataset.pre];['aR','aV','aB'].forEach((id,i)=>$('#'+id).value=p[i]);attr();}));

/* tabs */
$$('[data-tabs]').forEach(box=>{const ts=[...box.querySelectorAll('[role=tab]')],ps=[...box.querySelectorAll('[data-p]')];
  const show=t=>{ts.forEach(x=>{x.setAttribute('aria-selected',x===t);x.tabIndex=x===t?0:-1;});ps.forEach(p=>p.hidden=p.dataset.p!==t.dataset.t);};
  ts.forEach((t,i)=>{t.addEventListener('click',()=>show(t));t.addEventListener('keydown',e=>{const d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(!d)return;e.preventDefault();const n=ts[(i+d+ts.length)%ts.length];n.focus();show(n);});});});

/* stage nav */
const links=$$('.j-nav a');const map=new Map(links.map(a=>[a.getAttribute('href').slice(1),a]));
if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;links.forEach(l=>l.removeAttribute('aria-current'));const a=map.get(e.target.id);if(a){a.setAttribute('aria-current','true');const sn=a.parentElement;sn.scrollTo({left:a.offsetLeft-sn.clientWidth/2+a.offsetWidth/2,behavior:'smooth'});}}),{rootMargin:'-40% 0px -55% 0px'});map.forEach((a,id)=>{const s=document.getElementById(id);if(s)io.observe(s);});}

/* questions */
const qs=$('.j-qs'),items=$$('.j-q'),bs=$$('.j-qf button');let g='all';
function q(){const t=(qs.value||'').trim().toLowerCase();let n=0;items.forEach(it=>{const ok=(g==='all'||it.dataset.g===g)&&(!t||it.textContent.toLowerCase().includes(t));it.hidden=!ok;if(ok)n++;});$('#qn').textContent=n;$('.j-qe').hidden=n>0;}
if(qs){qs.addEventListener('input',q);bs.forEach(b=>b.addEventListener('click',()=>{g=b.dataset.f;bs.forEach(x=>x.setAttribute('aria-pressed',x===b));q();}));}

budget();rev();attr();charts();
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(charts,200);});
})();
