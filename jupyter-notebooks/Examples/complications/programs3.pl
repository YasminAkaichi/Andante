% Mode Declarations
modeh(*, complications(+patientid)).
modeb(*, experience(+patientid)).
modeb(*, hta(+patientid)).
modeb(*, diabetes(+patientid)).
modeb(*, copd(+patientid)).
modeb(*, coronary_artery_disease(+patientid)).
modeb(*, ic(+patientid)).
modeb(*, patientobese(+patientid)).
modeb(*, high_arched_palate(+patientid)).
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
determination(complications/1, high_arched_palate/1).
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
experience(patient52).
largetongue(patient52).
indication(patient52, 2).
lemonscore(patient52, 1).
cormack(patient52, 2).
hta(patient104).
diabetes(patient104).
coronary_artery_disease(patient104).
patientobese(patient104).
shortneck(patient104).
thyromentaldistance(patient104).
betweenhyoidboneandthyroid(patient104).
laryngodifficile(patient104).
secondoperator(patient104).
indication(patient104, 0).
lemonscore(patient104, 3).
cormack(patient104, 4).
experience(patient50).
indication(patient50, 0).
lemonscore(patient50, 1).
cormack(patient50, 0).
experience(patient102).
patientobese(patient102).
shortneck(patient102).
thyromentaldistance(patient102).
laryngodifficile(patient102).
indication(patient102, 2).
lemonscore(patient102, 2).
cormack(patient102, 3).
patientobese(patient10).
shortneck(patient10).
indication(patient10, 2).
lemonscore(patient10, 2).
cormack(patient10, 0).
copd(patient8).
beardormoustache(patient8).
largetongue(patient8).
laryngodifficile(patient8).
secondoperator(patient8).
eichman(patient8).
indication(patient8, 0).
lemonscore(patient8, 2).
cormack(patient8, 4).
experience(patient35).
indication(patient35, 0).
lemonscore(patient35, 1).
cormack(patient35, 0).
hta(patient32).
largetongue(patient32).
indication(patient32, 2).
lemonscore(patient32, 0).
cormack(patient32, 0).
diabetes(patient23).
beardormoustache(patient23).
largetongue(patient23).
betweenhyoidboneandthyroid(patient23).
elderly(patient23).
indication(patient23, 2).
lemonscore(patient23, 4).
cormack(patient23, 0).
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
hta(patient100).
diabetes(patient100).
indication(patient100, 2).
lemonscore(patient100, 1).
cormack(patient100, 0).
experience(patient59).
laryngodifficile(patient59).
indication(patient59, 2).
lemonscore(patient59, 1).
cormack(patient59, 3).
largetongue(patient11).
openingmouth(patient11).
eichman(patient11).
indication(patient11, 4).
lemonscore(patient11, 2).
cormack(patient11, 2).
diabetes(patient103).
laryngodifficile(patient103).
secondoperator(patient103).
indication(patient103, 2).
lemonscore(patient103, 1).
cormack(patient103, 3).
experience(patient43).
high_arched_palate(patient43).
indication(patient43, 2).
lemonscore(patient43, 0).
cormack(patient43, 2).
experience(patient96).
shortneck(patient96).
betweenhyoidboneandthyroid(patient96).
laryngodifficile(patient96).
eichman(patient96).
indication(patient96, 2).
lemonscore(patient96, 2).
cormack(patient96, 3).
hta(patient1).
coronary_artery_disease(patient1).
ic(patient1).
beardormoustache(patient1).
elderly(patient1).
laryngodifficile(patient1).
indication(patient1, 1).
lemonscore(patient1, 2).
cormack(patient1, 4).
beardormoustache(patient27).
largetongue(patient27).
indication(patient27, 0).
lemonscore(patient27, 2).
cormack(patient27, 2).
hta(patient88).
diabetes(patient88).
coronary_artery_disease(patient88).
ic(patient88).
high_arched_palate(patient88).
elderly(patient88).
secondoperator(patient88).
indication(patient88, 1).
lemonscore(patient88, 1).
cormack(patient88, 2).
experience(patient44).
indication(patient44, 2).
lemonscore(patient44, 1).
cormack(patient44, 2).
:- end_bg.

% Positive Examples
:- begin_in_pos.
complications(patient52).
complications(patient104).
complications(patient50).
complications(patient10).
complications(patient8).
complications(patient35).
complications(patient23).
complications(patient11).
complications(patient103).
complications(patient43).
complications(patient27).
complications(patient88).
:- end_in_pos.

% Negative Examples
:- begin_in_neg.
complications(patient102).
complications(patient32).
complications(patient97).
complications(patient100).
complications(patient59).
complications(patient96).
complications(patient1).
complications(patient44).
:- end_in_neg.
