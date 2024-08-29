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
indication(patient24, 2).
lemonscore(patient24, 1).
cormack(patient24, 0).
beardormoustache(patient53).
largetongue(patient53).
laryngodifficile(patient53).
indication(patient53, 2).
lemonscore(patient53, 2).
cormack(patient53, 3).
hta(patient77).
diabetes(patient77).
elderly(patient77).
secondoperator(patient77).
indication(patient77, 2).
lemonscore(patient77, 1).
cormack(patient77, 0).
experience(patient59).
laryngodifficile(patient59).
indication(patient59, 2).
lemonscore(patient59, 1).
cormack(patient59, 3).
experience(patient60).
hta(patient60).
copd(patient60).
shortneck(patient60).
elderly(patient60).
indication(patient60, 0).
lemonscore(patient60, 0).
cormack(patient60, 2).
hta(patient54).
patientobese(patient54).
shortneck(patient54).
thyromentaldistance(patient54).
betweenhyoidboneandthyroid(patient54).
indication(patient54, 2).
lemonscore(patient54, 3).
cormack(patient54, 0).
diabetes(patient82).
secondoperator(patient82).
indication(patient82, 0).
lemonscore(patient82, 1).
cormack(patient82, 2).
hta(patient84).
diabetes(patient84).
patientobese(patient84).
indication(patient84, 1).
lemonscore(patient84, 1).
cormack(patient84, 2).
experience(patient42).
hta(patient42).
diabetes(patient42).
shortneck(patient42).
beardormoustache(patient42).
openingmouth(patient42).
elderly(patient42).
indication(patient42, 0).
lemonscore(patient42, 3).
cormack(patient42, 2).
experience(patient18).
indication(patient18, 2).
lemonscore(patient18, 1).
cormack(patient18, 0).
patientobese(patient91).
shortneck(patient91).
indication(patient91, 2).
lemonscore(patient91, 0).
cormack(patient91, 2).
experience(patient20).
laryngodifficile(patient20).
eichman(patient20).
indication(patient20, 4).
lemonscore(patient20, 1).
cormack(patient20, 3).
experience(patient102).
patientobese(patient102).
shortneck(patient102).
thyromentaldistance(patient102).
laryngodifficile(patient102).
indication(patient102, 2).
lemonscore(patient102, 2).
cormack(patient102, 3).
indication(patient113, 2).
lemonscore(patient113, 1).
cormack(patient113, 0).
experience(patient50).
indication(patient50, 0).
lemonscore(patient50, 1).
cormack(patient50, 0).
coronary_artery_disease(patient45).
elderly(patient45).
indication(patient45, 4).
lemonscore(patient45, 1).
cormack(patient45, 0).
experience(patient99).
hta(patient99).
ic(patient99).
shortneck(patient99).
openingmouth(patient99).
laryngodifficile(patient99).
indication(patient99, 0).
lemonscore(patient99, 2).
cormack(patient99, 3).
indication(patient61, 2).
lemonscore(patient61, 1).
cormack(patient61, 0).
beardormoustache(patient27).
largetongue(patient27).
indication(patient27, 0).
lemonscore(patient27, 2).
cormack(patient27, 2).
diabetes(patient28).
coronary_artery_disease(patient28).
elderly(patient28).
indication(patient28, 4).
lemonscore(patient28, 1).
cormack(patient28, 2).
:- end_bg.

% Positive Examples
:- begin_in_pos.
complications(patient60).
complications(patient54).
complications(patient82).
complications(patient42).
complications(patient18).
complications(patient91).
complications(patient20).
complications(patient50).
complications(patient45).
complications(patient99).
complications(patient27).
complications(patient28).
:- end_in_pos.

% Negative Examples
:- begin_in_neg.
complications(patient24).
complications(patient53).
complications(patient77).
complications(patient59).
complications(patient84).
complications(patient102).
complications(patient113).
complications(patient61).
:- end_in_neg.
