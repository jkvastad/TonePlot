from collections import defaultdict
from fractions import Fraction
import matplotlib.pyplot as plt
from math import lcm
from math import gcd

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


def get_undertones_for_harmonic(harmonic, number_of_undertones):
    return [Fraction(harmonic, i) for i in range(1, number_of_undertones + 1)]


def plot_undertones_for_harmonics(harmonics: list[int, ...]):
    fig, ax = plt.subplots(1, 1, layout='constrained')
    ax.set_xlabel('Fraction')
    ax.set_ylabel('Harmonic')

    harmonics = sorted(harmonics, reverse=True)
    all_undertones = set()

    for harmonic in harmonics:
        undertones = get_undertones_for_harmonic(harmonic, 2 * harmonic)
        all_undertones.update(undertones)
        wavelengths = [Fraction(undertone.denominator, undertone.numerator) for undertone in undertones]

        bar_heights = [harmonic] * len(undertones)
        bar_widths = [Fraction(-1, harmonic)] * len(undertones)
        ax.bar(wavelengths, bar_heights, bar_widths, align='edge', **{'edgecolor': 'black', 'linewidth': 0.5})

    all_undertones.add(Fraction(1, 1))
    all_wavelengths = {Fraction(undertone.denominator, undertone.numerator) for undertone in all_undertones}
    # ax.set_xticks(sorted(all_wavelengths), sorted(all_undertones, reverse=True))

    x_ticks = sorted(all_wavelengths) + [0]
    ax.set_xticks(x_ticks, x_ticks)

    plt.show()


def plot_wavelength_multiples_for_fraction_sets(fraction_sets: list[set[Fraction, ...], ...], lcm_plot=False):
    fig, axs = plt.subplots(len(fraction_sets), 1, layout='constrained', squeeze=False)
    for i in range(len(fraction_sets)):
        plot_wavelength_multiples_for_fractions(axs[i][0], fraction_sets[i], lcm_plot)


def plot_wavelength_multiples_for_fractions(ax, fractions, lcm_plot):
    wavelengths = sorted([Fraction(fraction.denominator, fraction.numerator) for fraction in fractions], reverse=True)
    wavelength_gcd = gcd(*[fraction.denominator for fraction in wavelengths])
    wavelength_lcm = lcm(*[fraction.numerator for fraction in wavelengths])  # / wavelength_gcd
    all_multiples = set()

    for wavelength in wavelengths:
        if lcm_plot:
            multiples = int(wavelength_lcm * wavelength.denominator / wavelength.numerator)
        elif wavelength == Fraction(1):
            multiples = max(wavelength.numerator for wavelength in wavelengths)
        else:
            multiples = wavelength.denominator

        current_wavelengths = [wavelength * i for i in range(1, multiples + 1)]
        all_multiples.update(current_wavelengths)

        bar_heights = [wavelength] * len(current_wavelengths)
        bar_widths = [-wavelength] * len(current_wavelengths)
        ax.bar(current_wavelengths, bar_heights, bar_widths, align='edge', **{'edgecolor': 'black', 'linewidth': 0.5})

    x_ticks = sorted(all_multiples) + [0]
    y_ticks = sorted(wavelengths) + [Fraction(0), Fraction(1)]
    ax.set_xticks(x_ticks, x_ticks)
    ax.set_yticks(y_ticks, y_ticks)

    ax.margins(0)

    ax.set_xlabel('Wavelength')
    ax.set_ylabel('Original Wavelength')


if __name__ == '__main__':
    C_4_major = {Fraction(1), Fraction(5, 4), Fraction(3, 2)}
    D_4_major = {Fraction(9, 8), Fraction(9 * 5, 8 * 4), Fraction(9 * 3, 8 * 2)}
    G_4_major = {Fraction(3, 2), Fraction(15, 8), Fraction(9, 4)}
    Bb_4_major = {Fraction(7, 4), Fraction(7 * 5, 4 * 4), Fraction(7 * 3, 4 * 2)}
    Bb_6_major = {Fraction(7, 1), Fraction(7 * 5, 1 * 4), Fraction(7 * 3, 1 * 2)}

    # print(get_closest_scientific_pitch(Fraction(7)))

    my_fractions = [C_4_major, {fraction * 2 for fraction in sorted(C_4_major)[1:]} | {Fraction(1)},
                    {fraction * 3 for fraction in sorted(C_4_major)[1:]} | {Fraction(1)}]
    plot_wavelength_multiples_for_fraction_sets(my_fractions, lcm_plot=True)
    plt.show()
