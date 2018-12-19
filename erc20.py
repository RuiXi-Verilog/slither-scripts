#!/usr/bin/python3
import sys
from slither.slither import Slither
from slither.slithir.operations.event_call import EventCall
from constants import (
    ERC20_EVENT_SIGNATURES,
    ERC20_FX_SIGNATURES, ERC20_GETTERS,
    ERC20_EVENT_BY_FUNCTION
)


def is_visible(function):
    """Check if function's visibility is external or public"""
    return is_public(function) or is_external(function)


def is_external(function):
    """Check if function's visibility is external"""
    return function.visibility == "external"


def is_public(element):
    """Check if element's (Function or Event) visibility is public"""
    return element.visibility == "public"


def find_match(elements, signature):
    """
    Check whether a signature is found in a list of elements

    Parameters
    ----------
    elements : list
        List of slither.core.declarations.Event or slither.core.declarations.Function

    signature : Signature

    Returns
    -------
    slither.core.declarations.Event or slither.core.declarations.Function
        Element that matches the signature
    None otherwise.
    """
    return next((e for e in elements if e.signature == signature), None)


def verify_signatures(elements, expected_signatures):
    """
    Compares a list of elements (functions or events) and expected signatures.
    Returns a list of tuples containing (Signature, matching object or None)
    """
    return [(sig, find_match(elements, sig)) for sig in expected_signatures]


def verify_getters(state_variables, functions, expected_getters):
    """
    Checks whether a list of getters is present
    either as public state variables or as visible functions.

    Parameters
    ----------
    state_variables : list

    functions : list

    expected_getters : list

    Returns
    -------
    generator : containing tuples (Signature, bool)
    """
    for getter in expected_getters:
        # Check in state variables. If none is found, check in functions.
        if (
            any(name_and_return_match(v, getter) and is_public(v) for v in state_variables) or
            find_match(functions, getter)
        ):
            yield (getter, True)
        else:
            yield (getter, False)


def verify_erc20_event_calls(function_matches):
    """
    Checks if ERC20 functions found emit the expected ERC20 events

    Parameters
    ----------
    function_matches : list
        List of tuples (Signature, slither.core.declarations.Function or None)

    Returns
    -------
    generator
        Generator of tuples (Signature, bool)
    """
    for match in function_matches:
        if match[1] and ERC20_EVENT_BY_FUNCTION[match[0].name]:
            yield (match[0], emits_event(match[1], ERC20_EVENT_BY_FUNCTION[match[1].name]))


def name_and_return_match(variable, signature):
    """
    Checks that a variable's name and type match a signature
    
    Parameters
    ----------
    variable : slither.solc_parsing.variables.state_variable.StateVariableSolc

    signature : Signature

    Returns
    -------
    bool
    """
    return (variable.name == signature.name and
            str(variable.type) == signature.returns[0])


def get_visible_functions(functions):
    """
    Filters a list of functions, keeping the visible ones

    Parameters
    ----------
    functions : list
        List of slither.core.declarations.Function

    Returns
    -------
    list
    """
    return [f for f in functions if is_visible(f)]


def log_matches(matches):
    """
    Parameters
    ----------
    matches : list
        List of tuples (Signature, bool)
    """
    for match in matches:
        mark = '\u2713' if match[1] else 'x'
        print(f"[{mark}] {match[0].to_string()}")


def log_event_per_function(matches):
    """
    Parameters
    ----------
    matches : list
        List of tuples (Signature, bool)
    """
    for match in matches:
        function_name = match[0].name
        expected_event = ERC20_EVENT_BY_FUNCTION[function_name].to_string()
        mark = '\u2713' if match[1] else 'x'
        print(f"[{mark}] {function_name} must emit {expected_event}")


def is_event_call(obj):
    """Returns True if given object is an instance of Slither's EventCall class. False otherwise."""
    return isinstance(obj, EventCall)


def get_events(function):
    """
    Get a generator to iterate over the events emitted by a function

    Parameters
    ----------
    function : slither.core.declarations.Function

    Returns
    -------
    generator
    """
    for node in getattr(function, 'nodes', []):
        for ir in node.irs:
            if is_event_call(ir):
                yield ir


def emits_event(function, expected_event):
    """
    Recursively check whether a function emits an event
    
    Parameters
    ----------
    function : slither.core.declarations.Function

    expected_event : Signature

    Returns
    -------
    bool
    """
    for event in get_events(function):
        if (
            event.name == expected_event.name and 
            all(str(arg.type) == expected_event.args[i] for i, arg in enumerate(event.arguments))
        ):
            return True

    # Event is not fired in function, so check internal calls to other functions
    if any(emits_event(f, expected_event) for f in getattr(function, 'internal_calls', [])):
        return True

    # Event is not fired in function nor in internal calls
    return False


def run(filename, contract_name):
    """Executes script"""

    # Init Slither
    slither = Slither(filename)

    # Get an instance of the contract to be analyzed
    contract = slither.get_contract_from_name(contract_name)
    if not contract:
        print(f"Contract {contract_name} not found")
        exit(-1)

    # Obtain visible functions
    visible_functions = get_visible_functions(contract.functions)

    # Check signature matches for functions and events
    function_matches = verify_signatures(visible_functions, ERC20_FX_SIGNATURES)
    event_definition_matches = verify_signatures(contract.events, ERC20_EVENT_SIGNATURES)

    functions_firing_events = verify_erc20_event_calls(function_matches)

    print("== ERC20 functions ==")
    log_matches(function_matches)

    print("\n== ERC20 events ==")
    log_matches(event_definition_matches)

    log_event_per_function(functions_firing_events)

    getters_matches = verify_getters(
        contract.state_variables,
        visible_functions,
        ERC20_GETTERS
    )
    print("\n== ERC20 getters ==")
    log_matches(getters_matches)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python erc20.py <contract.sol> <contract-name>')
        exit(-1)

    FILE_NAME = sys.argv[1]
    CONTRACT_NAME = sys.argv[2]
    run(FILE_NAME, CONTRACT_NAME)
