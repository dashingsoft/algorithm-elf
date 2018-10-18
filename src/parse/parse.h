#if !defined(PARSE_H)
#define PARSE_H

#include <assert.h>
#include <stdio.h>
#include <stdarg.h>
#include "config.h"

#include "libintl.h"

#if defined(__cplusplus)
extern "C" {
#endif

#if defined(ENABLE_NLS)
  #define _(string) gettext(string)
  #define YY_(msgid) dgettext ("bison-runtime", msgid)
#endif

#if !defined(HAVE_ASPRINTF)
  extern int asprintf (char **, const char *, ...);
#endif

  #define MAX_PARA_NUMBER 16
  #define MAX_FUNC_NUMBER 16
  #define MAX_VARS_NUMBER 16
  #define MAX_ITEM_SIZE 512

  typedef struct
  {
    char * name;
    char * type;
    int varflag;
  } PARA;
  typedef PARA * PPARA;

  typedef struct
  {
    char * name;
    char * rettype;
    PARA paras[MAX_PARA_NUMBER];
  } FUNC;
  typedef FUNC * PFUNC;

  typedef struct
  {
    char * name;
    char * type;
    char * value;
  } VARS;
  typedef VARS * PVAR;

  typedef struct
  {
    FUNC funcs[MAX_FUNC_NUMBER];
    int findex;        	            /* 当前函数列表的指针 */
    int indent;			    /* 缩进宽度 */
    VARS vars[MAX_VARS_NUMBER];
    char * algorithm;               /* 算法名称 */
    char datapool[MAX_ITEM_SIZE];   /* 数据池数据项 */    
    int error;                      /* 错误计数器 */
  } CONTEXT;
  typedef CONTEXT * PCONTEXT;
  
  void print_file_header(PCONTEXT);
  void print_file_footer(PCONTEXT);
  void print_class_header(PCONTEXT);
  void print_class_footer(PCONTEXT);
  void print_main_entry(PCONTEXT, int);
  void print_func_header(PCONTEXT, int);
  void print_func_footer(PCONTEXT);

  void print_type(PCONTEXT, char*, char*);
  void print_type_array(PCONTEXT, char*, char*, char*, char*);
  void print_type_array1(PCONTEXT, char*, char*);
  void print_type_enum(PCONTEXT, char*);
  void print_type_pointer(PCONTEXT, char*, char*);
  void print_type_record(PCONTEXT, char*);
  void print_type_set(PCONTEXT, char*, char*);

  void print_stmt_expr(PCONTEXT, int, const char*);
  void print_stmt_case(PCONTEXT, int, const char*);
  void print_case_clause(PCONTEXT, int, const char*);
  void print_case_else_clause(PCONTEXT, int);
  
  void push_var_name(PCONTEXT, char*, int);
  void set_var_type(PCONTEXT, char*);
  void push_para_name(PCONTEXT, char*);
  void set_para_type(PCONTEXT, char*, int);

  char * format_tokname(const char*);

  void i_printf (int, const char *, ...);

  char * get_func_scope(const char*);

  /* 缩进单位，四个空格 */
  extern int INDENT_UNIT;

#if defined(__cplusplus)
}
#endif

#endif	/* PARSE_H */
