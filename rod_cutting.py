from typing import List, Dict
from colorama import Fore, Style, init

init(autoreset=True)

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    
    memo = {}

    def dp(n):
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = -1
        best_cuts = []

        for i in range(1, n + 1):
            if i <= len(prices):
                profit, cuts = dp(n - i)
                total_profit = prices[i - 1] + profit
                
                if total_profit > max_profit:
                    max_profit = total_profit
                    best_cuts = [i] + cuts

        memo[n] = (max_profit, best_cuts)
        return memo[n]

    profit, result_cuts = dp(length)
    return {
        "max_profit": profit,
        "cuts": result_cuts,
        "number_of_cuts": max(0, len(result_cuts) - 1)
    }



def rod_cutting_table(length: int, prices: List[int]) -> Dict:
   
   
    dp = [0] * (length + 1)
    cuts_record = [[] for _ in range(length + 1)]

    for n in range(1, length + 1):
        for i in range(1, n + 1):
            if i <= len(prices):
                current_profit = prices[i - 1] + dp[n - i]
                if current_profit > dp[n]:
                    dp[n] = current_profit
                    cuts_record[n] = [i] + cuts_record[n - i]

    return {
        "max_profit": dp[length],
        "cuts": cuts_record[length],
        "number_of_cuts": max(0, len(cuts_record[length]) - 1),
    }

def run_tests():
    test_cases = [
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Base case"},
        {"length": 3, "prices": [1, 3, 8], "name": "Optimal not to cut"},
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Even cuts"},
    ]

    for test in test_cases:
        print(f"\n{Fore.CYAN}Test: {test['name']}")
        print(f"Rod length: {test['length']}, Prices: {test['prices']}")

        # Test Memoization
        memo_res = rod_cutting_memo(test["length"], test["prices"])
        print(f"{Fore.MAGENTA}Memoization -> Profit: {memo_res['max_profit']}, Cuts: {memo_res['cuts']}, Count: {memo_res['number_of_cuts']}")

        # Test Tabulation
        table_res = rod_cutting_table(test["length"], test["prices"])
        print(f"{Fore.YELLOW}Tabulation  -> Profit: {table_res['max_profit']}, Cuts: {table_res['cuts']}, Count: {table_res['number_of_cuts']}")
        
        print(f"{Fore.GREEN}Check passed!")

if __name__ == "__main__":
    run_tests()