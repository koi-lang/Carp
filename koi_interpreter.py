#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import sys

from koicore.other import KoiVariable

from KoiParser import KoiParser
from KoiListener import KoiListener

from koicore import KoiObject
from koicore.types import KoiInteger
from koicore.types import KoiString
from koicore.types import KoiBoolean
from koicore import KoiException


def python_keyword(value):
    if value == "true" or value == "false":
        value = value.title()

    return eval(value)


class KoiInterpreter(KoiListener):
    def __init__(self):
        self.variables = {}

        self.type_dict = {object: KoiObject,
                          str: KoiString,
                          int: KoiInteger,
                          bool: KoiBoolean}

    def exitLocal_asstmt(self, ctx:KoiParser.Local_asstmtContext):
        type_value = KoiObject()
        var = KoiVariable(type_value)

        if ctx.vars_() is None:
            # my = 0
            if not self.variables.get(ctx.name().getText()):
                # Error - variable does not exist
                KoiException("Error - variable does not exist")
                sys.exit()

            else:
                if self.variables.get(ctx.name().getText()).final:
                    # Error - reassignment to final
                    KoiException("Error - reassignment to final")
                    sys.exit()

        else:
            if self.variables.get(ctx.name().getText()):
                # Error - variable already exists
                KoiException("Error - variable already exists")
                sys.exit()

            if ctx.type_() is None:
                # var my := 0
                # The type isn't inferred

                type_value = self.type_dict[type(python_keyword(ctx.true_value().getText()))]

            else:
                # var my: int = 0
                # The type is inferred
                type_value = self.type_dict[eval(ctx.type_().getText())]

            if ctx.vars_().getText() == "val":
                var.final = True

        if not self.variables.get(ctx.name().getText()):
            var.name = ctx.name().getText()
            var.value = ctx.true_value().getText()
            var.type_ = type_value
            self.variables[var.name] = var

        else:
            self.variables[ctx.name().getText()].value = ctx.true_value().getText()

        # for i in self.variables.keys():
        #     print(f"Name: {self.variables[i].name}, Value: {self.variables[i].value}, Type: {self.variables[i].type_}")

        # print("---")

    def print_list(self, list_):
        print_list = []

        for i in list_:
            if self.variables.get(i.getText()):
                print_list.append(python_keyword(self.variables[i.getText()].value))

            else:
                print_list.append(python_keyword(i.getText()))

        return " ".join(print_list)

    def exitPrint_stmt(self, ctx:KoiParser.Print_stmtContext):
        if ctx.PRINT():
            list_ = self.print_list(ctx.true_value())
            print(list_, end="")

        elif ctx.PRINTLN():
            list_ = self.print_list(ctx.true_value())
            print(list_)
