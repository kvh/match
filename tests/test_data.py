
datatype_instances = {
    'phonenumber': {
        'valid': [
            '6083456789',
            '(608)3456789',
            '(608) 3456789',
            '(608) 345-6789',
            '608-345-6789',
            '608.345.6789',
            '+1608.345.6789',
            '+1 608.345.6789',
            '+1 (608) 345-6789',
        ],
        'invalid': [
            '608456789',
            '(23)3456789',
            '(608) 456789',
            '(608) 345-789',
            '1234(608)-345-6789',
        ],
        'equivalent': [
            # First is normalized version
            '+16083456789',

            '6083456789',
            '(608)3456789',
            '(608) 3456789',
            '(608) 345-6789',
            '608-345-6789',
            '608.345.6789',
            '+1608.345.6789',
            '+1 608.345.6789',
            '+1 (608) 345-6789',
        ]
    },
    'email': {
        'valid': [
            'k@r.vh',
            'a.b+c@a.b.cd',
            'AAA@bb.cc',
            'a_b_c@a.b.c.def',
            'aaaaaaaaaaaaa@bbbbb.ccccccccc',
        ],
        'invalid': [
            'a\nb@b.cd',
            'a b@b.cd',
            'b @b.cd',
            'a@b',
            'a@b.',
            'a@b. cd',
            'a@b.c',
            'aaaa@bbb. ccc',
        ],
        'equivalent': [
            # First is normalized version
            'a.b.c@bb.cc',

            ' a.b.c@bb.cc ',
            'a.b.c@BB.cc',
            'A.B.c@bb.cc',
            # 'A.B.c+d@BB.cc',
        ]
    },
}

