from scipy.optimize import linprog


class BranchAndBound:
    def __init__(self, weights, values, capacity):
        self.costs = [-cost for cost in values]
        self.weights = weights
        self.capacity = capacity

        self.optimum = -1
        self.best_items = []

        self.total_profit = 0
        self.total_weight = 0
        self.counter = 0

    def find_optimum(self, A_eq: list[any], b_eq: list[any]) -> None:
        result = linprog(c=self.costs, A_ub=[self.weights], b_ub=[self.capacity],
                         A_eq=A_eq, b_eq=b_eq, bounds=(0, 1), method='simplex')

        optimum = -result.fun
        backpack = [round(i, 2) for i in result.x]

        self.counter += 1
        if optimum < self.optimum:
            return

        for i in range(len(backpack)):
            self.counter += 1
            if not round(backpack[i], 2).is_integer():
                temp_A_eq = A_eq.copy()
                temp_b_eq = b_eq.copy()

                temp_A_eq.append([0 for _ in range(len(backpack))])
                temp_A_eq[-1][i] = 1

                temp_b_eq += [1]
                self.find_optimum(temp_A_eq, temp_b_eq)

                temp_b_eq[-1] = 0
                self.find_optimum(temp_A_eq, temp_b_eq)

                return

        self.counter += 1
        if optimum > self.optimum:
            total_weight = 0
            total_profit = 0
            items_idx = []
            for ind in range(len(backpack)):
                self.counter += 1
                if backpack[ind] == 1:
                    total_weight += self.weights[ind]
                    total_profit -= self.costs[ind]
                    items_idx.append(ind)

            self.counter += 1
            if total_weight <= self.capacity:
                self.total_weight = total_weight
                self.total_profit = total_profit
                self.optimum = optimum
                self.best_items = items_idx

        return

    def solver(self) -> [int, int, list[int], int]:
        A_eq = [[0 for _ in range(len(self.costs))]]
        b_eq = [0]

        self.find_optimum(A_eq, b_eq)

        return self.total_weight, self.total_profit, self.best_items, self.counter


if __name__ == "__main__":
    knapsack = BranchAndBound([23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
                              [92, 57, 49, 68, 60, 43, 67, 84, 87, 72],
                              165)
    weight, profit, items, comparison = knapsack.solver()

    print(f"Items index: {items}, final backpack weight: {weight}, total cost of backpack: {profit}")
    print(f"Comparisons count: {comparison}")