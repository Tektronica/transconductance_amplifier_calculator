# TODO -  LCAPY for circuit rendering?


def TCA_0(Vsupply, Vin, Gain, Rset, Ioffset, Ra, R2, beta=100):
    # Single Class-A TCA
    Vpeak = Vin * 1.4149
    Iout_max = Vpeak * Gain + Ioffset

    Vemitter_max = Vsupply - Ioffset * ((beta + 1) / beta) * Rset
    Vemitter_min = Vsupply - (Iout_max * ((beta + 1) / beta)) * Rset
    Vemitter_swing = Vemitter_max - Vemitter_min

    Rb = Ra * (Vemitter_min / (Vsupply - Vemitter_min))

    gain_input = ((Vemitter_swing / Vpeak) * (1 + Rb / Ra))
    R1 = R2 * (gain_input - 1)

    return R1, Rb


def TCA_1(Vsupply, Vin, Gain, Rset, Ioffset, Ra, R2, beta=100):
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


def TCA_circuit():
    # from lcapy import Circuit
    # cct = Circuit('TCA.sch')
    # cct.draw()
    pass


def main():
    # Single Class-A TCA -----------------------------------------------------------------------------------------------
    Vsupply = 10
    Vin = 1
    Gain = 1  # A/V
    Rset = 0.4
    Ioffset = 0.01  # A
    beta = 100

    R2 = 10000
    Ra = 1000

    R1, Rb = TCA_0(Vsupply, Vin, Gain, Rset, Ioffset, Ra, R2, beta)
    print('Single Class-A TCA')
    print(f'R1: {round(R1, 2)}\tR2: {round(R2, 2)}\nRa: {round(Ra, 2)}\tRb: {round(Rb, 2)}')

    # Balanced Complementary Class-A TCA -------------------------------------------------------------------------------
    Vsupply = 10
    Vin = 6
    Gain = 0.517  # A/V
    Rset = 0.04
    Ioffset = 0.130  # A
    beta = 100

    R2 = 10000
    Ra = 1000

    R1, Rb = TCA_1(Vsupply, Vin, Gain, Rset, Ioffset, Ra, R2, beta)
    print('\nBalanced Complementary Class-A TCA')
    print(f'R1: {round(R1, 2)}\tR2: {round(R2, 2)}\nRa: {round(Ra, 2)}\tRb: {round(Rb, 2)}')


if __name__ == '__main__':
    main()