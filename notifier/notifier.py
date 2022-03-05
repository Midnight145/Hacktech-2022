import platform
import WindowsNotifier


def notify():
    global response
    if platform.system() == 'Windows':
        response = WindowsNotifier.run()


if __name__ == "__main__":
    notify()
    print(f'{response}')