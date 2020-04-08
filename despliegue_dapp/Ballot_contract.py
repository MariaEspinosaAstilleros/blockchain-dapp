#!/usr/bin/python3
# -*- coding: utf-8 -*-

from solcx import compile_source, set_solc_version

set_solc_version("v0.5.16")

with open('contracts/VotacionElecciones.sol', 'r') as content:
    CODIGO = content.read()

COMPILACION = list(compile_source(CODIGO).values())[0]

ABI = COMPILACION['abi']
ASM = COMPILACION['asm']
BYTECODE = COMPILACION['bin']
RUNTIME = COMPILACION['bin-runtime']
OPCODES = COMPILACION['opcodes']
AST = COMPILACION['ast']