# -----------------------------------------------------------------------------
# @author globit
# This is template code of markdown generating by ply
# @update 2014-12-16
# @lience MIT
# -----------------------------------------------------------------------------
import sys

tokens = (
    'H1','H2','H3','STRONG','EM','HR', 'CR', 'TEXT', 'BR', 'CODE', 'ATITLELEFT', 'ATITLERIGHT', 'ALINKLEFT', 'ALINKRIGHT', 'ALEFT', 'ARIGHT', 'LI', 'IMG', 'MULICODE', 'TABSTAR', 'TABTABSTAR',
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
t_MULICODE       = r'\`\`\`\n'
t_ATITLELEFT     = r'\['
t_ATITLERIGHT    = r'\]' 
t_ALINKLEFT      = r'\('
t_ALINKRIGHT     = r'\)'
t_ALEFT          = r'\<'
t_ARIGHT         = r'\>'
t_LI             = r'\+'
t_IMG            = r'\!'
t_TABSTAR        = r'\t\*'
t_TABTABSTAR     = r'\t\t\*'


def t_TEXT(t):
    r'[a-zA-Z0-9\.\, \'\"\:\/]+'
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

def p_state_segment(p):
    '''statement : segment
                 | statement EM subseg CR segment
                 | statement MULICODE segment MULICODE segment'''
    if len(p) == 2:
        p[0] = str(p[1])
    # if len(p) == 4:
    #     p[0] = str(p[1]) + '<ul>' + '<li>' + str(p[3]) + '</ul>'
    if len(p) == 6:
        if str(p[2]) == '*':

            p[0] = str(p[1]) + '<ul>' + '<li>' + str(p[3]) + '</ul>' + str(p[5])
        else:
            p[0] = str(p[1]) + '<code>' + str(p[3]) + '</code>' + str(p[5])

def p_subseg_subsubseg(p):
    '''subseg : segment
              | subseg TABSTAR subsubseg'''
    if len(p) == 4:
        p[0] = str(p[1]) + '</li>' + '<ul>' + '<li>' + str(p[3]) + '</ul>'
    elif len(p) == 2:
        p[0] = str(p[1]).replace("<p>","").replace("</p>","").replace("<br>","")
        
def p_subsubseg_subsubsubseg(p):
    '''subsubseg : segment
                 | subsubseg TABTABSTAR subsubsubseg CR TABTABSTAR subsubsubseg'''
    if len(p) == 7:
        p[0] = str(p[1]) + '</li>' + '<ul>' + '<li>' + str(p[3]) + '</li>' + '<li>' + str(p[6]) + '</ul>'
    elif len(p) == 2:
        p[0] = str(p[1]).replace("<p>","").replace("</p>","").replace("<br>","")

def p_subsubsubseg_list(p):
    '''subsubsubseg : list
                    '''
    if len(p) == 2:
        p[0] = str(p[1]) + '</li>'
    if len(p) == 4:
        p[0] = str(p[1]) + '</li>' + '<ul>' + '<li>' + str(p[3]) + '</ul>'
    

def p_state(p):
    '''segment   : expression
                 | segment CR ARIGHT list CR ARIGHT list
                 | segment CR expression
                 | segment CR
                 | CR expression
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
        if str(p[1]) == '\n':
            p[0] = str(p[2])
        elif str(p[1]) == '*':
            p[0] = str(p[2])
        else :
            p[0] = str(p[1]) + '<br>'
    elif (len(p) == 8):
        p[0] = str(p[1]) + '<blockquote><p>'  + str(p[4])  + str(p[7]) + '</p></blockquote>'


def p_list_cr(p):
    '''list : factor
            | HR'''
    if (len(p) == 2):
        # print("printtttttt")
        # for x in p:
        #     print(x)
        # print("printtttttt")
        if p[1] == '---' or p[1] == '* * *':
            p[0] = '<hr></hr>'
        else:
            p[0] = p[1]
    


def p_exp_cr(p):
    '''expression : H1 factor
                  | H2 factor
                  | H3 factor
                  | LI factor
                  | HR
                  | BR
                  | factor'''


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
            if str(p[1])[0:2] == '1.':
                p[0] = '<li>' + str(p[1])[2:] + '</li>'
            else:
                p[0] = '<p>' + str(p[1]) + '</p>'
            

    elif (len(p) == 3):
        if p[1] == '#':
            p[0] = '<h1>' + str(p[2]) + '</h1>'
        elif p[1] == '##':
            p[0] = '<h2>' + str(p[2]) + '</h2>'
        elif p[1] == '###': 
            p[0] = '<h3>' + str(p[2]) + '</h3>'
        elif p[1] == '+' :
            p[0] = '<li>' + str(p[2]) + '</li>'
        

def p_factor_term(p):
    '''factor : factor STRONG term STRONG term
              | STRONG term STRONG term
              | factor EM term EM term
              | factor CODE term CODE term
              | factor ATITLELEFT term ATITLERIGHT ALINKLEFT term ALINKRIGHT term
              | IMG ATITLELEFT term ATITLERIGHT ALINKLEFT term ALINKRIGHT
              | factor CODE EM term EM CODE term
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
        if p[1] == '!':
            p[0] = '<p><img src="' + str(p[6]) + '" alt="' + str(p[3]) + '"></p>'
        if p[2] == '`' and p[3] == '_':
            p[0] = str(p[1]) + '<code>' + str(p[3]) + str(p[4]) + str(p[5]) + '</code>' + str(p[7])
        
    elif (len(p) == 9):
        p[0] = str(p[1]) + '<a href="' + str(p[6]) + '">' + str(p[3]) + '</a>' + str(p[8])
        
def p_term_letter(p):
    '''term : letter'''
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
