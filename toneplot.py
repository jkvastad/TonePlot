from collections import defaultdict
from fractions import Fraction
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def plot_notes_with_dissonance_less_than(max_dissonance):
    fig, axs = plt.subplots(1, 2, sharey=True)
    ratios = get_unique_notes_with_dissonance_less_than(max_dissonance)
    ratios_one_and_below = ratios[:ratios.index(Fraction(1, 1)) + 1]
    ratios_one_and_above = ratios[ratios.index(Fraction(1, 1)):]

    ax1 = axs[0]
    ax1.set_xscale('log')
    bar_colors = get_colors_by_consonance(ratios_one_and_below)
    bar_heights = get_heights_by_dissonance(ratios_one_and_below)
    bar_widths = get_widths_by_fractions(ratios_one_and_below)
    ax1.bar(ratios_one_and_below, bar_heights, width=bar_widths, color=bar_colors,
            **{'edgecolor': 'black', 'linewidth': 0.5})

    ax2 = axs[1]
    bar_colors = get_colors_by_consonance(ratios_one_and_above)
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


def get_colors_by_consonance(unique_fractions):
    return [(1 - 1 / fraction.denominator, 1 - 1 / fraction.denominator, 1) for fraction in
            unique_fractions]


def get_heights_by_dissonance(unique_fractions):
    return [fraction.numerator + fraction.denominator for fraction in unique_fractions]


def get_widths_by_fractions(unique_fractions):
    widths = [(unique_fractions[i + 1] - unique_fractions[i]) * 0.8 / 2 for i in range(len(unique_fractions) - 1)]
    widths = widths + [widths[-1]]
    return widths


def main():
    fig, ax = plt.subplots()
    unique_notes = sorted(get_unique_notes_with_dissonance_less_than(6))
    bar_colors = get_colors_by_consonance(unique_notes)
    bar_heights = get_heights_by_dissonance(unique_notes)
    bar_widths = get_widths_by_fractions(unique_notes)
    ax.bar(unique_notes, bar_heights, width=bar_widths, color=bar_colors, **{'edgecolor': 'black', 'linewidth': 0.5})
    plt.show()


if __name__ == '__main__':
    # TODO: Tick labels valbart som andel eller frekvens (ax.set_major_locator, ax.set_major_formatter)
    # TODO: lägg till legend för färg
    # TODO: lägg till ylabel för dissonans, xlabel för andel av grundton
    # TODO: Animerbar graf med valbar dissonans
    # TODO: tydligare färgningar för konsonansklasser, kanske en colorbar med nummer som förklarar gradienten?

    plot_notes_with_dissonance_less_than(10)
