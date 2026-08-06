def pass_fail(answer, must_include):
    text = answer.casefold()
    return "pass" if all(m.casefold() in text for m in must_include) else "fail"
