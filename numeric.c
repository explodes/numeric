//
//  numeric.c
//  CGenerics
//
//  Created by Evan Leis on 5/23/14.
//  Copyright (c) 2014 explod.io. All rights reserved.
//

#include <stdlib.h>
#include <stdio.h>

#include "numeric.h"

#define CLEAR_SPEC() if(spec) { free(spec); spec = NULL; }

// I'm just asking for dangerous code using this.
#define START_GENERATOR(var) switch(var){
#define ENTRY_POINT(n) case n: printf("hit entry point %d\n", n);
#define END_GENERATOR() default:return NULL;}


typedef enum State {
    STATE_NONE,
    STATE_NUM,
    STATE_CHAR
} State;

static State state;
static bool hasDecimal;
static int entry_point;
static token_spec *spec;
static char c;
static char *string;
static int stringIndex;

void genBegin(char *s) {
    // state
    state = STATE_NONE;
    // decimal
    hasDecimal = false;
    // code position
    entry_point = 0;
    // spec
    CLEAR_SPEC();
    spec = calloc(1, sizeof(token_spec));
    spec->state = GenResultContinue;
    // current char
    c = '\0';
    // string
    string = s;
    stringIndex = 0;
}

void genEnd() {
    genBegin(NULL);
}

bool isFunctional(char c) {
    puts("isFunctional");
    return c == '(' || c == ')' || c == ',';
}

bool isOp(char c) {
    puts("isOp");
    return
        c == '+' ||
        c == '-' ||
        c == '*' ||
        c == '/' ||
        c == '^'
    ;
}

bool isNumeric (char c) {
    puts("isNumeric");
    return (c >= '0' && c <= '9') || c == '.';
}

void clearCurrent () {
    puts("clearCurrent");
    spec->pos = stringIndex;
    spec->len = 0;
}

void appendChar () {
    puts("appendChar");
    spec->len++;
}

bool hasCurrent () {
    puts("hasCurrent");
    return spec->len > 0;
}

token_spec* yieldCurrent(int next) {
    puts("yieldCurrent");
    entry_point = next;
    return spec;
}

token_spec* yieldState(int next, gen_result state) {
    puts("yieldState");
    entry_point = next;
    spec->state = state;
    return spec;
}

token_spec* yieldOp(int next, char op) {
    puts("yieldOp");
    entry_point = next;
    spec->state = GenResultOp;
    spec->op = op;
    return spec;
}

token_spec* genToken() {
    START_GENERATOR(entry_point);
    ENTRY_POINT(0);
    while ((c = string[stringIndex]) != '\0') {
        printf("got char: %c with: ", c);
        for (int i=0; i<spec->len; i++) {
            printf("%c", string[spec->pos + i]);
        }
        printf("\n");
        if (c == ' ') {
            if (hasCurrent()) {
                // yield current and continue
                return yieldCurrent(1);
                ENTRY_POINT(1);
                clearCurrent();
            }
            state = STATE_NONE;
        } else if (isFunctional(c) || isOp(c)) {
            if (hasCurrent()) {
                // yield current and char and continue
                return yieldCurrent(2);
                ENTRY_POINT(2);
                clearCurrent();
            }
            return yieldOp(3, c);
            ENTRY_POINT(3);
            clearCurrent();
            state = STATE_NONE;
        } else if (isNumeric(c)) {
            if (state == STATE_CHAR) {
                // automatically multiply
                if (hasCurrent()) {
                    return yieldCurrent(4);
                    ENTRY_POINT(4);
                }
                return yieldOp(5, '*');
                ENTRY_POINT(5);
                clearCurrent();
                // enter num mode
                state = STATE_NUM;
                hasDecimal = false;
            } else {
                if (state == STATE_NONE) {
                    // enter num mode
                    state = STATE_NUM;
                    hasDecimal = false;
                }
                if (c == '.') {
                    if (hasDecimal) {
                        return yieldState(6, GenResultErrorDecimals);
                        ENTRY_POINT(6);
                    }
                    hasDecimal = true;
                }
            }
            // append char to current number
            appendChar();
        // have char
        // var name or function name
        } else {
            if (state == STATE_NUM) {
                // automatically multiply
                if (hasCurrent()) {
                    return yieldCurrent(7);
                    ENTRY_POINT(7);
                }
                return yieldOp(8, '*');
                ENTRY_POINT(8);
                clearCurrent();
                // end mode
                state = STATE_NONE;
            }
            if (state == STATE_NONE) {
                // enter char mode
                state = STATE_CHAR;
            }
            // append char to current token
            appendChar();
        }
        stringIndex++;
    }
    // if has current
    if (hasCurrent()) {
        return yieldCurrent(9);
        ENTRY_POINT(9);
    }
    return yieldState(10, GenResultFinished);
    ENTRY_POINT(10);
    END_GENERATOR();
}

void genTokentest() {
    char *string = "5.3 + 6 * pow(3, 4) - 3^a";
    genBegin(string);
    token_spec *spec;
    while ((spec = genToken())) {
        gen_result result = spec->state;
        switch (result) {
            case GenResultErrorDecimals:
                puts("Too many decimals");
                break;
            case GenResultError:
                puts("Functional error");
                break;
            case GenResultFinished:
                puts("Finished!");
                break;
            case GenResultOp:
                printf("%c\n", spec->op);
                break;
            case GenResultContinue:
            default:
                for (int i=0; i<spec->len; i++) {
                    printf("%c", string[spec->pos + i]);
                }
                puts("");
                break;
        }
    }
    genEnd();
    
}