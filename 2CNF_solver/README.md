## Task

The input is a Boolean formula in 2-CNF, given as a string of symbols. A *literal* is a variable name 
(at least any small Latin letter should be a legal variable name) or its negation, denoted by `~`.
A *clause* is either a literal, or `(L1 \/ L2)`, or `(L1 -> L2)`, where `L1` and `L2` are literals.
Finally, the *2-CNF* is either one clause or a conjunction of two or more clauses, where conjunction is
denoted by `/\`.

Example: `p /\ (p -> q) /\ (p -> ~r) /\ (~r \/ ~s) /\ (s \/ ~q)`

The *first* task is to check whether the given 2-CNF is satisfiable. The *second* task is, given a 2-CNF,
report that it is not satisfiable or return one of its satisfying assignments.
