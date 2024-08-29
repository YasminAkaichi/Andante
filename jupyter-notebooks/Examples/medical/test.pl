% Mode Declarations
modeh(*, complications(+patientid)).
modeb(*, experience(+patientid)).
modeb(*, hta(+patientid)).
modeb(*, diabetes(+patientid)).
modeb(*, copd(+patientid)).
modeb(*, coronary_artery_disease(+patientid)).
modeb(*, ic(+patientid)).
modeb(*, patientobese(+patientid)).
modeb(*, shortneck(+patientid)).
modeb(*, beardormoustache(+patientid)).
modeb(*, largetongue(+patientid)).
modeb(*, openingmouth(+patientid)).
modeb(*, thyromentaldistance(+patientid)).
modeb(*, betweenhyoidboneandthyroid(+patientid)).
modeb(*, elderly(+patientid)).
modeb(*, laryngodifficile(+patientid)).
modeb(*, secondoperator(+patientid)).
modeb(*, eichman(+patientid)).
modeb(*, indication(+patientid, -value)).
modeb(*, lemonscore(+patientid, -value)).
modeb(*, cormack(+patientid, -value)).

% Determinations
determination(complications/1, experience/1).
determination(complications/1, hta/1).
determination(complications/1, diabetes/1).
determination(complications/1, copd/1).
determination(complications/1, coronary_artery_disease/1).
determination(complications/1, ic/1).
determination(complications/1, patientobese/1).
determination(complications/1, shortneck/1).
determination(complications/1, beardormoustache/1).
determination(complications/1, largetongue/1).
determination(complications/1, openingmouth/1).
determination(complications/1, thyromentaldistance/1).
determination(complications/1, betweenhyoidboneandthyroid/1).
determination(complications/1, elderly/1).
determination(complications/1, laryngodifficile/1).
determination(complications/1, secondoperator/1).
determination(complications/1, eichman/1).
determination(complications/1, indication/2).
determination(complications/1, lemonscore/2).
determination(complications/1, cormack/2).


% Background Knowledge
:- begin_bg.
hta(patient6).
copd(patient6).
patientobese(patient6).
shortneck(patient6).
largetongue(patient6).
openingmouth(patient6).
thyromentaldistance(patient6).
recentnecksurgery(patient6).
secondoperator(patient6).
eichman(patient6).
indication(patient6, 2).
lemonscore(patient6, 6).
cormack(patient6, 2).
indication(patient46, 2).
lemonscore(patient46, 1).
cormack(patient46, 0).
hta(patient36).
ic(patient36).
patientobese(patient36).
shortneck(patient36).
largetongue(patient36).
indication(patient36, 4).
lemonscore(patient36, 3).
cormack(patient36, 0).
experience(patient14).
hta(patient14).
patientobese(patient14).
beardormoustache(patient14).
elderly(patient14).
laryngodifficile(patient14).
indication(patient14, 2).
lemonscore(patient14, 3).
cormack(patient14, 3).
hta(patient112).
diabetes(patient112).
patientobese(patient112).
openingmouth(patient112).
elderly(patient112).
laryngodifficile(patient112).
eichman(patient112).
indication(patient112, 4).
lemonscore(patient112, 0).
cormack(patient112, 4).
experience(patient97).
hta(patient97).
diabetes(patient97).
patientobese(patient97).
shortneck(patient97).
thyromentaldistance(patient97).
laryngodifficile(patient97).
indication(patient97, 0).
lemonscore(patient97, 2).
cormack(patient97, 3).
diabetes(patient82).
secondoperator(patient82).
indication(patient82, 0).
lemonscore(patient82, 1).
cormack(patient82, 2).
experience(patient66).
hta(patient66).
diabetes(patient66).
high_arched_palate(patient66).
largetongue(patient66).
openingmouth(patient66).
indication(patient66, 4).
lemonscore(patient66, 3).
cormack(patient66, 2).
hta(patient114).
diabetes(patient114).
coronary_artery_disease(patient114).
indication(patient114, 0).
lemonscore(patient114, 1).
cormack(patient114, 0).
thyromentaldistance(patient57).
indication(patient57, 2).
lemonscore(patient57, 0).
cormack(patient57, 0).
hta(patient32).
largetongue(patient32).
indication(patient32, 2).
lemonscore(patient32, 0).
cormack(patient32, 0).
experience(patient55).
hta(patient55).
diabetes(patient55).
thyromentaldistance(patient55).
elderly(patient55).
secondoperator(patient55).
indication(patient55, 0).
lemonscore(patient55, 0).
cormack(patient55, 0).
experience(patient73).
laryngodifficile(patient73).
indication(patient73, 2).
lemonscore(patient73, 1).
cormack(patient73, 3).
experience(patient4).
high_arched_palate(patient4).
largetongue(patient4).
openingmouth(patient4).
elderly(patient4).
laryngodifficile(patient4).
secondoperator(patient4).
indication(patient4, 4).
lemonscore(patient4, 4).
cormack(patient4, 3).
hta(patient30).
diabetes(patient30).
indication(patient30, 2).
lemonscore(patient30, 1).
cormack(patient30, 0).
experience(patient43).
high_arched_palate(patient43).
indication(patient43, 2).
lemonscore(patient43, 0).
cormack(patient43, 2).
indication(patient62, 2).
lemonscore(patient62, 1).
cormack(patient62, 0).
hta(patient1).
coronary_artery_disease(patient1).
ic(patient1).
beardormoustache(patient1).
elderly(patient1).
laryngodifficile(patient1).
indication(patient1, 1).
lemonscore(patient1, 2).
cormack(patient1, 4).
experience(patient98).
thyromentaldistance(patient98).
indication(patient98, 0).
lemonscore(patient98, 0).
cormack(patient98, 2).
experience(patient95).
copd(patient95).
openingmouth(patient95).
indication(patient95, 0).
lemonscore(patient95, 2).
cormack(patient95, 0).
:- end_bg.

% Positive Examples
:- begin_in_pos.
complications(patient6).
complications(patient36).
complications(patient14).
complications(patient112).
complications(patient82).
complications(patient66).
complications(patient55).
complications(patient73).
complications(patient4).
complications(patient30).
complications(patient43).
complications(patient95).
:- end_in_pos.

% Negative Examples
:- begin_in_neg.
complications(patient46).
complications(patient97).
complications(patient114).
complications(patient57).
complications(patient32).
complications(patient62).
complications(patient1).
complications(patient98).
:- end_in_neg.
