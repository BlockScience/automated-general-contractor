

def count_members(subcontractors):
    value = sum(1 for subcontractor in subcontractors.values() if subcontractor.member)
    return value


def count_subcontractors(params, step, prev_states, state, input):

    value = count_members(state['subcontractors'])
    key = 'num_member_subcontractors'
    return key, value
    