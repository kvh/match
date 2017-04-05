
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
    'datetime': {
        'valid': [
            'Sep 25 2003',
            'Sep 25th 2003',
            'Sep 25 10:36:28 2003',
            'Thu Sep 25 2003',
            'Thu Sep 25th 2003',
            'Thu Sep 25 10:36:28 2003',
            'Thursday Sep 25 10:36:28 2003',
            'Thursday September 25 10:36:28 2003',
            'Thursday September 25th 10:36:28am 2003',
            '2003-09-25T10:49:41.5-03:00',
            '2003-09-25T10:49:41',
            '20030925T104941-0300',
            '20030925T104941',
            1064486188,
            1064486188000,
            '1064486188',
            '1064486188000',
        ],
        'invalid': [
            # '64th of February', Well, dateutil.parser actually likes this one...
            '1st of Neptune',
            'Neptune 1',
            'definitely not a date',
            '10000000000000000000000',
            'ahem',
        ],
        'equivalent': [
            # First is normalized version
            '2003-09-25T10:36:28',

            'Thu Sep 25 10:36:28 2003',
            'Thursday Sep 25 10:36:28 2003',
            'Thursday September 25 10:36:28 2003',
            'Thursday September 25th 10:36:28am 2003',
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

