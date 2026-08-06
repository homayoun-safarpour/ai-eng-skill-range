def remap(exit_code):
    if exit_code == 0 or exit_code == 3:
        return 0
    if exit_code == 2:
        return 2
    return 1
