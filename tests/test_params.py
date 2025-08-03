#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from tests.dsl.context import DslContext
from tests.dsl.params import Params


@pytest.fixture
def context() -> DslContext:
    return DslContext()


def test_return_optional_value_of_params(context) -> None:
    case_name = "Three"
    case_default = "3"
    expected = "3"

    params = Params(context)
    output = params.optional(case_name, case_default)
    assert expected == output


def test_return_defined_value_overriding_default(context) -> None:
    case_args = ["One: 1"]
    expected = "1"

    params = Params(context, case_args)
    output = params.optional("One", "3")
    assert expected == output


def test_return_start_value_of_optional_sequence(context) -> None:
    case_param = "Param1"
    case_start = 3
    expected = "3"

    params = Params(context)
    output = params.optional_sequence(case_param, case_start)
    assert expected == output


def test_return_next_value_of_optional_sequence(context) -> None:
    case_param = "SomeParam"
    case_start = 5
    expected = "6"

    params = Params(context)
    params.optional_sequence(case_param, case_start)
    output = params.optional_sequence(case_param, case_start)
    assert expected == output


def test_return_value_overriding_optional_sequence_value(context) -> None:
    case_args = ["SomeParam: 1"]
    case_param_seq = "SomeParam"
    case_start = 3
    expected = "1"

    params = Params(context, case_args)
    output = params.optional_sequence(case_param_seq, case_start)
    assert expected == output


def test_alias_name_with_different_value(context) -> None:
    case_args = ["name: nameTest"]
    case_param_alias = "name"
    expected = "name"

    params: Params = Params(context, case_args)
    output = params.alias(case_param_alias)
    assert expected != output


def test_alias_name_with_unique_value(context) -> None:
    case_args = ["name1: nameTest", "name2: nameTest2"]
    case_alias1 = "name1"
    case_alias2 = "name2"

    params = Params(context, case_args)
    output1 = params.alias(case_alias1)
    output2 = params.alias(case_alias2)

    assert output1 != output2


def test_return_default_value_given_alias(context) -> None:
    case_name = "name"
    case_default = "someDefaultName"
    expected = case_default

    params = Params(context)
    alias = params.alias(case_name, case_default)
    output = params.decode_alias(alias)

    assert expected == output


def test_return_empty_str_when_decoding_and_alias_not_found(context) -> None:
    case = "UnknownAlias"
    expected = ""

    params = Params(context)
    output = params.decode_alias(case)
    assert expected == output


def test_fail_alias_if_value_not_present(context) -> None:
    case_args = ["name: nameTest"]
    case = "name2"

    params = Params(context, case_args)
    with pytest.raises(ValueError):
        params.alias(case)


def test_supply_consistent_alias_within_context(context) -> None:
    case_args = ["name: nameTest"]
    case_alias = "name"

    params = Params(context, case_args)
    expected = params.alias(case_alias)
    output = params.alias(case_alias)

    assert expected == output


def test_supply_different_alias_for_same_name_across_contexts(context) -> None:
    case_args = ["name: nameTest"]
    case_alias = "name"

    params = Params(context, case_args)
    other_context = DslContext()
    other_params = Params(other_context, case_args)

    output = params.alias(case_alias)
    output_other = other_params.alias(case_alias)
    assert output != output_other


def test_use_supplied_name_as_root_of_alias(context) -> None:
    case_args = ["name: nameTest"]
    case_name = "name"

    params = Params(context, case_args)
    output = params.alias(case_name)
    assert output.startswith(case_name)


def test_use_default_value_as_root_of_alias(context) -> None:
    case_name = "name"
    case_default = "defaultValue"

    params = Params(context)
    output = params.alias(case_name, case_default)
    assert output.startswith(case_default)
