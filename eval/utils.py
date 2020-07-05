# Everything from HPL #


from collections import deque


pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    ')': '(',
    ']': '[',
    '}': '{',
}


symbols = (
    '(', ')', '{', '}', '[', ']',
    '<', '>', '=', '!',
    '+', '-', '*', '/', '%',
    ',', ':', '.', '\n', '#',
    '@', '&', '|', ';', ' ', '^',
    '`'
)

long_symbols = (
    '<=', '>=', '==', '!=',
)

white_spaces = (
    ' ', '\n', '\t'
)



def is_name(token):

    if token.isalnum() and not token[0].isnumeric():
        return True

    for t in token:

        if not(t.isalnum()) and t != '_':
            return False

    return True


def find_partner(tokens, index, reverse=False):

    start = tokens[index]
    partner = pairs[start]

    if reverse:
      stack = -1
      index -= 1

      while stack < 0:

          if tokens[index] == partner:
              stack += 1

          elif tokens[index] == start:
              stack -= 1

          index -= 1

      return index + 1

    else:
      stack = 1
      index += 1

      while stack > 0:

          if tokens[index] == partner:
              stack -= 1

          elif tokens[index] == start:
              stack += 1

          index += 1

      return index - 1


# parentheses could be either function call, function definition, or just parentheses
# IT MUST BE CALLED BEFORE ALL THE OTHER OPERATOR PACKERS
def pack_parentheses(tokens):
    
    i = 0

    while i < len(tokens):

        if tokens[i] == '(':

            if i > 0 and (is_name(tokens[i - 1]) or tokens[i - 1] == ')' or tokens[i - 1] == ':' or tokens[i - 1] == ']'):
                i += 1
                continue

            else:
                tokens = tokens[:i] + ['__bi_identity', '(', 'output', '='] + tokens[i + 1:]  # identity function -> will be removed later but it helps the parser parsing

        i += 1

    return tokens


def remove_identity_function(tokens):

    i = 0

    while i < len(tokens):

        if tokens[i] == '__bi_identity' and i + 1 < len(tokens) and tokens[i + 1] == '(':
            end = find_partner(tokens, i + 1)
            tokens = tokens[:i] + tokens[i + 4:end] + tokens[end + 1:]

        i += 1

    return tokens


# a() + b() -> add(p1=a(), p2=b())
def pack_binary_operators(tokens, target='+', func_name='__bi_add'):
    
    i = 0

    while i < len(tokens):

        if tokens[i] == target:

            where_it_begins = where_atom_begins(tokens, i - 1)
            a0 = tokens[where_it_begins:i]

            where_it_ends = where_atom_ends(tokens, i + 1)
            a1 = tokens[i + 1:where_it_ends + 1]

            tokens = tokens[:where_it_begins] + [func_name, '(', '__a0', '='] + a0 + [',', '__a1', '='] + a1 + [')'] + tokens[where_it_ends + 1:]

        i += 1

    return tokens


# - is a binary operator only when it's preceded by ), num, or name
def pack_unary_operators_2(tokens, target='-', func_name='__bi_neg'):

    i = 0

    while i < len(tokens):

        if tokens[i] == target:

            if i > 0 and (tokens[i - 1].isnumeric() or is_name(tokens[i - 1]) or tokens[i - 1] == ')'):
                i += 1
                continue

            else:
                to = where_atom_ends(tokens, i + 1)
                tokens = tokens[:i] + [func_name, '(', '__a0', '='] + tokens[i + 1:to + 1] + [')'] + tokens[to + 1:]

        i += 1

    return tokens


def where_atom_begins(tokens, index):
  
    if tokens[index].isnumeric():
        return index

    elif is_name(tokens[index]):
        return index

    elif tokens[index] in (')', ']'):
        return where_atom_begins(tokens, find_partner(tokens, index, True))

    elif tokens[index] in ('`', '^'):
        return where_atom_begins(tokens, index - 1)

    elif tokens[index] in ('(', '['):
        return find_func(tokens, index)


# tokens[index] -> begining of an atom
def where_atom_ends(tokens, index):

    if index + 1 >= len(tokens):
        return index

    elif tokens[index] in ('(', '['):
        return where_atom_ends(tokens, find_partner(tokens, index))

    elif tokens[index + 1] in ('(', '['):
        return where_atom_ends(tokens, find_partner(tokens, index + 1))

    elif tokens[index + 1] in ('^', '`'):
        return where_atom_ends(tokens, index + 1)

    else:
        return index


# tokens[index] is '(' or '['
# a(), a[]()[]() -> returns the index of 'a'
def find_func(tokens, index, recursive=False):

    if index == 0:
        
        if recursive:
            return 0

        return None
  
    elif is_name(tokens[index - 1]):
        return index - 1

    elif tokens[index - 1] in (')', ']'):
        return find_func(tokens, find_partner(tokens, index - 1, True), True)

    elif recursive:
        return index

    else:
        return None


# code -> tokens
def lexer(code):

    tokens = _split(code)
    tokens = _erase_white_spaces(tokens)
    tokens = _combine_long_symbols(tokens)

    return tokens


# code -> tokens
def _split(code):

    tokens = deque()

    ii = 0

    for i, t in enumerate(code):

        if t in symbols:
            tokens.append(code[ii:i])
            tokens.append(t)
            ii = i + 1

    tokens.append(code[ii:])

    return list(tokens)


# tokens -> tokens
def _erase_white_spaces(tokens):

    for i, t in enumerate(tokens):

        while len(t) > 0 and t[0] in white_spaces:
            t = t[1:]
            tokens[i] = t

        while len(t) > 0 and t[-1] in white_spaces:
            t = t[:-1]
            tokens[i] = t

    erase_white_spaces = deque()

    for t in tokens:

        if len(t) > 0:
            erase_white_spaces.append(t)

    return list(erase_white_spaces)


# tokens -> tokens
def _combine_long_symbols(tokens):

    combine_long_symbols = deque()

    skip_next = False

    for i, t in enumerate(tokens):

        if skip_next:
            skip_next = False
            continue

        if i + 1 < len(tokens) and t + tokens[i + 1] in long_symbols:
            combine_long_symbols.append(t + tokens[i + 1])
            skip_next = True

        else:
            combine_long_symbols.append(t)

    return list(combine_long_symbols)