% Mode Declarations
modeh(*, recommend(+user, +movie)).
modeb(*, b35to44(+user)).
modeb(*, b25to34(+user)).
modeb(*, b45to49(+user)).
modeb(*, b50to55(+user)).
modeb(*, plus56(+user)).
modeb(*, b18to24(+user)).
modeb(*, f(+user)).
modeb(*, m(+user)).
modeb(*, sci_fi(+movie)).
modeb(*, drama(+movie)).
modeb(*, horror(+movie)).
modeb(*, comedy(+movie)).
modeb(*, adventure(+movie)).
modeb(*, crime(+movie)).
modeb(*, action(+movie)).

% Determinations
determination(recommend/2, b35to44/1).
determination(recommend/2, b25to34/1).
determination(recommend/2, b45to49/1).
determination(recommend/2, b50to55/1).
determination(recommend/2, plus56/1).
determination(recommend/2, b18to24/1).
determination(recommend/2, f/1).
determination(recommend/2, m/1).
determination(recommend/2, sci_fi/1).
determination(recommend/2, drama/1).
determination(recommend/2, horror/1).
determination(recommend/2, comedy/1).
determination(recommend/2, adventure/1).
determination(recommend/2, crime/1).
determination(recommend/2, action/1).

% Background Knowledge
:- begin_bg.
action(m1374).
action(m1676).
adventure(m1259).
adventure(m2987).
b18to24(u1433).
b18to24(u1778).
b18to24(u2777).
b18to24(u3418).
b18to24(u4103).
b18to24(u4411).
b18to24(u621).
b25to34(u2840).
b25to34(u3123).
b25to34(u3539).
b25to34(u4138).
b25to34(u4560).
b25to34(u4607).
b25to34(u5077).
b35to44(u1197).
b45to49(u5127).
b50to55(u4981).
comedy(m19).
comedy(m2596).
comedy(m2888).
comedy(m3909).
comedy(m691).
crime(m47).
drama(m1178).
drama(m1619).
drama(m17).
drama(m1960).
drama(m337).
drama(m924).
f(u1433).
f(u3418).
f(u3539).
horror(m1348).
m(u1197).
m(u1778).
m(u2777).
m(u2840).
m(u3123).
m(u4083).
m(u4103).
m(u4138).
m(u4411).
m(u4560).
m(u4607).
m(u4981).
m(u5077).
m(u5127).
m(u621).
plus56(u4083).
sci_fi(m1206).


:- end_bg.

% Positive Examples
:- begin_in_pos.
recommend(u5127, m924).
recommend(u4411, m1619).
recommend(u4103, m1960).
recommend(u3418, m47).
recommend(u5077, m1348).
recommend(u3539, m2596).
recommend(u3123, m2987).
recommend(u621, m1259).
recommend(u4138, m17).
recommend(u4607, m1178).

:- end_in_pos.

% Negative Examples
:- begin_in_neg.
recommend(u1778, m2888).
recommend(u4981, m691).
recommend(u2840, m19).
recommend(u2777, m1374).
recommend(u4083, m1206).
recommend(u1433, m1676).
recommend(u1197, m3909).
recommend(u4560, m337).
:- end_in_neg.
