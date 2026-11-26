from pathlib import Path
import json
r=Path(__file__).resolve().parent
p=r/'config/users.json';u=json.loads(p.read_text());next(x for x in u if x['id']=='u2')['editableLeadOwners']=['u1'];p.write_text(json.dumps(u,indent=2)+'\n')
def replace(name,old,new,count=1):
 p=r/name;s=p.read_text();assert s.count(old)==count,(name,old,s.count(old));p.write_text(s.replace(old,new))
replace('server/engine.mjs','editAllLeads:users.find(x=>x.id===u.id)?.editAllLeads===true,','editableLeadOwners:users.find(x=>x.id===u.id)?.editableLeadOwners||[],editAllLeads:users.find(x=>x.id===u.id)?.editAllLeads===true,',2)
replace('site/api.js',"const canEditLead=l=>!!l&&(isAdmin()||me().editAllLeads===true||l.rep===S.me);","const canEditLead=l=>!!l&&(isAdmin()||me().editAllLeads===true||l.rep===S.me||((me().editableLeadOwners||[]).includes(l.rep)&&(me().buildingAccess==='all'||(me().buildingAccess||[]).includes(l.building))));")
replace('site/app.js','(l&&TL.me().editAllLeads?l.rep:S().me)','(l&&TL.canEditLead(l)?l.rep:S().me)')
# This assertion deliberately changes: Morgan-owned visible leads are now editable.
replace('test/olivia-access.test.mjs','views Morgan without general editing','edits Morgan without general editing')
replace('test/olivia-access.test.mjs',"for(const id of ['L_riverside_u1','L_riverside_u3','L_hallmark_u2'])", "s=execute(s,'u2',{op:'setTemp',expectedVersion:1,args:['L_riverside_u1','cold']});for(const id of ['L_riverside_u3','L_hallmark_u2'])")
for name in ['app.js','api.js']:(r/'dist'/name).write_text((r/'site'/name).read_text())

p=r/"test/olivia-access.test.mjs"
p.write_text(p.read_text()+"\ntest('Olivia saves Morgan profiles while preserving ownership, source credit and conflict protection',()=>{\n let s=fixture(),id='L_riverside_u1',row=s.leads.find(l=>l.id===id);const original={rep:row.rep,originRep:row.originRep,createdBy:row.createdBy};\n s=execute(s,'u2',{op:'saveReferral',expectedVersion:row.version,args:[id,{notes:'Synthetic Olivia update',rep:'u1'},{assessment:'pending',approval:'missing',paperworkReceived:false,moveStatus:'none',moveDate:'',reason:'',due:'2026-12-20',note:'Synthetic progress'}]});\n row=s.leads.find(l=>l.id===id);assert.equal(row.notes,'Synthetic Olivia update');for(const [k,v] of Object.entries(original))assert.equal(row[k],v);assert.equal(row.referralProgress.updatedBy,'u2');\n assert.throws(()=>execute(s,'u2',{op:'updateLead',expectedVersion:1,args:[id,{notes:'stale'}]}),e=>e.status===409);\n assert.throws(()=>execute(s,'u2',{op:'updateLead',expectedVersion:row.version,args:[id,{rep:'u2'}]}),e=>e.status===403);\n for(const blocked of ['L_riverside_u0','L_riverside_u3','L_hallmark_u1','L_pointe_u1','L_carrington_u1'])assert.throws(()=>execute(s,'u2',{op:'updateLead',expectedVersion:1,args:[blocked,{notes:'blocked'}]}),e=>e.status===404);\n assert.throws(()=>execute(s,'u2',{op:'settings',args:[{}]}),e=>e.status===403);\n const view=scoped(s,'u2');assert.deepEqual(view.users.find(u=>u.id==='u2').editableLeadOwners,['u1']);\n});\n")

replace('test/paperwork.test.mjs',"execute(state,'u2',{op:'setDoc'","execute(state,'u3',{op:'setDoc'")

replace('test/server.test.mjs',"execute(s,'u2',{op:'setTemp',args:[id,'cold'],expectedVersion:1})","execute(s,'u3',{op:'setTemp',args:[id,'cold'],expectedVersion:1})")
