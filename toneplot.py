from collections import defaultdict
from fractions import Fraction
import matplotlib.pyplot as plt
from math import lcm
from math import gcd
from itertools import combinations

C_4 = 261.6256
TWELVE_TET_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def get_closest_scientific_pitch(fraction, fundamental_frequency=C_4):
    fraction_as_pitch = fraction * fundamental_frequency
    smallest_diff = 100000
    name_number = '-'
    for n in range(-48, 60):
        scientific_pitch = C_4 * 2 ** (n / 12)
        current_diff = abs(fraction_as_pitch - scientific_pitch)
        if current_diff < smallest_diff:
            smallest_diff = current_diff
            name_number = n
    pitch_name = TWELVE_TET_NAMES[name_number % 12] + f'{4 + name_number // 12}'
    return fraction, pitch_name, smallest_diff / (C_4 * 2 ** (name_number / 12)), smallest_diff


def get_lcm_for_fractions(*fractions: Fraction):
    fractions_gcd = gcd(*[fraction.denominator for fraction in fractions])
    fractions_lcm = Fraction(lcm(*[fraction.numerator for fraction in fractions]), fractions_gcd)
    return fractions_lcm


def get_lcm_for_combinations(fractions: set[Fraction, Fraction, ...]) -> list[Fraction]:
    lcm_combinations = set()
    for i in range(2, len(fractions) + 1):
        for combination in combinations(fractions, r=i):
            lcm_combinations.add(get_lcm_for_fractions(*combination))
    return sorted(lcm_combinations)


def get_all_notes_with_dissonance_less_than(max_dissonance):
    all_notes = defaultdict(list)
    for dissonance in range(2, max_dissonance + 1):
        for j in range(1, dissonance):
            k = dissonance - j
            fraction = Fraction(j, k)
            if fraction not in all_notes[dissonance]:
                all_notes[dissonance].append(fraction)
    for notes in all_notes.values():
        notes.sort()
    return all_notes


def get_unique_notes_with_dissonance_less_than(max_dissonance):
    unique_notes = {fraction for fractions in get_all_notes_with_dissonance_less_than(max_dissonance).values() for
                    fraction in fractions}
    return sorted(list(unique_notes))


def get_colors_by_consonance(unique_fractions, max_dissonance):
    rgb = [(0, 0, 0), (0, 0, 1), (0, 0.5, 0.5), (0, 1, 0), (0.5, 0.5, 0), (1, 0, 0)] + [(0, 0, 0)] * max_dissonance
    return [rgb[fraction.denominator] for fraction in unique_fractions]


def get_heights_by_dissonance(unique_fractions):
    return [fraction.numerator + fraction.denominator - 1 for fraction in unique_fractions]


def get_widths_by_fractions(unique_fractions):
    widths = [(unique_fractions[i + 1] - unique_fractions[i]) * 0.8 / 2 for i in range(len(unique_fractions) - 1)]
    widths = widths + [widths[-1]]
    return widths


def get_undertones_for_harmonic(harmonic, number_of_undertones):
    return [Fraction(harmonic, i) for i in range(1, number_of_undertones + 1)]


def get_octave_reduction(fraction, octave=2):
    while fraction >= 1:
        fraction = fraction / octave
    while fraction < 1:
        fraction = fraction * octave
    return fraction


def get_octave_pair(fraction, octave=2):
    fraction = get_octave_reduction(fraction, octave)
    octave_pair = Fraction(fraction.denominator, fraction.numerator)
    return fraction, get_octave_reduction(octave_pair, octave)


def get_extended_octave_pair(fraction, octaves):
    extended_octave_pair = set()
    for octave in octaves:
        extended_octave_pair.update(get_octave_pair(fraction, octave))
    return extended_octave_pair


def plot_notes_with_dissonance_less_than(max_dissonance):
    # noinspection PyTypeChecker
    fig, axs = plt.subplots(1, 2, sharey=True)
    ratios = get_unique_notes_with_dissonance_less_than(max_dissonance)
    ratios_one_and_below = ratios[:ratios.index(Fraction(1, 1)) + 1]
    ratios_one_and_above = ratios[ratios.index(Fraction(1, 1)):]

    ax1 = axs[0]
    ax1.set_xscale('log')
    bar_colors = get_colors_by_consonance(ratios_one_and_below, max_dissonance)
    bar_heights = get_heights_by_dissonance(ratios_one_and_below)
    bar_widths = get_widths_by_fractions(ratios_one_and_below)
    ax1.bar(ratios_one_and_below, bar_heights, width=bar_widths, color=bar_colors,
            **{'edgecolor': 'black', 'linewidth': 0.5})

    ax2 = axs[1]
    bar_colors = get_colors_by_consonance(ratios_one_and_above, max_dissonance)
    bar_heights = get_heights_by_dissonance(ratios_one_and_above)
    bar_widths = get_widths_by_fractions(ratios_one_and_above)
    ax2.bar(ratios_one_and_above, bar_heights, width=bar_widths, color=bar_colors,
            **{'edgecolor': 'black', 'linewidth': 0.5})

    fig.subplots_adjust(wspace=0)

    ax1.set_xlim(float(ratios_one_and_below[0]), float(ratios_one_and_below[-1]))
    ax2.set_xlim(float(ratios_one_and_above[0]), float(ratios_one_and_above[-1]))

    ax1.spines.right.set_visible(False)
    ax2.spines.left.set_visible(False)
    ax2.tick_params(which='both', left=False)
    plt.setp(ax2.get_xticklabels()[0], visible=False)

    plt.show()


def plot_wavelength_multiples_for_fraction_sets(fraction_sets: list[set[Fraction, ...], ...], lcm_plot=False,
                                                title=None, label_style=None):
    fig, axs = plt.subplots(len(fraction_sets), 1, layout='constrained', squeeze=False)
    for i in range(len(fraction_sets)):
        plot_wavelength_multiples_for_fractions(axs[i][0], fraction_sets[i], lcm_plot, title, label_style)


def plot_wavelength_multiples_for_fractions(ax, fractions, lcm_plot, title, label_style):
    wavelengths = sorted([Fraction(fraction.denominator, fraction.numerator) for fraction in fractions], reverse=True)
    global_wavelength_lcm = get_lcm_for_fractions(*wavelengths)
    all_multiples = set()

    for wavelength in wavelengths:
        if lcm_plot:
            multiples = int(global_wavelength_lcm * wavelength.denominator / wavelength.numerator)
        else:
            multiples = wavelength.denominator

        current_wavelengths = [wavelength * i for i in range(1, multiples + 1)]
        all_multiples.update(current_wavelengths)

        bar_heights = [wavelength] * len(current_wavelengths)
        bar_widths = [-wavelength] * len(current_wavelengths)
        ax.bar(current_wavelengths, bar_heights, bar_widths, align='edge', **{'edgecolor': 'black', 'linewidth': 0.5})

    if label_style[:3] == 'lcm':
        lcm_for_combinations = get_lcm_for_combinations(set(wavelengths))
        lcm_multiples = set()
        if label_style == 'lcm_print':
            for combination_lcm in sorted(lcm_for_combinations):
                print(combination_lcm)
        for lcm_for_combination in lcm_for_combinations:
            multiples = int(global_wavelength_lcm * lcm_for_combination.denominator / lcm_for_combination.numerator)
            lcm_multiples.update([lcm_for_combination * i for i in range(1, multiples + 1)])

        lcm_multiples.add(Fraction(0))
        x_ticks = list(lcm_multiples)
    else:
        x_ticks = sorted(all_multiples) + [0]
    y_ticks = sorted(wavelengths) + [Fraction(0), Fraction(1)]

    ax.set_xticks(x_ticks, x_ticks)
    ax.set_yticks(y_ticks, y_ticks)

    ax.set_xlabel('Wavelength')
    ax.set_ylabel('Original Wavelength')
    ax.margins(0)
    ax.set_title(title)


def temp():
    A_sharp_6_major = {Fraction(7), Fraction(7 * 5, 4), Fraction(7 * 3, 2)}
    C_4_major = {Fraction(1), Fraction(5, 4), Fraction(3, 2)}
    C_5_major = {Fraction(2), Fraction(2 * 5, 4), Fraction(2 * 3, 2)}
    C_6_major = {Fraction(4), Fraction(4 * 5, 4), Fraction(4 * 3, 2)}
    C_4_minor = {Fraction(1), Fraction(6, 5), Fraction(3, 2)}
    C_sharp_4_major = {Fraction(16, 15), Fraction(16 * 5, 15 * 4), Fraction(16 * 3, 15 * 2)}
    D_4_major = {Fraction(9, 8), Fraction(9 * 5, 8 * 4), Fraction(9 * 3, 8 * 2)}
    E_6_major = {Fraction(5), Fraction(5 * 5, 4), Fraction(5 * 3, 2)}
    F_4_major = {Fraction(4, 3), Fraction(4 * 5, 3 * 4), Fraction(4 * 3, 3 * 2)}
    F_3_major = {Fraction(2, 3), Fraction(2 * 5, 3 * 4), Fraction(2 * 3, 3 * 2)}
    G_4_major = {Fraction(3, 2), Fraction(15, 8), Fraction(9, 4)}
    G_5_major = {Fraction(3), Fraction(3 * 5, 4), Fraction(3 * 3, 2)}
    G_6_major = {Fraction(6), Fraction(6 * 5, 4), Fraction(6 * 3, 2)}
    Bb_4_major = {Fraction(7, 4), Fraction(7 * 5, 4 * 4), Fraction(7 * 3, 4 * 2)}
    Bb_6_major = {Fraction(7, 1), Fraction(7 * 5, 1 * 4), Fraction(7 * 3, 1 * 2)}

    # my_fractions = [C_4_major, C_4_major | C_5_major, C_4_major | C_5_major | G_5_major]
    my_fractions = [
        # C_4_major,
        # C_4_major | C_5_major,
        C_4_major | C_5_major | G_5_major,
        # C_4_major | C_5_major | G_5_major | C_6_major,
        # C_4_major | C_5_major | G_5_major | C_6_major | E_6_major,
        # C_4_major | C_5_major | G_5_major | C_6_major | E_6_major | G_6_major,
        # C_4_major | C_5_major | G_5_major | C_6_major | E_6_major | G_6_major | A_sharp_6_major
    ]
    my_inverted_fractions = [{Fraction(fraction.denominator, fraction.numerator) for fraction in fractions} for
                             fractions in my_fractions]
    plot_wavelength_multiples_for_fraction_sets(my_fractions, lcm_plot=True, label_style='lcm_print')
    # plot_wavelength_multiples_for_fraction_sets(my_inverted_fractions, lcm_plot=True)


def plot_harmonic_undertones():
    for harmonic in range(3, 7):
        my_fractions = [{Fraction(i, j) for i in range(1, harmonic + 1) for j in range(1, i + 1)}]
        plot_wavelength_multiples_for_fraction_sets(my_fractions, lcm_plot=True, title=f"Max harmonic {harmonic}")


if __name__ == '__main__':
    # TODO: "naturliga" toner borde vara bra på att behålla lcm för ackord. Implicerar små primtalskonsonanser.
    # TODO: Hur ser lcm ut vid vanliga ackordövergångar? Virtuella ackord p.g.a. rytm?
    # TODO: Hur ser lcm ut vid vanliga melodier?
    # for i in range(1, 10):
    #    for j in range(1, 10):
    #        print(get_closest_scientific_pitch(Fraction(i, j)))
    temp()
    plt.show()
