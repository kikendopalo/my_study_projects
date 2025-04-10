import ply.lex as lex
import ply.yacc as yacc


def parsing(s):
    tokens = (
        'NEGATION',
        'IMPLICATION',
        'VAR',
        'CONJUNCTION',
        'DISJUNCTION',
        'LPAREN',
        'RPAREN'
    )

    t_NEGATION = r'~'
    t_IMPLICATION = r'->'
    t_VAR = r'[a-zA-Z]'
    t_CONJUNCTION = r'/\\'
    t_DISJUNCTION = r'\\/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    t_ignore = " \t"

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    lexer = lex.lex()

    variables = {}
    closes = set({})

    def p_cnf_final(t):
        'cnf : cnf CONJUNCTION clause'
        t[0] = t[1]

    def p_statement_cnf(t):
        'cnf : clause'
        t[0] = t[1]

    def p_expression_group(t):
        'clause : LPAREN clause RPAREN'
        t[0] = t[2]

    def p_expression_clause(t):
        '''clause : variable IMPLICATION variable
                    | NEGATION variable IMPLICATION variable
                    | variable IMPLICATION NEGATION variable
                    | NEGATION variable IMPLICATION NEGATION variable
                    | variable DISJUNCTION variable
                    | NEGATION variable DISJUNCTION variable
                    | variable DISJUNCTION NEGATION variable
                    | NEGATION variable DISJUNCTION NEGATION variable'''
        if t[1] == '~':
            if t[3] == '->':
                if t[4] == '~':
                    closes.add(tuple(sorted([variables[t[2]], -variables[t[5]]], key=(lambda x: abs(x)))))
                else:
                    closes.add(tuple(sorted([variables[t[2]], variables[t[4]]], key=(lambda x: abs(x)))))
            else:
                if t[4] == '~':
                    closes.add(tuple(sorted([-variables[t[2]], -variables[t[5]]], key=(lambda x: abs(x)))))
                else:
                    closes.add(tuple(sorted([-variables[t[2]], variables[t[4]]], key=(lambda x: abs(x)))))
        else:
            if t[2] == '->':
                if t[3] == '~':
                    closes.add(tuple(sorted([-variables[t[1]], -variables[t[4]]], key=(lambda x: abs(x)))))
                else:
                    closes.add(tuple(sorted([-variables[t[1]], variables[t[3]]], key=(lambda x: abs(x)))))
            else:
                if t[3] == '~':
                    closes.add(tuple(sorted([variables[t[1]], -variables[t[4]]], key=(lambda x: abs(x)))))
                else:
                    closes.add(tuple(sorted([variables[t[1]], variables[t[3]]], key=(lambda x: abs(x)))))
        t[0] = '->'

    def p_expression_solo(t):
        '''clause : variable
                      | NEGATION variable'''
        if t[1] == '~':
            closes.add(-variables[t[2]])
            t[0] = t[2]
        else:
            closes.add(variables[t[1]])
            t[0] = t[1]

    def p_expression_var(t):
        'variable : VAR'
        if t[1] not in variables:
            variables[t[1]] = len(variables) + 1
        t[0] = t[1]

    def p_error(t):
        pass

    parser = yacc.yacc()
    parser.parse(s)
    return closes, variables


def is_satisfiable(s):
    cv = parsing(s)
    cnf = cv[0]
    additional_clauses = set({})
    satisfiable = True
    start_index = 1
    while True:
        cnf = list(cnf)
        for i in range(start_index, len(cnf)):
            for j in range(i):
                if type(cnf[i]) == int:
                    if type(cnf[j]) == int:
                        if cnf[i] == -cnf[j]:
                            satisfiable = False
                            break
                    else:
                        for k in range(len(cnf[j])):
                            if cnf[i] == -cnf[j][k]:
                                additional_clauses.add(cnf[j][-(k + 1)])
                else:
                    if type(cnf[j]) == int:
                        for k in range(len(cnf[i])):
                            if cnf[j] == -cnf[i][k]:
                                additional_clauses.add(cnf[i][-(k + 1)])
                    else:
                        for k in range(len(cnf[j])):
                            for m in range(len(cnf[i])):
                                if cnf[i][m] == -cnf[j][k]:
                                    temp_clause = [cnf[j][-(k + 1)], cnf[i][-(m + 1)]]
                                    if temp_clause[0] == temp_clause[1]:
                                        additional_clauses.add(temp_clause[0])
                                    elif temp_clause[0] == -temp_clause[1]:
                                        pass
                                    else:
                                        additional_clauses.add(tuple(sorted(temp_clause, key=(lambda x: abs(x)))))
            if not satisfiable:
                break
        if not satisfiable:
            break

        old_length = len(cnf)
        start_index = old_length
        cnf = set(cnf)
        cnf.update(additional_clauses)
        new_length = len(cnf)
        if old_length == new_length:
            break
    return satisfiable


def sat_assignment(s):
    cv = parsing(s)
    cnf = cv[0]
    variables = cv[1]
    answer_variables = {}
    additional_clauses = set({})
    satisfiable = True
    start_index = 1
    while True:
        cnf = list(cnf)
        for i in range(start_index, len(cnf)):
            for j in range(i):
                if type(cnf[i]) == int:
                    if type(cnf[j]) == int:
                        if cnf[i] == -cnf[j]:
                            satisfiable = False
                            break
                    else:
                        for k in range(len(cnf[j])):
                            if cnf[i] == -cnf[j][k]:
                                additional_clauses.add(cnf[j][-(k + 1)])
                else:
                    if type(cnf[j]) == int:
                        for k in range(len(cnf[i])):
                            if cnf[j] == -cnf[i][k]:
                                additional_clauses.add(cnf[i][-(k + 1)])
                    else:
                        for k in range(len(cnf[j])):
                            for m in range(len(cnf[i])):
                                if cnf[i][m] == -cnf[j][k]:
                                    temp_clause = [cnf[j][-(k + 1)], cnf[i][-(m + 1)]]
                                    if temp_clause[0] == temp_clause[1]:
                                        additional_clauses.add(temp_clause[0])
                                    elif temp_clause[0] == -temp_clause[1]:
                                        pass
                                    else:
                                        additional_clauses.add(tuple(sorted(temp_clause, key=(lambda x: abs(x)))))
            if not satisfiable:
                break
        if not satisfiable:
            break

        old_length = len(cnf)
        start_index = old_length
        cnf = set(cnf)
        cnf.update(additional_clauses)
        new_length = len(cnf)
        if old_length == new_length:
            var_counter = 0
            for i in list(variables.values()):
                counter = 0
                for j in cnf:
                    if type(j) == int:
                        if abs(j) != i:
                            counter += 1
                    else:
                        counter += 1
                if counter == new_length:
                    cnf.add(i)
                    break
                else:
                    var_counter += 1
            if var_counter == len(list(variables.values())):
                for i in cnf:
                    if type(i) == int:
                        answer_variables[list(variables.keys())[list(variables.values()).index(abs(i))]] = (i > 0)
                return answer_variables
