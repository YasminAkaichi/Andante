% Mode Declarations
modeh(*, recommend(+user, -movie)).
modeb(*, m(+user)).
modeb(*, not_n(+user)).
modeb(*, not_n(+user)). 
modeb(*, f(+user)).
modeb(*, b18to24(+user)).
modeb(*, b25to34(+user)).
modeb(*, b35to44(+user)).
modeb(*, not_18to24(+user)).
modeb(*, not_25to34(+user)).
modeb(*, not_35to44(+user)).
modeb(*, action(+movie)).
modeb(*, comedy(+movie)).
modeb(*, drama(+movie)).
modeb(*, musical(+movie)).
modeb(*, not_action(+movie)).
modeb(*, not_comedy(+movie)).
modeb(*, not_drama(+movie)).
modeb(*, not_musical(+movie)).
modeb(*, watched(+user,-movie)).

% Determinations
determination(recommend/2, m/1).
determination(recommend/2, f/1).
determination(recommend/2, b18to24/1).
determination(recommend/2, b25to34/1).
determination(recommend/2, b35to44/1).
determination(recommend/2, not_18to24/1).
determination(recommend/2, not_25to34/1).
determination(recommend/2, not_35to44/1).
determination(recommend/2, action/1).
determination(recommend/2, comedy/1).
determination(recommend/2, drama/1).
determination(recommend/2, musical/1).
determination(recommend/2, not_action/1).
determination(recommend/2, not_comedy/1).
determination(recommend/2, not_drama/1).
determination(recommend/2, not_musical/1).
determination(recommend/2, watched/2).
% Background Knowledge
:- begin_bg.

not_comedy(A) :- drama(A).
not_comedy(A) :- musical(A).
not_comedy(A) :- action(A).

not_musical(A) :- drama(A).
not_musical(A) :- action(A).
not_musical(A) :- comedy(A).

not_action(A) :- drama(A).
not_action(A) :- musical(A).
not_action(A) :- comedy(A).

not_drama(A) :- musical(A).
not_drama(A) :- action(A).
not_drama(A) :- comedy(A).


m(1780).
not_18to24(1780).
not_25to34(1780).
b35to44(1780).
m(2790).
not_18to24(2790).
b25to34(2790).
not_35to44(2790).
m(3192).
b18to24(3192).
not_25to34(3192).
not_35to44(3192).
f(3664).
not_18to24(3664).
not_25to34(3664).
b35to44(3664).
m(3925).
not_18to24(3925).
b25to34(3925).
not_35to44(3925).
m(3999).
not_18to24(3999).
not_25to34(3999).
b35to44(3999).
m(4577).
not_18to24(4577).
not_25to34(4577).
b35to44(4577).
m(5285).
b18to24(5285).
not_25to34(5285).
not_35to44(5285).
action(153).
not_comedy(153).
not_drama(153).
not_musical(153).
not_action(953).
not_comedy(953).
drama(953).
not_musical(953).
action(1722).
not_comedy(1722).
not_drama(1722).
not_musical(1722).
action(2692).
not_comedy(2692).
not_drama(2692).
not_musical(2692).
not_action(223).
comedy(223).
not_drama(223).
not_musical(223).
not_action(3176).
not_comedy(3176).
drama(3176).
not_musical(3176).
not_action(3392).
comedy(3392).
not_drama(3392).
not_musical(3392).
not_action(1947).
not_comedy(1947).
not_drama(1947).
musical(1947).
watched(3664,953).
watched(5285,223).
watched(2790,3176).
watched(3999,1722).
watched(3925,2692).
watched(4577,1947).
watched(1780,3392).
watched(3192,153).

:- end_bg.
% Positive Examples
:- begin_in_pos.
recommend(3664,953).
recommend(5285,223).
recommend(2790,3176).
recommend(3999,1722).
recommend(3925,2692).
:- end_in_pos.

% Negative Examples
:- begin_in_neg.
recommend(4577,1947).
recommend(1780,3392).
recommend(3192,153).
:- end_in_neg.