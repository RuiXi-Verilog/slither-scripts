def log_matches(matches, log_return=True):
    """
    Parameters
    ----------
    matches : iterable
        Iterable of tuples (Signature, bool)
    """
    for match in matches:
        mark = '\u2713' if match[1] else 'x'
        print(f"[{mark}] {match[0].to_string(log_return)}")


def log_event_per_function(matches, expected_events):
    """
    Parameters
    ----------
    matches : iterable
        Iterable of tuples (Signature, bool)

    expected_events : list(Signature)
    """
    for match in matches:
        function_name = match[0].name
        expected_event = expected_events[function_name].to_string(with_return=False)
        mark = '\u2713' if match[1] else 'x'
        print(f"[{mark}] {function_name} must emit {expected_event}")


def log_modifiers_per_function(matches):
    """
    Parameters
    ----------
    matches : iterable
        Iterable of tuples (Signature, list(slither.core.declarations.Modifier))
    """
    printed = False
    for match in matches:
        print(
            f"[x] {match[0].name} modified by {', '.join([mod.full_name for mod in match[1]])}"
        )
        printed = True
    if not printed:
        print("[\u2713] No custom modifiers in ERC20 functions")
