% Mode Declarations
modeh(*, complications(+patientid)).
modeb(*, experience(+patientid)).
modeb(*, hta(+patientid)).
modeb(*, diabetes(+patientid)).
modeb(*, copd(+patientid)).
modeb(*, asthma(+patientid)).
modeb(*, patientobese(+patientid)).
modeb(*, high_arched_palate(+patientid)).
modeb(*, shortneck(+patientid)).
modeb(*, largetongue(+patientid)).
modeb(*, openingmouth(+patientid)).
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
determination(complications/1, asthma/1).
determination(complications/1, patientobese/1).
determination(complications/1, high_arched_palate/1).
determination(complications/1, shortneck/1).
determination(complications/1, largetongue/1).
determination(complications/1, openingmouth/1).
determination(complications/1, elderly/1).
determination(complications/1, laryngodifficile/1).
determination(complications/1, secondoperator/1).
determination(complications/1, eichman/1).
determination(complications/1, indication/2).
determination(complications/1, lemonscore/2).
determination(complications/1, cormack/2).

% Background Knowledge
:- begin_bg.
patientobese(patient10).
shortneck(patient10).
indication(patient10, 2).
lemonscore(patient10, 2).
cormack(patient10, 0).
hta(patient3).
diabetes(patient3).
patientobese(patient3).
shortneck(patient3).
openingmouth(patient3).
elderly(patient3).
laryngodifficile(patient3).
eichman(patient3).
indication(patient3, 4).
lemonscore(patient3, 4).
cormack(patient3, 3).
hta(patient93).
indication(patient93, 2).
lemonscore(patient93, 1).
cormack(patient93, 0).
experience(patient75).
openingmouth(patient75).
indication(patient75, 2).
lemonscore(patient75, 0).
cormack(patient75, 0).
experience(patient12).
copd(patient12).
patientobese(patient12).
high_arched_palate(patient12).
largetongue(patient12).
laryngodifficile(patient12).
indication(patient12, 0).
lemonscore(patient12, 4).
cormack(patient12, 3).
indication(patient61, 2).
lemonscore(patient61, 1).
cormack(patient61, 0).
experience(patient17).
patientobese(patient17).
shortneck(patient17).
openingmouth(patient17).
eichman(patient17).
indication(patient17, 1).
lemonscore(patient17, 3).
cormack(patient17, 0).
experience(patient116).
asthma(patient116).
indication(patient116, 1).
lemonscore(patient116, 1).
cormack(patient116, 2).
experience(patient15).
hta(patient15).
copd(patient15).
patientobese(patient15).
shortneck(patient15).
largetongue(patient15).
laryngodifficile(patient15).
indication(patient15, 2).
lemonscore(patient15, 3).
cormack(patient15, 3).
openingmouth(patient29).
indication(patient29, 2).
lemonscore(patient29, 0).
cormack(patient29, 0).
diabetes(patient19).
eichman(patient19).
indication(patient19, 4).
lemonscore(patient19, 1).
cormack(patient19, 0).
experience(patient58).
laryngodifficile(patient58).
secondoperator(patient58).
indication(patient58, 2).
lemonscore(patient58, 1).
cormack(patient58, 3).
experience(patient95).
copd(patient95).
openingmouth(patient95).
indication(patient95, 0).
lemonscore(patient95, 2).
cormack(patient95, 0).
experience(patient96).
shortneck(patient96).
laryngodifficile(patient96).
eichman(patient96).
indication(patient96, 2).
lemonscore(patient96, 2).
cormack(patient96, 3).
indication(patient46, 2).
lemonscore(patient46, 1).
cormack(patient46, 0).
patientobese(patient34).
shortneck(patient34).
indication(patient34, 0).
lemonscore(patient34, 2).
cormack(patient34, 0).
eichman(patient13).
indication(patient13, 2).
lemonscore(patient13, 1).
cormack(patient13, 2).
patientobese(patient79).
laryngodifficile(patient79).
secondoperator(patient79).
indication(patient79, 2).
lemonscore(patient79, 1).
cormack(patient79, 3).
largetongue(patient27).
indication(patient27, 0).
lemonscore(patient27, 2).
cormack(patient27, 2).
experience(patient66).
hta(patient66).
diabetes(patient66).
high_arched_palate(patient66).
largetongue(patient66).
openingmouth(patient66).
indication(patient66, 4).
lemonscore(patient66, 3).
cormack(patient66, 2).
:- end_bg.

% Positive Examples
:- begin_in_pos.
complications(patient10).
complications(patient3).
complications(patient93).
complications(patient17).
complications(patient116).
complications(patient15).
complications(patient19).
complications(patient58).
complications(patient95).
complications(patient13).
complications(patient27).
complications(patient66).
:- end_in_pos.

% Negative Examples
:- begin_in_neg.
complications(patient75).
complications(patient12).
complications(patient61).
complications(patient29).
complications(patient96).
complications(patient46).
complications(patient34).
complications(patient79).
:- end_in_neg.
