# FLOW-MATIC 2025 Language Grammar

---

The following grammar is a modified EBNF formatted for [Bottlecaps.de](https://www.bottlecaps.de/rr/ui) and is provided for reference only.

Many thanks to [Bottlecaps.de](https://www.bottlecaps.de/rr/ui) for their excellent railroad diagram generator.

```ebnf
/* ===== PROGRAM STRUCTURE ===== */
program          ::= line+
line             ::= line-number? label? (use-extensions-statement | statement) comment?

/* ===== LINE NUMBERS ===== */
line-number      ::= digit digit digit digit  /* 0000-9999 */

/* ===== STATEMENTS ===== */
statement        ::= input-statement
                  | output-statement
                  | compare-statement
                  | move-statement
                  | jump-statement
                  | set-statement
                  | arithmetic-statement
                  | call-routine-statement
                  | stop-statement
                  | description-statement
                  | define-constant-statement
                  | encoding-statement
                  | date-time-statement
                  | format-statement
                  | record-statement
                  | collection-statement

/* === I/O STATEMENTS === */
input-statement  ::= ('INPUT' | 'READ') 'FROM' device-spec 'TO' variable-list
output-statement ::= ('OUTPUT' | 'WRITE') 'TO' device-spec ('RECORD' variable)?

/* === DATA MANIPULATION === */
compare-statement    ::= 'COMPARE' variable 'TO' constant-or-variable
move-statement       ::= 'MOVE' variable 'TO' variable
set-statement        ::= 'SET' variable 'TO' constant-or-variable
arithmetic-statement ::= variable ':=' expression

/* === CONTROL FLOW === */
jump-statement  ::= 'JUMP' 'TO' identifier ('UNLESS' condition)?
condition       ::= variable comparison-op constant-or-variable
comparison-op   ::= '=' | '<>' | '<' | '<=' | '>' | '>='

/* === DEFINITIONS === */
description-statement     ::= 'DEFINE' variable 'AS' string
define-constant-statement ::= 'CODE' 'CONSTANT' identifier 'IS' constant
constant                 ::= number 
                          | string 
                          | 'CR' | 'LF' | 'VTAB' | 'TAB' 
                          | 'NULL' | 'ESC'

/* ===== TOKENS ===== */
variable-list        ::= variable (',' variable)*
variable             ::= identifier
constant-or-variable ::= constant | variable
expression           ::= term (('+' | '-' | '&') term)*
term                 ::= factor (('*' | '/' | 'MOD') factor)*
factor               ::= variable 
                      | constant 
                      | '(' expression ')'

/* === IDENTIFIERS/LITERALS === */
identifier ::= letter (letter | digit | '_')*
number     ::= digit+ ('.' digit+)?
string     ::= '"' character* '"'
comment    ::= '*' character*

digit    ::= '0'..'9'
letter   ::= 'A'..'Z' | 'a'..'z'
character ::= #x20-#x7E /* Except '"' */

/* ===== EXTENSIONS ===== */
use-extensions-statement ::= 'USE' 'EXTENSIONS' extension-name (',' extension-name)*
extension-name ::= 'CONSOLE-IO' 
                 | 'ENCODING' 
                 | 'DATETIME' 
                 | 'CURRENCY'
                 | 'RECORDS' 
                 | 'COLLECTIONS' 
                 | 'MODERN-DEVICES'

/* === TEXT ENCODING === */
encoding-statement ::= 'CONFIG' 'TEXT-ENCODING' encoding-type (':' encoding-param)*
encoding-type      ::= 'ASCII' 
                    | 'UTF-8' 
                    | 'UTF-16' 
                    | 'UTF-32' 
                    | 'LATIN-1'
                    | 'ISO-8859-' ('1'..'16')
                    | 'CP437' 
                    | 'CP1252'
                    | 'EUC-JP' 
                    | 'SHIFT-JIS'
encoding-param     ::= 'ERRORS' '=' ('STRICT' | 'REPLACE' | 'IGNORE' | 'XMLCHARREFREPLACE')
                    | 'NORMALIZE' '=' ('NFC' | 'NFD' | 'NFKC' | 'NFKD')

/* === CONSOLE I/O === */
console-spec  ::= 'CONSOLE' console-unit (':' console-param)*
console-unit  ::= '1'  /* STDOUT */ 
                | '2'  /* STDERR */ 
                | '3'  /* STDIN */
console-param ::= 'BUFFER' '=' number 
                | 'NEWLINE' '=' ('CR' | 'LF' | 'CRLF')
                | 'ESCAPE' '=' ('NONE' | 'ANSI' | 'VT100')

/* === DATE/TIME === */
date-time-statement ::= 'GET' ('CURRENT-DATE' | 'CURRENT-TIME' | 'CURRENT-DATETIME') 
                        'INTO' variable (':' format-spec)?
                      | 'FORMAT' ('DATE' | 'TIME' | 'DATETIME') variable 
                        'AS' format-spec 'TO' variable
format-spec ::= 'ISO8601' | 'RFC2822' | 'LOCALE' | 'CUSTOM' string

/* === FORMATTING === */
format-statement ::= 'FORMAT' 'CURRENCY' variable 'AS' currency-spec 'TO' variable
                   | 'FORMAT' 'NUMBER' variable 'AS' number-spec 'TO' variable
currency-spec    ::= 'USD' | 'EUR' | 'JPY' | 'LOCALE' | 'CUSTOM' string
number-spec      ::= 'SCIENTIFIC' | 'PERCENT' | 'HEX' | 'CUSTOM' string

/* === RECORDS === */
record-statement    ::= 'DEFINE' 'RECORD' identifier field-definition+ 'END-RECORD'
field-definition    ::= identifier 'AS' ('STRING' | 'NUMBER' | 'DATE' | identifier)

/* === COLLECTIONS === */
collection-statement ::= 'DEFINE' 'COLLECTION' identifier 
                         'OF' ('STRING' | 'NUMBER' | 'RECORD' identifier)
                       | 'ADD' 'TO' identifier 'VALUE' constant-or-variable
                       | 'GET' 'FROM' identifier 'AT' number 'INTO' variable

/* === DEVICES === */
modern-device-spec ::= ('DISK' | 'NET' | 'USB') unit-spec? (':' supplemental-spec)+
supplemental-spec  ::= ('PATH' | 'ADDR' | 'PORT') (string | number)
                     | 'PROTOCOL' '=' ('HTTP' | 'FTP' | 'SSL')
```
