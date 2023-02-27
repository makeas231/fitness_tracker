class InfoMessage:
    """Выводит на экран состояние тренеровки"""
    def __init__(self,
                 trainig_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ):
        """
        Инициализация атрибутов для класса.
        
        Атрибуты класса:
         trainig_type (str) - тип тренировки
         duration (int или float) - длительность
         distance (float) - пройденная дистанция(в км)
         speed (int или float) - средняя скорость
         calories (int или float) - израсходованое количество калорий
        """
        self.trainig_type = trainig_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    def get_message(self) -> str:
        """Выводит на экран состояние тренировки"""
        print(
              f'Тип данной тренировки: {self.trainig_type},',
              f'Длительность: {self.duration} час или {self.duration * 60} Минут,',
              f'Вы преодолели дистанцию в {self.distance} км',
              f'\nВаша средняя скорость: {self.speed} км/час,',
              f'и Вы сожгли {self.calories} килокалорий \n'
             )


class Training:   # Родительский класс
    """Описывает тренеровку"""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        """
        Инициализирует атрибуты класса
        
        Атрибуты класса:
         action (тип int) - количество совершенных действий
         duration (тип int или float) - продолжительность тренеровки(в часах)
         weight (тип int или float) - вес спортсмена (в кг)
        """
        self.action = action
        self.duration = duration
        self.weight = weight
        
    def get_distance(self) -> float:
        """Расчитывает дистанцию в километрах"""
        M_IN_KM = 1000
        return self.action * self.LEN_STEP / M_IN_KM
        
    def get_mean_speed(self) -> float:
        """Возвращает среднее значение скорости"""
        return self.get_distance() / self.duration
         
    def get_spent_calories(self) -> float:
        """
        Возвращает израсходованное количество килокалорий,
        потраченных за тренировку
        """
        pass
        
    def show_trainig_info(self) -> str:
        """Возвращает информационое сообщение о тренировке"""
        trainig_type = self.__class__.__name__
        message = InfoMessage(trainig_type=trainig_type,
                              duration=self.duration,
                              distance=self.get_distance(),
                              speed=self.get_mean_speed(),
                              calories=self.get_spent_calories()
                             )
        return message


class Running(Training):
    """Класс описывет бег"""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        """
        Инициализируем атрибутов родительского класса.
        Данный класс не имеет собственных атрибутов.
        """
        super().__init__(action, duration, weight)
        self.LEN_STEP = 0.65
        self.M_IN_KM = 1000
        self.CALORIES_MEAN_SPEED_MULTIPLIER = 18
        self.CALORIES_MEAN_SPEED_SHIFT = 1.79
        
    def get_spent_calories(self) -> float:
        """
        Возвращает израсходованное количество килокалорий,
        потраченных за тренирвоку c учетом класса Running
        """
        act1 = self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
        act2 = self.CALORIES_MEAN_SPEED_SHIFT
        act3 = self.weight / self.M_IN_KM * self.duration * 60
        result_run = ((act1 + act2) * act3)
        return round(result_run, 3)


class SportsWalking(Training):
    """Класс описывает спортивную ходьбу"""
    def __init__(self, 
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ):
        """
        Инициализация атрибутов класса и атрубутов класса родителя
        Собственные атрибуты класса(без учета родительского класса):
         height (int) - рост спортсмена
        """
        super().__init__(action, duration, weight)   
        self.height = height
        self.LEN_STEP = 0.65
    
    def get_spent_calories(self) -> float:
        """
        Возвращает израсходованное количество килокалорий,
        потраченных за тренирвку, с учетом класса SportsWalking
        """
        act1 = 0.035 * self.weight + (self.get_mean_speed() / 3.6)**2
        act2 = self.height / 100  # Перевод из см в метры
        act3 = 0.029 * self.weight *  self.duration * 60
        result_wlk = (act1 / act2) * act3
        return round(result_wlk, 3)


class Swimming(Training):
    """Класс описывет Плаванье"""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: int,
                 count_pool: int
                 ):
        """
        Инициализация атрибутов класса и атрубутов класса родителя
        
        Собственные атрибуты класса:
         lenght_pool (int) - длина бассейна
         count_pool (int или float) - сколько раз спортсмен переплыл бассейн
        """
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool
        self.M_IN_KM = 1000
        self.LEN_STEP = 0.75
        
    def get_mean_speed(self) -> float:
        """Расчитывает среднюю скорость при ПЛАВАНЬЕ"""
        return self.lenght_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """
        Возвращает израсходованное количество килокалорий,
        потраченных за тренировку, с учетом класса Swimming
        """
        act1 = (self.get_mean_speed() + 1.1) * 2 * self.weight
        act2 = self.duration
        result_swm = act1 * act2
        return round(result_swm, 3)

def read_package(workout_type: str, data: list[float]) -> Training:
    """
    Определяет тип тренировки и создает обьект соответствующего класса

    Аргументы метода: 
     workout_type (str) - тип тренировки
     data (list[float]) - присущные для типа тренировки значения(атрибуты)
    """
    try:
        if workout_type == "WLK":
            obj = SportsWalking(action=data[0], duration=data[1],
                                weight=data[2], height=data[3])
        if workout_type == "RUN":
            obj = Running(action=data[0], duration=data[1],
                          weight=data[2])
        if workout_type == "SWM":
            obj = Swimming(action=data[0], duration=data[1],
                           weight=data[2], lenght_pool=data[3],
                           count_pool=data[4])
            
        return obj
    
    except IndexError:
        print(
             'ВЫ ВВЕЛИ НЕСУЩЕСТВУЮЩИЙ ИНДЕКС ДЛЯ DATA,',
             'ВВЕДИТЕ ПРАВИЛЬНОЕ КОЛИЧЕСТВО ЗНАЧЕНИЙ ДЛЯ СПИСКА DATA'
             )

def main(training: Training) -> str:
    """
    Главная функция
    
    Аргументы метода:
     trainiтg(object) - содержит в себе обьект Training
    """
    info = training.show_trainig_info()
    info.get_message()

if __name__ == '__main__': # Делаем проверку,
    package = [            # Запускатеся ли программа как основная
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180])
    ]
    for workout_type, data in package:
        trainig = read_package(workout_type, data)
        main(trainig)


 

        
    
 
    