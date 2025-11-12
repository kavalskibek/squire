import time


class Waiter:
    def __init__(self, timeout=10, interval=0.5):
        """
        :param timeout: Максимальное время ожидания (в секундах)
        :param interval: Интервал между проверками
        """
        self.timeout = timeout
        self.interval = interval

    def until(self, condition, message="Condition not met in time"):
        """
        Ждёт, пока функция condition() не вернёт True.
        Если время истекло — бросает TimeoutError.
        """
        start = time.time()

        while True:
            try:
                result = condition()
                if result:
                    return result
            except Exception:
                pass  # игнорируем временные ошибки

            if time.time() - start >= self.timeout:
                raise TimeoutError(message)

            time.sleep(self.interval)

    def until_not(self, condition, message="Condition still true after timeout"):
        """
        Ждёт, пока функция condition() не вернёт False.
        """
        start = time.time()

        while True:
            try:
                result = condition()
                if not result:
                    return True
            except Exception:
                return True  # если condition выбросил ошибку — считаем, что False

            if time.time() - start >= self.timeout:
                raise TimeoutError(message)

            time.sleep(self.interval)


# ✅ Функция должна быть вне класса
def wait_for(condition, timeout=10, interval=0.5, message="Condition not met in time"):
    waiter = Waiter(timeout=timeout, interval=interval)
    return waiter.until(condition, message)
