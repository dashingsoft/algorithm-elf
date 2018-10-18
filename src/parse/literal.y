/*

算法语言分析器：

文档结构

entry: 主函数名称( 实际参数常量 )

函数定义或者过程定义

函数定义和过程定义使用类Pascal语法。

如果 Entry 部分为空，那么默认的入口点是第一个定义的函数

关键字：
entry,
procedure, function, const, var, type, record, array, of

for, while, if, do,

begin, end

integer, float, char, boolean, string

and or not + - * / = := <> > >= < <= <>

. ^ : ;

注释：使用大括号 {}，单行注释使用 //

 */

%{
#include <stdio.h>
  #define YYSTYPE char *
  #define BUFFER_SIZE 102400
  typedef void * yyscan_t;
  extern int yylex_init (yyscan_t* scanner);
  extern int yylex_destroy (yyscan_t yyscanner );
  extern void yyset_in  ( FILE * in_str, yyscan_t scanner );
  void yyerror (void *locp, void *scanner, char *buffer, char const *msg);
  static void print_token_value (FILE *, int, YYSTYPE);
  #define YYPRINT(file, type, value) print_token_value (file, type, value);
%}

%debug
%token-table
%pure-parser
%locations
%lex-param   {void *scanner}
%parse-param {void *scanner}
%parse-param {char *buffer}

%token  COMMENT_S               "{"
%token  COMMENT_E               "}"
%token  INLINE_COMMENT_S        "//"
%token  INLINE_COMMENT_E        "\n"

%token  TOK_NEGATIVE

%token  STRING
%token  NAME
%token  TYPENAME
%token  INTEGER
%token  NUMBER
%token  TRUE
%token  FALSE

%left '>' '<' '=' "<=" "<>" ">="
%left "or" "and"
%left '+' '-'
%left '*' '/'
%left '^'

%right "not"
%right TOK_NEGATIVE

%% /* Grammar rules and actions follow.  */

algorithm:  entry funcs
                  {
		    printf("%s\n%s\n",
			   $1 == NULL?"":$1,
			   $2 == NULL?"":$2
			   );
		    if ($1) free($1);
		    if ($2) free($2);
		  }
		;

entry:            /* Empty */
                | "entry" ':' stmt_call
		    { printf("\nentry:%s\n", $3); }
		;

funcs:             /* Empty */
                | decl_func
		| decl_func  ';' funcs
		;

decl_func:        func_header decls func_body
		;

func_header: 	  "function" NAME '(' paras ')' ':' TYPENAME  ';'
                | "procedure" NAME '(' paras ')' ';'
                ;

func_body:        "begin" stmts "end"
                ;

paras:             /* Empty */
                |  decl_para
	        |  decl_para ',' paras
		;

decl_para:         NAME ':' TYPENAME
                |  "var" NAME ':' TYPENAME
		;

decls:            /* Empty */
                | "const" constants decls
		| "var" vars decls
		| "type" types decls
		;

constants:        /* Empty */
                | decl_const ';' constants
                ;

decl_const:       NAME '=' INTEGER
                | NAME ':' "integer" '=' INTEGER
		| NAME ':' "string" '=' STRING
		| NAME ':' "double" '=' NUMBER
		| NAME ':' "boolean" '=' TRUE
		| NAME ':' "boolean" '=' FALSE
                ;

vars:             /* Empty */
                | decl_var ';' vars
                ;

decl_var:         NAME ':' TYPENAME
                ;

types:            /* Empty */
                | decl_type ';' types
                ;

decl_type:        NAME '=' TYPENAME
	        | NAME '=' '^' TYPENAME
		| NAME '=' "record" "of" vars "end"
                ;

stmts:            /* Empty */
                | stmt
                | stmt ';' stmts
                ;

stmt:             stmt_if
		| stmt_loop
		| stmt_assign
		| stmt_call
                ;

stmt_call:        NAME '(' exprs ')'
                ;

exprs:            /* Empty */
                | expr
                | expr ',' exprs
                ;

stmt_assign:      name ":=" expr
                ;

name:             NAME
                | NAME '^'
                | NAME '.' name
                ;

compound_stmt:    stmt
                | "begin" stmts "end"
                ;

stmt_if:          "if" expr "then" compound_stmt
                | "if" expr "then" "begin" stmts "end" "else" compound_stmt
                ;

stmt_loop:        "while" expr "do" compound_stmt
                | "repeat" stmts "until" expr
		| "for" name ":=" expr "to" expr "do" compound_stmt
                ;

expr:             STRING
                | NUMBER
                | INTEGER
                | TRUE
                | FALSE
                | name
                | '(' expr ')'
		| expr '+' expr
		| expr '-' expr
		| expr '*' expr
		| expr '/' expr
		| TOK_NEGATIVE expr
		| expr "and" expr
		| expr "or"  expr
		| "not" expr
		| expr '='  expr
                | expr "<>" expr
		| expr '>'  expr
		| expr '<'  expr
		| expr ">=" expr
		| expr "<=" expr
                ;

/* Error Recovery Rulers */

%%

int getTokenID(char * token_buffer)
{
  if ( token_buffer == NULL ) return 0;
  int i;
  for ( i = 0; i < YYNTOKENS; i++ ) {    
    if (   yytname[i] != 0
        && yytname[i][0] == '"'
	&& strncmp (yytname[i] + 1, token_buffer, strlen(token_buffer))
        && yytname[i][strlen(token_buffer) + 1] == '"'
	&& yytname[i][strlen(token_buffer) + 2] == 0) {
        return i;
    }
  }
  return 0;
}

static void
print_token_value (FILE *file, int type, YYSTYPE value)
{
  fprintf (file, "%s", value);
}

/* Called by yyparse on error.  */
void
yyerror (void *locp, void *scanner, char *buffer, char const *msg)
{
  fprintf (stderr, "%d:%s\n", ((YYLTYPE*)locp)->first_line, msg);
  //fprintf (stderr, "Error:%s\n",  msg);
}

int
main (int argc, char * argv[])
{
    yydebug = 1;

    char buffer[BUFFER_SIZE];
    yyscan_t scanner;
    FILE * infile;
    ++argv, --argc;  /* skip over program name */
    if ( argc > 0 ) {
      infile = fopen( argv[0], "r" );
      if ( infile == NULL ) {
	printf ( "Error when open file '%s'\n", argv [ 0 ] );
	return -1;
      }
    }
    else
        infile = stdin;

    printf("%s\n", "Start algorithm");
    yylex_init ( &scanner );
    yyset_in( infile, scanner );
    yyparse ( scanner, buffer );
    yylex_destroy ( scanner );

    fclose ( infile );
    return 0;
}
