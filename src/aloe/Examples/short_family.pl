:- use_module(library(aleph)).
:- aleph.

:- modeh(*,daughter(+person,-person)).
:- modeb(*,parent(+person,-person)).
:- modeb(*,parent(-person,+person)).
:- modeb(1,female(+person)).
:- modeb(*,female(-person)).
%
:- determination(daughter/2,parent/2).
:- determination(daughter/2,female/1).
%    
:- aleph_set(verbose,1).

:- begin_bg.
person(ann).
person(mary).
person(tom).
person(eve).

parent(ann,mary).
parent(ann,tom).
parent(tom,eve).

female(ann).
female(mary).
female(eve).
:- end_bg.
    

:- begin_in_pos.
daughter(mary,ann).
daughter(eve,tom).
:- end_in_pos.

:- begin_in_neg.
daughter(tom,ann).
daughter(tom,eve).
:- end_in_neg.

    
    

    
    
    
    
    

    
