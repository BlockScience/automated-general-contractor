def update_time_attached(params, step, sL, s, inputs):

    for subcontractor in s['subcontractors'].values():
        if subcontractor.member:
            subcontractor.time_attached += 1

    key = 'subcontractors'
    value = s['subcontractors']

    return key, value


def total_subcontractor_stake(params, step, sL, s, inputs):
    total_subcontractor_stake = sum([b.stake for b in s['subcontractors'].values()])

    key = 'total_subcontractor_stake'
    value = total_subcontractor_stake

    return key, value
