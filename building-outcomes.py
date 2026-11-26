from pathlib import Path
p = Path("site/app.js")
s = p.read_text()
start = s.index("V.buildings=function(){")
end = s.index("V.building=function(id)", start)
s = s[:start] + '''function buildingOutcomes(id, leads){
 const open=leads.filter(TL.isOpen);
 const counts=[
  ['open','Open leads',open.length],
  ['approved-unscheduled','Approved',open.filter(approvedUnscheduled).length],
  ['upcoming','Scheduled move-ins',open.filter(l=>TL.simpleSummary(l).scheduled).length],
  ['moved','Won (moved in)',leads.filter(l=>l.stage==='movein').length]
 ];
 return `<div class="building-outcomes">${counts.map(([view,label,count])=>`<button type="button" class="btn ghost" data-act="simpleView" data-building="${esc(id)}" data-view="${view}"><b>${count}</b> ${label}</button>`).join('')}</div>`;
}
V.buildings=function(){
 const all=TL.visibleLeads();
 return `<section class="hello"><h2>Choose a building</h2></section><div class="bgrid">${sortedBuildings().map(b=>`<section class="card bcard"><h3><a href="#/building/${esc(b.id)}">${esc(b.name)}</a></h3><small class="muted">${esc(b.county||'County needs confirmation')} · ${esc(b.contact||'Tharon Group')}</small>${buildingOutcomes(b.id,all.filter(l=>l.building===b.id))}</section>`).join('')}</div>`;
};
''' + s[end:]
for old,new in [
 ("if(a==='simpleView'||a==='simpleApproval'){e.preventDefault();UI.rep='all';UI.bld='all';","if(a==='simpleView'||a==='simpleApproval'){e.preventDefault();UI.rep='all';UI.bld=el.dataset.building||'all';"),
 ('</p></section><section class="card"><h3>Lead profiles','</p>${buildingOutcomes(id,ls)}</section><section class="card"><h3>Lead profiles')]:
    if s.count(old)!=1: raise ValueError(old)
    s=s.replace(old,new)
p.write_text(s)
with Path("site/styles.css").open("a") as f:
    f.write("\n.building-outcomes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.4rem;margin-top:.6rem}.building-outcomes .btn{white-space:normal;text-align:start;justify-content:flex-start}\n")
