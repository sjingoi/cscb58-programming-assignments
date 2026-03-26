import argparse
import importlib
import sys
from decl import *
from type import *
from codetypes import *
from exprstmt import *
from labelasm import assembleCode


type ExpressionTypes = dict[Expression|LValue, TType]
type SymbolTable = dict[str, FunctionInformation]


@dataclass
class FunctionInformation:
    paramTypes: list[TType]
    returnType: TType
    varTable: dict[str, TType]


def typecheckNode(node, f_table: SymbolTable, f_current: FunctionInformation) -> ExpressionTypes:
    expr_types: ExpressionTypes = {}

    # TODO: Implement typechecking for each node type and add the types of expressions to expr_types
    match node:
        case Function():
            pass
        case VarDef():
            pass
        case TType():
            pass
        case Constant():
            pass
    # ...
    return expr_types


def generateNode(node, expr_types: ExpressionTypes, f_table: SymbolTable, f_current: FunctionInformation) -> list[LabeledAssemblyCode]:
    assembly_code: list[LabeledAssemblyCode] = []
    
    # TODO: Implement assembly code generation for each node type and add the generated instructions to assembly_code
    match node:
        case Function():
            pass
        case VarDef():
            pass
        case TType():
            pass
        case Constant():
            pass
    # ...
    return assembly_code


def typecheck(input_fs: list[Function]) -> tuple[ExpressionTypes, SymbolTable]:
    expr_types: ExpressionTypes = {}
    f_table: SymbolTable = {}

    # Initialize function table
    for function in input_fs:
        paramTypes: list[TType] = []        # TODO: Initialize paramTypes
        returnType: TType = TType.Int       # TODO: Initialize returnType
        f_table[function.name] = FunctionInformation(paramTypes, returnType, {})
    
    # Run typechecking on each function and add returned types to expr_types
    for function in input_fs:
        expr_types = expr_types | typecheckNode(function, f_table, f_table[function.name])

    return (expr_types, f_table)


def generate(input_fs: list[Function], expr_types: ExpressionTypes, f_table: SymbolTable) -> list[list[LabeledAssemblyCode]]:
    assembly_code: list[list[LabeledAssemblyCode]] = []

    # Generate each function's labeled assembly code
    for function in input_fs:
        asm_code = generateNode(function, expr_types, f_table, f_table[function.name])
        assembly_code.append(asm_code)

    return assembly_code


def compileCode(input_fs: list[Function], output = sys.stdout.buffer):
    expr_types, f_table = typecheck(input_fs)
    asm_fns = generate(input_fs, expr_types, f_table)
    concatAsm = [elem for sublist in asm_fns for elem in sublist]
    assembleCode(concatAsm, output)

if __name__ == "__main__":
    if sys.platform == "win32":
        import os, msvcrt
        msvcrt.setmode(sys.stdout.fileno(  ), os.O_BINARY)

    parser = argparse.ArgumentParser(
                    prog="compiler",
                    description="Assembles a sequence of Function objects")
    parser.add_argument("filename")
    args = parser.parse_args()
    
    spec = importlib.util.spec_from_file_location("code", args.filename)
    code = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(code)
    compileCode(code.CODE) 
