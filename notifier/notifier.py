import platform


def notify():
    global response
    if platform.system() == 'Windows':

        from . import WindowsNotifier
        response = WindowsNotifier.run()
    else:
        import MacNotifier
        response = MacNotifier.run()


if __name__ == "__main__":
    notify()
    print(f'{response}')