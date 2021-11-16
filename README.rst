=========================================
Numeric pseudonym generation for Stratify
=========================================

We generated PSC1 codes on 20 July 2017, 13 December 2017, 17 September 2018 and 16 November 2021 using these commands::

    ./stratify_generate_psc1.py | sort > stratify_codes_2017-07-20.txt
    ./stratify_generate_psc1_berlin.py | sort > stratify_codes_berlin_2017-12-13.txt
    ./stratify_generate_psc1_aachen.py | sort > stratify_codes_aachen_2018-09-17.txt
    ./stratify_generate_psc1_london_2021.py | sort | head -200 > stratify_codes_2021-11-16.txt

We generated PSC2 codes on 20 July 2017, 21 December 2017, 17 September 2018 and 16 November 2021 using these commands::

    ./stratify_generate_psc2.py | sort > stratify_psc2_2017-07-28.txt
    ./stratify_generate_psc2_berlin.py | sort > stratify_psc2_berlin_2017-12-21.txt
    ./stratify_generate_psc2_aachen.py | sort > stratify_psc2_aachen_2018-09-17.txt
    ./stratify_generate_psc2_london_2021.py | sort > stratify_psc2_london_2021-11-16.txt
