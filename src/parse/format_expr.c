#include <stdio.h>

#define MAX_STMT_SIZE 1024
#define MAX_EXPR_SIZE 1024
#define MAX_DATA_SIZE 4

#define MAX_EXPR_NODE 32
#define MAX_EXPR_STACK 32
typedef struct {
  int level;
  char * exprs[ MAX_EXPR_NODE ];
} EXPR_NODE;

typedef EXPR_NODE *PEXPR_NODE;

char * increase_indent( const char * , int );
char * increase_indent1( char *, const int, const char *, int );
int get_level( const char * );
char * merge_expr( PEXPR_NODE, int, int );

int main( int argc, char * argv[] )
{
  char buf[ MAX_STMT_SIZE ];

  char * data[ MAX_DATA_SIZE ] = {
    "\n",
    "a",
    "1\n2\n3",
    "1\n"
  };
  int i;
  for ( i = 0; i < MAX_DATA_SIZE; i ++ ){
    printf( "Test Data:\n%s\n", data[ i ] );
    printf( "Result:\n'%s'\n",
            increase_indent( data[ i ], 2 )
            );
    printf( "Result1:\n'%s'\n",
            increase_indent1 ( buf, MAX_STMT_SIZE, data[ i ], 2 )
            );
  }
  return 0;
}

char *
increase_indent( const char * expr, int indent )
{
  char * buf = (char *) malloc( MAX_STMT_SIZE );
  if ( !buf ){
    fprintf( stderr, "Error: memory fault\n" );
    return NULL;
  }

  char *s = (char *)expr;
  char *p = strchr( s, '\n' );

  int len = 0;
  int offset = 0;

  while ( p ){
    len = p - s + 1;
    if ( len + offset + indent >= MAX_STMT_SIZE ){
      fprintf( stderr, "Error: buffer override\n" );
      free( buf );
      return NULL;
    }
    strncpy( buf + offset, s, len );
    offset += len;

    /* 增加一个缩进单位 */
    memset( buf + offset, ' ', indent );
    offset += indent;

    /*  查找下一个换行符号 */
    s = p + 1;
    p = strchr( s, '\n' );
  }

  if ( s ){
    if ( snprintf( buf + offset,
                   MAX_STMT_SIZE - offset,
                   "%s",
                   s
                   ) < 0 ){
      fprintf( stderr, "Error: buffer override\n" );
      free( buf );
      return NULL;
    }
  }
  else {
    if ( offset < MAX_STMT_SIZE )
      buf[ offset ] = 0;
    else {
      fprintf( stderr, "Error: buffer override\n" );
      free( buf );
      return NULL;
    }
  }
  return buf;
}
/* expr 中的每一个换行符号被替换成为换行加上缩进宽度个空格，返回到 buf 中。
   buf 是一个预先分配好的缓冲区。
   */
char *
increase_indent1( char * buf,
                  const int buf_size,
                  const char * expr,
                  int indent
                  )
{
  char *s = (char *)expr;
  char *p = strchr( s, '\n' );

  int len = 0;
  int offset = 0;

  while ( p ){
    len = p - s + 1;
    if ( offset + len + indent >= buf_size ){
      fprintf( stderr, "Error: buffer override\n" );
      return NULL;
    }
    strncpy( buf + offset, s, len );
    offset += len;

    /* 增加一个缩进单位 */
    memset( buf + offset, ' ', indent );
    offset += indent;

    /*  查找下一个换行符号 */
    s = p + 1;
    p = strchr( s, '\n' );
  }

  if ( s ){
    if ( snprintf( buf + offset,
                   buf_size - offset,
                   "%s",
                   s
                   ) < 0 ){
      fprintf( stderr, "Error: buffer override\n" );
      return NULL;
    }
  }
  else {
    if ( offset < buf_size )
      buf[ offset ] = 0;
    else {
      fprintf( stderr, "Error: buffer override\n" );
      return NULL;
    }
  }
  return buf;
}

/*  合并表达式，将其中的换行符号替换成为空格 */
char *
merge_expr1( char * expr )
{
  char * p = strchr( expr, '\n' );
  while ( p ){
    *p = ' ';
    p = strchr( p + 1, '\n' );
  }
  return expr;  
}

/*
  对齐策略
  1. 第一操作数顶格对齐，操作数全部折行。
     例如
     1 + 2 + 3 =>
        1
        + 2
        + 3
  2. 第一操作数与第二操作数缩进对齐，操作数全部折行。
     例如
     1 + 2 + 3 =>
           1
         + 2
         + 3
  3. 第一操作数顶格对齐，操作数仅在必要的时候折行。
  4. 第一操作数与第二操作数缩进对齐，操作数仅在必要的时候折行。

  前两种方式实现简单，直接在规则中增加缩进空格即可。后两种方
  式需要对表达式进行二次处理，重新判断是否换行。对于不需要换
  行的运算符要放在一行。
*/

/*
 * 将一个缩进折行表达式重新格式化成为没有必要则不折行的表达式。
 *
 * 例如，将下面的缩进折行表达式
 *    1
 *    + 2
 *      * 3
 *      * 4
 *    + 5
 *
 *    转换成为
 *
 *    1
 *    + 2 * 3 * 4
 *    + 5
 */
char *
format_stmt( const char * expr, int indent, int width )
{
  int x1, x2;
  char * s = (char *)expr;
  char * p;
  EXPR_NODE stack[ MAX_EXPR_STACK ];
  PEXPR_NODE pexpr = stack;
  int i;
  char *pp;
  char buffer [ MAX_EXPR_SIZE ];

  /* 得到第一行的缩进 */
  x1 = get_level ( p );
  x2 = x1;

  /* 初始化堆栈 */
  memset( stack, 0, sizeof( EXPR_NODE ) * MAX_EXPR_STACK );
  pexpr -> level = x1;
  p = strchr( s, '\n' );

  while ( p ){
    if ( x1 < x2 ){
      /* 出栈操作 */

      /* 计算当前栈的表达式的全部长度是否一行可以放的下 */
      /* 如果可以，那么合并成为一行，放到上一层堆栈的最后一个表达式 */
      /* 如果不可以，那么使用缩进方式，合并到上一层堆栈的最后一个表达式 */
      pp = merge_expr( pexpr, indent, width );

      /* 将当前栈顶清零，出栈 */
      memset( pexpr, 0, sizeof( EXPR_NODE ) );
      pexpr --;
      x1 = pexpr -> level;

      if ( pexpr -> exprs[ 0 ] ){
        for ( i = MAX_EXPR_NODE - 1; i >= 0; i -- )
	  if ( pexpr -> exprs[ i ] )
	    break;
        if ( snprintf(
		      buffer,
		      MAX_EXPR_SIZE,
		      "%s %s",
		      pexpr -> exprs[ i ],
		      pp
		      ) < 0 )
	  return NULL;
	free( pexpr -> exprs[ i ] );
	free( pp );
	pexpr -> exprs[ i ] = strdup( buffer );
      }
      else {
	pexpr -> exprs[ 0 ] = pp;
      }
      continue ;
    }

    if ( x1 > x2 ){
      /* 入栈 */
      pexpr ++;
      pexpr -> level = x2;
    }

    /* 表达式拷贝到栈顶 */
    if ( pexpr -> exprs[ MAX_EXPR_NODE - 1 ] ){
      return NULL;
    }
    for ( i = 0; i < MAX_EXPR_NODE; i ++ )
      if ( !( pexpr -> exprs [ i ] ) ){
        pexpr -> exprs[ i ] = strndup( s, p - s );
        break;
        }
    /* 读下一行 */
    s = p + 1;
    p = strchr( s, '\n' );
    x1 = x2;
    x2 = get_level( s );
  }

  /* 最后一个表达式入栈 */
  if ( pexpr -> exprs[ MAX_EXPR_NODE - 1 ] ){
    return NULL;
  }
  for ( i = 0; i < MAX_EXPR_NODE; i ++ )
    if ( !pexpr -> exprs [ i ] ){
      pexpr -> exprs[ i ] = strdup( s );
      break;
      }

  /* 全部格式化输出堆栈之中的内容 */
  while ( pexpr > stack){
    /* 出栈操作 */
    pp = merge_expr( pexpr, indent, width );
    pexpr --;
    if ( pexpr -> exprs[ 0 ] ){
      for ( i = MAX_EXPR_NODE - 1; i >= 0; i -- )
        if ( pexpr -> exprs[ i ] )
          break;
      if ( snprintf(
      	      buffer,
      	      MAX_EXPR_SIZE,
      	      "%s %s",
      	      pexpr -> exprs[ i ],
      	      pp
      	      ) < 0 )
        return NULL;
      free( pexpr -> exprs[ i ] );
      free( pp );
      pexpr -> exprs[ i ] = strdup( buffer );
    }
    else {
      pexpr -> exprs[ 0 ] = pp;
    }
  }
  return buffer;
}

int
get_level( const char * expr )
{
  int x = 0;
  char * p = ( char *)expr;
  while ( p ){
    if ( ( char )*p != ' ' )
      return x;
    p ++, x ++;
  }
  return x;
}

char *
merge_expr( PEXPR_NODE pexpr, int indent, int width )
{
  /* 合并多个表达式到一行 */
  char * s = pexpr -> exprs;
  int len = 0;
  int counter = 0;
  int level = pexpr -> level;
  while ( s ){
    len += strlen( s ) - level;
    counter ++;
    s ++;
  }
  /* 判断是否一行放得下，根据公式 len + indent + level < 列宽
     确定 */
  char * buf;
  int offset = 0;
  if ( len + level + indent > width ){
    buf = malloc ( len + 1 );
    s = pexpr -> exprs;
    while ( s ){
      if ( strncpy( buf + offset, s + level, strlen( s ) - level )
	   <= 0 )
	return NULL;
      offset += strlen( s ) - level;
      *( buf + offset ) = ' ';      
      s ++;      
    }
    *( buf + offset ) = 0;
  }
  else {
    buf = malloc( len + counter * level + counter * indent );
    s = pexpr -> exprs;
    while ( s ){
      strcpy( buf + offset, s );
      offset += strlen( s );
      s ++;
      if ( s ){
	memset( buf + offset, ' ', indent );
	offset += indent;
      }
    }
  }
  return buf;
}
