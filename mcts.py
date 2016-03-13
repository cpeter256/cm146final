from mcts_node import MCTSNode
from random import choice
from math import sqrt, log
from time import clock


num_nodes = 1000
explore_factor = 1.0    

def traverse_nodes(node, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """

    if len(node.untried_actions) > 0:
        return node

    max_child = None
    max_value = -1
    for child_act in node.child_nodes:
        child = node.child_nodes[child_act]
        #print("child: ", child)
        value = explore_factor*sqrt((2*log(node.visits))/child.visits);
        if state.turn == identity:
            value += child.consumed/child.visits
        else:
            value += 0 #1 - (child.consumeds/child.visits)
        if value > max_value:
            max_child = child
            max_value = value

    #max_child.visits += 1
    state.apply_move(max_child.parent_action)
    return traverse_nodes(max_child, state, identity)
    # Hint: return leaf_node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """

    # return current node if the game is already over
    #if state.is_terminal():
    #    return node

    # choose randomly I guess
    action = choice(node.untried_actions)

    node.untried_actions.remove(action)
    
    state.apply_move(action)
    node.child_nodes[action] = MCTSNode(parent=node, parent_action=action, action_list=state.legal_moves)

    #node.child_nodes[action].visits += 1
    return node.child_nodes[action]
    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """

    depth = 10 #TODO this isnt nearly enough
    
    while depth > 0:
        # shitty random rollout
        state.apply_move(choice(state.legal_moves))
        depth -= 1
        
    return state.ai_consumed


def backpropagate(node, consumed):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    #print("backprop: ", node)
    
    if node == None:
        return

    node.consumed += consumed
    node.visits += 1

    backpropagate(node.parent, won)
    
    pass


def think(state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity = state.turn
    root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)

    start_time = clock()
    for step in range(num_nodes):
    #while clock() < start_time+think_time:
        # Copy the game for sampling a playthrough
        sampled_game = state.copy()

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
    
        leaf = traverse_nodes(node, sampled_game, identity_of_bot)
        #print("Selected leaf: ", leaf)

        new_leaf = expand_leaf(leaf, sampled_game)
        #print("Expanded leaf: ", new_leaf)
        
        rollout_result = rollout(sampled_game)
        #print("rollout result: ", rollout_result)
        
        backpropagate(new_leaf, rollout_result)
        
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_node = None
    best_rate = -1
    for act in root_node.child_nodes:
        node = root_node.child_nodes[act]
        if node.visits == 0:
            continue
        node_rate = node.consumed/node.visits
        if node_rate > best_rate:
            best_rate = node_rate
            best_node = node

    print("MCTSBot picking ", best_node.parent_action, " with consumption rate ", best_rate)
    return best_node.parent_action
