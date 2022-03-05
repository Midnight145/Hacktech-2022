import platform
import WindowsNotifier
import MacNotifier


def notify():
    global response
    if platform.system() == 'Windows':
        response = WindowsNotifier.run()
    else:
        response = MacNotifier.run()


if __name__ == "__main__":
    notify()
    print(f'{response}')