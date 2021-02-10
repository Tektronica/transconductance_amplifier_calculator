import math

# TODO -  LCAPY for circuit rendering?

"""
def TCA_2(Vsupply, Vin, Gain, Rset, Ioffset, Ra, R2, beta=100):
    # Balanced Complementary Class-A TCA
    Vpeak = Vin * 1.4149
    Iout_max = Vpeak * Gain  # A

    Vemitter_max = Vsupply - Ioffset * ((beta + 1) / beta) * Rset
    Vemitter_min = Vsupply - (Iout_max * ((beta + 1) / beta) + Ioffset) * Rset
    Vemitter_swing = Vemitter_max - Vemitter_min
    Vemitter_mid = Vemitter_max - Vemitter_swing / 2

    Rb = Ra * (Vemitter_mid / (Vsupply - Vemitter_mid))

    gain_input = ((Vemitter_swing / (2 * Vpeak)) * (1 + Rb / Ra))
    R1 = R2 * (gain_input - 1)

    return R1, Rb
"""


def print_dictionary(d):
    for k, v in d.items():
        print(k)
        print('------------------------------------')
        for _k, _v in v.items():
            print(f'{_k}: {_v}')
        print('')


def TCA_circuit():
    # from lcapy import Circuit
    # cct = Circuit('TCA.sch')
    # cct.draw()
    pass


# TODO - Simplified model
def TCA_1(Vsupply, Vinput, transconductance, Rset, Iquiescent, Ra=1000, R2=10000, beta=100):
    # Balanced Complementary Class-A TCA
    Vpeak = Vinput * 1.4149
    Ipeak = Vpeak * transconductance

    a = beta / (beta + 1)
    Imid = (Ipeak / 2) / a

    Vin = Imid * Rset
    Voffset = Vsupply - Rset * (Imid + Iquiescent / a)

    Rb = Ra * (Vsupply / (Vsupply - Voffset) - 1)

    gain = ((Vin + Voffset) * (Ra + Rb) - Vsupply * Rb) / (Ra * Vpeak)
    R1 = R2 * (gain - 1)

    return {'R1': round(R1, 2), 'Rb': round(Rb, 2)}


def get_1A3A_Values(Vsupply, Rset, Ra=1000, R2=10000, beta=100):
    HighTCA_dict = {'1.2A': TCA_1(Vsupply=Vsupply, Vinput=6, transconductance=0.2,
                                  Rset=Rset, Iquiescent=0.150, Ra=Ra, R2=R2, beta=beta),

                    '3.1A': TCA_1(Vsupply=Vsupply, Vinput=3.1, transconductance=1,
                                  Rset=Rset, Iquiescent=0.1, Ra=Ra, R2=R2, beta=beta)}
    print_dictionary(HighTCA_dict)

    print('------------------------------------')
    # the value used in parallel with the 3.1A range resistor when in the 1.2A range
    R11 = HighTCA_dict['1.2A']['R1']
    R13 = HighTCA_dict['3.1A']['R1']
    try:
        R1_parallel = round(1 / (1 / R11 - 1 / R13), 2)
    except ZeroDivisionError:
        print(f'No parallel value needed for R1')
    else:
        print(f'parallel R1: {R1_parallel} for 1.2A')

    # the value used in parallel with the 1.2A range resistor when in the 3.1A range
    Rb1 = HighTCA_dict['1.2A']['Rb']
    Rb3 = HighTCA_dict['3.1A']['Rb']
    Rb_parallel = round(1 / (1 / Rb3 - 1 / Rb1), 2)
    print(f'parallel Rb: {Rb_parallel} for 3.1A')
    print('------------------------------------')


def main():
    # Balanced Complementary Class-A TCA -------------------------------------------------------------------------------
    Vsupply = 10
    Rset = 0.2

    get_1A3A_Values(Vsupply, Rset)


if __name__ == '__main__':
    main()
