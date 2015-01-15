# -----------------------------------------------------------------------------
# @author globit
# This is template code of markdown generating by ply
# @update 2014-12-16
# @lience MIT
# -----------------------------------------------------------------------------
import sys

tokens = (
    'H1','H2','H3','STRONG','EM','HR', 'CR', 'TEXT', 'BR'
    )

# Tokens
t_H1     = r'\# '
t_H2     = r'\#\# '
t_H3     = r'\#\#\# '
t_STRONG = r'__ |\*\* '
t_EM     = r'_ |\* '
t_HR     = r'\-\-\-|\*\ \*\ \*'
t_BR     = r'==='


def t_TEXT(t):
    r'[a-zA-Z0-9\,\. \']+'
    t.value = str(t.value)
    return t

# t_ignore = " \t"

def t_CR(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# ------------------------------------
# definitions of parsing rules by yacc
# ------------------------------------
precedence = (
    )
names = {}

def p_body(p):
    '''body : statement'''

    # print("printtttttt")
    # for x in p:
    #     print(x)
    # print("printtttttt")
    htmlDom = '<body>' + p[1] + '</body>'
    f = file('output.html','w')
    f.write(htmlDom)
    f.close()
    print '<body>' + p[1] + '</body>'

def p_state(p):
    '''statement : expression
                 | statement CR expression
                 | statement CR
                 | CR'''

    # print("printtttttt")
    # for x in p:
    #     print(x)
    # print("printtttttt")

    
    if (len(p)==2):
        p[0] = str(p[1])
    elif (len(p) == 4):
        p[0] = str(p[1]) + str(p[3])
    elif (len(p) == 3):
        p[0] = str(p[1]) + '<br>'

def p_exp_cr(p):
    '''expression : H1 factor
                  | H2 factor
                  | H3 factor
                  | HR
                  | BR
                  |    factor'''


    # print("printtttttt")
    # for x in p:
    #     print(x)
    # print("printtttttt")

    # if (len(p) == 7):
    #     p[0] = '<hr></hr>'
    if (len(p) == 2):
        if p[1] == '---' or p[1] == '* * *':
            p[0] = '<hr></hr>'
        elif p[1] == '===':
            p[0] = '<h1></h1>'
        else:
            p[0] = '<p>' + str(p[1]) + '</p>'

    elif (len(p) == 3):
        if p[1] == '#':
            p[0] = '<h1>' + str(p[2]) + '</h1>'
        elif p[1] == '##':
            p[0] = '<h2>' + str(p[2]) + '</h2>'
        elif p[1] == '###': 
            p[0] = '<h3>' + str(p[2]) + '</h3>'
        

def p_factor_term(p):
    '''factor : factor STRONG term STRONG term
              | factor EM term EM term
              | term'''
    
    # print("printtttttt")
    # for x in p:
    #     print(x)
    # print("printtttttt")

    if (len(p) == 2):
        p[0] = str(p[1])
    elif (len(p) == 6):
        if p[2] == '**' or p[2] == '__':
            p[0] = str(p[1]) + '<strong>' + str(p[3]) + '</strong>' + str(p[5])
        if p[2] == '*'  or p[2] == '_' :
            p[0] = str(p[1]) + '<em>' + str(p[3]) + '</em>' + str(p[5])
        

def p_term_text(p):
    '''term : TEXT'''
    # print("printtttttt")
    # for x in p:
    #     print(x)
    # print("printtttttt")
    p[0] = p[1]

def p_error(p):
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")

import ply.yacc as yacc
yacc.yacc()

if __name__ == '__main__':
    filename = '../TestDocument/test01.md'
    yacc.parse(open(filename).read())
