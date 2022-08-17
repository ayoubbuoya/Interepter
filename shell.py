import lang

while True:
    cmd = input("lang > ")
    if cmd == "q":
        break
    # toks, error = lang.run(cmd)
    # if error:
    #     print(error)
    # else:
    #     print(toks)
    result, error = lang.run(cmd)

    if error:
        print(error)
    else:
        print(result)
