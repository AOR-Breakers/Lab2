class KnapsackDP:
    def __init__(self):
        self.comparisons = 0
        self.common_weight = 0

    # Метод ДП на весах
    def solve(self, capacity: int, weights: list[int], values: list[int], n: int) -> tuple[int, list[int]]:
        table = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

        for i in range(n + 1):
            for w in range(capacity + 1):
                self.comparisons += 1
                if i == 0 or w == 0:
                    table[i][w] = 0
                elif weights[i - 1] <= w:
                    self.comparisons += 1
                    table[i][w] = max(values[i - 1] + table[i - 1][w - weights[i - 1]], table[i - 1][w])
                else:
                    table[i][w] = table[i - 1][w]

        return table[n][capacity], self.get_selected_items(table, values, weights, capacity, n)

    def get_selected_items(self, table: list[list[int]], values: list[int], weights: list[int], capacity: int,
                           n: int) -> list[int]:
        cost = table[n][capacity]
        temp_capacity = capacity
        items_list = [0 for _ in range(n)]

        for i in range(n, 0, -1):
            self.comparisons += 1
            if cost <= 0:
                break
            if cost == table[i - 1][temp_capacity]:
                continue
            else:
                items_list[i - 1] = 1
                cost -= values[i - 1]
                temp_capacity -= weights[i - 1]
                self.common_weight += weights[i - 1]

        return items_list

    def get_comparisons_count(self) -> int:
        return self.comparisons

    def get_common_weight(self) -> int:
        return self.common_weight


if __name__ == "__main__":
    knapsack = KnapsackDP()
    profit, items = knapsack.solve(165, [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
                                   [92, 57, 49, 68, 60, 43, 67, 84, 87, 72], 10)

    print(f"items: {items}, resulted weight: {knapsack.get_common_weight()}, resulted profit: {profit}")
    print(f"Comparisons count: {knapsack.get_comparisons_count()}")
