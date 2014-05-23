//
//  numeric.h
//  CGenerics
//
//  Created by Evan Leis on 5/23/14.
//  Copyright (c) 2014 explod.io. All rights reserved.
//

#ifndef CGenerics_numeric_h
#define CGenerics_numeric_h

#import <stdbool.h>

typedef enum States {
    GenResultContinue      = 0x0,
    GenResultOp            = 0x1,
    GenResultFinished      = 0x2,
    GenResultError         = 0x2 | 0x4, // implies finished
    GenResultErrorDecimals = 0x2 | 0x4 | 0x8, // implies finished, error
} gen_result;

typedef struct {
    gen_result state;
    char op;
    int pos;
    int len;
} token_spec;

/** Prime the generator with a null-terminated string */
void genBegin(char *string);

/** Retrieve an individual, not thread-safe */
token_spec* genToken();

/** Finalize the parser */
void genEnd();

#endif
