set(verbose,1).

modeh(1,parent_of(+person,-person)).
modeh(1,grandfather_of(+person,-person)).
modeh(1,grandparent_of(+person,-person)).
modeb(*,father_of(+person,-person)).
modeb(*,mother_of(+person,-person)).
modeb(*,parent_of(+person,-person)).
determination(grandfather_of/2,father_of/2).
determination(grandfather_of/2,mother_of/2).
determination(grandfather_of/2,parent_of/2).
determination(grandparent_of/2,father_of/2).
determination(grandparent_of/2,mother_of/2).
determination(grandparent_of/2,parent_of/2).
determination(parent_of/2,father_of/2).
determination(parent_of/2,mother_of/2).

%%%%%%%%%%%%%%%%%%%%%%
% Type information

:- begin_bg.


person(andrew).  person(bernard).  person(cathleen).  person(daphne).
person(edith).  person(fred).  person(george).  person(john).
person(louis).  person(oscar).  person(paul).  person(robert).
person(stephen).  person(sylvia).  person(william). person(ada).


%%%%%%%%%%%%%%%%%%%%%%
% Background knowledge


father_of(william,sylvia).
father_of(oscar,louis).
father_of(oscar,daphne).
father_of(oscar,cathleen).
father_of(oscar,fred).
father_of(oscar,bernard).
father_of(louis,stephen).
father_of(louis,andrew).
father_of(louis,robert).
father_of(louis,john).
father_of(george,oscar).
father_of(paul,edith).

mother_of(sylvia,stephen).
mother_of(sylvia,andrew).
mother_of(sylvia,robert).
mother_of(sylvia,john).
mother_of(edith,louis).
mother_of(edith,daphne).
mother_of(edith,cathleen).
mother_of(edith,fred).
mother_of(edith,bernard).
mother_of(ada,sylvia).

:- end_bg.


%%%%%%%%%%%%%%%%%%%%%%
% Positive examples

:- begin_in_pos.

parent_of(ada,sylvia).
parent_of(edith,bernard).
parent_of(edith,cathleen).
parent_of(edith,daphne).
parent_of(edith,fred).
parent_of(edith,louis).
parent_of(george,oscar).
parent_of(louis,andrew).
parent_of(louis,john).
parent_of(louis,robert).
parent_of(louis,stephen).
parent_of(oscar,bernard).
parent_of(oscar,cathleen).
parent_of(oscar,daphne).
parent_of(oscar,fred).
parent_of(oscar,louis).
parent_of(paul,edith).
parent_of(sylvia,andrew).
parent_of(sylvia,john).
parent_of(sylvia,robert).
parent_of(sylvia,stephen).
parent_of(william,sylvia).

grandfather_of(george,bernard).
grandfather_of(george,cathleen).
grandfather_of(george,daphne).
grandfather_of(george,fred).
grandfather_of(george,louis).
grandfather_of(oscar,andrew).
grandfather_of(oscar,john).
grandfather_of(oscar,robert).
grandfather_of(oscar,stephen).
grandfather_of(paul,bernard).
grandfather_of(paul,cathleen).
grandfather_of(paul,daphne).
grandfather_of(paul,fred).
grandfather_of(paul,louis).
grandfather_of(william,andrew).
grandfather_of(william,john).
grandfather_of(william,robert).
grandfather_of(william,stephen).

grandparent_of(ada,andrew).
grandparent_of(ada,john).
grandparent_of(ada,robert).
grandparent_of(ada,stephen).
grandparent_of(edith,andrew).
grandparent_of(edith,john).
grandparent_of(edith,robert).
grandparent_of(edith,stephen).
grandparent_of(george,bernard).
grandparent_of(george,cathleen).
grandparent_of(george,daphne).
grandparent_of(george,fred).
grandparent_of(george,louis).
grandparent_of(oscar,andrew).
grandparent_of(oscar,john).
grandparent_of(oscar,robert).
grandparent_of(oscar,stephen).
grandparent_of(paul,bernard).
grandparent_of(paul,cathleen).
grandparent_of(paul,daphne).
grandparent_of(paul,fred).
grandparent_of(paul,louis).
grandparent_of(william,andrew).
grandparent_of(william,john).
grandparent_of(william,robert).
grandparent_of(william,stephen).

:- end_in_pos.



%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Negative examples

:- begin_in_neg.

parent_of(ada,andrew).
parent_of(ada,john).
parent_of(ada,robert).
parent_of(ada,stephen).
parent_of(edith,andrew).
parent_of(edith,john).
parent_of(edith,robert).
parent_of(edith,stephen).
parent_of(george,bernard).
parent_of(george,cathleen).
parent_of(george,daphne).
parent_of(george,fred).
parent_of(george,louis).
parent_of(oscar,andrew).
parent_of(oscar,john).
parent_of(oscar,robert).
parent_of(oscar,stephen).
parent_of(paul,bernard).
parent_of(paul,cathleen).
parent_of(paul,daphne).
parent_of(paul,fred).
parent_of(paul,louis).
parent_of(william,andrew).
parent_of(william,john).
parent_of(william,robert).
parent_of(william,stephen).

parent_of(sylvia,ada).
parent_of(bernard,edith).
parent_of(cathleen,edith).
parent_of(daphne,edith).
parent_of(fred,edith).
parent_of(louis,edith).
parent_of(oscar,george).
parent_of(andrew,louis).
parent_of(john,louis).
parent_of(robert,louis).
parent_of(stephen,louis).
parent_of(bernard,oscar).
parent_of(cathleen,oscar).
parent_of(daphne,oscar).
parent_of(fred,oscar).
parent_of(louis,oscar).
parent_of(edith,paul).
parent_of(andrew,sylvia).
parent_of(john,sylvia).
parent_of(robert,sylvia).
parent_of(stephen,sylvia).
parent_of(sylvia,william).

grandparent_of(ada,sylvia).
grandparent_of(edith,bernard).
grandparent_of(edith,cathleen).
grandparent_of(edith,daphne).
grandparent_of(edith,fred).
grandparent_of(edith,louis).
grandparent_of(george,oscar).
grandparent_of(louis,andrew).
grandparent_of(louis,john).
grandparent_of(louis,robert).
grandparent_of(louis,stephen).
grandparent_of(oscar,bernard).
grandparent_of(oscar,cathleen).
grandparent_of(oscar,daphne).
grandparent_of(oscar,fred).
grandparent_of(oscar,louis).
grandparent_of(paul,edith).
grandparent_of(sylvia,andrew).
grandparent_of(sylvia,john).
grandparent_of(sylvia,robert).
grandparent_of(sylvia,stephen).
grandparent_of(william,sylvia).

grandfather_of(ada,sylvia).
grandfather_of(edith,bernard).
grandfather_of(edith,cathleen).
grandfather_of(edith,daphne).
grandfather_of(edith,fred).
grandfather_of(edith,louis).
grandfather_of(george,oscar).
grandfather_of(louis,andrew).
grandfather_of(louis,john).
grandfather_of(louis,robert).
grandfather_of(louis,stephen).
grandfather_of(oscar,bernard).
grandfather_of(oscar,cathleen).
grandfather_of(oscar,daphne).
grandfather_of(oscar,fred).
grandfather_of(oscar,louis).
grandfather_of(paul,edith).
grandfather_of(sylvia,andrew).
grandfather_of(sylvia,john).
grandfather_of(sylvia,robert).
grandfather_of(sylvia,stephen).
grandfather_of(william,sylvia).

grandfather_of(ada,andrew).
grandfather_of(ada,john).
grandfather_of(ada,robert).
grandfather_of(ada,stephen).
grandfather_of(edith,andrew).
grandfather_of(edith,john).
grandfather_of(edith,robert).
grandfather_of(edith,stephen).

:- end_in_neg.
