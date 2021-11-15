from Lexer.Token import Token
from Lexer.Lexemes.Lexemes import Token_Enum
from typing import List
from AST.AST_Nodes import *
from Stubs.AST_Statement_Stub import AST_Statement_Stub
from Parser.Parse_Error import Parser_Syntax_Error
import copy




def Parse_Statement(tokens:List[Token], id:int) -> AST_Node:
    ### TODO: Temporary code below! (also id needs to be removed)

    tokens = copy.deepcopy(tokens)

    if tokens[-1].get_type() != Token_Enum.Line_End.Line_End:
        raise(Parser_Syntax_Error("Reached EOF while parsing statement, expected ;"))

    return AST_Statement_Stub(id)

