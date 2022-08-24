set(verbose,0).

modeh(1,parent(+person,-person)).
modeh(1,grandfather(+person,-person)).
modeh(1,grandparent(+person,-person)).
modeb(*,father(+person,-person)).
modeb(*,mother(+person,-person)).
modeb(*,parent(+person,-person)).
determination(grandfather/2,father/2).
determination(grandfather/2,mother/2).
determination(grandfather/2,parent/2).
determination(grandparent/2,father/2).
determination(grandparent/2,mother/2).
determination(grandparent/2,parent/2).
determination(parent/2,father/2).
determination(parent/2,mother/2).


%%%%%%%%%%%%%%%%%%%%%%
% Background knowledge

:- begin_bg.

person(andrew).  person(bernard).  person(cathleen).  person(daphne).
person(edith).  person(fred).  person(george).  person(john).
person(louis).  person(oscar).  person(paul).  person(robert).
person(stephen).  person(sylvia).  person(william). person(ada).

father(william,sylvia).
father(oscar,louis).
father(oscar,daphne).
father(oscar,cathleen).
father(oscar,fred).
father(oscar,bernard).
father(louis,stephen).
father(louis,andrew).
father(louis,robert).
father(louis,john).
father(george,oscar).
father(paul,edith).

mother(sylvia,stephen).
mother(sylvia,andrew).
mother(sylvia,robert).
mother(sylvia,john).
mother(edith,louis).
mother(edith,daphne).
mother(edith,cathleen).
mother(edith,fred).
mother(edith,bernard).
mother(ada,sylvia).

:- end_bg.


%%%%%%%%%%%%%%%%%%%%%%
% Positive examples

:- begin_in_pos.

parent(ada,sylvia).
parent(edith,bernard).
parent(edith,cathleen).
parent(edith,daphne).
parent(edith,fred).
parent(edith,louis).
parent(george,oscar).
parent(louis,andrew).
parent(louis,john).
parent(louis,robert).
parent(louis,stephen).
parent(oscar,bernard).
parent(oscar,cathleen).
parent(oscar,daphne).
parent(oscar,fred).
parent(oscar,louis).
parent(paul,edith).
parent(sylvia,andrew).
parent(sylvia,john).
parent(sylvia,robert).
parent(sylvia,stephen).
parent(william,sylvia).

grandfather(george,bernard).
grandfather(george,cathleen).
grandfather(george,daphne).
grandfather(george,fred).
grandfather(george,louis).
grandfather(oscar,andrew).
grandfather(oscar,john).
grandfather(oscar,robert).
grandfather(oscar,stephen).
grandfather(paul,bernard).
grandfather(paul,cathleen).
grandfather(paul,daphne).
grandfather(paul,fred).
grandfather(paul,louis).
grandfather(william,andrew).
grandfather(william,john).
grandfather(william,robert).
grandfather(william,stephen).

grandparent(ada,andrew).
grandparent(ada,john).
grandparent(ada,robert).
grandparent(ada,stephen).
grandparent(edith,andrew).
grandparent(edith,john).
grandparent(edith,robert).
grandparent(edith,stephen).
grandparent(george,bernard).
grandparent(george,cathleen).
grandparent(george,daphne).
grandparent(george,fred).
grandparent(george,louis).
grandparent(oscar,andrew).
grandparent(oscar,john).
grandparent(oscar,robert).
grandparent(oscar,stephen).
grandparent(paul,bernard).
grandparent(paul,cathleen).
grandparent(paul,daphne).
grandparent(paul,fred).
grandparent(paul,louis).
grandparent(william,andrew).
grandparent(william,john).
grandparent(william,robert).
grandparent(william,stephen).

:- end_in_pos.



%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Negative examples

:- begin_in_neg.

parent(ada,andrew).
parent(ada,john).
parent(ada,robert).
parent(ada,stephen).
parent(edith,andrew).
parent(edith,john).
parent(edith,robert).
parent(edith,stephen).
parent(george,bernard).
parent(george,cathleen).
parent(george,daphne).
parent(george,fred).
parent(george,louis).
parent(oscar,andrew).
parent(oscar,john).
parent(oscar,robert).
parent(oscar,stephen).
parent(paul,bernard).
parent(paul,cathleen).
parent(paul,daphne).
parent(paul,fred).
parent(paul,louis).
parent(william,andrew).
parent(william,john).
parent(william,robert).
parent(william,stephen).

parent(sylvia,ada).
parent(bernard,edith).
parent(cathleen,edith).
parent(daphne,edith).
parent(fred,edith).
parent(louis,edith).
parent(oscar,george).
parent(andrew,louis).
parent(john,louis).
parent(robert,louis).
parent(stephen,louis).
parent(bernard,oscar).
parent(cathleen,oscar).
parent(daphne,oscar).
parent(fred,oscar).
parent(louis,oscar).
parent(edith,paul).
parent(andrew,sylvia).
parent(john,sylvia).
parent(robert,sylvia).
parent(stephen,sylvia).
parent(sylvia,william).

grandparent(ada,sylvia).
grandparent(edith,bernard).
grandparent(edith,cathleen).
grandparent(edith,daphne).
grandparent(edith,fred).
grandparent(edith,louis).
grandparent(george,oscar).
grandparent(louis,andrew).
grandparent(louis,john).
grandparent(louis,robert).
grandparent(louis,stephen).
grandparent(oscar,bernard).
grandparent(oscar,cathleen).
grandparent(oscar,daphne).
grandparent(oscar,fred).
grandparent(oscar,louis).
grandparent(paul,edith).
grandparent(sylvia,andrew).
grandparent(sylvia,john).
grandparent(sylvia,robert).
grandparent(sylvia,stephen).
grandparent(william,sylvia).

grandfather(ada,sylvia).
grandfather(edith,bernard).
grandfather(edith,cathleen).
grandfather(edith,daphne).
grandfather(edith,fred).
grandfather(edith,louis).
grandfather(george,oscar).
grandfather(louis,andrew).
grandfather(louis,john).
grandfather(louis,robert).
grandfather(louis,stephen).
grandfather(oscar,bernard).
grandfather(oscar,cathleen).
grandfather(oscar,daphne).
grandfather(oscar,fred).
grandfather(oscar,louis).
grandfather(paul,edith).
grandfather(sylvia,andrew).
grandfather(sylvia,john).
grandfather(sylvia,robert).
grandfather(sylvia,stephen).
grandfather(william,sylvia).

grandfather(ada,andrew).
grandfather(ada,john).
grandfather(ada,robert).
grandfather(ada,stephen).
grandfather(edith,andrew).
grandfather(edith,john).
grandfather(edith,robert).
grandfather(edith,stephen).

:- end_in_neg.
