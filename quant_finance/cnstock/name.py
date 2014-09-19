from kuankr_utils import log, debug, unicode_utils

def normalize_name(name):
    """
    desc: 股票名规一化,半角,大写,去空格
    example:
    -   args: ["＊ＳＴ苏 宁"]
        ret : "*ST苏宁"
    """
    name = unicode_utils.strQ2B(name).replace(' ','').upper()
    return name


