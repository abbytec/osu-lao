def apply_modifiers(ar, cs, mod):
    if mod == 'HR':
        ar = min(10, ar * 1.4)
        cs = min(10, cs * 1.4)
    elif mod == 'DT':
        if ar < 5:
            ar = min(10, ar * 1.5)
        else:
            ar = min(10, 5 + (ar - 5) * 1.5)
    return ar, cs
