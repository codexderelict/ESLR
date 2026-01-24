from .constemplate import Constraint 
constraints = [
    Constraint(
        check=[
            lambda p: p.w1.check("pos", "preposition"),
            lambda p: p.w1.check("type","abl"),
            lambda p: p.w2.check("case","abl"),
            lambda p: p.difference == -1 
        ],
        actions=[
            lambda p: p.w2.make_assertion("case","abl")
        ]
    )
]