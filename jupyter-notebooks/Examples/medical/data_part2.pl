modeh(1, complication(+patient)).
modeb(*, experience(+patient)).
modeb(*, hta(+patient)).
modeb(*, diabete(+patient)).
modeb(*, bpco(+patient)).
modeb(*, asthme(+patient)).
modeb(*, coronarien(+patient)).
modeb(*, ic(+patient)).
modeb(*, patientobese(+patient)).
modeb(*, higharchedpalate(+patient)).
modeb(*, shortneck(+patient)).
modeb(*, necktrauma(+patient)).
modeb(*, beardormoustache(+patient)).
modeb(*, largetongue(+patient)).
modeb(*, openingmouth(+patient)).
modeb(*, thyromentaldistance(+patient)).
modeb(*, betweenhyoidboneandthyroid(+patient)).
modeb(*, epiglottitis(+patient)).
modeb(*, recentnecksurgery(+patient)).
modeb(*, cervicalcollar(+patient)).
modeb(*, elderly(+patient)).
modeb(*, eichman(+patient)).
modeb(*, hardlaryngo(+patient)).
modeb(*, cardiacarrest(+patient)).
modeb(*, secondoperator(+patient)).
modeb(*, hardintubation(+patient)).
determination(complication/1, experience/1).
determination(complication/1, hta/1).
determination(complication/1, diabete/1).
determination(complication/1, bpco/1).
determination(complication/1, asthme/1).
determination(complication/1, coronarien/1).
determination(complication/1, ic/1).
determination(complication/1, patientobese/1).
determination(complication/1, higharchedpalate/1).
determination(complication/1, shortneck/1).
determination(complication/1, necktrauma/1).
determination(complication/1, beardormoustache/1).
determination(complication/1, largetongue/1).
determination(complication/1, openingmouth/1).
determination(complication/1, thyromentaldistance/1).
determination(complication/1, betweenhyoidboneandthyroid/1).
determination(complication/1, epiglottitis/1).
determination(complication/1, recentnecksurgery/1).
determination(complication/1, cervicalcollar/1).
determination(complication/1, elderly/1).
determination(complication/1,hardlaryngo/1).
determination(complication/1, eichman/1).
determination(complication/1, hardintubation/1).
determination(complication/1, secondoperator/1).
determination(complication/1, cardiacarrest/1).

:- begin_bg.
complication(x) :- hardlaryngo(x).
largetongue(patient1).
hardlaryngo(patient1).
cardiacarrest(patient1).
hta(patient5).
bpco(patient5).
patientobese(patient5).
shortneck(patient5).
largetongue(patient5).
openingmouth(patient5).
thyromentaldistance(patient5).
recentnecksurgery(patient5).
secondoperator(patient5).
eichman(patient5).
hardintubation(patient5).
hypotention(patient5).
desaturation(patient5).
hta(patient6).
beardormoustache(patient6).
largetongue(patient6).
openingmouth(patient6).
thyromentaldistance(patient6).
betweenhyoidboneandthyroid(patient6).
elderly(patient6).
eichman(patient6).
hardintubation(patient6).
hypotention(patient6).
desaturation(patient6).
cardiacarrest(patient6).
bradycardie(patient6).
bpco(patient7).
beardormoustache(patient7).
largetongue(patient7).
hardlaryngo(patient7).
secondoperator(patient7).
eichman(patient7).
hardintubation(patient7).
hypotention(patient7).
desaturation(patient7).
extubation(patient7).
experience(patient11).
bpco(patient11).
coronarien(patient11).
patientobese(patient11).
higharchedpalate(patient11).
beardormoustache(patient11).
largetongue(patient11).
hardlaryngo(patient11).
eichman(patient12).
hardintubation(patient12).
cardiacarrest(patient12).
experience(patient17).

hypotention(patient17).

diabete(patient18).
eichman(patient18).
hardintubation(patient18).
cardiacarrest(patient18).
experience(patient20).
hta(patient20).
diabete(patient20).
patientobese(patient20).
shortneck(patient20).
openingmouth(patient20).
elderly(patient20).
eichman(patient20).
hardintubation(patient20).
hypotention(patient20).
diabete(patient22).
beardormoustache(patient22).
largetongue(patient22).
betweenhyoidboneandthyroid(patient22).
elderly(patient22).
extubation(patient22).
hta(patient24).
diabete(patient24).
patientobese(patient24).
shortneck(patient24).
elderly(patient24).
cardiacarrest(patient24).
diabete(patient27).
coronarien(patient27).

elderly(patient27).
desaturation(patient27).
cardiacarrest(patient27).
openingmouth(patient28).
hta(patient29).
diabete(patient29).

hypotention(patient29).
experience(patient36).
coronarien(patient36).
ic(patient36).
higharchedpalate(patient36).
largetongue(patient36).
hardlaryngo(patient36).
secondoperator(patient36).
eichman(patient36).
hardintubation(patient36).
desaturation(patient36).
cardiacarrest(patient36).

experience(patient47).
shortneck(patient47).
necktrauma(patient47).
cervicalcollar(patient47).
experience(patient54).

hta(patient54).
diabete(patient54).
thyromentaldistance(patient54).
elderly(patient54).
secondoperator(patient54).
hypotention(patient54).

hta(patient55).
patientobese(patient55).
shortneck(patient55).

thyromentaldistance(patient56).
experience(patient57).


hardlaryngo(patient57).
secondoperator(patient57).
hypotention(patient57).
desaturation(patient57).
intubationoesophagienne(patient57).
experience(patient65).
hta(patient65).
diabete(patient65).
higharchedpalate(patient65).
largetongue(patient65).
openingmouth(patient65).
bradycardie(patient65).
experience(patient66).

intubationselective(patient66).

thyromentaldistance(patient70).
hardlaryngo(patient70).
secondoperator(patient70).
eichman(patient70).
hardintubation(patient70).
desaturation(patient70).
experience(patient71).
asthme(patient71).

desaturation(patient71).
bradycardie(patient71).
coronarien(patient77).
patientobese(patient77).
higharchedpalate(patient77).
shortneck(patient77).
openingmouth(patient77).

desaturation(patient85).
experience(patient91).
hta(patient91).

secondoperator(patient91).
hypotention(patient91).
hta(patient92).
hypotention(patient92).
desaturation(patient92).
bradycardie(patient92).
experience(patient96).
hta(patient96).
diabete(patient96).
patientobese(patient96).
shortneck(patient96).
thyromentaldistance(patient96).
hardlaryngo(patient96).
experience(patient97).
thyromentaldistance(patient97).
hta(patient106).
patientobese(patient106).
necktrauma(patient106).
patientobese(patient107).


hta(patient111).
diabete(patient111).
patientobese(patient111).
openingmouth(patient111).
elderly(patient111).
hardlaryngo(patient111).
eichman(patient111).
hardintubation(patient111).
desaturation(patient111).
hta(patient113).
diabete(patient113).
coronarien(patient113).

experience(patient116).
hta(patient116).
diabete(patient116).
ic(patient116).

hardlaryngo(patient116).
secondoperator(patient116).
eichman(patient116).
hardintubation(patient116).
desaturation(patient116).
cardiacarrest(patient116).
experience(patient117).
hta(patient117).
diabete(patient117).
patientobese(patient117).
thyromentaldistance(patient117).
hardlaryngo(patient117).
eichman(patient117).
hardintubation(patient117).
:- end_bg.

:- begin_in_pos.
complication(patient18).
complication(patient54).
complication(patient111).
complication(patient1).
complication(patient6).
complication(patient92).
complication(patient27).
complication(patient29).
complication(patient91).
complication(patient22).
complication(patient66).
complication(patient7).
complication(patient65).
complication(patient12).
complication(patient17).
complication(patient5).
complication(patient20).
complication(patient36).
complication(patient116).
complication(patient57).
complication(patient85).
complication(patient70).
complication(patient24).
complication(patient71).
:- end_in_pos.

:- begin_in_neg.
complication(patient107).
complication(patient67).
complication(patient46).
complication(patient38).
complication(patient97).
complication(patient28).
complication(patient106).
complication(patient117).
complication(patient77).
complication(patient47).
complication(patient11).
complication(patient113).
complication(patient55).
complication(patient56).
complication(patient96).
:- end_in_neg.