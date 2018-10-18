/*
 *
 * 算法语言分析器：
 *
 * 文档结构
 *
 * entry = 主函数名称( 实际参数常量 );
 *
 * 函数定义或者过程定义
 *
 * 函数定义和过程定义使用类Pascal语法。
 *
 * 如果 Entry 部分为空，那么默认的入口点是第一个定义的函数
 *
 * 关键字：
 *
 * entry,
 *
 * procedure, function, const, var, type, record, array, of
 *
 * for, while, if, do,
 *
 * begin, end
 *
 * integer, float, char, boolean, string
 *
 * and or not + - * / = := > >= < <= <>
 *
 * . ^ : ;
 *
 * 注释：使用大括号 {}，单行注释使用 //
 *
 * 备注
 *
 * XOX 是一个虚拟的二元操作符号，其优先级在二元操作符中为最高。
 *
 * 规则 expr: expr XOX expr 主要是为了保证二元操作符必定存在
 * 一个 lookahead token。因为最高优先级的运算符不会去读
 * lookahead token，所以如果没有这个虚拟的二元操作符，乘和除
 * 的运算不会读 lookahead token,从而无法正确折行。
 *
 * 目前暂不支持：
 *     with, case 语句
 *     子范围类型，Subrange
 *     in 运算符
 *
 */

%{
  #include <stdio.h>
  #include <limits.h>
  #include <parse.h>
  #define YYSTYPE char *
  typedef void * yyscan_t;
  extern int yylex_init (yyscan_t *);
  extern int yylex_destroy (yyscan_t);
  extern void yyset_in  ( FILE *, yyscan_t );
  void yyerror (void *, void *, PCONTEXT, char const *);

  int OUTPUT_WIDTH = 60;
  int INDENT_UNIT = 4;
%}

%debug
%token-table
%pure-parser
%locations

%lex-param   {void *scanner}
%parse-param {void *scanner}
%parse-param {PCONTEXT pcontext}

%token  ADD    '+'
%token  MINUS  '-'
%token  MUL    '*'
%token  DIV    '/'
%token  EQ     '='
%token  GT     '>'
%token  LT     '<'
%token  GE     ">="
%token  LE     "<="
%token  NE     "<>"

%token  AND    "and"
%token  OR     "or"
%token  NOT    "not"
%token  IN     "in"
%token  TRUE
%token  FALSE
%token  XOX

%token  DOT          '.'
%token  COMMA        ','
%token  COLON        ':'
%token  SEMICOLON    ';'
%token  INDICATOR    '^'

%token  IS           ":="

%token  LP    '('
%token  RP    ')'

%token  LSP   '['
%token  RSP   ']'

%token  ENTRY        "entry"
%token  PROCEDURE    "procedure"
%token  FUNCTION     "function"
%token  CONST        "const"
%token  VAR          "var"
%token  TYPE         "type"
%token  RECORD       "record"
%token  SET          "set"
%token  ARRAY	     "array"
%token  OF	     "of"
%token  FOR	     "for"
%token  WHILE	     "while"
%token  IF	     "if"
%token  DO	     "do"
%token  TO	     "to"
%token  REPEAT	     "repeat"
%token  UNTIL	     "until"
%token  ELSE	     "else"
%token  THEN	     "then"

%token  LB	     "begin"
%token  RB           "end"

%token  INTEGER      "integer"
%token  REAL         "real"
%token  CHAR         "char"
%token  BOOLEAN      "boolean"
%token  STRING       "string"

%token  TOK_STRING
%token  TOK_NAME
%token  TOK_TYPENAME
%token  TOK_INTEGER
%token  TOK_NUMBER

%left GT LT EQ LE NE GE
%left OR AND

%left ADD MINUS
%left MUL DIV
%left XOX

%right NOT
%right NEG

%destructor { free ( $$ ); } name expr exprs func_expr

%% /* Grammar rules and actions follow.  */

algorithm:  entry funcs
                                { /* 输出类结束语句 */
                                  print_class_end ( pcontext );
                                  pcontext -> indent -= INDENT_UNIT;
                                  /* 输出文件结束语句 */
                                  print_file_footer ( pcontext );
                                  }
                ;
entry:            /* Empty */
                | ENTRY EQ TOK_NAME
                ;

funcs:             /* Empty */
                | decl_func
                | decl_func SEMICOLON funcs
                ;

decl_func:        func_header decls func_body
                                { /*  */
                                  print_func_end ( @$.last_line, pcontext );
                                  pcontext -> findex ++;
                                  pcontext -> indent -= INDENT_UNIT;
				  pcontext -> indent -= INDENT_UNIT;
                                  }
                ;

func_header:      func_id TOK_NAME LP paras RP func_ret SEMICOLON
                                { int i;
                                  i = pcontext -> findex;
                                  if ( i >= MAX_FUNC_NUMBER ) {
                                    fprintf (
                                        stderr,
                                        "Error: The stack of Functions overflowed\n"
                                        );
                                    YYABORT;
                                  }
                                  pcontext -> funcs [ i ].name = strdup ( $2 );
                                  pcontext -> funcs [ i ].rettype = 0;

                                  /* 是否入口函数 */
                                  if ( i == 0 ) {
                                    print_class_begin ( pcontext );
                                    pcontext -> indent += INDENT_UNIT;
                                  }

                                  /* 打印函数头 */
                                  print_func_begin ( @$.first_line, pcontext );
                                  pcontext -> indent += INDENT_UNIT;
				  pcontext -> indent += INDENT_UNIT;
                                  }
                ;

func_id:          FUNCTION | PROCEDURE ;

func_ret:         /* Empty */
                | COLON TOK_TYPENAME
		;

func_body:        LB stmts RB ;

paras:             /* Empty */
                |  decl_para
                |  decl_para COMMA paras
                ;

decl_para:         para_names COLON TOK_TYPENAME
                            { PFUNC pfunc = pcontext -> funcs + pcontext -> findex;
                              int i;
                              for ( i = 0; i < MAX_PARA_NUMBER; i ++ ) {
                                if ( pfunc -> paras [ i ].name == 0 )
                                  break;
                                if ( pfunc -> paras [ i ].type == 0 ) {
                                  pfunc -> paras [ i ].varflag = 0;
                                  pfunc -> paras [ i ].type = strdup( $3 );
                                }
                              }
                             }
                |  VAR TOK_NAME COLON TOK_TYPENAME
                            { PFUNC pfunc = pcontext -> funcs + pcontext -> findex;
                              int i = 0;
                              while ( pfunc -> paras [ i ].name ) {
                                i ++;
                                if ( i > MAX_PARA_NUMBER ) {
                                  fprintf (
                                      stderr,
                                      "Error: The stack of Parameters overflowed\n"
                                      );
                                  YYABORT;
                                }
                              }
                              pfunc -> paras [ i ].varflag = 1;
                              pfunc -> paras [ i ].name = strdup( $2 );
                              pfunc -> paras [ i ].type = strdup( $4 );
                             }
                ;


para_names:        TOK_NAME { PFUNC pfunc = pcontext -> funcs + pcontext -> findex;
                              int i = 0;
                              while ( pfunc -> paras [ i ].name ) {
                                i ++;
                                if ( i > MAX_PARA_NUMBER ) {
                                  fprintf (
                                      stderr,
                                      "Error: The stack of Parameters overflowed\n"
                                      );
                                  YYABORT;
                                }
                              }
                              pfunc -> paras [ i ].name = strdup( $1 );
                             }

                |  TOK_NAME
                             { PFUNC pfunc = pcontext -> funcs + pcontext -> findex;
                              int i = 0;
                              while ( pfunc -> paras [ i ].name ) {
                                i ++;
                                if ( i > MAX_PARA_NUMBER ) {
                                  fprintf (
                                      stderr,
                                      "Error: The stack of Parameters overflowed\n"
                                      );
                                  YYABORT;
                                }
                              }
                              pfunc -> paras [ i ].name = strdup( $1 );
                             }
                   COMMA para_names
                ;

decls:            /* Empty */
                | CONST constants decls
                | VAR vars decls
                                { /* 输出变量表，然后重新初始化 */
                                  PVAR pvar = pcontext -> vars;
                                  int i;
                                  for ( i = 0; i < MAX_VARS_NUMBER; i ++, pvar ++ ) {
                                    if ( ! pvar -> name )
                                      break;
                                    print_indent( pcontext -> indent );
                                    printf(
                                            "%s = %s()\n",
                                            pvar -> name,
                                            pvar -> type
                                            );
				    print_indent(pcontext -> indent);
                                    printf("%s.name = '%s'\n", pvar -> name, pvar -> name);
                                    free ( pvar -> name );
                                    free ( pvar -> type );
                                    pvar -> name = 0;
                                    pvar -> type = 0;
                                  }
                                }
                | TYPE types decls
                ;

constants:        /* Empty */
                | decl_const SEMICOLON constants
                ;

decl_const:       TOK_NAME EQ TOK_INTEGER
                                { /*  输出常量 */
                                  print_indent(pcontext -> indent);
                                  printf("%s = Integer()\n", $1);
				  print_indent(pcontext -> indent);
                                  printf("%s.name = '%s'\n", $1, $3);
				  print_indent(pcontext -> indent);
                                  printf("%s.set(%s)\n", $1, $3);
                                }
                | TOK_NAME COLON TOK_TYPENAME EQ TOK_INTEGER
                                { /*  输出常量 */
				  print_indent(pcontext -> indent);
                                  printf("%s = %s()\n", $1, $3);
				  print_indent(pcontext -> indent);
                                  printf("%s.name = '%s'\n", $1, $5);
				  print_indent(pcontext -> indent);
                                  printf("%s.set(%s)\n", $1, $5);
                                }
                ;

vars:             /* Empty */
                | decl_var SEMICOLON vars
                ;

decl_var:         var_names COLON TOK_TYPENAME
                            { PVAR pvar = pcontext -> vars;
                              int i;
                              for ( i = 0; i < MAX_VARS_NUMBER; i ++ ) {
                                if ( pvar -> name == 0 )
                                  break;
                                if ( pvar -> type == 0 )
                                  pvar -> type = strdup( $3 );
                                pvar ++;
                              }
                             }
                ;

var_names:        TOK_NAME  { PVAR pvar = pcontext -> vars;
                              int i = 0;
                              while ( pvar -> name ) {
                                i ++;
                                pvar ++;
                                if ( i > MAX_VARS_NUMBER ) {
                                  fprintf (
                                      stderr,
                                      "Error: The stack of Variables overflowed\n"
                                      );
                                  YYABORT;
                                }
                              }
                              pvar -> name = strdup( $1 );
                             }
                | TOK_NAME
                            { PVAR pvar = pcontext -> vars;
                              int i = 0;
                              while ( pvar -> name ) {
                                i ++;
                                pvar ++;
                                if ( i > MAX_VARS_NUMBER ) {
                                  fprintf (
                                      stderr,
                                      "Error: The stack of Variables overflowed\n"
                                      );
                                  YYABORT;
                                }
                              }
                              pvar -> name = strdup( $1 );
                             }
                  COMMA var_names
                ;

types:            /* Empty */
                | decl_type SEMICOLON types
                ;

decl_type:        TOK_NAME EQ TOK_NAME
                                {
				  print_indent(pcontext -> indent);
                                  printf("class %s(%s): pass\n", $1, $3);
                                }
                | TOK_NAME EQ INDICATOR TOK_NAME
                                {
				  print_indent(pcontext -> indent);
                                  printf("class %s(Pointer): pass\n", $1, $3);
                                }
		| TOK_NAME EQ ARRAY OF TOK_NAME
                                {
				  print_indent(pcontext -> indent);
                                  printf("class %s(Array): pass\n", $1, $3);
                                }
		| TOK_NAME EQ SET OF TOK_NAME
                                {
				  print_indent(pcontext -> indent);
                                  printf("class %s(Set): pass\n", $1);
                                }
                | TOK_NAME EQ LP items RP
		                {
				  print_indent(pcontext -> indent);
                                  printf("class %s(Enum): pass\n", $1);
				  pcontext -> enum_counter = 0;
                                }
                | TOK_NAME EQ RECORD OF vars RB
                                {
				  print_indent(pcontext -> indent);
                                  printf("class %s(Record): pass\n", $1, $3);
                                }
                ;

items:            TOK_NAME
                                {
				  print_indent(pcontext -> indent);
                                  printf("global %s\n", $1);
				  print_indent(pcontext -> indent);
				  printf("%s = %d\n", $1, pcontext -> enum_counter);
				  pcontext -> enum_counter ++;
                                }
                | TOK_NAME
		                {
				  print_indent(pcontext -> indent);
                                  printf("global %s\n", $1);
				  print_indent(pcontext -> indent);
				  printf("%s = %d\n", $1, pcontext -> enum_counter);
				  pcontext -> enum_counter ++;
                                }
		  COMMA items
                ;

stmts:            /* Empty */
                | SEMICOLON
                | stmt
                | stmt SEMICOLON stmts
                ;

stmt:             stmt_if
                | stmt_loop
                | stmt_assign
                | expr
                                {
				  print_indent(pcontext -> indent);
				  increase_indent(
                                                  pcontext -> stmt,
                                                  MAX_STMT_SIZE,
                                                  $1,
                                                  pcontext -> indent
                                                  );
				  printf("%s\n", pcontext -> stmt);
				}
                ;

exprs:            /* Empty */   { $$ = strdup( "" ); }
                | expr          { $$ = strdup( $1 ); }
                | expr COMMA exprs
                                { /* 以逗号分开的多个表达式 */
                                  snprintf (
                                      pcontext -> expr,
                                      MAX_EXPR_SIZE,
                                      "%s,\n%s",
                                      $1,
                                      $3
                                      );
                                  $$ = strdup ( pcontext -> expr );
                                }
                ;

stmt_assign:      name IS   { pcontext -> indent += strlen($1) + 5; }
                  expr
                                { /*  */
                                  int len = strlen( $1 ) + 5;
				  pcontext -> indent -= len;
                                  if ( snprintf(pcontext -> stmt,
                                                MAX_STMT_SIZE,
                                                "%s.set(",
                                                $1
                                                )
                                       < 0
                                       ){
                                    fprintf ( stderr, "Error: memory fault\n" );
                                    YYABORT;
                                  }
                                  increase_indent(
                                                  pcontext -> stmt + len,
                                                  MAX_STMT_SIZE - len - 2,
                                                  $4,
                                                  len + pcontext -> indent
                                                  );
				  strcpy(pcontext -> stmt + strlen(pcontext -> stmt), ")");
                                  print_stmt ( @$.first_line, pcontext );
                                }
                ;

name:             TOK_NAME                { $$ = strdup ( $1 ); }
                | TOK_NAME INDICATOR
                                { /*  指针 */
                                  snprintf (
                                            pcontext -> stmt,
                                            MAX_STMT_SIZE,
                                            "%s.get()",
                                            $1
                                            );
                                  $$ = strdup ( pcontext -> stmt );
                                }
		| TOK_NAME LSP expr RSP
                                { /*  数组 */
                                  snprintf (
                                            pcontext -> stmt,
                                            MAX_STMT_SIZE,
                                            "%s[%s]",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> stmt );
                                }
                | name DOT TOK_NAME
                                { /*  结构 */
                                  snprintf (
                                            pcontext -> stmt,
                                            MAX_STMT_SIZE,
                                            "%s[%s]",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> stmt );
                                }
                | func_expr     { $$ = strdup($1) }
                ;

compound_stmt:    stmt
                | LB stmts RB
                ;

stmt_if:          stmt_if_part compound_stmt
                                { /* 减少一个缩进单位 */
                                  pcontext -> indent -= INDENT_UNIT;
                                }
                | stmt_if_part compound_stmt ELSE
                                { /* 规则中动作 */
                                  print_indent ( pcontext -> indent - INDENT_UNIT );
                                  printf ( "else:\n" );
                                }
                  compound_stmt
                                { /* 减少一个缩进单位 */
                                  pcontext -> indent -= INDENT_UNIT;
                                }
                ;

stmt_if_part:    IF expr THEN
                                { /*  */
                                  if ( snprintf ( pcontext -> stmt,
                                                  MAX_STMT_SIZE,
                                                  "if %s:",
                                                  $2
                                                  ) < 0 ) {
                                    fprintf ( stderr, "Error: memory fault\n" );
                                    YYABORT;
                                  }
                                  print_control_stmt ( @$.first_line, pcontext );

                                  /* 增加一个缩进单位 */
                                  pcontext -> indent += INDENT_UNIT;
                                }
                ;

stmt_loop:        WHILE expr DO
                                { /* 打印语句头部，规则中动作 */
                                  if ( snprintf ( pcontext -> stmt,
                                                  MAX_STMT_SIZE,
                                                  "while %s:",
                                                  $2
                                                  ) < 0 ) {
                                    fprintf ( stderr, "Error: memory fault\n" );
                                    YYABORT;
                                  }
                                  print_control_stmt ( @$.first_line, pcontext );

                                  /* 增加一个缩进单位 */
                                  pcontext -> indent += INDENT_UNIT;
                                }
                  compound_stmt
                                { /* 减少一个缩进单位 */
                                  pcontext -> indent -= INDENT_UNIT;
                                }
                | REPEAT stmts
                                { /* 打印语句头部，规则中动作 */
                                  if ( snprintf ( pcontext -> stmt,
                                                  MAX_STMT_SIZE,
                                                  "while True:",
                                                  $2
                                                  ) < 0 ) {
                                    fprintf ( stderr, "Error: memory fault\n" );
                                    YYABORT;
                                  }
                                  print_control_stmt ( @$.first_line, pcontext );

                                  /* 增加一个缩进单位 */
                                  pcontext -> indent += INDENT_UNIT;
                                }
                  UNTIL expr
                                { /* 打印语句结束 */
                                  if ( snprintf ( pcontext -> stmt,
                                                  MAX_STMT_SIZE,
                                                  "if %s: break",
                                                  $5
                                                  ) < 0 ) {
                                    fprintf ( stderr, "Error: memory fault\n" );
                                    YYABORT;
                                  }
                                  print_stmt ( @$.first_line, pcontext );

                                  /* 减少一个缩进单位 */
                                  pcontext -> indent -= INDENT_UNIT;
                                }
                | FOR name IS expr TO expr DO
                                { /* 打印语句头部，规则中动作 */
                                  if ( snprintf ( pcontext -> stmt,
                                                  MAX_STMT_SIZE,
                                                  "for %s in range ( %s, %s ):",
                                                  $2,
                                                  $4,
                                                  $6
                                                  ) < 0 ) {
                                    fprintf ( stderr, "Error: memory fault\n" );
                                    YYABORT;
                                  }
                                  print_control_stmt ( @$.first_line, pcontext );

                                  /* 增加一个缩进单位 */
                                  pcontext -> indent += INDENT_UNIT;
                                }
                  compound_stmt
                                { /* 减少一个缩进单位 */
                                  pcontext -> indent -= INDENT_UNIT;
                                }
                ;

func_expr:        TOK_NAME LP { pcontext -> indent += INDENT_UNIT; }
                  exprs RP
                                { /*  恢复当前缩进 */
				  pcontext -> indent -= INDENT_UNIT;

				  /* 判断是否类方法，如果是类的方法 */
				  char * prefix;
				  prefix = strdup("self.");

				  if ( strlen( $4 ) == 0 ){
				    /* 没有实参的函数输出 */
				    snprintf ( pcontext -> expr,
					       MAX_EXPR_SIZE,
					       "%s%s()",
					       prefix,
					       $1
					       );
				  }
				  else {

				    if ( pcontext -> indent
				         + strlen( $1 )
				         + strlen( $4 )
				         + 4
				         < OUTPUT_WIDTH
				         ){
				      /* 没有折行的函数调用输出 */
				      snprintf( pcontext -> expr,
                                                MAX_EXPR_SIZE,
                                                "%s%s(%s)",
						prefix,
                                                $1,
                                                merge_expr( $4 )
                                                );

				      }
				      else {
					/* 折行输出 */
					snprintf( pcontext -> expr,
						  MAX_EXPR_SIZE,
						  "%s%s(",
						  prefix,
						  $1
						  );
					int len = strlen( pcontext -> expr);
					int indent = INDENT_UNIT;
					increase_indent( pcontext -> expr + len,
							 MAX_EXPR_SIZE - len,
							 "\n",
							 indent
							 );
					len = strlen( pcontext -> expr);
				        increase_indent( pcontext -> expr + len,
							 MAX_EXPR_SIZE - len,
							 $4,
							 indent
							 );
					len = strlen( pcontext -> expr);
					increase_indent( pcontext -> expr + len,
							 MAX_EXPR_SIZE - len,
							 "\n)",
							 indent
							 );
				      }
				  }
				  if (strcmp(prefix, "self.") == 0){				  
				    print_call_expr(@$.first_line, pcontext);
				    $$ = strdup("_ret_of_%s", $1);
				  }
				  else
				    $$ = strdup(pcontext -> expr);
                                }
                ;


expr:             TOK_STRING        { $$ = strdup ( $1 ); }
                | TOK_NUMBER        { $$ = strdup ( $1 ); }
                | TOK_INTEGER       { $$ = strdup ( $1 ); }
                | TRUE              { $$ = strdup ( "True" ); }
                | FALSE             { $$ = strdup ( "False" ); }
                | name              { $$ = strdup ( $1 ); }
                | expr XOX expr     { $$ = $1 == $3 ? $3 : $1; }
                | LP { pcontext -> indent += 2; }
                  expr
                  RP
                                { /*  */
                                  pcontext -> indent -= 2;
                                  snprintf( pcontext -> expr,
					    MAX_EXPR_SIZE,
					    "( "
					    );
                                  increase_indent(
						  pcontext -> expr + 2,
                                                  MAX_EXPR_SIZE - 2,
                                                  $3,
                                                  2
                                                  );
                                  strncat( pcontext -> expr,
					   " )",
					   MAX_EXPR_SIZE
					   - strlen( pcontext -> expr )
					   - 4
					  );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr ADD { pcontext -> indent += 2; }
                  expr
                                { /*  */
                                  int len = strlen( $1 );
                                  pcontext -> indent -= 2;
                                  /* 判断下一个运算符是否同级 */
                                  if ( ( yychar == ADD )
                                       || ( yychar == MINUS )
                                       ){
                                       /* 需要换行处理 */
                                    snprintf( pcontext -> expr,
                                              MAX_EXPR_SIZE,
                                              "%s\n+ ",
                                              $1
                                              );
                                    increase_indent(
                                                    pcontext -> expr + len + 3,
                                                    MAX_EXPR_SIZE - len - 3,
                                                    $4,
                                                    2
                                                    );
                                  }
                                  else if ( pcontext -> indent
                                            + len
                                            + 3
                                            + strlen( $4 )
                                            < OUTPUT_WIDTH
                                            ){
                                    /* 不同级运算符，无需换行 */
                                    snprintf(
                                             pcontext -> expr,
                                             MAX_EXPR_SIZE,
                                             "%s + %s",
                                             merge_expr( $1 ),
                                             merge_expr( $4 )
                                             );
                                  }
                                  else {
                                    /* 需要换行处理 */
                                    snprintf( pcontext -> expr,
                                              MAX_EXPR_SIZE,
                                              "%s\n+ ",
                                              $1
                                              );
                                    increase_indent(
                                                    pcontext -> expr + len + 3,
                                                    MAX_EXPR_SIZE - len - 3,
                                                    $4,
                                                    2
                                                    );
                                  }
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr MINUS expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            "%s - %s",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr MUL { pcontext -> indent += 2; }
                  expr
                                { /*  */
                                  int len = strlen( $1 );
                                  pcontext -> indent -= 2;
                                  /* 判断下一个运算符是否同级 */
                                  if ( ( yychar == MUL )
                                       || ( yychar == DIV )
                                       ){
                                       /* 需要换行处理 */
                                    snprintf( pcontext -> expr,
                                              MAX_EXPR_SIZE,
                                              "%s\n* ",
                                              $1
                                              );
                                    increase_indent(
                                                    pcontext -> expr + len + 3,
                                                    MAX_EXPR_SIZE - len - 3,
                                                    $4,
                                                    2
                                                    );
                                  }
                                  else if ( pcontext -> indent
                                            + len
                                            + 3
                                            + strlen( $4 )
                                            < OUTPUT_WIDTH
                                            ){
                                    /* 不同级运算符，无需换行 */
                                    snprintf(
                                             pcontext -> expr,
                                             MAX_EXPR_SIZE,
                                             "%s * %s",
                                             merge_expr( $1 ),
                                             merge_expr( $4 )
                                             );
                                  }
                                  else {
                                    /* 需要换行处理 */
                                    snprintf( pcontext -> expr,
                                              MAX_EXPR_SIZE,
                                              "%s\n* ",
                                              $1
                                              );
                                    increase_indent(
                                                    pcontext -> expr + len + 3,
                                                    MAX_EXPR_SIZE - len - 3,
                                                    $4,
                                                    2
                                                    );
                                  }
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr DIV expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            "%s / %s",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | MINUS expr %prec NEG
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            " -%s ",
                                            $2
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr AND { pcontext -> indent += 4; }
                  expr
                                { /*  */
                                  int len = strlen( $1 );
                                  pcontext -> indent -= 4;
                                  /* 判断下一个运算符是否同级 */
                                  if ( ( yychar == AND )
                                       || ( yychar == OR )
                                       ){
                                       /* 需要换行处理 */
                                    snprintf( pcontext -> expr,
                                              MAX_EXPR_SIZE,
                                              "%s\nand ",
                                              $1
                                              );
				    len = strlen( pcontext -> expr );
                                    increase_indent(
                                                    pcontext -> expr + len,
                                                    MAX_EXPR_SIZE - len,
                                                    $4,
                                                    4
                                                    );
                                  }
                                  else if ( pcontext -> indent
                                            + len
                                            + 5
                                            + strlen( $4 )
                                            < OUTPUT_WIDTH
                                            ){
                                    /* 不同级运算符，无需换行 */
                                    snprintf(
                                             pcontext -> expr,
                                             MAX_EXPR_SIZE,
                                             "%s and %s",
                                             merge_expr( $1 ),
                                             merge_expr( $4 )
                                             );
                                  }
                                  else {
                                    /* 需要换行处理 */
                                    snprintf( pcontext -> expr,
                                              MAX_EXPR_SIZE,
                                              "%s\nand ",
                                              $1
                                              );
				    len = strlen( pcontext -> expr );
                                    increase_indent(
                                                    pcontext -> expr + len,
                                                    MAX_EXPR_SIZE - len,
                                                    $4,
                                                    4
                                                    );
                                  }
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr OR expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            "%s or %s",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | NOT expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            " not %s",
                                            $2
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr EQ expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            "%s = %s",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr NE expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            "%s + %s",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr GT expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            "%s > %s",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr LT expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            "%s < %s",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr GE expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            "%s >= %s",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                | expr LE expr
                                { /*  */
                                  snprintf (
                                            pcontext -> expr,
                                            MAX_EXPR_SIZE,
                                            "%s <= %s",
                                            $1,
                                            $3
                                            );
                                  $$ = strdup ( pcontext -> expr );
                                }
                ;

/* Error Recovery Rulers */

%%

/* Called by yyparse on error.  */
void
yyerror (void *locp, void *scanner, PCONTEXT pcontext, char const *msg)
{
  fprintf (stderr, "Line %d:%s\n", ((YYLTYPE*)locp)->first_line, msg);
  //fprintf (stderr, "Error:%s\n",  msg);
}

int
main (int argc, char * argv[])
{
  CONTEXT context;
  yyscan_t scanner;
  FILE * infile;
  int i,j;

  ++argv, --argc;  /* skip over program name */

  if ( ( argc > 0 ) && ( strcmp( argv [ 0 ], "-d" ) == 0 ) ) {
    yydebug = 1;
    ++argv, --argc;  /* skip over this option */
  }
  else
    yydebug = 0;

  if ( argc == 0 ) {
    fprintf ( stderr, "Error: no specify filename found\n" );
    return -1;
  }
  infile = fopen( argv[0], "r" );
  if ( infile == NULL ) {
    fprintf ( stderr, "Error: can't open file '%s'\n", argv [ 0 ] );
    return -2;
  }

  /* 初始化上下文 */
  memset( &context, 0, sizeof( CONTEXT ) );

  /* 初始化算法名称 */
  char * filename = strdup ( ( char * )basename ( argv [ 0 ] ) );
  if ( strchr ( filename, '.' ) )
    context.algorithm = ( char * )strtok ( filename, "." );
  else
    context.algorithm = filename;


  /* 重定向输出 */

  char * ofilename = malloc ( PATH_MAX );
  if ( snprintf ( ofilename, PATH_MAX, "%s.py", context.algorithm ) < 0 ) {
    printf ( "Error: memroy fault when get outfile name\n" );
    exit ( -1 );
  }

  FILE * outfile = fopen(ofilename, "w");
  if ( ! outfile ) {
    printf ( "Error: can't open output file '%s'\n", ofilename );
    return -3;
  }
  int fd = fileno ( outfile );
  if ( fd == -1 ) {
    fclose ( outfile );
    printf ( "Error: can't get file id of '%s'\n", ofilename );
    return -4;
  }
  int s_fd = dup( STDOUT_FILENO );
  if ( s_fd < 0 ) {
    close( fd );
    printf ( "Error: duplicate the stdout\n" );
    return -5;
  }
  int n_fd = dup2( fd, s_fd); /* STDOUT_FILENO ); */
  if ( n_fd < 0) {
    close( fd );
    printf ( "Error: redirect the stdout\n" );
    return -6;
  }

  /* 解析文件 */
  print_file_header ( &context );
  yylex_init ( &scanner );
  yyset_in( infile, scanner );
  yyparse ( scanner, &context );
  yylex_destroy ( scanner );

  fflush(outfile);
  fclose ( infile );
  fclose ( outfile );
  free ( filename );
  free ( ofilename );
  return 0;
}
