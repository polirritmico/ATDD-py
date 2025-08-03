#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DslContext:
    global_seq_numbers: dict[str, int] = {}

    def __init__(self):
        self.sequence_numbers: dict[str, int] = {}
        self.aliases: dict[str, str] = {}

    def alias(self, name: str) -> str:
        alias: str | None = self.aliases.get(name)
        if alias:
            return alias

        sequence_number = self.seq_for_name(name, 1, DslContext.global_seq_numbers)
        alias = f"{name}{sequence_number}"
        self.aliases[name] = alias
        return alias

    def seq_for_name(
        self, name: str, start: int, sequence_numbers: dict[str, int]
    ) -> str:
        current = sequence_numbers.get(name, start)
        sequence_numbers[name] = current + 1
        return str(current)

    def decode_alias(self, name: str) -> str:
        for registered_name, alias in self.aliases.items():
            if name == alias:
                return registered_name
        return ""

    def sequence_number_for_name(self, name: str, start: int) -> str:
        return self.seq_for_name(name, start, self.sequence_numbers)
