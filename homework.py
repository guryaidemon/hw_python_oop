from dataclasses import dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить информационное сообщение о тренировке."""

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
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError("To be implemented")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__, self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    RUN_COEF_CAL_EIGHTEEN: float = 18
    RUN_COEF_CAL_TWENTY: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.RUN_COEF_CAL_EIGHTEEN * self.get_mean_speed()
                - self.RUN_COEF_CAL_TWENTY) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    SWT_COEF_CAL_F: float = 0.035
    SWT_COEF_CAL_S: float = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.SWT_COEF_CAL_F * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * self.SWT_COEF_CAL_S * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    LEN_STEP: float = 1.38
    SWM_COEF_CAL_ONE: float = 1.1
    SWM_COEF_CAL_TWO: float = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.SWM_COEF_CAL_ONE)
                * self.SWM_COEF_CAL_TWO * self.weight)


def read_package(work_type: str, data_work: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_dict: Dict[str] = {'SWM': Swimming,
                                'RUN': Running,
                                'WLK': SportsWalking,
                                }

    return training_dict[work_type](*data_work)


def main(var_training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = var_training.show_training_info()
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
