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
modeb(*, largetongue(+patientid)).
modeb(*, openingmouth(+patientid)).
modeb(*, thyromentaldistance(+patientid)).
modeb(*, elderly(+patientid)).
modeb(*, laryngodifficile(+patientid)).
modeb(*, secondoperator(+patientid)).
modeb(*, eichman(+patientid)).
modeb(*, moyensupraglottique(+patientid)).
modeb(*, indication(+patientid, -value)).
modeb(*, lemonscore(+patientid, -value)).
modeb(*, cormack(+patientid, -value)).

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
determination(complications/1, largetongue/1).
determination(complications/1, openingmouth/1).
determination(complications/1, thyromentaldistance/1).
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
coronary_artery_disease(patient70).
elderly(patient70).
indication(patient70, 4).
lemonscore(patient70, 1).
cormack(patient70, 0).
coronary_artery_disease(patient45).
elderly(patient45).
indication(patient45, 4).
lemonscore(patient45, 1).
cormack(patient45, 0).
hta(patient84).
diabetes(patient84).
patientobese(patient84).
indication(patient84, 1).
lemonscore(patient84, 1).
cormack(patient84, 2).
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
experience(patient116).
asthma(patient116).
indication(patient116, 1).
lemonscore(patient116, 1).
cormack(patient116, 2).
indication(patient62, 2).
lemonscore(patient62, 1).
cormack(patient62, 0).
hta(patient5).
diabetes(patient5).
patientobese(patient5).
largetongue(patient5).
laryngodifficile(patient5).
secondoperator(patient5).
eichman(patient5).
indication(patient5, 4).
lemonscore(patient5, 2).
cormack(patient5, 3).
experience(patient66).
hta(patient66).
diabetes(patient66).
high_arched_palate(patient66).
largetongue(patient66).
openingmouth(patient66).
indication(patient66, 4).
lemonscore(patient66, 3).
cormack(patient66, 2).
experience(patient118).
hta(patient118).
diabetes(patient118).
patientobese(patient118).
thyromentaldistance(patient118).
laryngodifficile(patient118).
eichman(patient118).
indication(patient118, 2).
lemonscore(patient118, 0).
cormack(patient118, 3).
high_arched_palate(patient16).
largetongue(patient16).
laryngodifficile(patient16).
secondoperator(patient16).
eichman(patient16).
moyensupraglottique(patient16).
indication(patient16, 2).
lemonscore(patient16, 2).
cormack(patient16, 4).
copd(patient111).
ic(patient111).
indication(patient111, 0).
lemonscore(patient111, 1).
cormack(patient111, 0).
copd(patient81).
laryngodifficile(patient81).
secondoperator(patient81).
indication(patient81, 0).
lemonscore(patient81, 0).
cormack(patient81, 3).
experience(patient90).
hta(patient90).
diabetes(patient90).
coronary_artery_disease(patient90).
indication(patient90, 2).
lemonscore(patient90, 1).
cormack(patient90, 0).
experience(patient59).
laryngodifficile(patient59).
indication(patient59, 2).
lemonscore(patient59, 1).
cormack(patient59, 3).
patientobese(patient10).
shortneck(patient10).
indication(patient10, 2).
lemonscore(patient10, 2).
cormack(patient10, 0).
hta(patient107).
patientobese(patient107).
indication(patient107, 2).
lemonscore(patient107, 0).
cormack(patient107, 0).
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
indication(patient39, 2).
lemonscore(patient39, 1).
cormack(patient39, 2).
experience(patient51).
diabetes(patient51).
elderly(patient51).
indication(patient51, 1).
lemonscore(patient51, 1).
cormack(patient51, 2).
patientobese(patient91).
shortneck(patient91).
indication(patient91, 2).
lemonscore(patient91, 0).
cormack(patient91, 2).
:- end_bg.

% Positive Examples
:- begin_in_pos.
complications(patient70).
complications(patient45).
complications(patient3).
complications(patient116).
complications(patient5).
complications(patient66).
complications(patient16).
complications(patient81).
complications(patient90).
complications(patient10).
complications(patient9).
complications(patient91).
:- end_in_pos.

% Negative Examples
:- begin_in_neg.
complications(patient84).
complications(patient62).
complications(patient118).
complications(patient111).
complications(patient59).
complications(patient107).
complications(patient39).
complications(patient51).
:- end_in_neg.
