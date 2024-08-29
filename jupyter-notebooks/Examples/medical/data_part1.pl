set(verbose,0).
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

:- begin_bg.
hta(patient2).
diabete(patient2).
patientobese(patient2).
shortneck(patient2).
openingmouth(patient2).
elderly(patient2).
hardlaryndo(patient2).
eichman(patient2).
hardintubation(patient2).
arret(patient2).
hta(patient4).
diabete(patient4).
patientobese(patient4).
largetongue(patient4).
hardlaryndo(patient4).
secondoperator(patient4).
eichman(patient4).
hardintubation(patient4).
desaturation(patient4).
arret(patient4).
experience(patient8).
hta(patient8).
diabete(patient8).
coronarien(patient8).
higharchedpalate(patient8).
largetongue(patient8).
elderly(patient8).
hardlaryndo(patient8).
hypotention(patient8).
desaturation(patient8).
arret(patient8).
largetongue(patient10).
openingmouth(patient10).
eichman(patient10).
hardintubation(patient10).
arret(patient10).
experience(patient14).
hta(patient14).
bpco(patient14).
patientobese(patient14).
shortneck(patient14).
largetongue(patient14).
hardlaryndo(patient14).
desaturation(patient14).
arret(patient14).
hta(patient25).
diabete(patient25).
patientobese(patient25).
largetongue(patient25).
secondoperator(patient25).
arret(patient25).
beardormoustache(patient26).
largetongue(patient26).
hypotention(patient26).
desaturation(patient26).
hta(patient31).
largetongue(patient31).
hta(patient32).
diabete(patient32).
coronarien(patient32).
patientobese(patient32).
shortneck(patient32).
hardlaryndo(patient32).
arret(patient32).
hta(patient35).
ic(patient35).
patientobese(patient35).
shortneck(patient35).
largetongue(patient35).
arret(patient35).
experience(patient40).
experience(patient41).
hta(patient41).
diabete(patient41).
shortneck(patient41).
beardormoustache(patient41).
openingmouth(patient41).
elderly(patient41).
hypotention(patient41).
experience(patient42).
higharchedpalate(patient42).
desaturation(patient42).

experience(patient48).
higharchedpalate(patient48).
shortneck(patient48).
openingmouth(patient48).
thyromentaldistance(patient48).
hardlaryndo(patient48).
experience(patient49).
desaturation(patient49).
hta(patient53).
patientobese(patient53).
shortneck(patient53).
thyromentaldistance(patient53).
betweenhyoidboneandthyroid(patient53).
arret(patient53).
experience(patient58).
hardlaryndo(patient58).
patientobese(patient63).
largetongue(patient63).
hypotention(patient63).
desaturation(patient63).
arret(patient63).
experience(patient64).
hta(patient64).
diabete(patient64).
coronarien(patient64).
patientobese(patient64).
beardormoustache(patient64).
largetongue(patient64).
elderly(patient64).
hardintubation(patient64).
desaturation(patient64).
shortneck(patient68).
largetongue(patient68).
thyromentaldistance(patient68).
betweenhyoidboneandthyroid(patient68).
hardlaryndo(patient68).
secondoperator(patient68).
eichman(patient68).
hardintubation(patient68).
desaturation(patient68).
arret(patient68).
intubationoesophagienne(patient68).
coronarien(patient69).
elderly(patient69).
hypotention(patient69).
desaturation(patient69).
experience(patient72).
hardlaryndo(patient72).
hypotention(patient72).
diabete(patient73).
patientobese(patient73).
shortneck(patient73).
desaturation(patient73).
experience(patient74).
openingmouth(patient74).
bpco(patient75).
secondoperator(patient75).
hta(patient76).
diabete(patient76).
elderly(patient76).
secondoperator(patient76).
hardintubation(patient76).
hta(patient79).
ic(patient79).
patientobese(patient79).
shortneck(patient79).
hypotention(patient79).
arret(patient79).
hta(patient83).
diabete(patient83).
indication(patient83).
patientobese(patient83).
experience(patient89).
hta(patient89).
diabete(patient89).
coronarien(patient89).
desaturation(patient89).
patientobese(patient90).
shortneck(patient90).
hypotention(patient90).
experience(patient98).
hta(patient98).
ic(patient98).
shortneck(patient98).
openingmouth(patient98).
hardlaryndo(patient98).
hypotention(patient98).
arret(patient98).
hta(patient99).
diabete(patient99).
indication(patient100).
hta(patient103).
diabete(patient103).
coronarien(patient103).
patientobese(patient103).
shortneck(patient103).
thyromentaldistance(patient103).
betweenhyoidboneandthyroid(patient103).
hardlaryndo(patient103).
secondoperator(patient103).
hardintubation(patient103).
desaturation(patient103).
diabete(patient108).
bpco(patient108).
beardormoustache(patient108).
openingmouth(patient108).
elderly(patient108).
bpco(patient110).
ic(patient110).
:- end_bg.

:- begin_in_pos.
complication(patient79).
complication(patient4).
complication(patient26).
complication(patient73).
complication(patient103).
complication(patient72).
complication(patient89).
complication(patient25).
complication(patient49).
complication(patient98).
complication(patient90).
complication(patient14).
complication(patient64).
complication(patient42).
complication(patient10).
complication(patient8).
complication(patient68).
complication(patient53).
complication(patient63).
complication(patient41).
complication(patient2).
complication(patient35).
complication(patient69).
complication(patient32).
:- end_in_pos.

:- begin_in_neg.
complication(patient110).
complication(patient31).
complication(patient58).
complication(patient75).
complication(patient74).
complication(patient100).
complication(patient48).
complication(patient76).
complication(patient99).
complication(patient61).
complication(patient45).
complication(patient83).
complication(patient40).
complication(patient108).
complication(patient60).
:- end_in_neg.