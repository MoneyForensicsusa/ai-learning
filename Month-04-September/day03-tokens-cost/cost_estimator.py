def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    input_rate_per_million: float,
    output_rate_per_million: float,
) -> dict:
    input_cost = (input_tokens / 1_000_000) * input_rate_per_million
    output_cost = (output_tokens / 1_000_000) * output_rate_per_million
    total_cost = input_cost + output_cost

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }

input_rate = float(input("Input price per 1M tokens: $"))
output_rate = float(input("Output price per 1M tokens: $"))

result = estimate_cost(
    input_tokens=99,
    output_tokens=343,
    input_rate_per_million=input_rate,
    output_rate_per_million=output_rate,
)

print(f"\nInput cost:  ${result['input_cost']:.8f}")
print(f"Output cost: ${result['output_cost']:.8f}")
print(f"Total cost:  ${result['total_cost']:.8f}")