from Lexer.Lexemes.Lexemes import *
from Lexer.Token import Token
from typing import List, Dict


### ======================================== Lexer / Errors ======================================== ###


class Lexer_Match_Error(BaseException):
    """Exception raised because the base Lexer could not find a matching token

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


### ======================================== Lexer ======================================== ###

class Lexer():

    def __init__(self) -> None:
        self._lexemes = [
            Lxm_Op_Power,Lxm_Op_Int_Division,Lxm_Op_Bitshift_Right,Lxm_Op_Bitshift_Left,Lxm_Op_And,Lxm_Op_Or,Lxm_Op_Not_Equal,Lxm_Op_Double_Equal,Lxm_Op_Less_Equal,Lxm_Op_Greater_Equal,
            Lxm_Op_Add,Lxm_Op_Subtract,Lxm_Op_Multiply,Lxm_Op_Division,Lxm_Op_Modulo,Lxm_Op_Bitwise_And,Lxm_Op_Bitwise_Or,Lxm_Op_Bitwise_Xor,Lxm_Op_Bitwise_Not,Lxm_Op_Not,Lxm_Op_Less,Lxm_Op_Greater,Lxm_Op_Equal,
            Lxm_Close_Paren_Open,Lxm_Close_Paren_Close,Lxm_Close_Square_Open,Lxm_Close_Square_Close,Lxm_Close_Curly_Open,Lxm_Close_Curly_Close,
            Lxm_Keywords_If,Lxm_Keywords_Else,Lxm_Keywords_While,
            Lxm_Function_Log,Lxm_Function_Print,Lxm_Function_To_Int,Lxm_Function_To_Float,Lxm_Function_To_Bool,Lxm_Function_To_String,
            Lxm_Line_End,
            Lxm_Literals_Int, Lxm_Literals_Float, Lxm_Literals_Bool, Lxm_Literals_String,
            Lxm_Identifiers_Iden,
            Lxm_Comment_Single, Lxm_Comment_Block,
        ]
        self._lexemes = [l() for l in self._lexemes]


    def _possible_tokens(self, char_stream:List[str]) -> List[Token]:
        ### Important! Do not modify the char_stream!
        [lxm.reset() for lxm in self._lexemes]

        any_open = True

        i = 0
        while i < len(char_stream) and any_open:
            any_open = False
            next_char = char_stream[i]

            for lxm in self._lexemes:
                lxm.feed(next_char)
                any_open = any_open or lxm.is_open()
            
            i += 1

        ### make a dictionary of tokens that match the head of the char_stream
        possible_tokens = []
        for lxm in self._lexemes:
            if lxm.is_complete():
                new_token = Token(lxm.get_token(), lxm.get_captured())
                possible_tokens.append(new_token)

        ### returns dictionary of Tokens indexed by token type
        return possible_tokens
        

    def match_tokens(self, char_stream:str) -> List[str]:

        tokens = []
        
        char_stream = list(char_stream)

        while len(char_stream) > 0:
            if char_stream[0].isspace():
                char_stream.pop(0)
                continue

            possible_tokens = self._possible_tokens(char_stream)

            ### make sure at least one token matched and raise an error if none did
            if len(possible_tokens) == 0:
                raise(Lexer_Match_Error("No matching Token for:\n{}".format(''.join(char_stream))))

            if len(possible_tokens) == 1:
                tokens.append(possible_tokens[0])
            else:
                ### remove anything shorter than the longest token
                longest = 0
                for token in possible_tokens:
                    if len(token.get_string()) > longest:
                        longest = len(token.get_string())
                for i in range(len(possible_tokens)-1,-1,-1):
                    if len(possible_tokens[i].get_string()) < longest:
                        del possible_tokens[i]
                
                if len(possible_tokens) == 1:
                    tokens.append(possible_tokens[0])
                else:
                    ### resolve any conflicts that still occure

                    ### raise an error if ther are too many conflicting tokens
                    if len(possible_tokens) > 2:
                        raise(Lexer_Match_Error("Cannot resolve conflict between 3 or more tokens: {}".format(possible_tokens)))

                    token_types = [token.get_type() for token in possible_tokens]
                    
                    if Token_Enum.Identifiers.Iden in token_types:
                        if Token_Enum.Literals.Bool in token_types:
                            index = token_types.index(Token_Enum.Literals.Bool)
                            tokens.append(possible_tokens[index])

                        elif Token_Enum.Functions.Log in token_types:
                            index = token_types.index(Token_Enum.Functions.Log)
                            tokens.append(possible_tokens[index])

                        elif Token_Enum.Functions.Print in token_types:
                            index = token_types.index(Token_Enum.Functions.Print)
                            tokens.append(possible_tokens[index])

                        elif Token_Enum.Functions.To_Bool in token_types:
                            index = token_types.index(Token_Enum.Functions.To_Bool)
                            tokens.append(possible_tokens[index])

                        elif Token_Enum.Functions.To_Float in token_types:
                            index = token_types.index(Token_Enum.Functions.To_Float)
                            tokens.append(possible_tokens[index])

                        elif Token_Enum.Functions.To_Int in token_types:
                            index = token_types.index(Token_Enum.Functions.To_Int)
                            tokens.append(possible_tokens[index])

                        elif Token_Enum.Functions.To_String in token_types:
                            index = token_types.index(Token_Enum.Functions.To_String)
                            tokens.append(possible_tokens[index])

                        elif Token_Enum.Keywords.If in token_types:
                            index = token_types.index(Token_Enum.Keywords.If)
                            tokens.append(possible_tokens[index])

                        elif Token_Enum.Keywords.Else in token_types:
                            index = token_types.index(Token_Enum.Keywords.Else)
                            tokens.append(possible_tokens[index])

                        elif Token_Enum.Keywords.While in token_types:
                            index = token_types.index(Token_Enum.Keywords.While)
                            tokens.append(possible_tokens[index])
                        
                        else:
                            raise(Lexer_Match_Error("Unable to resolve Iden conflict"))

                    else:
                        raise(Lexer_Match_Error("Unable to resolve equal length conflict"))

            new_token = tokens[-1]
            char_stream = char_stream[len(new_token.get_string()):]

            if new_token.get_type() == Token_Enum.Literals.String:
                new_token.set_string(new_token.get_string()[1:-1])

        return tokens
                    



                    


                



            
        


