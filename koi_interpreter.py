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
                print("Error - variable does not exist")
                sys.exit()

            else:
                if self.variables.get(ctx.name().getText()).final:
                    # Error - reassignment to final
                    print("Error - reassignment to final")
                    sys.exit()

        else:
            if self.variables.get(ctx.name().getText()):
                # Error - variable already exists
                print("Error - variable already exists")
                sys.exit()

            if ctx.type_() is None:
                # var my := 0
                # The type isn't inferred
                value = ctx.true_value().getText()

                if value == "true" or value == "false":
                    value = value.title()

                type_value = self.type_dict[type(eval(value))]

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
