# from .behavior import update_a
from .model.allocate_payments import (allocated_funds, unallocated_funds,
                                      check_subcontractors,
                                      allocate_funds_to_member_subcontractors
                                      )

from .model.leaves import (should_leaves, leaves,
                           decrement_allocated_funds_due_to_leaves,
                           increment_unallocated_funds_due_to_forfeit_stake,
                           allowed_to_leave)

from .model.joins import should_join, joins

from .model.helper_functions import count_subcontractors

from .model.claims import (should_make_claims, make_claims,
                           decrement_allocated_funds_by_claims)

from .model.bookkeeping import update_time_attached, total_subcontractor_stake

from .model.payments import payment_to_unallocated

from .behavior import payment_amt

psubs = [
    {
        'label': 'Update Time Attached',
        'policies': {
        },
        'variables': {
            'subcontractors': update_time_attached
        }
    },
    {
        'label': 'Payments',
        'policies': {
            'payment_amt': payment_amt  # how much is paid in.
        },
        'variables': {
            'unallocated_funds': payment_to_unallocated
        },
    },
    {
        'label': 'Allocate Payments',
        'policies': {
            'check_subcontractors': check_subcontractors
        },
        'variables': {
            'allocated_funds': allocated_funds,       # A
            'unallocated_funds': unallocated_funds,   # R
            'subcontractors': allocate_funds_to_member_subcontractors,
        }
    },
    {
        'label': 'Claims',
        'policies': {
            'should_make_claims': should_make_claims
        },
        'variables': {
            'subcontractors': make_claims,
            'allocated_funds': decrement_allocated_funds_by_claims
        },
    },
    {
        'label': 'Allowed to Leave',
        'policies': {},
        'variables': {
            'subcontractors': allowed_to_leave
        },
    },
    {
        'label': 'Leaves',
        'policies': {
            'should_leaves': should_leaves
            },
        'variables': {
            'subcontractors': leaves,
            'allocated_funds': decrement_allocated_funds_due_to_leaves,
            'unallocated_funds': increment_unallocated_funds_due_to_forfeit_stake,
            'num_member_subcontractors': count_subcontractors
            }
    },
    {
        # if there's a vacant spot, flip a coin
        # (heads, they join, tails nobody joins)
        'label': 'Joins',
        'policies': {
            'should_join': should_join
            },
        'variables': {
            'subcontractors': joins,
            'num_member_subcontractors': count_subcontractors,
            },
    },
    {
        'label': 'Bookkeeping',
        'policies': {
        },
        'variables': {
            'total_subcontractor_stake': total_subcontractor_stake,
            'subcontractors': update_time_attached
        }

    }
]
