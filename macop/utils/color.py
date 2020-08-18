import sys


class Colors:
    ENDC = '\033[m'
    GREEN = '\033[32m'
    GREY = '\033[90m'


def macop_text(msg):
    """Display Macop message to user interface
    """
    return Colors.GREEN + 'M' + Colors.ENDC + Colors.GREY + 'acop' \
        + Colors.ENDC + Colors.GREEN + ' :: ' + Colors.ENDC \
        + Colors.GREY + msg + Colors.ENDC


def macop_line():
    """Macop split line
    """
    line = ''

    for i in range(41):

        if i % 2 == 0:
            line += Colors.GREEN + '----' + Colors.ENDC
        else:
            line += Colors.GREY + '----' + Colors.ENDC

    return line


def macop_progress(evaluations, max):

    barWidth = 156

    progress = evaluations / float(max)

    output_str = Colors.GREEN + '[' + Colors.ENDC
    pos = int(barWidth * progress)
    for i in range(barWidth):
        if i < pos:
            output_str = output_str + Colors.GREY + '=' + Colors.ENDC
        elif i == pos:
            output_str = output_str + Colors.GREEN + '>' + Colors.ENDC
        else:
            output_str = output_str + Colors.GREY + ' ' + Colors.ENDC

    output_str = output_str + Colors.GREEN + '] ' + Colors.ENDC + str(
        int(progress * 100.0)) + "%\r"
    print(output_str)
    sys.stdout.write("\033[F")

    # go to line
    if progress >= 1.:
        print()
        print(macop_line())
