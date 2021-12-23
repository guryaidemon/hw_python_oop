from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Получить информационное сообщение о тренировке."""

        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:

        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError('To be implemented '
                                  f'{type(self).__name__}.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    MULTIPLIER_RUN_CALLORIE_COEFF: float = 18
    SUBSTRACING_RUN_CALLORIE_COEFF: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.MULTIPLIER_RUN_CALLORIE_COEFF * self.get_mean_speed()
                - self.SUBSTRACING_RUN_CALLORIE_COEFF)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:

        super().__init__(action, duration, weight)
        self.height: float = height

    SPEED_WLK_COEFF_CALLORIE: float = 0.035
    WEIGHT_WLK_COEFF_CALLORIE: float = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.SPEED_WLK_COEFF_CALLORIE * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * self.WEIGHT_WLK_COEFF_CALLORIE * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SUMMAND_SWM_COEFF_CALLORIE: float = 1.1
    MULTIPLIER_SWM_COEFF_CALLORIE: float = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.SUMMAND_SWM_COEFF_CALLORIE)
                * self.MULTIPLIER_SWM_COEFF_CALLORIE * self.weight)


def read_package(work_type: str, data_work: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    try:
        return training_dict[work_type](*data_work)
    except KeyError as key_error:
        raise ValueError('Что-то пошло не так') from key_error


def main(exercise: Training) -> None:
    """Главная функция."""

    info: InfoMessage = exercise.show_training_info()
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
