# Grammar for Bed Spread


## Precedence
Precedence rules are fairly normal.
```
%bogus UMINUS
%left '(' '.'
%right '^'
%left '*' '/' '{'
%left '+' '-'
%left RELOP
%left NOT
%left LOGIC

%void WHEN THEN ELSE
%void_set punct
```


## Productions start

This is mostly a traditional-style infix expression syntax.
The one maybe-surprising caveat is there are no literal tuples.
Functions of several arguments are all keyword-only.
However, the `@` symbol provides anaphoric abbreviation,
which should encourage you to use consistent names for parameters.

```
start -> condex
  | $error$ :error

condex -> exp | cases otherwise :switch | sequence

exp -> grouping
  | LITERAL
  | NAME
  | exp '.' NAME :field_access
  | exp '(' argument ')'  :apply
  | exp '(' '@' ')'  :apply_anaphor
  | exp '(' $error$ ')' :broken_apply
  |     '-' exp   :prefix  %prec UMINUS
  | '{' custom '}' exp     :prefix  %prec UMINUS
  | exp '^' exp   :infix
  | exp '{' custom '}' exp :infix
  | exp '*' exp   :infix
  | exp '/' exp   :infix
  | exp '+' exp   :infix
  | exp '-' exp   :infix
  | exp RELOP exp :infix
  |       NOT exp :prefix
  | exp LOGIC exp :infix
  | '\' parameter grouping    :abstraction
  | '\' $error$ grouping :error
  | '(' $error$ ')' :error
  | '[' $error$ ']' :error
  | '{' $error$ '}' :error
  
argument -> exp | kwargs | kwargs ',' | sequence
parameter -> NAME | params

kwargs -> binding       :first_binding
  | kwargs ',' binding  :another_binding

binding -> NAME ':' exp :bind_expression
  | '@' NAME :bind_anaphor

params -> NAME NAME  :two_params
  | params NAME      :another_param

grouping -> '(' condex ')' | '[' condex ']'
  
cases -> case :first_case | cases case :another_case
case -> WHEN exp THEN exp ';' :case
otherwise -> ELSE exp

custom -> NAME | '^' | '*' | '/' | '+' | '-' | RELOP | LOGIC | NAME custom :adverbial

sequence ->  ':' items ':'
items -> :empty | ctl(exp) :list | ctl(pair) :dict
pair -> exp '->' exp

ctl(x) -> csl(x) | csl(x) ','
csl(x) -> x :first | csl(x) ',' x :more

```

## Definitions
This scanner does not attempt to recognize negative numbers.
This allows expressions like `3-1i` (without whitespace) to function properly.
For reference, the minus-sign in the above expression has ordinary subtraction precedence.

In a nod to human factors, you can use the underscore between digits to demarcate groups.
No attempt is made to restrict the groupings to any particular size;
you can separate each digit if you like. However, the separator cannot come first or last.

You can also use the separators in hexadecimal literals.
```
leadingDigit    [1-9]
moreDigits      {digit}+(_{digit})*
wholeNumber     0|{leadingDigit}(_?{moreDigits})?
mantissa        {wholeNumber}(\.{moreDigits})?
exponent        [Ee][-+]?{wholeNumber}
real            {mantissa}{exponent}?
hex             {xdigit}+(_{xdigit}+)*
sigil           ([#$]|0[xX])
```
## Patterns
Nothing fancy here, but the observant will note that complex numbers are supported.
```
{real}             :real
{real}[iI]         :imaginary
{sigil}{hex}       :hexadecimal
{alpha}{word}*     :word
\"[^"\v]*\"        :short_string
\s+                :ignore whitespace
<        :relop LT
<=       :relop LE
==?      :relop EQ
<>|!=    :relop NE
>=       :relop GE
>        :relop GT
->    |
{punct}            :punctuation
```
