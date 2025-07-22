#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.dsl.context import DslContext


class Params:
    def __init__(self, context: DslContext, args: list[str] | None = None):
        self.context: DslContext = context
        self.args: list[str] = [] if args is None else list(args)

    def get_param_value(self, name: str) -> str | None:
        for arg in self.args:
            index: int = arg.find(name + ": ")
            if index != -1:
                return arg[index + len(name) + 2 :]
        return

    def optional(self, name: str, default_value: str) -> str:
        arg: str | None = self.get_param_value(name)
        if arg is None:
            return default_value
        return arg

    def alias(self, name: str, default_value: str | None = None) -> str:
        value: str | None = self.get_param_value(name)
        if value is not None:
            return self.context.alias(value)
        elif default_value is None:
            raise ValueError(f"No '{name}' supplied for alias")

        self.args.append(name + ": " + default_value)
        return self.context.alias(default_value)

    def decode_alias(self, alias: str) -> str:
        return self.context.decode_alias(alias)

    def optional_sequence(self, name: str, start: int) -> str:
        return self.optional(name, self.context.sequence_number_for_name(name, start))
