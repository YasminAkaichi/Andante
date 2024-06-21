modeh(1, complication(+patient)).
modeb(*, experience(+patient)).
modeb(*, age(+patient)).
modeb(*, sexe(+patient)).
modeb(*, hta(+patient)).
modeb(*, diabete(+patient)).
modeb(*, bpco(+patient)).
modeb(*, asthme(+patient)).
modeb(*, coronarien(+patient)).
modeb(*, autres(+patient)).
modeb(*, ic(+patient)).
modeb(*, indication(+patient)).
modeb(*, diagnostic(+patient)).
modeb(*, patientobese(+patient)).
modeb(*, higharchedpalate(+patient)).
modeb(*, shortneck(+patient)).
modeb(*, necktrauma(+patient)).
modeb(*, beardormoustache(+patient)).
modeb(*, largetongue(+patient)).
modeb(*, openingmouth(+patient)).
modeb(*, thyromentaldistance(+patient)).
modeb(*, betweenhyoidboneandthyroid(+patient)).
modeb(*, tumor(+patient)).
modeb(*, epiglottitis(+patient)).
modeb(*, recentnecksurgery(+patient)).
modeb(*, hematoma(+patient)).
modeb(*, cervicalcollar(+patient)).
modeb(*, lemonscore(+patient)).
modeb(*, elderly(+patient)).
determination(complication/1, experience/1).
determination(complication/1, age/1).
determination(complication/1, sexe/1).
determination(complication/1, hta/1).
determination(complication/1, diabete/1).
determination(complication/1, bpco/1).
determination(complication/1, asthme/1).
determination(complication/1, coronarien/1).
determination(complication/1, autres/1).
determination(complication/1, ic/1).
determination(complication/1, indication/1).
determination(complication/1, diagnostic/1).
determination(complication/1, patientobese/1).
determination(complication/1, higharchedpalate/1).
determination(complication/1, shortneck/1).
determination(complication/1, necktrauma/1).
determination(complication/1, beardormoustache/1).
determination(complication/1, largetongue/1).
determination(complication/1, openingmouth/1).
determination(complication/1, thyromentaldistance/1).
determination(complication/1, betweenhyoidboneandthyroid/1).
determination(complication/1, tumor/1).
determination(complication/1, epiglottitis/1).
determination(complication/1, recentnecksurgery/1).
determination(complication/1, hematoma/1).
determination(complication/1, cervicalcollar/1).
determination(complication/1, lemonscore/1).
determination(complication/1, elderly/1).
:- begin_bg.
complication(x) :- laryngodifficile(x).
hta(patient0).
coronarien(patient0).
ic(patient0).
indication(patient0).
beardormoustache(patient0).
elderly(patient0).
laryngodifficile(patient0).
experience(patient3).
higharchedpalate(patient3).
largetongue(patient3).
openingmouth(patient3).
elderly(patient3).
laryngodifficile(patient3).
secondoperator(patient3).
hypotention(patient3).
arret(patient3).
sexe(patient9).
patientobese(patient9).
shortneck(patient9).
hypotention(patient9).
desaturation(patient9).
bradycardie(patient9).
experience(patient13).
hta(patient13).
patientobese(patient13).
beardormoustache(patient13).
elderly(patient13).
laryngodifficile(patient13).
desaturation(patient13).
arret(patient13).
higharchedpalate(patient15).
largetongue(patient15).
laryngodifficile(patient15).
secondoperator(patient15).
eichman(patient15).
moyensupraglottique(patient15).
intubationdifficile(patient15).
hypotention(patient15).
desaturation(patient15).
arret(patient15).
intubationselective(patient15).
intubationoesophagienne(patient15).
experience(patient16).
indication(patient16).
patientobese(patient16).
shortneck(patient16).
openingmouth(patient16).
eichman(patient16).
arret(patient16).
experience(patient19).
lemonscore(patient19).
laryngodifficile(patient19).
eichman(patient19).
intubationdifficile(patient19).
desaturation(patient19).
fracturedentaire(patient19).
arret(patient19).
experience(patient21).
bpco(patient21).
ic(patient21).
higharchedpalate(patient21).
elderly(patient21).
hypotention(patient21).
desaturation(patient21).
arret(patient21).
lemonscore(patient23).
hta(patient30).
lemonscore(patient30).
secondoperator(patient30).
eichman(patient30).
intubationdifficile(patient30).
hypotention(patient30).
desaturation(patient30).
sexe(patient33).
patientobese(patient33).
shortneck(patient33).
experience(patient34).
lemonscore(patient34).
hypotention(patient34).
desaturation(patient34).
experience(patient37).
hta(patient37).
lemonscore(patient37).
hta(patient39).
higharchedpalate(patient39).
openingmouth(patient39).
secondoperator(patient39).
desaturation(patient39).
experience(patient43).
lemonscore(patient43).
coronarien(patient44).
lemonscore(patient44).
elderly(patient44).
hypotention(patient44).
desaturation(patient44).
experience(patient50).
diabete(patient50).
indication(patient50).
lemonscore(patient50).
elderly(patient50).
experience(patient51).
lemonscore(patient51).
intubationselective(patient51).
beardormoustache(patient52).
largetongue(patient52).
laryngodifficile(patient52).
experience(patient59).
hta(patient59).
bpco(patient59).
shortneck(patient59).
elderly(patient59).
hypotention(patient59).
lemonscore(patient62).
patientobese(patient78).
lemonscore(patient78).
laryngodifficile(patient78).
secondoperator(patient78).
bpco(patient80).
laryngodifficile(patient80).
secondoperator(patient80).
hypotention(patient80).
desaturation(patient80).
arret(patient80).
sexe(patient81).
diabete(patient81).
lemonscore(patient81).
secondoperator(patient81).
intubationdifficile(patient81).
hypotention(patient81).
desaturation(patient81).
intubationoesophagienne(patient81).
hta(patient82).
higharchedpalate(patient82).
openingmouth(patient82).
laryngodifficile(patient82).
secondoperator(patient82).
eichman(patient82).
moyensupraglottique(patient82).
intubationdifficile(patient82).
desaturation(patient82).
intubationselective(patient82).
intubationoesophagienne(patient82).
lemonscore(patient84).
hta(patient86).
diabete(patient86).
coronarien(patient86).
ic(patient86).
indication(patient86).
shortneck(patient86).
secondoperator(patient86).
desaturation(patient86).
arret(patient86).
sexe(patient87).
hta(patient87).
diabete(patient87).
coronarien(patient87).
ic(patient87).
indication(patient87).
higharchedpalate(patient87).
lemonscore(patient87).
elderly(patient87).
secondoperator(patient87).
hypotention(patient87).
desaturation(patient87).
arret(patient87).
lemonscore(patient88).
desaturation(patient88).
experience(patient93).
sexe(patient93).
asthme(patient93).
thyromentaldistance(patient93).
desaturation(patient93).
experience(patient94).
bpco(patient94).
openingmouth(patient94).
hypotention(patient94).
experience(patient101).
sexe(patient101).
patientobese(patient101).
shortneck(patient101).
thyromentaldistance(patient101).
laryngodifficile(patient101).
diabete(patient102).
lemonscore(patient102).
laryngodifficile(patient102).
secondoperator(patient102).
desaturation(patient102).
intubationoesophagienne(patient102).
sexe(patient104).
lemonscore(patient104).
beardormoustache(patient105).
sexe(patient109).
lemonscore(patient109).
sexe(patient112).
lemonscore(patient112).
experience(patient114).
sexe(patient114).
hta(patient114).
diabete(patient114).
indication(patient114).
patientobese(patient114).
shortneck(patient114).
openingmouth(patient114).
hypotention(patient114).
desaturation(patient114).
experience(patient115).
asthme(patient115).
indication(patient115).
lemonscore(patient115).
arret(patient115).
bradycardie(patient115).
:- end_bg.

:- begin_in_pos.
complication(patient39).
complication(patient102).
complication(patient19).
complication(patient82).
complication(patient51).
complication(patient86).
complication(patient93).
complication(patient16).
complication(patient115).
complication(patient21).
complication(patient80).
complication(patient81).
complication(patient34).
complication(patient9).
complication(patient15).
complication(patient114).
complication(patient13).
complication(patient30).
complication(patient44).
complication(patient88).
complication(patient87).
complication(patient59).
complication(patient3).
complication(patient94).
:- end_in_pos.

:- begin_in_neg.
complication(patient52).
complication(patient37).
complication(patient78).
complication(patient101).
complication(patient43).
complication(patient50).
complication(patient0).
complication(patient62).
complication(patient104).
complication(patient105).
complication(patient23).
complication(patient112).
complication(patient33).
complication(patient109).
complication(patient84).
:- end_in_neg.