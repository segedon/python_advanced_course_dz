from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Journal:
    student_name: str
    grade: int
    lesson: str


class JournalRepository(ABC):
    def add(self, item: Journal) -> None: ...
    def get_all(self) -> list[Journal]: ...


class Statistic(ABC):
    def __init__(self, journal_repository: JournalRepository) -> None:
        self.journal_repository = journal_repository

    @abstractmethod
    def calculate(self) -> float: ...


class Notifier(ABC):
    @abstractmethod
    def notify(self, message) -> None: ...


class Trigger(ABC):
    @abstractmethod
    def is_triggered(self, value: float) -> bool: ...


class InMemoryJournalRepository(JournalRepository):
    def __init__(self, items: list[Journal] | None = None):
        self.items = [] if items is None else items

    def add(self, item: Journal):
        self.items.append(item)

    def get_all(self):
        return self.items


class AverageGradeStatistic(Statistic):
    def calculate(self) -> float:
        journal_items = self.journal_repository.get_all()
        return sum(item.grade for item in journal_items) / len(journal_items)


class ConsolerNotifier(Notifier):
    def notify(self, message):
        print(message)


class LessThenValueTrigger(Trigger):
    def __init__(self, value: float):
        super().__init__()
        self.__value = value

    def is_triggered(self, value):
        return value < self.__value


class Monitor:
    def __init__(self, statistic: Statistic, trigger: Trigger, notifier: Notifier):
        self.statistic = statistic
        self.trigger = trigger
        self.notifier = notifier

    def monitor(self) -> None:
        statistic_value = self.statistic.calculate()
        if self.trigger.is_triggered(statistic_value):
            self.notifier.notify("Сработал триггер!")
        else:
            self.notifier.notify("Треггер не сработал")


if __name__ == "__main__":
    journal_repository = InMemoryJournalRepository()
    statistic = AverageGradeStatistic(journal_repository=journal_repository)
    notifier = ConsolerNotifier()
    trigger = LessThenValueTrigger(value=3.5)
    monitor = Monitor(statistic, trigger, notifier)

    journal_repository.add(Journal("Petr", 5, "math"))
    # триггер не сработает
    monitor.monitor()

    journal_repository.add(Journal("Alexandr", 1, "math"))
    monitor.monitor()
