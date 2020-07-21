from subprocess import Popen, CREATE_NEW_CONSOLE

process = []
while True:
    choice = input('Выберите действие: q - выход, s - запустить сервер и клиенты, x - закрыть все окна\n')
    if choice == 'q':
        break
    elif choice == 's':
        number = int(input('Сколько запустить клиентов?\n'))
        process.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
        for i in range(1, number + 1):
            process.append(Popen(f'python client.py -n test{i}', creationflags=CREATE_NEW_CONSOLE))
    elif choice == 'x':
        while process:
            el = process.pop()
            el.kill()


