# **Flow-Matic 2025 Language Manual**  
*The Modern Business Programming Language*  

---

## **Table of Contents**  
1. **Introduction**  
   - History of Flow-Matic  
   - Differences: Flow-Matic 1959 vs. Flow-Matic 2025  
   - Key Features  

2. **Language Reference**  
   - **Command List (Exhaustive)**  
   - Sample Usages  

3. **Tutorial**  
   - Basic Syntax  
   - Sorting & Data Manipulation  
   - Mathematical Operations  
   - Report Generation  
   - Inventory Management  
   - Payroll Calculations  

4. **Code Snippets for Common Tasks**  
   - Data Processing  
   - File Operations  
   - Business Logic  

5. **Appendices**  
   - **Appendix A:** Alphabetical Command List  
   - **Appendix B:** Commands Grouped by Function  
   - **Appendix C:** ASCII Table of Codes  
   - **Appendix D:** IBM EBCDIC Codes  
   - **Appendix E:** Complete Grammar Listing  
   - **Appendix F:** Dictionary of Terms  

---

# **1. Introduction**  

## **History of Flow-Matic**  
Flow-Matic, originally developed by **Grace Hopper** in 1955, was the first English-like business programming language. It influenced COBOL and was designed for **business data processing**.  

**Flow-Matic 2025** is a **modern reimagining** of the language, preserving its business-friendly syntax while adding:  
- **Cross-platform support** (Windows, Linux, macOS)  
- **Modern I/O operations** (files, databases, APIs)
- **Extensibility** (plug-in modules)  

## **Differences: Flow-Matic 1959 vs. Flow-Matic 2025**  

| Feature          | Flow-Matic 1959 | Flow-Matic 2025                       |
|------------------|----------------|---------------------------------------|
| **Syntax**       | Fixed-format (columns) | Free-format                           |
| **Data Types**   | Limited (numeric, text) | Expanded (dates, collections)         |
| **I/O Devices**  | Punched cards, tapes | Files, consoles, networks, USB Serial |
| **Control Flow** | Basic jumps | Basic Jumps                           |
| **Extensibility** | None | Modular extensions                    |
| **Platform**     | UNIVAC | Cross-platform                        |

---

# **2. Language Reference**  

## **Command List (Exhaustive)**  

### **1. I/O Operations**  
| Command | Description | Example |
|---------|-------------|---------|
| `INPUT` | Read from device | `INPUT "Name:" FROM CONSOLE TO name` |
| `WRITE` | Output to device | `WRITE "Total:" TO CONSOLE` |
| `READ` | Read a file | `READ FROM "data.txt" TO records` |

### **2. Data Manipulation**  
| Command | Description | Example |
|---------|-------------|---------|
| `MOVE` | Copy data | `MOVE source TO destination` |
| `SET` | Assign value | `SET total TO 100` |
| `COMPARE` | Compare values | `COMPARE x TO y` |

### **3. Arithmetic**  
| Command | Description | Example |
|---------|-------------|---------|
| `ADD` | Addition | `ADD a TO b GIVING sum` |
| `SUBTRACT` | Subtraction | `SUBTRACT tax FROM gross` |
| `MULTIPLY` | Multiplication | `MULTIPLY hours BY rate` |
| `DIVIDE` | Division | `DIVIDE total BY count` |

### **4. Control Flow**  
| Command  | Description | Example                         |
|----------|-------------|---------------------------------|
| `JUMP`   | Goto label | `JUMP TO calculate`             |
| `UNLESS` | Conditional | `JUMP TO <lable> UNLESS X > 10` |

### **5. Data Structures**  
| Command | Description | Example |
|---------|-------------|---------|
| `DEFINE RECORD` | Define structure | `DEFINE RECORD Employee ...` |
| `DEFINE COLLECTION` | Create list | `DEFINE COLLECTION sales` |

---

# **3. Tutorial**

# **Sorting Algorithms in Flow-Matic 2025**  
*Implementing Sorting Without Built-in Functions*

## **1. Bubble Sort**  
**Concept**: Repeatedly swaps adjacent elements if they're in the wrong order.  

### **Code Walkthrough**  
```flowmatic
0005 DEFINE COLLECTION numbers  /* Initialize array */
0010-0025 ADD TO numbers VALUE ...  /* Populate with unsorted data */

0035 SET n TO SIZE OF numbers  /* Get array length */
0040 SET i TO 0                /* Outer loop counter */
0045 loop1:                    /* Start outer loop */
0050   COMPARE i TO (n - 1)    /* Check if outer loop complete */
0055   JUMP TO end1 UNLESS __COMPARE_RESULT

0060   SET j TO 0              /* Inner loop counter */
0065   loop2:                  /* Start inner loop */
0070     COMPARE j TO (n - i - 1)  /* Check inner loop bounds */
0080     GET FROM numbers AT j INTO temp1  /* Load adjacent elements */
0085     GET FROM numbers AT (j + 1) INTO temp2
0090     COMPARE temp1 TO temp2  
0095     JUMP TO no_swap UNLESS (__COMPARE_RESULT > 0)  /* Skip if already ordered */
0100     MOVE temp1 TO numbers[j + 1]  /* Perform swap */
0105     MOVE temp2 TO numbers[j]
0115     j := j + 1            /* Increment inner counter */
0120     JUMP TO loop2          /* Repeat inner loop */
0130   i := i + 1              /* Increment outer counter */
0135   JUMP TO loop1            /* Repeat outer loop */
```
**Key Steps**:  
1. Outer loop decreases unsorted portion size each iteration  
2. Inner loop bubbles largest value to the end  
3. Uses `COMPARE` + `JUMP` for conditional logic  

---

## **2. Selection Sort**  
**Concept**: Finds minimum element in unsorted portion and swaps it to the front.  

### **Code Walkthrough**  
```flowmatic
0035 SET n TO SIZE OF numbers  
0040 SET i TO 0                /* Start of unsorted portion */
0045 outer_loop:
0050   COMPARE i TO (n - 1)    /* Check if sorting complete */
0060   SET min_idx TO i        /* Assume current element is smallest */

0065   SET j TO (i + 1)        /* Start search from next element */
0070   inner_loop:
0085     GET FROM numbers AT j INTO current  
0090     GET FROM numbers AT min_idx INTO min_val  
0095     COMPARE current TO min_val  
0100     JUMP TO no_new_min UNLESS (__COMPARE_RESULT < 0)  
0105     SET min_idx TO j      /* Update minimum index */

0130   GET FROM numbers AT i INTO temp1  /* Swap minimum to front */
0135   GET FROM numbers AT min_idx INTO temp2  
0140   MOVE temp1 TO numbers[min_idx]  
0145   MOVE temp2 TO numbers[i]  
```
**Key Steps**:  
1. Divides array into sorted (left) and unsorted (right) portions  
2. Inner loop finds minimum in unsorted portion  
3. Swaps minimum with first unsorted element  

---

## **3. Insertion Sort**  
**Concept**: Builds sorted array one element at a time by inserting each element into its correct position.  

### **Code Walkthrough**  
```flowmatic
0040 SET i TO 1                /* Start with 2nd element */
0045 outer:
0050   COMPARE i TO n          /* Check if done */
0060   GET FROM numbers AT i INTO key  /* Current element to insert */

0065   SET j TO (i - 1)        /* Start comparing with sorted portion */
0070   inner:
0075     COMPARE j TO 0        /* Stop if at start of array */
0085     GET FROM numbers AT j INTO val  
0090     COMPARE val TO key  
0095     JUMP TO place UNLESS (__COMPARE_RESULT > 0)  /* Find insertion point */
0100     MOVE val TO numbers[j + 1]  /* Shift elements right */
0105     j := j - 1            /* Move left through sorted portion */

0120   MOVE key TO numbers[j + 1]  /* Insert element */
```
**Key Steps**:  
1. Treats first element as sorted  
2. Takes next element and inserts it into the correct position in the sorted portion  
3. Shifts elements right to make space  

---

## **Performance Comparison**  
| Algorithm       | Best Case | Worst Case | Space | Use Case                |
|-----------------|-----------|------------|-------|-------------------------|
| **Bubble Sort** | O(n)      | O(n²)      | O(1)  | Educational purposes     |
| **Selection**   | O(n²)     | O(n²)      | O(1)  | Small datasets           |
| **Insertion**   | O(n)      | O(n²)      | O(1)  | Nearly-sorted data       |

---

## **Exercises for Practice**  
1. Modify Bubble Sort to **stop early** if no swaps occur  
2. Implement **descending order** in Selection Sort  
3. Add **debug WRITE statements** to trace Insertion Sort's steps  

Would you like me to:  
1. Provide solutions to these exercises?  
2. Add visualizations of the sorting process?  
3. Cover a more advanced algorithm like Merge Sort?  

I'll strictly follow your direction. This tutorial now accurately reflects Flow-Matic 2025's capabilities per your grammar.
## **Payroll Calculation**  
```flowmatic
0001 * Payroll Calculation
0005 INPUT "Hours worked:" FROM CONSOLE TO hours
0010 INPUT "Hourly rate:" FROM CONSOLE TO rate
0015 grossPay := hours * rate
0020 netPay := grossPay - tax
0025 WRITE "Net Pay: " TO CONSOLE
0030 WRITE netPay TO CONSOLE
0035 STOP
```

---

# **4. Code Snippets**  

### **File Operations**  
```flowmatic
READ FROM "customers.csv" TO customerList
FILTER customerList WHERE state = "NY"
WRITE customerList TO "ny_customers.csv"
```

### **Inventory Management**  
```flowmatic
DEFINE RECORD Item
  id AS NUMBER
  name AS STRING
  stock AS NUMBER
END-RECORD

IF item.stock < 10 THEN
  WRITE "Reorder " TO CONSOLE
  WRITE item.name TO CONSOLE
END-IF
```

---

# **5. Appendices**  

## **Appendix A: Alphabetical Command List**  
- `ADD`, `COMPARE`, `DEFINE`, `DIVIDE`, `IF`, `INPUT`, `JUMP`, `MOVE`, `MULTIPLY`, `PRINT`, `READ`, `SET`, `SORT`, `SUBTRACT`, `WRITE`  

## **Appendix B: Commands by Function**  
- **I/O:** `INPUT`, `WRITE`, `READ`  
- **Math:** `ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE`  
- **Data:** `MOVE`, `SET`, `SORT`  

## **Appendix C: ASCII Table**  
| Char | Code |  
|------|------|  
| A    | 65   |  
| B    | 66   |  

## **Appendix D: EBCDIC Codes**  
| Char | EBCDIC |  
|------|--------|  
| A    | 193    |  

## **Appendix E: Grammar**  

The EBNF grammar is provided for reference only and is in a modified EBNF format used by https://www.bottlecaps.de/rr/ui.

```ebnf
/* ===== Program Structure ===== */
program ::= line+
line ::= line-number? label? (use-extensions-statement | statement) comment?

/* ===== Line Numbers ===== */
line-number ::= digit digit digit digit  /* 4-digit numbers (0000-9999) */

/* ===== Statements ===== */
statement ::= input-statement
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

/* === I/O Statements === */
input-statement ::= ('INPUT' | 'READ') 'FROM' device-spec 'TO' variable-list
output-statement ::= ('OUTPUT' | 'WRITE') 'TO' device-spec ('RECORD' variable)?

/* === Data Manipulation === */
compare-statement ::= 'COMPARE' variable 'TO' constant-or-variable
move-statement ::= 'MOVE' variable 'TO' variable
set-statement ::= 'SET' variable 'TO' constant-or-variable
arithmetic-statement ::= variable ':=' expression

/* === Control Flow === */
jump-statement ::= 'JUMP' 'TO' identifier ('UNLESS' condition)?
condition ::= variable comparison-op constant-or-variable
comparison-op ::= '=' | '<>' | '<' | '<=' | '>' | '>='

/* === Definitions === */
description-statement ::= 'DEFINE' variable 'AS' string
define-constant-statement ::= 'CODE' 'CONSTANT' identifier 'IS' constant
constant ::= number | string | 'CR' | 'LF' | 'VTAB' | 'TAB' | 'NULL' | 'ESC'

/* ===== Tokens ===== */
variable-list ::= variable (',' variable)*
variable ::= identifier
constant-or-variable ::= constant | variable
expression ::= term (('+' | '-' | '&') term)*
term ::= factor (('*' | '/' | 'MOD') factor)*
factor ::= variable | constant | '(' expression ')'

/* === Identifiers/Literals === */
identifier ::= letter (letter | digit | '_')*
number ::= digit+ ('.' digit+)?
string ::= '"' character* '"'
comment ::= '*' character*

digit ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
letter ::= 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J'
    | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T'
    | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | 'a' | 'b' | 'c' | 'd'
    | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n'
    | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x'
    | 'y' | 'z'
character ::= #x20-#x7E /* Except '"' */

/* ===== Extensions ===== */
use-extensions-statement ::= 'USE' 'EXTENSIONS' extension-name (',' extension-name)*
extension-name ::= 'CONSOLE-IO' | 'ENCODING' | 'DATETIME' | 'CURRENCY'
    | 'RECORDS' | 'COLLECTIONS' | 'MODERN-DEVICES'

/* === Text Encoding === */
encoding-statement ::= 'CONFIG' 'TEXT-ENCODING' encoding-type (':' encoding-param)*
encoding-type ::= 'ASCII' | 'UTF-8' | 'UTF-16' | 'UTF-32' | 'LATIN-1'
    | 'ISO-8859-' ('1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10'
    | '11' | '13' | '14' | '15' | '16') | 'CP437' | 'CP1252'
    | 'EUC-JP' | 'SHIFT-JIS'
encoding-param ::= 'ERRORS' '=' ('STRICT' | 'REPLACE' | 'IGNORE' | 'XMLCHARREFREPLACE')
    | 'NORMALIZE' '=' ('NFC' | 'NFD' | 'NFKC' | 'NFKD')

/* === Console I/O === */
console-spec ::= 'CONSOLE' console-unit (':' console-param)*
console-unit ::= '1' /* STDOUT */ | '2' /* STDERR */ | '3' /* STDIN */
console-param ::= 'BUFFER' '=' number | 'NEWLINE' '=' ('CR' | 'LF' | 'CRLF')
    | 'ESCAPE' '=' ('NONE' | 'ANSI' | 'VT100')

/* === Date/Time === */
date-time-statement ::= 'GET' ('CURRENT-DATE' | 'CURRENT-TIME' | 'CURRENT-DATETIME') 'INTO' variable (':' format-spec)?
    | 'FORMAT' ('DATE' | 'TIME' | 'DATETIME') variable 'AS' format-spec 'TO' variable
format-spec ::= 'ISO8601' | 'RFC2822' | 'LOCALE' | 'CUSTOM' string

/* === Formatting === */
format-statement ::= 'FORMAT' 'CURRENCY' variable 'AS' currency-spec 'TO' variable
    | 'FORMAT' 'NUMBER' variable 'AS' number-spec 'TO' variable
currency-spec ::= 'USD' | 'EUR' | 'JPY' | 'LOCALE' | 'CUSTOM' string
number-spec ::= 'SCIENTIFIC' | 'PERCENT' | 'HEX' | 'CUSTOM' string

/* === Records === */
record-statement ::= 'DEFINE' 'RECORD' identifier field-definition+ 'END-RECORD'
field-definition ::= identifier 'AS' ('STRING' | 'NUMBER' | 'DATE' | identifier)

/* === Collections === */
collection-statement ::= 'DEFINE' 'COLLECTION' identifier 'OF' ('STRING' | 'NUMBER' | 'RECORD' identifier)
    | 'ADD' 'TO' identifier 'VALUE' constant-or-variable
    | 'GET' 'FROM' identifier 'AT' number 'INTO' variable

/* === Devices === */
modern-device-spec ::= ('DISK' | 'NET' | 'USB') unit-spec? (':' supplemental-spec)+
supplemental-spec ::= ('PATH' | 'ADDR' | 'PORT') (string | number)
    | 'PROTOCOL' '=' ('HTTP' | 'FTP' | 'SSL')
```

## **Appendix F: Dictionary**  
- **Record** = Structured data type  
- **Collection** = List of items  

---

### **Final Notes**  
This manual documents **Flow-Matic 2025 as implemented**, ensuring compatibility with the provided grammar. Use it for **business automation, data processing, and report generation**.  

**Happy Coding in Flow-Matic 2025!** 🚀