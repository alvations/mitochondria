

def magic_square_params(diagonal_size):
    numbers = list(range(1, diagonal_size**2+1))
    optimal_fitness = 2 + 2 * diagonal_size
    expected_sum = diagonal_size * (diagonal_size**2 + 1) / 2
    return numbers, optimal_fitness, expected_sum
