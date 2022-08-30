modeh(*,daughter(+person,-person)).
modeb(*,parent(+person,-person)).
modeb(*,parent(-person,+person)).
modeb(*,female(+person)).
modeb(*,female(-person)).
%
determination(daughter/2,parent/2).
determination(daughter/2,female/1).
%    
set(verbose,1).

:- begin_bg.
person(ann).
person(mary).
person(tom).
person(eve).
person(lucy).

parent(ann,mary).
parent(ann,tom).
parent(tom,eve).
parent(tom,lucy).

female(ann).
female(mary).
female(eve).
female(lucy).
:- end_bg.
    

:- begin_in_pos.
daughter(lucy,tom).
daughter(mary,ann).
daughter(eve,tom).
:- end_in_pos.

:- begin_in_neg.
daughter(tom,ann).
daughter(tom,eve).
:- end_in_neg.
    

    
    
    
    
    

    
