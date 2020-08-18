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
