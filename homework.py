class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_CALORIE_1 * self.get_mean_speed() - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * (self.duration * 60))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    COEFF_CALORIE_3: float = 0.035
    COEFF_CALORIE_4: float = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_CALORIE_3 * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * self.COEFF_CALORIE_4 * self.weight) * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    LEN_STEP: float = 1.38
    COEFF_CALORIE_5: float = 1.1
    COEFF_CALORIE_6: int = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return (self.get_mean_speed() + self.COEFF_CALORIE_5) * self.COEFF_CALORIE_6 * self.weight


def read_package(work_type: str, data_work: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dict_train = {'SWM': Swimming,
                  'RUN': Running,
                  'WLK': SportsWalking
                  }
    train = dict_train[work_type]

    return train(*data_work)


def main(train: Training) -> None:
    """Главная функция."""
    info: InfoMessage = train.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
