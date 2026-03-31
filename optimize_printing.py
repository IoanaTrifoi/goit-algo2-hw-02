from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimises the 3D printing queue according to priorities and printer constraints
    """
    printer = PrinterConstraints(**constraints)
    
    jobs = [PrintJob(**job) for job in print_jobs]
    jobs.sort(key=lambda x: x.priority)

    print_order = []
    total_time = 0
    current_batch = []
    current_batch_volume = 0

    for job in jobs:
        if (len(current_batch) < printer.max_items and 
            current_batch_volume + job.volume <= printer.max_volume):
            current_batch.append(job)
            current_batch_volume += job.volume
        else:
            if current_batch:
                total_time += max(j.print_time for j in current_batch)
                print_order.extend(j.id for j in current_batch)
            
            # Start a new batch with the current job
            current_batch = [job]
            current_batch_volume = job.volume

    if current_batch:
        total_time += max(j.print_time for j in current_batch)
        print_order.extend(j.id for j in current_batch)

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Testing
def test_printing_optimization():
    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    # Test 1: Models with the same priority
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Test 2: Models with different priorities
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # lab work
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # thesis
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # personal project
    ]

    # Test 3: Exceeding volume constraints
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    print("Test 1 (same priority):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} minutes")

    print("\nTest 2 (different priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} minutes")

    print("\nTest 3 (exceeding constraints):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} minutes")

if __name__ == "__main__":
    test_printing_optimization()