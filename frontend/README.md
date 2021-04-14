
# MonAmi parser

The parser parses one formula according to the following
grammar.

```
<formula> ::=
    | <formula> '|' <formula>
    | <formula> '->' <formula>
    | <formula> '&' <formula>
    | '!' <formula>
    | <name> '<' <name>
    | <name> 'o' <name>
    | <name> 'i' <name>
    | <name> '(' <data> ')'
    | 'same' '(' <name> ',' <name> ')'
    | 'exist' <names> '.' <formula>
    | '(' <formula> ')'
    
 <name> ::= r'[a-zA-Z_][a-zA-Z0-9_\.]*'
 
 <names> ::= <name> | <names> ',' <name>
 
 <data> ::= <number> | <string>
 
 <number> ::= r'\d+'
 
 <string> ::= r'\"([^\\\n]|(\\.))*?\"'
```

The Boolean binary operators have precedence as follows: 
`|` and '->' have the same precedence, which is weaker than
the precedence of `&`, which is weaker than the precedence of 
`!`. So for example:

```
A < B & C < D | ! E < F & G < H
```

has the same meaning as this formula:

```
(A < B & C < D) | ((! E < F) & G < H)
```

