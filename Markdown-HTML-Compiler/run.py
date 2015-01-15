# -----------------------------------------------------------------------------
# @author globit
# This is template code of markdown generating by ply
# @update 2014-12-16
# @lience MIT
# -----------------------------------------------------------------------------
import sys

tokens = (
    'H1','H2','H3','STRONG','EM','HR', 'CR', 'TEXT', 'BR', 'CODE', 'ATITLELEFT', 'ATITLERIGHT', 'ALINKLEFT', 'ALINKRIGHT', 'ALEFT', 'ARIGHT', 'LI', 'NUMBER', 'IMG'
    )

# Tokens
t_H1             = r'\# '
t_H2             = r'\#\# '
t_H3             = r'\#\#\# '
t_STRONG         = r'__ |\*\* '
t_EM             = r'_ |\* '
t_HR             = r'\-\-\-|\*\ \*\ \*'
t_BR             = r'==='
t_CODE           = r'\`'
t_ATITLELEFT     = r'\['
t_ATITLERIGHT    = r'\]' 
t_ALINKLEFT      = r'\('
t_ALINKRIGHT     = r'\)'
t_ALEFT          = r'\<'
t_ARIGHT         = r'\>'
t_LI             = r'\+|1'
t_NUMBER         = r'[0-9]'
t_IMG            = r'\!'


def t_TEXT(t):
    r'[a-zA-Z\,\. \'\t\:\/]+'
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
                  | LI factor
                  | EM factor
                  | NUMBER factor
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
        elif p[1] == '+' or p[1] == '*':
            p[0] = '<li>' + str(p[2]) + '</li>'
        elif p[1] == '1':
            p[0] = '<li>' + str(p[2])[2:] + '</li>'
        

def p_factor_term(p):
    '''factor : factor STRONG term STRONG term
              | STRONG term STRONG term
              | factor EM term EM term
              | factor CODE term CODE term
              | factor ATITLELEFT term ATITLERIGHT ALINKLEFT term ALINKRIGHT term
              | IMG ATITLELEFT term ATITLERIGHT ALINKLEFT term ALINKRIGHT
              | ALEFT term ARIGHT
              | term'''
    
    # print("printtttttt")
    # for x in p:
    #     print(x)
    # print("printtttttt")

    if (len(p) == 2):
        p[0] = str(p[1])
    elif (len(p) == 4):
        if p[1] == '<':
            p[0] = '<a href=\"' + str(p[2]) + '">' + str(p[2]) + '</a>'


    elif (len(p) == 5):
        if p[1] == '**':
            p[0] = '<strong>' + str(p[2]) + '</strong>' + str(p[4])
    elif (len(p) == 6):
        if p[2] == '**' or p[2] == '__':
            p[0] = str(p[1]) + '<strong>' + str(p[3]) + '</strong>' + str(p[5])
        if p[2] == '*'  or p[2] == '_' :
            p[0] = str(p[1]) + '<em>' + str(p[3]) + '</em>' + str(p[5])
        if p[2] == '`':
            p[0] = str(p[1]) + '<code>' + str(p[3]) + '</code>' + str(p[5])
    elif (len(p) == 8):
        p[0] = '<p><img src="' + str(p[6]) + '" alt="' + str(p[3]) + '"></p>'
    elif (len(p) == 9):
        p[0] = str(p[1]) + '<a href="' + str(p[6]) + '">' + str(p[3]) + '</a>' + str(p[8])
        
def p_term_letter(p):
    '''term : letter'''

    if (len(p) == 3):
        p[0] = p[1] + p[2]
    elif (len(p) == 2):
        p[0] = p[1]
    

def p_term_text(p):
    '''letter : TEXT'''
    p[0] = p[1]

def p_error(p):
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")

import ply.yacc as yacc
yacc.yacc()

if __name__ == '__main__':
    filename = '../TestDocument/test copy.md'
    yacc.parse(open(filename).read())
