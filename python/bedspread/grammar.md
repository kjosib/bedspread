# Grammar for Bed Spread

This is not at all finished...
It started as a copy of the calculator example from booze-tools.

## Precedence
Precedence rules are fairly normal.
```
%bogus UMINUS
%left '('
%right '^'
%left '*' '/'
%left '+' '-'
%left RELOP
%left NOT
%left LOGIC
```

The so-called "void" symbols are but syntactic particles devoid of independent semantic value.
```
%void '(' ')' '[' ']' '{' '}' ',' '\' ':' ';' WHEN THEN ELSE
```


## Productions start

This is mostly an Euler-style expression syntax.
The one maybe-surprising caveat is there are no literal tuples.
Functions of several arguments are all keyword-only.

```
start -> exp
  | $error$ :error

exp -> '(' exp ')'   :parenthetical
  | exp '(' argument ')'  :apply
  | exp '(' $error$ ')' :broken_apply
  |     '-' exp   :unary  %prec UMINUS
  | exp '^' exp   :binary_operation
  | exp '*' exp   :binary_operation
  | exp '/' exp   :binary_operation
  | exp '+' exp   :binary_operation
  | exp '-' exp   :binary_operation
  | exp RELOP exp :binary_operation
  |       NOT exp :unary
  | exp LOGIC exp :binary_operation
  | NAME
  | LITERAL
  | block
  | '\' parameter block    :abstraction
  | '\' $error$ block :error
  | '(' $error$ ')' :error
  | '[' $error$ ']' :error
  | '{' $error$ '}' :error
  
argument -> exp | kwargs | kwargs ','
parameter -> NAME | params

kwargs -> binding       :first
  | kwargs ',' binding  :another

binding -> NAME ':' exp :bind

params -> NAME ',' NAME  :two_names
  | params ',' NAME      :another

block -> '[' exp ']' :block  | '{' cases otherwise '}' :switch

cases -> case :first | cases case :another
case -> WHEN exp THEN exp ';' :case
otherwise -> ELSE exp

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
\s+                :ignore whitespace
<        :relop LT
<=       :relop LE
==?      :relop EQ
<>|!=    :relop NE
>=       :relop GE
>        :relop GT
{punct}            :punctuation
```
