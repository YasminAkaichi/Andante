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

echec_pre(jean).
echec_pre(jacques).

echec_pre(anne) :- fail.
echec_pre(marie) :- fail.
    
:- end_bg.    

    
% POSITIVE EXAMPLES
:- begin_in_pos.

echec_cours(jean).
echec_cours(jacques).  

   
:- end_in_pos.

    

% NEGATIVE EXAMPLES
:- begin_in_neg.

echec_cours(anne).
echec_cours(marie).
    
:- end_in_neg.    
