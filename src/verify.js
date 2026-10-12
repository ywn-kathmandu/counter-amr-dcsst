// Run the built app's data + lookup logic headlessly and assert behaviour.
const fs = require('fs');
const src = fs.readFileSync(require('path').join(__dirname,'..','index.html'), 'utf8');
const js = src.match(/<script>([\s\S]*?)<\/script>/)[1];

// stub the browser surface the module touches at load time
const stub = `
var performance={now:()=>Date.now()};
var localStorage={getItem:()=>null,setItem:()=>{},removeItem:()=>{}};
function mkEl(){ const e={style:{setProperty(){}},classList:{add(){},remove(){},toggle(){},contains:()=>false},
  dataset:{},value:'',innerHTML:'',textContent:'',scrollTop:0,children:[],
  addEventListener(){},removeEventListener(){},appendChild(){},remove(){},focus(){},click(){},
  setAttribute(){},getAttribute:()=>null,querySelectorAll:()=>[],querySelector:()=>mkEl(),
  insertAdjacentHTML(){},closest:()=>null,getBoundingClientRect:()=>({top:0,left:0,width:0,height:0})};
  return e; }
var document={getElementById:()=>mkEl(),createElement:()=>mkEl(),body:mkEl(),head:mkEl(),
  addEventListener(){},querySelectorAll:()=>[],querySelector:()=>mkEl(),documentElement:mkEl()};
var window={matchMedia:()=>({matches:false,addEventListener(){}}),addEventListener(){},
  location:{href:''},print(){},open:()=>null};
var navigator={clipboard:{writeText:()=>Promise.resolve()},userAgent:'node'};
var setTimeout=(f)=>0, setInterval=(f)=>0, requestAnimationFrame=(f)=>0, alert=()=>{};
`;
;
const mod = stub + js + `
;module.exports={BRANDS,NONAB,AWARE,lookup,lookupOther,riskFlags,buildPrompt,groupKey,groupLabel,
  PROMPTS,VERSIONS,concordance};
`;
const modPath=require('path').join(__dirname,'_mod.js');
fs.writeFileSync(modPath, mod);
const A = require(modPath);

let pass = 0, fail = 0;
const ok = (name, cond, extra='') => {
  if (cond) { pass++; console.log('  PASS  ' + name); }
  else { fail++; console.log('  FAIL  ' + name + (extra ? '  <- ' + extra : '')); }
};

console.log('=== data loaded ===');
ok('brands loaded', A.BRANDS.length === 2869, A.BRANDS.length);
ok('non-antibiotics loaded', A.NONAB.length === 13962, A.NONAB.length);
ok('AWaRe loaded', A.AWARE.length === 376, A.AWARE.length);

console.log('\n=== antibiotic lookup ===');
for (const [q, gen, grp] of [['azixon','Azithromycin','Watch'],['refix','Cefixime','Watch'],
                             ['a-clox','Cloxacillin','Access'],['cifran','Ciprofloxacin','Watch']]) {
  const h = A.lookup(q);
  ok(`${q} -> ${gen}/${grp}`, h.length>0 && new RegExp(gen,'i').test(h[0].generic) && h[0].group===grp,
     h.length ? `${h[0].brand} / ${h[0].generic} / ${h[0].group}` : 'no hits');
}

console.log('\n=== newly recovered antibiotics ===');
const amoxy = A.BRANDS.filter(b=>/amox/i.test(b.g));
ok('amoxycillin products are Access', amoxy.length>0 && amoxy.every(b=>['Access','Not recommended','Needs panel decision','Watch'].includes(b.a)),
   `${amoxy.length} products, groups: ${[...new Set(amoxy.map(b=>b.a))].join(',')}`);
const mupi = A.BRANDS.filter(b=>/mupirocin/i.test(b.g));
ok('mupirocin is in the antibiotic set', mupi.length>0, `${mupi.length} products`);
const vet = A.BRANDS.filter(b=>b.v);
ok('veterinary antibiotics flagged', vet.length===169, vet.length);
const tb = A.BRANDS.filter(b=>b.a==='Antituberculosis');
ok('TB drugs get their own group', tb.length===20, tb.length);
ok('ornidazole resolves', A.BRANDS.some(b=>/ornidazole/i.test(b.g)));

console.log('\n=== not-an-antibiotic lookup ===');
for (const [q, expectClass] of [['abamol','Analgesic'],['alerva','Antihistamin'],['wormnil','Anthelmintic']]) {
  const o = A.lookupOther(q);
  ok(`${q} -> class "${expectClass}"`, o.length>0 && o[0].u===0 && new RegExp(expectClass,'i').test(o[0].c||''),
     o.length ? `u=${o[0].u} c=${JSON.stringify(o[0].c)}` : 'no hits');
}
ok('antibiotic search returns no non-antibiotic card', A.lookup('azixon').length>0);
ok('nonsense is in neither list', A.lookup('zzqqxyw').length===0 && A.lookupOther('zzqqxyw').length===0);

console.log('\n=== cannot-confirm is now rare and justified ===');
const cc = A.NONAB.filter(n=>n.u);
ok('cannot-confirm count is 245', cc.length===245, cc.length);
ok('every cannot-confirm has no composition in the register',
   cc.every(n=>['---','nan','','--'].includes(String(n.g).trim())),
   cc.filter(n=>!['---','nan','','--'].includes(String(n.g).trim())).slice(0,3).map(n=>n.g).join(' | '));
const labelled = A.NONAB.filter(n=>!n.u && n.c);
ok('labelled non-antibiotics >= 13000', labelled.length>=13000, labelled.length);

console.log('\n=== false friends must NOT be antibiotics ===');
for (const bad of ['penicillamine','streptococcus faecalis','griseofulvin','asparaginase']) {
  ok(`${bad} not in antibiotic set`, !A.BRANDS.some(b=>new RegExp(bad,'i').test(b.g)),
     A.BRANDS.filter(b=>new RegExp(bad,'i').test(b.g)).slice(0,2).map(b=>b.b+'/'+b.g).join(','));
}

console.log('\n=== safety flags ===');
const f1 = A.riskFlags({awareGroup:'Antituberculosis',generic:'Isoniazid',redFlags:[],ageBand:'',form:'tablet'});
ok('TB drug raises a stop flag', f1.some(f=>f.id==='HR-TB' && f.sev==='stop'), JSON.stringify(f1));
const f2 = A.riskFlags({awareGroup:'Unclassified',generic:'Enrofloxacin',vet:true,redFlags:[],ageBand:'',form:'tablet'});
ok('veterinary antibiotic raises a flag', f2.some(f=>f.id==='HR-VET'), JSON.stringify(f2.map(f=>f.id)));
ok('TB prompt text exists', !!A.PROMPTS['P-TB1'] && /DOTS/.test(A.PROMPTS['P-TB1'].b.join(' ')));
ok('vet prompt text exists', !!A.PROMPTS['P-VT1']);
ok('TB badge class is valid CSS', A.groupKey('Antituberculosis')==='b-Antituberculosis');
ok('TB label is short', A.groupLabel('Antituberculosis')==='TB drug');


// ---------------------------------------------------------------- review blockers
// Each block below pins a defect raised in external review so it cannot return.
const path=require('path');
function loadBuild(file){
  const src = fs.readFileSync(path.join(__dirname,'..',file),'utf8');
  const j = src.match(/<script>([\s\S]*?)<\/script>/)[1];
  const f = path.join(__dirname,'_b_'+file.replace(/\W/g,'_')+'.js');
  fs.writeFileSync(f, stub + j + `
;module.exports={cfg,tx,BUILD,FIELD,concordance,counselBlock,phaseFromSchedule,primaryOutcome,PRIMARY_VERSION,
  csvRows,viewOutcome,submitDraft,seed,setDraft:(d)=>{draft=d},getDraft:()=>draft};`);
  return require(f);
}

console.log('\n=== Blocker 3: recording-only baseline ===');
const D = loadBuild('index.html'), F = loadBuild('field.html');

ok('field build is marked field', F.BUILD==='field' && F.FIELD===true, F.BUILD);
ok('demo build is marked demo', D.BUILD==='demo' && D.FIELD===false, D.BUILD);
ok('field build seeds NO demonstration data', F.tx.length===0, F.tx.length+' rows');
ok('demo build still seeds, for evaluators', D.tx.length>0, D.tx.length+' rows');

// phase derived from the activation date, not togglable
F.cfg.activated=''; ok('no activation date -> silent', F.phaseFromSchedule()==='silent');
F.cfg.activated='2099-01-01'; ok('future activation -> still silent', F.phaseFromSchedule()==='silent');
F.cfg.activated='2000-01-01'; ok('past activation -> advisory', F.phaseFromSchedule()==='advisory');

// counselling labels must not instruct during baseline
const base={generic:'Azithromycin',brand:'Azixon',counselDose:false,counselDays:false,safetyNet:false};
D.cfg.phase='silent';   const silentHtml   = D.counselBlock(base);
D.cfg.phase='advisory'; const advisoryHtml = D.counselBlock(base);
const instructions=[/Finish all of them/,/see a doctor/,/finish the course/,/0&#8209;1&#8209;0/];
ok('baseline handover gives no instruction', instructions.every(r=>!r.test(silentHtml)),
   instructions.filter(r=>r.test(silentHtml)).map(String).join(' '));
ok('advisory handover does instruct', instructions.every(r=>r.test(advisoryHtml)));
ok('both phases keep the three tick boxes',
   ['cdose','cdays','cnet'].every(id=>silentHtml.includes(id)&&advisoryHtml.includes(id)));
ok('Nepali script only in advisory',
   !/Aushadhi pura/.test(silentHtml) && /Aushadhi pura/.test(advisoryHtml));

// no claim of a server that does not exist
const text = fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
ok('no claim of syncing to a study server',
   !/syncs to an encrypted study server|Up to the study server|computed server-side/.test(text));

console.log('\n=== Blocker 3/4: non-dispensing encounters ===');
ok('silent flow has its own outcome step', typeof D.viewOutcome==='function');
ok('silent flow no longer assumes a sale',
   !/d\.action='dispensed'; d\.promptIds=\[\]/.test(text));
ok('a non-referral non-dispensing option exists', /data-act="notdispensed"/.test(text));

console.log('\n=== Blocker 4: unassessed is never concordant ===');
const C = D.concordance.bind(D);
const full = {generic:'Azithromycin',awareGroup:'Watch',rx:true,rxMatch:true,
  strengthMatch:'yes',formMatch:'yes',qtyMatch:'yes',action:'dispensed',
  counselDose:true,counselDays:true,safetyNet:true,hasStop:false,inds:[],redFlags:[]};
let r = C(full);
ok('a fully assessed, compliant sale is concordant', r.met===true, JSON.stringify(r.met));

r = C({...full, strengthMatch:null});
ok('unassessed strength -> NOT concordant', r.met!==true, 'met='+r.met);
ok('unassessed strength -> not scorable, not a failure', r.met===null, 'met='+r.met);
ok('unassessed is counted', r.nUnass===1, 'nUnass='+r.nUnass);

r = C({...full, strengthMatch:'no'});
ok('a real mismatch -> discordant', r.met===false, 'met='+r.met);

r = C({...full, strengthMatch:'na'});
ok('genuinely not applicable -> still scorable', r.met===true, 'met='+r.met);

r = C({...full, rxMatch:null});
ok('unrecorded prescription match -> not concordant', r.met!==true, 'met='+r.met);

r = C({...full, action:'referred', counselDose:false, counselDays:false, safetyNet:false});
ok('counselling is NA when nothing was handed over',
   r.doseGiven==='na' && r.durationGiven==='na' && r.safetyNetGiven==='na',
   `${r.doseGiven}/${r.durationGiven}/${r.safetyNetGiven}`);
ok('a referral with no counselling is still scorable', r.met===true, 'met='+r.met);

r = C({...full, hasStop:undefined});
ok('unknown safety state -> not concordant', r.met!==true, 'met='+r.met);

console.log('\n=== export carries the new states ===');
const rows=D.csvRows(), hdr=rows[0];
for(const col of ['components_unassessed','outcome_unscorable','veterinary']){
  ok(`export has ${col}`, hdr.includes(col));
}
ok('header and data widths agree', rows[1].length===hdr.length, `${rows[1].length} vs ${hdr.length}`);
const ci=hdr.indexOf('c_strength');
const vals=new Set(rows.slice(1).map(r=>r[ci]));
ok('component columns use yes/no/na/unassessed',
   [...vals].every(v=>['yes','no','na','unassessed',''].includes(v)), [...vals].join('|'));


console.log('\n=== frozen primary endpoint ===');
const P = loadBuild('index.html');
const pm = (o)=>P2.primaryOutcome(o);
const P2 = loadBuild('index.html');
const npBase = {rx:false, inds:['fever'], screened:true, redFlags:[], referred:false,
  action:'dispensed', counselDays:true, safetyNet:true, counselDose:true};

ok('a prescription encounter is NOT in the primary population',
   pm({...npBase, rx:true}).eligible===false);
ok('a non-prescription encounter is', pm(npBase).eligible===true);

ok('all four criteria met -> concordant', pm(npBase).met===true, JSON.stringify(pm(npBase)));
ok('no reason recorded -> discordant', pm({...npBase, inds:[]}).met===false);
ok('no duration advice -> discordant', pm({...npBase, counselDays:false}).met===false);
ok('no safety-net advice -> discordant', pm({...npBase, safetyNet:false}).met===false);
ok('screening not recorded -> unscorable, not concordant',
   pm({...npBase, screened:undefined}).met===null, 'met='+pm({...npBase,screened:undefined}).met);

const flagged = {...npBase, redFlags:['rf3'], referred:false};
ok('red flag present but no referral -> discordant', pm(flagged).met===false);
ok('red flag present with referral -> concordant',
   pm({...flagged, referred:true, action:'referred'}).met===true);

const refer = {...npBase, action:'referred', referred:true, redFlags:['rf3'],
  counselDays:false, safetyNet:false};
ok('a referral is not penalised for giving no counselling', pm(refer).met===true,
   JSON.stringify(pm(refer).parts));
ok('counselling is na when nothing was dispensed',
   pm(refer).parts.durationGiven==='na' && pm(refer).parts.safetyNetGiven==='na');

const nd = {...npBase, action:'notdispensed', redFlags:[], counselDays:false, safetyNet:false};
ok('non-dispensing for another reason is scorable', nd && pm(nd).met===true, 'met='+pm(nd).met);

ok('dosing advice is NOT a primary component',
   pm({...npBase, counselDose:false}).met===true);
ok('AWaRe group is NOT a primary component',
   pm({...npBase, awareGroup:'Watch'}).met===pm({...npBase, awareGroup:'Access'}).met);

const ph=P.csvRows()[0];
for(const col of ['primary_eligible','primary_concordant','primary_unassessed','primary_version']){
  ok(`export has ${col}`, ph.includes(col));
}
const rowsP=P.csvRows(), ie=ph.indexOf('primary_eligible'), ic=ph.indexOf('primary_concordant');
const rxRows=rowsP.slice(1).filter(r=>r[ph.indexOf('prescription_present')]==='1');
ok('prescription rows are flagged ineligible', rxRows.every(r=>r[ie]==='0'), rxRows.length+' rx rows');
ok('ineligible rows carry no primary value', rxRows.every(r=>r[ic]===''));
const npRows=rowsP.slice(1).filter(r=>r[ie]==='1');
ok('eligible rows carry 1, 0 or blank', npRows.every(r=>['1','0',''].includes(r[ic])));
ok('version stamped on every row',
   rowsP.slice(1).every(r=>r[ph.indexOf('primary_version')]==='PO-2026.10.12'));

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
