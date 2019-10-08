import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_POSTAL_CODE_REGEXES = [  # source : https://gist.github.com/paulredmond/57bcae03e75ffc3256b7e6be100275d3
    re.compile(
        r"""GIR[ ]?0AA|((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\d{1,4}$"""
    ),
    re.compile(r"""^JE\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}$"""),
    re.compile(r"""^GY\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}$"""),
    re.compile(r"""^IM\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}$"""),
    re.compile(r"""^\d{5}([ \-]\d{4})?$"""),
    re.compile(
        r"""^[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ ]?\d[ABCEGHJ-NPRSTV-Z]\d$"""
    ),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{3}-\d{4}$"""),
    re.compile(r"""^\d{2}[ ]?\d{3}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}[ ]?[A-Z]{2}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{3}[ ]?\d{2}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}[\-]?\d{3}$"""),
    re.compile(r"""^\d{4}([\-]\d{3})?$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^22\d{3}$"""),
    re.compile(r"""^\d{3}[\-]\d{3}$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^\d{3}(\d{2})?$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^AD\d{3}$"""),
    re.compile(r"""^([A-HJ-NP-Z])?\d{4}([A-Z]{3})?$"""),
    re.compile(r"""^(37)?\d{4}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^((1[0-2]|[2-9])\d{2})?$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^(BB\d{5})?$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^[A-Z]{2}[ ]?[A-Z0-9]{2}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^BBND 1ZZ$"""),
    re.compile(r"""^[A-Z]{2}[ ]?\d{4}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{7}$"""),
    re.compile(r"""^\d{4,5}|\d{3}-\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{3}[ ]?\d{2}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^([A-Z]\d{4}[A-Z]|(?:[A-Z]{2})?\d{6})?$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{3}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{3}[ ]?\d{2}$"""),
    re.compile(r"""^39\d{2}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^(?:\d{5})?$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{3}$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^(\d{4}([ ]?\d{4})?)?$"""),
    re.compile(r"""^(948[5-9])|(949[0-7])$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^[A-Z]{3}[ ]?\d{2,4}$"""),
    re.compile(r"""^(\d{3}[A-Z]{2}\d{3})?$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^980\d{2}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^((\d{4}-)?\d{3}-\d{3}(-\d{1})?)?$"""),
    re.compile(r"""^(\d{6})?$"""),
    re.compile(r"""^(PC )?\d{3}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{2}-\d{3}$"""),
    re.compile(r"""^00[679]\d{2}([ \-]\d{4})?$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^4789\d$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{3}[ ]?\d{2}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^00120$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^96799$"""),
    re.compile(r"""^6799$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^8\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^6798$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^FIQQ 1ZZ$"""),
    re.compile(r"""^2899$"""),
    re.compile(r"""^(9694[1-4])([ \-]\d{4})?$"""),
    re.compile(r"""^9[78]3\d{2}$"""),
    re.compile(r"""^\d{3}$"""),
    re.compile(r"""^9[78][01]\d{2}$"""),
    re.compile(r"""^SIQQ 1ZZ$"""),
    re.compile(r"""^969[123]\d([ \-]\d{4})?$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{3}$"""),
    re.compile(r"""^\d{3}$"""),
    re.compile(r"""^969[67]\d([ \-]\d{4})?$"""),
    re.compile(r"""^\d{6}$"""),
    re.compile(r"""^9695[012]([ \-]\d{4})?$"""),
    re.compile(r"""^9[78]2\d{2}$"""),
    re.compile(r"""^988\d{2}$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^008(([0-4]\d)|(5[01]))([ \-]\d{4})?$"""),
    re.compile(r"""^987\d{2}$"""),
    re.compile(r"""^\d{3}$"""),
    re.compile(r"""^9[78]5\d{2}$"""),
    re.compile(r"""^PCRN 1ZZ$"""),
    re.compile(r"""^96940$"""),
    re.compile(r"""^9[78]4\d{2}$"""),
    re.compile(r"""^(ASCN|STHL) 1ZZ$"""),
    re.compile(r"""^\d{4}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^[HLMS]\d{3}$"""),
    re.compile(r"""^TKCA 1ZZ$"""),
    re.compile(r"""^986\d{2}$"""),
    re.compile(r"""^\d{5}$"""),
    re.compile(r"""^976\d{2}$"""),
]


def _check_postal_code(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"PostalCode cannot represent a non string value: < {value} >"
        )
    match = False
    if value != "":
        for postal_code_regex in _POSTAL_CODE_REGEXES:
            if postal_code_regex.search(value):
                match = True
                break
    if not match:
        raise ValueError(f"Value is not a valid postal code: < {value} >")
    return value


class PostalCode:
    """
    Scalar which handles postal codes
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a postal code, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_postal_code(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a postal code
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a postal code
        """
        return _check_postal_code(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a postal code
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a postal code
        """
        return _check_postal_code(value)
