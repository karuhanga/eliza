from src.one_start.actions.speech import resolve_keyword_action
from src.two_relay.actions import launch_application
from src.utils.constants import ACTIONS


def build_action(name, steps, last_n_prompts, action):
    return {
        'name': name,
        'steps': steps,
        'last_n_prompts': last_n_prompts,
        'action': action,
    }


def build_actions():
    results = {
        'launch': build_action("launch", 2, ["Which application would you like to open?", "Launching "], launch_application),
    }
    quick_actions = [{action: build_action(action, 1, ["Done."], resolve_keyword_action(action))} for action in ACTIONS.keys()]
    for action in quick_actions:
        results.update(action)
    return results


actions = build_actions()
