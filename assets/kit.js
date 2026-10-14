/* Casebook chart + component kit. Plain SVG, theme tokens only. */
(function(){
const NS='http://www.w3.org/2000/svg';
const C={flow:'var(--flow)',leak:'var(--leak)',move:'var(--move)',ink:'var(--ink-2)',mute:'var(--mute)',muted:'var(--ink-3)',est:'var(--est)'};
const col=c=>C[c]||c||C.flow;
function el(t,a,txt){const e=document.createElementNS(NS,t);for(const k in a){if(k==='style')e.setAttribute('style',a[k]);else e.setAttribute(k,a[k]);}if(txt!=null)e.textContent=txt;return e;}
let tip;
function showTip(html,ev){if(!tip){tip=document.createElement('div');tip.className='tip';tip.hidden=true;document.body.appendChild(tip);}tip.innerHTML=html;tip.hidden=false;const x=Math.min(ev.clientX+14,innerWidth-275),y=ev.clientY+16;tip.style.left=x+'px';tip.style.top=y+'px';}
function hideTip(){if(tip)tip.hidden=true;}
function bindTip(node,html){node.addEventListener('mousemove',e=>showTip(html,e));node.addEventListener('mouseleave',hideTip);node.addEventListener('focus',e=>{const r=node.getBoundingClientRect();showTip(html,{clientX:r.left+r.width/2,clientY:r.top});});node.addEventListener('blur',hideTip);node.setAttribute('tabindex','0');}
function niceMax(v){if(v<=0)return 1;const p=Math.pow(10,Math.floor(Math.log10(v)));const n=v/p;const m=n<=1?1:n<=2?2:n<=2.5?2.5:n<=5?5:10;return m*p;}
function niceStep(v){const p=Math.pow(10,Math.floor(Math.log10(v)));const n=v/p;return (n<=1?1:n<=2?2:n<=2.5?2.5:n<=5?5:10)*p;}
function scale(max,min){min=min||0;const st=niceStep((max-min)/4);return {min:Math.floor(min/st)*st,max:Math.ceil(max/st)*st,step:st};}
function tickList(sc){const o=[];for(let v=sc.min;v<=sc.max+1e-9;v+=sc.step)o.push(+v.toFixed(6));return o;}
const K={};
function fitW(host,o){const a=host.clientWidth||o.W||760;return Math.round(Math.max(320,Math.min(o.W||760,a)));}
const narrow=W=>W<520;

/* Line chart: one axis. opts {labels, series:[{name,values,color,dash}], yfmt, shade:[a,b], shadeLabel, height, ymax, mark:[{i,label}]} */
K.line=function(id,o){
  const host=document.getElementById(id);if(!host)return;
  const W=fitW(host,o),H=o.height||280,L=52,R=Math.min(o.right||64,W*0.14),T=18,B=34;
  const all=o.series.flatMap(s=>s.values.filter(v=>v!=null));
  const sc=scale(o.ymax||Math.max(...all)*1.04,o.ymin||0);const ymax=sc.max,ymin=sc.min;
  const n=o.labels.length;const x=i=>L+(W-L-R)*(n===1?0.5:i/(n-1));const y=v=>T+(H-T-B)*(1-(v-ymin)/(ymax-ymin));
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':o.aria||''});
  if(o.shade){const a=x(o.shade[0])-((W-L-R)/(n-1))/2,b=x(o.shade[1])+((W-L-R)/(n-1))/2;svg.append(el('rect',{x:Math.max(L,a),y:T,width:Math.min(W-R,b)-Math.max(L,a),height:H-T-B,class:'shade'}));if(o.shadeLabel)svg.append(el('text',{x:Math.max(L,a)+6,y:T+14,class:'ax',style:'fill:var(--flow)'},o.shadeLabel));}
  tickList(sc).forEach(v=>{svg.append(el('line',{x1:L,x2:W-R,y1:y(v),y2:y(v),class:'grid'}));svg.append(el('text',{x:L-8,y:y(v)+4,'text-anchor':'end',class:'ax'},o.yfmt?o.yfmt(v):v));});
  const step=Math.ceil(n/(o.xEvery?n/o.xEvery:10));
  const ev=(o.xEvery||step)*(narrow(W)?2:1);o.labels.forEach((t,i)=>{if((i%ev===0&&(n-1-i>=ev/2||i===n-1))||i===n-1)svg.append(el('text',{x:x(i),y:H-10,'text-anchor':'middle',class:'ax'},t));});
  o.series.forEach(s=>{
    let d='';s.values.forEach((v,i)=>{if(v==null)return;d+=(d?'L':'M')+x(i).toFixed(1)+','+y(v).toFixed(1);});
    svg.append(el('path',{d,fill:'none',style:`stroke:${col(s.color)}`,'stroke-width':2,'stroke-linejoin':'round','stroke-dasharray':s.dash||''}));
    const li=s.values.length-1;if(s.values[li]!=null){svg.append(el('circle',{cx:x(li),cy:y(s.values[li]),r:4.5,style:`fill:${col(s.color)};stroke:var(--surface)`,'stroke-width':2}));
      if(o.endLabels!==false)svg.append(el('text',{x:x(li)+8,y:y(s.values[li])+4,class:'val'},(o.yfmt?o.yfmt(s.values[li]):s.values[li])));}
  });
  (o.mark||[]).forEach(m=>{const s=o.series[m.s||0];const v=s.values[m.i];svg.append(el('circle',{cx:x(m.i),cy:y(v),r:4.5,style:`fill:var(--surface);stroke:${col(m.color||s.color)}`,'stroke-width':2}));svg.append(el('text',{x:x(m.i),y:y(v)+(m.below?18:-10),'text-anchor':'middle',class:'lbl2'},m.label));});
  // crosshair
  const cross=el('line',{x1:0,x2:0,y1:T,y2:H-B,style:'stroke:var(--ink-3)','stroke-dasharray':'3 3',visibility:'hidden'});svg.append(cross);
  const hit=el('rect',{x:L,y:T,width:W-L-R,height:H-T-B,class:'hit'});svg.append(hit);
  hit.addEventListener('mousemove',e=>{const r=svg.getBoundingClientRect();const px=(e.clientX-r.left)/r.width*W;let i=Math.round((px-L)/((W-L-R)/(n-1)));i=Math.max(0,Math.min(n-1,i));cross.setAttribute('x1',x(i));cross.setAttribute('x2',x(i));cross.setAttribute('visibility','visible');
    showTip('<div>'+o.labels[i]+'</div>'+o.series.map(s=>s.values[i]==null?'':`<div>${s.name}: <b>${o.yfmt?o.yfmt(s.values[i]):s.values[i]}</b></div>`).join(''),e);});
  hit.addEventListener('mouseleave',()=>{cross.setAttribute('visibility','hidden');hideTip();});
  host.appendChild(svg);
};

/* Vertical bars. opts {labels, values, colors(array or fn), yfmt, vfmt, height, labelEvery, notes} */
K.bars=function(id,o){
  const host=document.getElementById(id);if(!host)return;
  const W=fitW(host,o),H=o.height||280,L=52,R=12,T=22,B=34;const n=o.values.length;
  const sc=scale(o.ymax||Math.max(...o.values)*1.06);const ymax=sc.max;
  const bw=(W-L-R)/n;const y=v=>T+(H-T-B)*(1-v/ymax);
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':o.aria||''});
  if(o.shade){svg.append(el('rect',{x:L+bw*o.shade[0],y:T-8,width:bw*(o.shade[1]-o.shade[0]+1),height:H-T-B+8,class:'shade'}));if(o.shadeLabel)svg.append(el('text',{x:L+bw*o.shade[0]+6,y:T+4,class:'ax',style:'fill:var(--flow)'},o.shadeLabel));}
  tickList(sc).forEach(v=>{svg.append(el('line',{x1:L,x2:W-R,y1:y(v),y2:y(v),class:'grid'}));svg.append(el('text',{x:L-8,y:y(v)+4,'text-anchor':'end',class:'ax'},o.yfmt?o.yfmt(v):v));});
  o.values.forEach((v,i)=>{
    const c=typeof o.colors==='function'?o.colors(i,v):(o.colors?o.colors[i]:'flow');
    const g=el('g',{});const bx=L+bw*i+bw*0.18,w=bw*0.64,top=y(v),h=Math.max(1,y(0)-top);
    const r=Math.min(4,w/2,h);
    g.append(el('path',{d:`M${bx},${y(0)}V${top+r}Q${bx},${top} ${bx+r},${top}H${bx+w-r}Q${bx+w},${top} ${bx+w},${top+r}V${y(0)}Z`,style:`fill:${col(c)}`}));
    if(o.showVals&&o.showVals(i)&&!(narrow(W)&&n>8))g.append(el('text',{x:bx+w/2,y:top-6,'text-anchor':'middle',class:'val'},o.vfmt?o.vfmt(v):v));
    const le=(o.labelEvery||1)*(narrow(W)&&n>8?2:1);if((i%le===0&&n-1-i>=le/2)||i===n-1)svg.append(el('text',{x:bx+w/2,y:H-10,'text-anchor':'middle',class:'ax'},o.labels[i]));
    g.append(el('rect',{x:L+bw*i,y:T,width:bw,height:H-T-B,class:'hit'}));
    bindTip(g,`<div>${o.labels[i]}</div><div><b>${o.vfmt?o.vfmt(v):v}</b>${o.notes&&o.notes[i]?' · '+o.notes[i]:''}</div>`);
    svg.append(g);
  });
  svg.append(el('line',{x1:L,x2:W-R,y1:y(0),y2:y(0),class:'base'}));
  host.appendChild(svg);
};

/* Paired bars (two periods). opts {labels, a:{name,values,color}, b:{...}, yfmt, vfmt} */
K.paired=function(id,o){
  const host=document.getElementById(id);if(!host)return;
  const W=fitW(host,o),H=o.height||280,L=52,R=12,T=24,B=34;const n=o.labels.length;
  const sc=scale(o.ymax||Math.max(...o.a.values,...o.b.values)*1.08);const ymax=sc.max;const y=v=>T+(H-T-B)*(1-v/ymax);
  const gw=(W-L-R)/n;const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':o.aria||''});
  tickList(sc).forEach(v=>{svg.append(el('line',{x1:L,x2:W-R,y1:y(v),y2:y(v),class:'grid'}));svg.append(el('text',{x:L-8,y:y(v)+4,'text-anchor':'end',class:'ax'},o.yfmt?o.yfmt(v):v));});
  o.labels.forEach((lab,i)=>{
    const g=el('g',{});const w=gw*0.3;[o.a,o.b].forEach((s,j)=>{const v=s.values[i];const bx=L+gw*i+gw*0.18+j*(w+2),top=y(v),r=Math.min(3,w/2);
      g.append(el('path',{d:`M${bx},${y(0)}V${top+r}Q${bx},${top} ${bx+r},${top}H${bx+w-r}Q${bx+w},${top} ${bx+w},${top+r}V${y(0)}Z`,style:`fill:${col(s.color)}`}));});
    if(o.delta){const d=(o.b.values[i]/o.a.values[i]-1)*100;g.append(el('text',{x:L+gw*i+gw/2,y:y(Math.max(o.a.values[i],o.b.values[i]))-7,'text-anchor':'middle',class:'val',style:d>=0?'fill:var(--flow)':'fill:var(--leak)'},(d>=0?'+':'')+d.toFixed(1)+'%'));}
    svg.append(el('text',{x:L+gw*i+gw/2,y:H-10,'text-anchor':'middle',class:'ax'},lab));
    g.append(el('rect',{x:L+gw*i,y:T,width:gw,height:H-T-B,class:'hit'}));
    bindTip(g,`<div>${lab}</div><div>${o.a.name}: <b>${o.vfmt?o.vfmt(o.a.values[i]):o.a.values[i]}</b></div><div>${o.b.name}: <b>${o.vfmt?o.vfmt(o.b.values[i]):o.b.values[i]}</b></div>`);
    svg.append(g);});
  svg.append(el('line',{x1:L,x2:W-R,y1:y(0),y2:y(0),class:'base'}));
  host.appendChild(svg);
};

/* Horizontal bars. opts {rows:[{label,value,color,note}], vfmt, max, labelW, marker:{value,label}} */
K.hbar=function(id,o){
  const host=document.getElementById(id);if(!host)return;
  const rowH=o.rowH||30,W=fitW(host,o),L=Math.min(o.labelW||200,W*0.42),R=Math.min(o.right||90,W*0.26),T=6;const H=T+rowH*o.rows.length+(o.marker?22:6);
  const max=o.max||Math.max(...o.rows.map(r=>r.value));const x=v=>L+(W-L-R)*v/max;
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':o.aria||''});
  if(o.marker){svg.append(el('line',{x1:x(o.marker.value),x2:x(o.marker.value),y1:T,y2:T+rowH*o.rows.length,style:'stroke:var(--ink-3)','stroke-dasharray':'4 3'}));svg.append(el('text',{x:x(o.marker.value),y:H-4,'text-anchor':'middle',class:'ax'},o.marker.label));}
  o.rows.forEach((r,i)=>{const g=el('g',{});const y0=T+i*rowH,bh=Math.min(16,rowH-10);
    g.append(el('text',{x:L-10,y:y0+rowH/2+4,'text-anchor':'end',class:r.bold?'lbl':'lbl2'},r.label));
    const w=Math.max(2,x(r.value)-L),rr=Math.min(3,w/2);const by=y0+(rowH-bh)/2;
    g.append(el('path',{d:`M${L},${by}H${L+w-rr}Q${L+w},${by} ${L+w},${by+rr}V${by+bh-rr}Q${L+w},${by+bh} ${L+w-rr},${by+bh}H${L}Z`,style:`fill:${col(r.color)}`}));
    g.append(el('text',{x:L+w+8,y:y0+rowH/2+4,class:'val'},r.text||(o.vfmt?o.vfmt(r.value):r.value)));
    g.append(el('rect',{x:0,y:y0,width:W,height:rowH,class:'hit'}));
    bindTip(g,`<div>${r.label}</div><div><b>${r.text||(o.vfmt?o.vfmt(r.value):r.value)}</b>${r.note?' · '+r.note:''}</div>`);
    svg.append(g);});
  svg.append(el('line',{x1:L,x2:L,y1:T,y2:T+rowH*o.rows.length,class:'base'}));
  host.appendChild(svg);
};

/* Split bar: share of spend vs share of results. opts {rows:[{label,a,b}], aName,bName} values in % */
K.split=function(id,o){
  const host=document.getElementById(id);if(!host)return;
  const W=fitW(host,o),rowH=46,L=Math.min(o.labelW||150,W*0.3),R=60,T=4;const H=T+rowH*o.rows.length;const x=v=>L+(W-L-R)*v/100;
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':o.aria||''});
  o.rows.forEach((r,i)=>{const g=el('g',{});const y0=T+i*rowH;
    g.append(el('text',{x:L-10,y:y0+24,'text-anchor':'end',class:'lbl'},r.label));
    [[r.a,o.aColor||'ink',0],[r.b,o.bColor||'flow',1]].forEach(([v,c,j])=>{const by=y0+6+j*17;const w=Math.max(2,x(v)-L);g.append(el('rect',{x:L,y:by,width:w,height:13,rx:2,style:`fill:${col(c)}`}));g.append(el('text',{x:L+w+6,y:by+11,class:'val'},v.toFixed(1)+'%'));});
    g.append(el('rect',{x:0,y:y0,width:W,height:rowH,class:'hit'}));
    bindTip(g,`<div>${r.label}</div><div>${o.aName}: <b>${r.a.toFixed(1)}%</b></div><div>${o.bName}: <b>${r.b.toFixed(1)}%</b></div>${r.note?'<div>'+r.note+'</div>':''}`);
    svg.append(g);});
  host.appendChild(svg);
};

/* copy buttons */
document.addEventListener('click',e=>{const b=e.target.closest('[data-copy]');if(!b)return;const txt=b.getAttribute('data-copy');const done=()=>{const o=b.textContent;b.textContent='Copied';setTimeout(()=>b.textContent=o,1300);};
  try{navigator.clipboard.writeText(txt).then(done,()=>sel(b));}catch(err){sel(b);} });
function sel(b){const t=b.previousElementSibling;if(!t)return;const r=document.createRange();r.selectNodeContents(t);const s=getSelection();s.removeAllRanges();s.addRange(r);}
K.fmt={cr:v=>'₹'+v.toFixed(2)+' Cr',L:v=>'₹'+v.toFixed(2)+' L',inr:v=>'₹'+Math.round(v).toLocaleString('en-IN'),n:v=>Math.round(v).toLocaleString('en-IN'),k:v=>v>=1000?(v/1000).toFixed(v>=10000?0:1)+'k':String(Math.round(v)),usd:v=>'$'+(Math.round(v*100)/100).toLocaleString('en-US'),pct:v=>v.toFixed(1)+'%'};
window.K=K;
})();

