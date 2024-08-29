% Mode Declarations
modeh(*, complications(+patientid)).
modeb(*, experience(+patientid)).
modeb(*, hta(+patientid)).
modeb(*, diabetes(+patientid)).
modeb(*, copd(+patientid)).
modeb(*, asthma(+patientid)).
modeb(*, coronary_artery_disease(+patientid)).
modeb(*, ic(+patientid)).
modeb(*, patientobese(+patientid)).
modeb(*, high_arched_palate(+patientid)).
modeb(*, shortneck(+patientid)).
modeb(*, beardormoustache(+patientid)).
modeb(*, largetongue(+patientid)).
modeb(*, openingmouth(+patientid)).
modeb(*, elderly(+patientid)).
modeb(*, laryngodifficile(+patientid)).
modeb(*, secondoperator(+patientid)).
modeb(*, eichman(+patientid)).
modeb(*, moyensupraglottique(+patientid)).
modeb(*, indication(+patientid, -value)).
modeb(*, lemonscore(+patientid, -valuelemonscore)).
modeb(*, cormack(+patientid, -valuecormackscore)).

% Determinations
determination(complications/1, experience/1).
determination(complications/1, hta/1).
determination(complications/1, diabetes/1).
determination(complications/1, copd/1).
determination(complications/1, asthma/1).
determination(complications/1, coronary_artery_disease/1).
determination(complications/1, ic/1).
determination(complications/1, patientobese/1).
determination(complications/1, high_arched_palate/1).
determination(complications/1, shortneck/1).
determination(complications/1, beardormoustache/1).
determination(complications/1, largetongue/1).
determination(complications/1, openingmouth/1).
determination(complications/1, elderly/1).
determination(complications/1, laryngodifficile/1).
determination(complications/1, secondoperator/1).
determination(complications/1, eichman/1).
determination(complications/1, moyensupraglottique/1).
determination(complications/1, indication/2).
determination(complications/1, lemonscore/2).
determination(complications/1, cormack/2).

% Background Knowledge
:- begin_bg.
largetongue(patient11).
openingmouth(patient11).
eichman(patient11).
indication(patient11, 4).
lemonscore(patient11, 2).
cormack(patient11, 2).
experience(patient73).
laryngodifficile(patient73).
indication(patient73, 2).
lemonscore(patient73, 1).
cormack(patient73, 3).
experience(patient116).
asthma(patient116).
indication(patient116, 1).
lemonscore(patient116, 1).
cormack(patient116, 2).
hta(patient84).
diabetes(patient84).
patientobese(patient84).
indication(patient84, 1).
lemonscore(patient84, 1).
cormack(patient84, 2).
patientobese(patient79).
laryngodifficile(patient79).
secondoperator(patient79).
indication(patient79, 2).
lemonscore(patient79, 1).
cormack(patient79, 3).
copd(patient111).
ic(patient111).
indication(patient111, 0).
lemonscore(patient111, 1).
cormack(patient111, 0).
hta(patient87).
diabetes(patient87).
coronary_artery_disease(patient87).
ic(patient87).
shortneck(patient87).
secondoperator(patient87).
indication(patient87, 1).
lemonscore(patient87, 0).
cormack(patient87, 2).
experience(patient43).
high_arched_palate(patient43).
indication(patient43, 2).
lemonscore(patient43, 0).
cormack(patient43, 2).
largetongue(patient2).
laryngodifficile(patient2).
indication(patient2, 4).
lemonscore(patient2, 0).
cormack(patient2, 3).
hta(patient56).
patientobese(patient56).
shortneck(patient56).
indication(patient56, 2).
lemonscore(patient56, 0).
cormack(patient56, 2).
copd(patient8).
beardormoustache(patient8).
largetongue(patient8).
laryngodifficile(patient8).
secondoperator(patient8).
eichman(patient8).
indication(patient8, 0).
lemonscore(patient8, 2).
cormack(patient8, 4).
experience(patient9).
hta(patient9).
diabetes(patient9).
coronary_artery_disease(patient9).
high_arched_palate(patient9).
largetongue(patient9).
elderly(patient9).
laryngodifficile(patient9).
indication(patient9, 2).
lemonscore(patient9, 3).
cormack(patient9, 3).
hta(patient83).
high_arched_palate(patient83).
openingmouth(patient83).
laryngodifficile(patient83).
secondoperator(patient83).
eichman(patient83).
moyensupraglottique(patient83).
indication(patient83, 2).
lemonscore(patient83, 0).
cormack(patient83, 4).
hta(patient77).
diabetes(patient77).
elderly(patient77).
secondoperator(patient77).
indication(patient77, 2).
lemonscore(patient77, 1).
cormack(patient77, 0).
indication(patient62, 2).
lemonscore(patient62, 1).
cormack(patient62, 0).
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
experience(patient38).
hta(patient38).
indication(patient38, 2).
lemonscore(patient38, 1).
cormack(patient38, 2).
indication(patient63, 2).
lemonscore(patient63, 1).
cormack(patient63, 0).
hta(patient40).
high_arched_palate(patient40).
openingmouth(patient40).
secondoperator(patient40).
indication(patient40, 4).
lemonscore(patient40, 2).
cormack(patient40, 2).
experience(patient35).
indication(patient35, 0).
lemonscore(patient35, 1).
cormack(patient35, 0).
:- end_bg.

% Positive Examples
:- begin_in_pos.
complications(patient11).
complications(patient73).
complications(patient116).
complications(patient87).
complications(patient43).
complications(patient2).
complications(patient8).
complications(patient9).
complications(patient83).
complications(patient4).
complications(patient40).
complications(patient35).
:- end_in_pos.

% Negative Examples
:- begin_in_neg.
complications(patient84).
complications(patient79).
complications(patient111).
complications(patient56).
complications(patient77).
complications(patient62).
complications(patient38).
complications(patient63).
:- end_in_neg.
