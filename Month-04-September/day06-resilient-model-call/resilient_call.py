import time
import uuid
import os
import random

from openai import (
    OpenAI,
    APITimeoutError,
    RateLimitError,
    AuthenticationError,
    PermissionDeniedError,
    BadRequestError,
    APIConnectionError,
    APIStatusError,
)


client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    max_retries=0,
    timeout=20.0,
)

def get_retry_delay(attempt: int) -> float:
    base_delay = 1.0
    backoff = base_delay * (2 ** (attempt - 1))
    jitter = random.uniform(0, 0.5)

    return backoff + jitter

def call_model(prompt: str, max_attempts: int = 3) -> str | None:
    operation_id = str(uuid.uuid4())

    print(f"Operation ID: {operation_id}")

    for attempt in range(1, max_attempts + 1):
        print(f"\nAttempt: {attempt}")

        start = time.perf_counter()

        try:
            response = client.responses.create(
                model="gpt-5-mini",
                input=prompt,
            )

            latency = time.perf_counter() - start

            print("Outcome: success")
            print(f"Latency: {latency:.2f} seconds")

            return response.output_text

        except RateLimitError as error:
            latency = time.perf_counter() - start

            print("Outcome: rate_limited")
            print(f"Latency: {latency:.2f} seconds")

            if attempt == max_attempts:
                print("Maximum attempts reached.")
                return None

            retry_after = None

            if error.response is not None:
                retry_after_ms = error.response.headers.get("retry-after-ms")
                retry_after_seconds = error.response.headers.get("retry-after")

                if retry_after_ms:
                    retry_after = float(retry_after_ms) / 1000

                elif retry_after_seconds:
                    retry_after = float(retry_after_seconds)

            if retry_after is None:
                retry_after = get_retry_delay(attempt)

            print(f"Retrying in {retry_after:.2f} seconds...")
            time.sleep(retry_after)
        
        except APITimeoutError:
            latency = time.perf_counter() - start

            print("Outcome: timeout")
            print(f"Latency: {latency:.2f} seconds")

            if attempt == max_attempts:
                print("Maximum attempts reached.")
                return None

            delay = get_retry_delay(attempt)

            print(f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)

        except APIConnectionError:
            latency = time.perf_counter() - start

            print("Outcome: connection_error")
            print(f"Latency: {latency:.2f} seconds")

            if attempt == max_attempts:
                print("Maximum attempts reached.")
                return None

            delay = get_retry_delay(attempt)

            print(f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)

        except AuthenticationError:
            print("Outcome: authentication_failed")
            print("Action: fail immediately")
            return None

        except PermissionDeniedError:
            print("Outcome: permission_denied")
            print("Action: fail immediately")
            return None

        except BadRequestError:
            print("Outcome: bad_request")
            print("Action: fail immediately")
            return None

        except APIStatusError as error:
            latency = time.perf_counter() - start

            print(f"Outcome: API error {error.status_code}")
            print(f"Latency: {latency:.2f} seconds")

            if 500 <= error.status_code < 600:
                if attempt == max_attempts:
                    print("Maximum attempts reached.")
                    return None

                delay = get_retry_delay(attempt)

                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)

            else:
                print("Action: fail immediately")
                return None

    return None

response = call_model(
    "Explain the principle of least privilege in two sentences."
)

print("\nModel response:")
print(response)