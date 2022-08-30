:- use_module(library(aleph)).
:- aleph.

:- aleph_set(verbose,1).
% :- aleph_set(evalfn,posonly).

:- modeh(1,echec_cours(+personne)).
:- modeb(1,echec_pre(+personne)).

:- determination(echec_cours/1,echec_pre/1).
    
% BACKGROUND    
:- begin_bg.

personne(anne).
personne(marie).
personne(jean).
personne(jacques).

echec_pre(X) :- points(X,pre,Y), Y < 10.

points(jean,pre,4).
points(jacques,pre,7).
points(anne,pre,13).
points(marie,pre,13).
points(jean,cours,14).
points(jacques,cours,17).
points(anne,cours,14).
points(marie,cours,17).

echec_cours(X) :- points(X,cours,Y), Y < 10.
    
:- end_bg.    

    
% POSITIVE EXAMPLES
:- begin_in_pos.

echec_cours(jean).

   
:- end_in_pos.

    

% NEGATIVE EXAMPLES
:- begin_in_neg.

echec_cours(anne).
echec_cours(marie).
    
:- end_in_neg.    
