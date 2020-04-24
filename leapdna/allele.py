def repeat_to_seq(bracketed):
    seq = ''
    in_braket = False
    in_nrepeat = False
    repeat = ''
    nrepeat = 0
    for char in bracketed:
        if char.isspace(): continue
        
        if in_nrepeat:
            if char.isdigit():
                nrepeat = 10 * nrepeat + int(char)
            else:
                seq += repeat * nrepeat
                in_nrepeat = False
                repeat = ''
    
        if char in ('[', '('):
            in_braket = True
            repeat = ''
            continue
        elif char in (']', ')'):
            in_braket = False
            in_nrepeat = True
            nrepeat = 0
            continue

        if in_braket:
            repeat += char
        elif not in_nrepeat:
            seq += char

    # return accumulated sequence plus a possible last repeat
    return seq + repeat * nrepeat
            