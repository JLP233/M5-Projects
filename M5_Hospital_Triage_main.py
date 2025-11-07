from __future__ import annotations
import heapq
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass(order=True)
class _PriorityItem:
    # Invert severity (max-heap behavior via min-heap): higher severity -> smaller key
    key: Tuple[int,int]
    name: str
    severity: int

class TriageSystem:
    "Priority queue places higher severity conditions first and ties use FIFO arrival order."
    _arrival_counter = 0  # class-level

    def __init__(self) -> None:
        self._pq = []  # private heap

    @classmethod
    def _next_arrival(cls) -> int:
        v = cls._arrival_counter
        cls._arrival_counter += 1
        return v

    def AddPatient(self, name: str, severity: int) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Name Must be a Non-Empty String")
        if not isinstance(severity, int) or not (1 <= severity <= 5):
            raise ValueError("Severity Must be an Int from 1 to 5")
        arrival = self._next_arrival()
        # priority: (-severity, arrival) -> larger severity sorts first; earlier arrival sorts first among ties
        item = _PriorityItem(key=(-severity, arrival), name=name, severity=severity)
        heapq.heappush(self._pq, item)

    def ProcessNext(self) -> Optional[Tuple[str,int]]:
        if not self._pq:
            return None
        item = heapq.heappop(self._pq)
        return (item.name, item.severity)

    def PeekNext(self) -> Optional[Tuple[str,int]]:
        if not self._pq:
            return None
        item = self._pq[0]
        return (item.name, item.severity)

    def IsEmpty(self) -> bool:
        return not self._pq

    def Size(self) -> int:
        return len(self._pq)

    def Clear(self) -> None:
        self._pq.clear()
        
def run_demo():
    data = [
        ("Sofia", 5),
        ("Bob", 2),
        ("Charlie", 4),
        ("Diana", 3),
        ("Eli", 1),
        ("Tom", 4),
        ("Alice", 5),
        ("Rachel", 4),
    ]
    T = TriageSystem()
    for name, sev in data:
        T.AddPatient(name, sev)

    print("Processing Patients:\n")
    while not T.IsEmpty():
        name, sev = T.ProcessNext()
        print(f"Now Treating: {name} (Severity {sev})")

if __name__ == "__main__":
    run_demo()
