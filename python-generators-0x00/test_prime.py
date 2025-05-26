from prime_generator import prime_generator

gen = prime_generator()

# Print the first 10 prime numbers
for _ in range(10):
    print(next(gen))

