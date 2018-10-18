/*
 *
 * 算法语言分析器：
 *
 * 文档结构
 *

--------------------------

 program 算法名称;

 可选：常量或者类型定义；

 可选：变量声明, 注意： 变量声明必须放在类型定义之下；

 可选： 函数或者过程定义，注意：如果有的话，必须在变量和类型声明之后；

 begin

     变量赋值;

     调用算法主函数;

 end.

----------------------------

 *
 * 函数定义和过程定义使用类Pascal语法。
 *
 * 可以使用的特殊变量： datapool.name，用于访问数据池中名称为 name 的数据。
 *
 * 譬如：

   node := datapool.mynode;

   可以引用数据池中定义的数据项 mynode ;

   node := datapool.hanoi.mynode，暂时不支持

   可以引用数据池定义的组 hanoi 中的数据项 mynode
 *
 * 函数的返回值使用特殊变量 result，也即是说，通过给 result
 * 赋值，来设定函数的返回值；Pascal 中是直接给 函数名称赋值，
 * 这里略有区别。
 *
 * 所有的声明中，在同一个函数或者过程中，变量声明必须在类型之
 * 后，因为目前的实现中需要在函数体内使用变量列表，而类型中的
 * 结构、枚举类型的定义会覆盖变量名称列表，所以会导致问题。
 *
 * program
 *
 * procedure, function, const, var, type, record, array, of
 *
 * for, while, if, do, case,
 *
 * begin, end
 *
 * integer, real, char, boolean, string
 *
 * and or not + - * / = := > >= < <= <>
 *
 * . ^ : ;
 *
 * 注释：使用大括号 {}
 *
 * 备注
 *
 * VOP 是一个虚拟的二元操作符号，其优先级在二元操作符中为最高。
 *
 * 规则 expr: expr VOP expr 主要是为了保证二元操作符必定存在
 * 一个 lookahead token。因为最高优先级的运算符不会去读
 * lookahead token，所以如果没有这个虚拟的二元操作符，乘和除
 * 的运算不会读 lookahead token,从而无法正确折行。
 *     
 * 目前暂不支持：
 *     with 语句
 *     子范围类型，Subrange。
 *     枚举类型指定值，譬如 (red=1, green=3)
 *     不支持没有括号的过程调用，譬如： myprocedure, 使用 myprocedure() 代替
 *     不支持枚举类型的 pred 和 succ 函数
 *
 */

%{
  #include <stdio.h>
  #include <limits.h>
  #include <unistd.h>
  #include "parse.h"

  #define PRINT_CONST(t,n,v)                \
           i_printf(pcontext -> indent,     \
                   "%s = %s(%s)\n",         \
                    n,                      \
                    t,                      \
                    v                       \
                    );

  #define YYSTYPE char *
  typedef void * yyscan_t;

  extern int yylex_init(yyscan_t *);
  extern int yylex_destroy(yyscan_t);
  extern void yyset_in(FILE *, yyscan_t);
  static void yyerror(void *, void *, PCONTEXT, char const *);

  int INDENT_UNIT = 4;
%}

%debug
%error-verbose
%token-table
%pure-parser
%locations
/* %expect 1     /* if else 的摇摆造成的冲突 */

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
%token  AT     '@'

%token  AND    "and"
%token  OR     "or"
%token  NOT    "not"
%token  IN     "in"
%token  TRUE
%token  FALSE
%token  VOP

%token  DOT          '.'
%token  COMMA        ','
%token  COLON        ':'
%token  SEMICOLON    ';'
%token  INDICATOR    '^'
%token  DDOT         ".."

%token  IS           ":="

%token  LP    '('
%token  RP    ')'

%token  LSP   '['
%token  RSP   ']'

%token  PROGRAM      "program"
%token  PROCEDURE    "procedure"
%token  FUNCTION     "function"
%token  CONST        "const"
%token  CASE         "case"
%token  VAR          "var"
%token  TYPE         "type"
%token  RECORD       "record"
%token  SET          "set"
%token  ARRAY        "array"
%token  OF           "of"
%token  FOR          "for"
%token  WHILE        "while"
%token  IF           "if"
%token  DO           "do"
%token  TO           "to"
%token  DOWNTO       "downto"
%token  REPEAT       "repeat"
%token  UNTIL        "until"
%token  ELSE         "else"
%token  THEN         "then"

%token  TOK_BEGIN    "begin"
%token  TOK_END      "end"

%token  TOK_CHAR
%token  TOK_STRING
%token  TOK_NAME
%token  TOK_INTEGER
%token  TOK_NUMBER

%left IN
%left GT LT EQ LE NE GE
%left OR AND

%left ADD MINUS
%left MUL DIV
%left VOP

%right NOT
%right NEG

%destructor { free($$); } name expr exprs func_expr

%% /* Grammar rules and actions follow.  */

program: PROGRAM TOK_NAME SEMICOLON { pcontext -> algorithm = strdup($2);
                                      print_file_header(pcontext);
                                      pcontext -> findex = 1;
                                      }

         decls                      { print_class_header(pcontext);
                                      pcontext -> indent += INDENT_UNIT;
                                      }

         decl_funcs                 

         TOK_BEGIN                  { print_main_entry(pcontext, @8.first_line);
                                      pcontext -> indent += INDENT_UNIT;
                                      }

         stmts

         TOK_END                    { i_printf(pcontext -> indent,
                                               "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                               @11.first_line
                                               );
                                      }

         DOT                        { pcontext -> indent -= INDENT_UNIT;
                                      pcontext -> indent -= INDENT_UNIT;
                                      print_class_footer(pcontext);
                                      print_file_footer(pcontext);
                                      }
;

decl_funcs: decl_func
          | decl_funcs decl_func
;

decl_func: func_header
           decls
           func_body
           SEMICOLON                   { /* 打印函数结束语句 */
                                         print_func_footer(pcontext);
                                         pcontext -> findex ++;
                                         pcontext -> indent -= INDENT_UNIT;
                                         }
;

func_header: func_id TOK_NAME func_ret SEMICOLON
                     {
		       pcontext -> funcs[pcontext -> findex].name = strdup($2);
                       print_func_header(pcontext, @1.first_line);
                       pcontext -> indent += INDENT_UNIT;
                       }
           | func_id TOK_NAME LP decl_paras RP func_ret SEMICOLON
                     {
                       pcontext -> funcs[pcontext -> findex].name = strdup($2);
                       print_func_header(pcontext, @1.first_line);
                       pcontext -> indent += INDENT_UNIT;
                       }
;
func_id:          FUNCTION | PROCEDURE ;
func_ret:         /* Empty */ | COLON TOK_NAME ;

func_body: TOK_BEGIN    { i_printf(pcontext -> indent,
                                   "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                   @1.first_line
                                   );
                          }
           stmts
           TOK_END      { i_printf(pcontext -> indent,
                                   "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                   @4.first_line
                                   );
                          }
;

decl_paras: decl_para
          | decl_paras SEMICOLON decl_para
;

decl_para: para_names COLON TOK_NAME      { set_para_type(pcontext, $3, 0); }
         | VAR para_names COLON TOK_NAME  { set_para_type(pcontext, $4, 1); }
;


para_names: TOK_NAME                   { push_para_name(pcontext, $1); }
          | para_names COMMA TOK_NAME  { push_para_name(pcontext, $3); }
;

decls: /* Empty */
     | decls CONST decl_constants SEMICOLON
     | decls VAR decl_vars SEMICOLON             { print_var_list(pcontext); }
     | decls TYPE decl_types SEMICOLON
;

decl_constants: decl_const
              | decl_constants SEMICOLON decl_const
;

decl_const: TOK_NAME EQ TOK_INTEGER         { PRINT_CONST("Integer", $1, $3); }
          | TOK_NAME COLON TOK_NAME EQ const_value { PRINT_CONST($3, $1, $5); }
;

const_value: TRUE | FALSE | TOK_INTEGER | TOK_CHAR | TOK_STRING | TOK_NUMBER ;

decl_vars: decl_var
         | decl_vars SEMICOLON decl_var
;

decl_var: var_names COLON TOK_NAME { set_var_type(pcontext, $3); }
        | var_names COLON TOK_NAME LP TOK_NAME RP
                        { /* set_complex_type(pcontext, $3, $5);*/ }
        | var_names COLON INDICATOR TOK_NAME
                        { char * typename;
                          asprintf(&typename, "%s%d", $4, @4.first_line);
                          print_type_pointer(pcontext, typename, $4);
                          set_var_type(pcontext, typename);
                        }
        | var_names COLON ARRAY OF TOK_NAME
                        { char * typename;
                          asprintf(&typename, "%s%d", $5, @5.first_line);
                          print_type_pointer(pcontext, typename, $5);
                          set_var_type(pcontext, typename);
                        }

        | var_names COLON ARRAY LSP TOK_INTEGER DDOT TOK_INTEGER RSP OF TOK_NAME
                        { char * typename;
                          asprintf(&typename, "%s%d", $10, @10.first_line);
                          print_type_array(pcontext, typename, $10, $5, $7);
                          set_var_type(pcontext, typename);
                        }
;

var_names: TOK_NAME                  { push_var_name(pcontext, $1, 0); }
         | AT TOK_NAME               { push_var_name(pcontext, $2, 1); }
         | var_names COMMA TOK_NAME  { push_var_name(pcontext, $3, 0); }
         | var_names COMMA AT TOK_NAME  { push_var_name(pcontext, $4, 1); }
;

decl_types: decl_type
          | decl_types SEMICOLON decl_type
;

decl_type: TOK_NAME EQ TOK_NAME             { print_type(pcontext, $1, $3); }
         | TOK_NAME EQ INDICATOR TOK_NAME   { print_type_pointer(pcontext, $1, $4); }
         | TOK_NAME EQ ARRAY OF TOK_NAME    { print_type_pointer(pcontext, $1, $5); }
         | TOK_NAME EQ ARRAY
           LSP TOK_INTEGER DDOT TOK_INTEGER
           RSP OF TOK_NAME        { print_type_array(pcontext, $1, $10, $5, $7); }
         | TOK_NAME EQ SET OF TOK_NAME      { print_type_set(pcontext, $1, $3); }
         | TOK_NAME EQ LP items RP          { print_type_enum(pcontext, $1); }
         | TOK_NAME EQ RECORD OF decl_vars TOK_END
                                            { print_type_record(pcontext, $1); }
;

items: TOK_NAME                  { push_var_name(pcontext, $1, 0); }
     | items COMMA TOK_NAME      { push_var_name(pcontext, $3, 0); }
;

stmts: /* Empty */
     | stmt
     | stmts SEMICOLON           { if (YYRECOVERING()) yyerrok; }
     | stmts SEMICOLON stmt      { if (YYRECOVERING()) yyerrok; }
;

/*
stmts: stmts DLB stmt_exts DRB
;

stmt_exts: stmt_ext
         | stmt_exts COMMA stmt_ext
;
stmt_ext: MUL name      { i_printf(pcontext -> indent, "%s.active()\n", $2);}
        | LT name GT    { i_printf(pcontext -> indent, "%s.deactive()\n", $2);}
        | name MINUS GT
                  name  { i_printf(pcontext -> indent, "%s.watch(%s)\n", $1, $4);}
        | ADD name      { i_printf(pcontext -> indent, "%s.show()\n", $2);}
        | MINUS name    { i_printf(pcontext -> indent, "%s.hide()\n", $2);}
        | LSP name RSP  { i_printf(pcontext -> indent, "%s.select()\n", $2);}
        | name EQ name  { i_printf(pcontext -> indent, "%s.vcopy(%s)\n", $1, $3);}
        | LP name RP    { i_printf(pcontext -> indent, "%s.invisible()\n", $2);}
        | name          { i_printf(pcontext -> indent, "%s.visible()\n", $1);}
;
*/

stmt: stmt_if
    | stmt_loop
    | stmt_assign
    | stmt_case
    | expr                 { print_stmt_expr(pcontext, @1.first_line, $1); }
;


stmt_case: CASE expr OF    { print_stmt_case(pcontext, @1.first_line, $2); }
           case_clauses case_else_clause TOK_END
;

case_clauses: case_clause
            | case_clauses case_clause
;

case_clause: expr COLON      { print_case_clause(pcontext, @1.first_line, $1);
                               pcontext -> indent += INDENT_UNIT + INDENT_UNIT;
                               }
             case_stmts      { pcontext -> indent -= INDENT_UNIT + INDENT_UNIT; }
;

case_else_clause: /* */
                | ELSE          { print_case_else_clause(pcontext, @1.first_line);
                                  pcontext -> indent += INDENT_UNIT;
                                  }
                  case_stmts    { pcontext -> indent -= INDENT_UNIT; }
;

case_stmts: stmt SEMICOLON
          | TOK_BEGIN stmts TOK_END
;

exprs: /* Empty */       { $$ = strdup( ""); }
     | expr              { $$ = strdup( $1); }
     | exprs COMMA expr  { asprintf(&$$, "%s, %s", $1, $3); }
;

stmt_assign: name IS expr { i_printf(pcontext -> indent,
                                     "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                     @1.first_line
                                     );
                            i_printf(pcontext -> indent, "%s.assign(%s)\n", $1, $3);
                            }
;

name: TOK_NAME                      { $$ = format_tokname($1); }
    | TOK_NAME INDICATOR            { asprintf(&$$, "%s.get()", $1); }
    | name LSP expr RSP             { asprintf(&$$, "%s[%s]", $1, $3); }
    | func_expr                     { $$ = strdup($1); }
    | name DOT TOK_NAME             { asprintf(&$$, "%s['%s']", $1, $3);}
    | name DOT TOK_NAME LP exprs RP { asprintf(&$$, "%s.%s(%s)", $1, $3, $5); }
;

compound_stmt: stmt
             | TOK_BEGIN stmts TOK_END
;

stmt_if: stmt_if_part compound_stmt      { pcontext -> indent -= INDENT_UNIT; }
       | stmt_if_part compound_stmt ELSE { i_printf(pcontext -> indent - INDENT_UNIT,
                                                    "else:\n"
                                                    );
                                           }
         compound_stmt                   { pcontext -> indent -= INDENT_UNIT; }
;

stmt_if_part: IF expr THEN      { i_printf(pcontext -> indent,
                                           "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                           @1.first_line
                                           );
                                  i_printf(pcontext -> indent,
                                           "if %s:\n",
                                           $2
                                           );
                                  pcontext -> indent += INDENT_UNIT;
                                  }
;

stmt_loop: WHILE expr DO { i_printf(pcontext -> indent,
                                      "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                      @1.first_line
                                      );
                           i_printf(pcontext -> indent,
                                      "while %s:\n",
                                      $2
                                      );
                           pcontext -> indent += INDENT_UNIT;
                           }
            compound_stmt { pcontext -> indent -= INDENT_UNIT; }
          | REPEAT stmts  { i_printf(pcontext -> indent,
                                       "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                       @1.first_line
                                       );
                            i_printf(pcontext -> indent,
                                       "%s\n",
                                       "while True:"
                                       );
                            pcontext -> indent += INDENT_UNIT;
                            }
            UNTIL expr    { i_printf(pcontext -> indent,
                                       "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                       @4.first_line
                                       );
                            i_printf(pcontext -> indent,
                                       "if %s: break\n",
                                       $5
                                       );
                            pcontext -> indent -= INDENT_UNIT;
                            }
          | FOR name IS expr TO expr DO
                                {
                                  i_printf(pcontext -> indent,
                                           "%s.assign(%s - Integer(1))\n",
                                           $2,
                                           $4
                                           );
                                  i_printf(pcontext -> indent,
                                           "_for_end = %s\n",
                                           $6
                                           );
                                  i_printf(pcontext -> indent,
                                           "%s\n",
                                           "while True:"
                                           );
                                  i_printf(pcontext -> indent + INDENT_UNIT,
                                           "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                           @1.first_line
                                           );
                                  i_printf(pcontext -> indent + INDENT_UNIT,
                                           "%s.assign(%s + Integer(1))\n",
                                           $2,
                                           $2
                                           );
                                  i_printf(pcontext -> indent + INDENT_UNIT,
                                           "if %s > _for_end: break\n",
                                           $2
                                           );
                                  pcontext -> indent += INDENT_UNIT;
                                  }
              compound_stmt { pcontext -> indent -= INDENT_UNIT; }
            | FOR name IS expr DOWNTO expr DO
                                {
                                  i_printf(pcontext -> indent,
                                           "%s.assign(%s + Integer(1))\n",
                                           $2,
                                           $4
                                           );
                                  i_printf(pcontext -> indent,
                                           "_for_end = %s\n",
                                           $6
                                           );
                                  i_printf(pcontext -> indent,
                                           "%s",
                                           "while True:\n"
                                           );
                                  i_printf(pcontext -> indent + INDENT_UNIT,
                                           "DRIVER.simulate_statement(%d, sys._getframe())\n",
                                           @1.first_line
                                           );
                                  i_printf(pcontext -> indent + INDENT_UNIT,
                                           "%s.assign(%s - Integer(1))\n",
                                           $2,
                                           $2
                                           );
                                  i_printf(pcontext -> indent + INDENT_UNIT,
                                           "if %s < _for_end: break\n",
                                           $2
                                           );
                                  pcontext -> indent += INDENT_UNIT;
                                  }
              compound_stmt { pcontext -> indent -= INDENT_UNIT; }
;

func_expr: TOK_NAME LP exprs RP
                { /* 判断是自己定义的函数还是Pascal的系统函数 */
                char * prefix = get_func_scope($1);
                if (strcmp(prefix, "self.") == 0){
                  print_expr_func(pcontext, @1.first_line, $1, $3);
                  asprintf(&$$, "_%s", $1);
                }
                else{
                  char * name = format_tokname($1);
                  asprintf(&$$,
                           "%s%s(%s)",
                           prefix,
                           $1,
                           $3
                           );
                  free(name);
                }
                                }
;

expr: TOK_STRING             { asprintf(&$$, "String(%s)", $1); }
    | TOK_CHAR               { asprintf(&$$, "Char(%s)", $1); }
    | TOK_NUMBER             { asprintf(&$$, "Real(%s)", $1); }
    | TOK_INTEGER            { asprintf(&$$, "Integer(%s)", $1); }
    | TRUE                   { asprintf(&$$, "True"); }
    | FALSE                  { asprintf(&$$, "False"); }
    | AT TOK_NAME            { asprintf(&$$, "Pointer(%s)", $2); }
    | name                   { asprintf(&$$, "%s", $1); }
    | LSP exprs  RSP         { asprintf(&$$, "[ %s ]", $2); }
    | LP expr RP             { asprintf(&$$, "( %s)", $2); }
    | expr ADD expr          { asprintf(&$$, "%s + %s", $1, $3); }
    | expr MINUS expr        { asprintf(&$$, "%s - %s", $1, $3); }
    | expr MUL expr          { asprintf(&$$, "%s * %s", $1, $3); }
    | expr DIV expr          { asprintf(&$$, "%s / %s", $1, $3); }
    | expr AND expr          { asprintf(&$$, "%s and %s", $1, $3); }
    | expr OR expr           { asprintf(&$$, "%s or %s", $1, $3); }
    | NOT expr               { asprintf(&$$, "not %s", $2); }
    | expr EQ expr           { asprintf(&$$, "%s == %s", $1, $3); }
    | expr NE expr           { asprintf(&$$, "%s != %s", $1, $3); }
    | expr GT expr           { asprintf(&$$, "%s > %s", $1, $3); }
    | expr LT expr           { asprintf(&$$, "%s < %s", $1, $3); }
    | expr GE expr           { asprintf(&$$, "%s >= %s", $1, $3); }
    | expr LE expr           { asprintf(&$$, "%s <= %s", $1, $3); }
    | expr IN expr           { asprintf(&$$, "%s in %s", $1, $3); }
    | MINUS expr %prec NEG   { asprintf(&$$, "-%s", $2); }
;

/* 虚拟操作符，永远不会执行； 只是为了让任何有效运算符都有
   lookahead token，从而正确实现不同运算符根据优先级的折行。
   */ 
expr: expr VOP expr { $$ = $1 == $3 ? $3 : $1; }; 

/* Error Recovery Rulers */

/* 错误恢复规则 1：
   
   如果当前函数或者过程声明中出现语法错误，那么只要碰到下一个
   函数或者过程的头部，当前函数或者过程错误恢复就完成；然后重
   新开始解析下一个函数。
   */
decl_func: func_id TOK_NAME error
                  { if (yychar == PROCEDURE || yychar == FUNCTION){
                      yyerrok;
                      pcontext -> indent -= INDENT_UNIT;
                    }
                    }

/* 错误恢复规则 2：

   如果当前语句出现错误，那么只要碰到一个分号，错误恢复就完
   成；然后重新开始下一个语句的解析。
   */
stmts: stmts error { if (yychar == SEMICOLON)
                       yyerrok;
                     else if (yychar == PROCEDURE || yychar == FUNCTION){
                       yyerrok;
                       YYERROR;
                     }
                     }
;

%%

/* Called by yyparse on error.  */
static void
yyerror(void *locp, void *scanner, PCONTEXT pcontext, char const *msg)
{
  ++ pcontext -> error;
  fprintf(stderr,
          _("Error:%d: %s\n"),
          ((YYLTYPE*)locp)->first_line,
          msg
          );
}

static int
set_options(PCONTEXT pcontext, int argc, char **argv)
{
  int c;

  opterr = 0;

  yydebug = 0;

  while ((c = getopt (argc, argv, "c:dL:")) != -1)

    switch (c){

    case 'c':
      bind_textdomain_codeset("algorithm-elf", optarg);
      bind_textdomain_codeset("bison-runtime", optarg);
      break;

    case 'd':
      yydebug = 1;
      break;

    case 'L':
      break;

    case '?':
      if ((optopt == 'c') || (optopt == 'L'))
        fprintf(stderr, _("Option -%c requires an argument.\n"), optopt);

      else if (isprint(optopt))
        fprintf(stderr, _("Warning: Unknown option `-%c'.\n"), optopt);

      else
        fprintf(stderr,
                _("Warning: Unknown option character `\\x%x'.\n"),
                optopt
                );
      break;

    default:
      fprintf(stderr,
              _("Warning: ?? getopt returned character code 0%o ??\n"),
              c
              );

    }
  return optind;
}


int
main(int argc, char * argv[])
{
  CONTEXT context = { NULL };
  yyscan_t scanner;
  FILE * infile;
  int i,j;
  char *lang;
  char *codeset;
 
  setlocale(LC_ALL, "");
  bindtextdomain("algorithm-elf", "locale");
  bindtextdomain("bison-runtime", "locale");
  textdomain("algorithm-elf");

  /*
  if (context.lang){    
    asprintf(&lang, "LANG=%s", context.lang);
    putenv(lang);
  }
  else
  */
  lang = (char*)getenv("LANG");
  codeset = strchr(lang ? lang : "", '.');
  if (codeset){
    ++ codeset;
    bind_textdomain_codeset("algorithm-elf", codeset);
    bind_textdomain_codeset("bison-runtime", codeset);
  }

  if (set_options(&context, argc, argv) == -1)
    return -1;
    
  if (optind >= argc){
    fprintf(stderr, _("Error: no specify filename found\n"));
    return -1;
  }
  infile = fopen(argv[optind], "r");
  if (infile == NULL) {
    fprintf(stderr, _("Error: can't open file '%s'\n"), argv[optind]);
    return -2;
  }

  /* 重定向输出 */
  char * ofilename = strdup(argv[optind]);
  char * s = strrchr(ofilename, '.');
  if (s == NULL || strlen(s) < 3){
    fprintf(stderr, _("Error: the extention of file name should be '.pal'\n"));
    return -8;
  }
  strcpy(s, ".py");

  FILE * outfile = fopen(ofilename, "w");
  if (!outfile) {
    fprintf(stderr, _("Error: can't open output file '%s'\n"), ofilename);
    return -3;
  }
  int fd = fileno(outfile);
  if (fd == -1) {
    fclose(outfile);
    fprintf(stderr, _("Error: can't get file id of '%s'\n"), ofilename);
    return -4;
  }
  int s_fd = dup(STDOUT_FILENO);
  if (s_fd < 0) {
    close(fd);
    fprintf(stderr, _("Error: duplicate the stdout\n"));
    return -5;
  }
  int n_fd = dup2(fd, STDOUT_FILENO);
  if (n_fd < 0) {
    close(fd);
    fprintf(stderr, _("Error: redirect the stdout\n"));
    return -6;
  }

  fprintf(stderr, _("Building '%s' ...\n"), argv[optind]);

  yylex_init(&scanner);
  yyset_in(infile, scanner);
  int retcode = yyparse(scanner, &context);
  yylex_destroy(scanner);

  if (retcode == 0 && context.error == 0)
    fprintf(stderr,
            _("Building over! The target file '%s' "
              "has been generated successfully.\n"),
              ofilename
              );
  else if (retcode == 1)
    fprintf(stderr,
            _("Building failed! There are %d errors found, "
              "you can click the error message above to locate the error, "
              "fix it and rebuild the source file.\n"),
            context.error
            );
  else
    fprintf(stderr,
            _("Building abort! Memory is exhausted when parsing the source file. "
              "Please quit other applications and try it again, if the same "
              "error is occured, send the email to jondy.zhao@gmail.com to "
              "get some advice\n")
            );
            
  /* 下面语句实际上没有什么意义，程序终止后自动进行下面的清理动作的。
  fflush(outfile);
  fclose(infile);
  fclose(outfile);
  free(context.algorithm);
  free(ofilename);
  */
  return 0;
}
