from Interepter.interepter import run


while True:
    cmd = input("lang >> ")
    if cmd == "q":
        break
    result, error = run(cmd)
    if error:
        print(error)
    elif result:
        print(result)
