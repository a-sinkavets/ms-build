#!/usr/bin/env python3
"""Generates random exit codes for testing error handling."""
import os
import sys
import time
import random


def get_int_env(var_name, default, min_val=None, max_val=None):
    """Get integer from environment variable with validation."""
    value_str = os.getenv(var_name, str(default))
    try:
        value = int(value_str)
        if min_val is not None and value < min_val:
            print(
                f"Error: {var_name}={value} is below minimum "
                f"{min_val}. Using default: {default}",
                file=sys.stderr
            )
            return default
        if max_val is not None and value > max_val:
            print(
                f"Error: {var_name}={value} exceeds maximum "
                f"{max_val}. Using default: {default}",
                file=sys.stderr
            )
            return default
        return value
    except ValueError:
        print(
            f"Error: {var_name}='{value_str}' is not a valid integer. "
            f"Using default: {default}",
            file=sys.stderr
        )
        return default


def get_float_env(var_name, default, min_val=None, max_val=None):
    """Get float from environment variable with validation."""
    value_str = os.getenv(var_name, str(default))
    try:
        value = float(value_str)
        if min_val is not None and value < min_val:
            print(
                f"Error: {var_name}={value} is below minimum "
                f"{min_val}. Using default: {default}",
                file=sys.stderr
            )
            return default
        if max_val is not None and value > max_val:
            print(
                f"Error: {var_name}={value} exceeds maximum "
                f"{max_val}. Using default: {default}",
                file=sys.stderr
            )
            return default
        return value
    except ValueError:
        print(
            f"Error: {var_name}='{value_str}' is not a valid number. "
            f"Using default: {default}",
            file=sys.stderr
        )
        return default


def get_bool_env(var_name, default):
    """Get boolean from environment variable."""
    value_str = os.getenv(var_name, str(default)).lower()
    return value_str in ('true', '1', 'yes', 'on')


def main():
    """Main execution function."""
    # Get configuration from environment variables with validation
    min_code = get_int_env('MIN_EXIT_CODE', 10, min_val=1, max_val=999)
    max_code = get_int_env('MAX_EXIT_CODE', 199, min_val=1, max_val=999)
    interval = get_int_env('INTERVAL_SECONDS', 5, min_val=1)
    special_code = get_int_env(
        'SPECIAL_EXIT_CODE', 200, min_val=1, max_val=999
    )
    special_code_chance = get_float_env(
        'SPECIAL_CODE_CHANCE', 0.3, min_val=0.0, max_val=1.0
    )
    dry_run = get_bool_env('DRY_RUN', False)

    # Validate range logic
    if min_code > max_code:
        print(
            f"Error: MIN_EXIT_CODE ({min_code}) is greater than "
            f"MAX_EXIT_CODE ({max_code}). Swapping values.",
            file=sys.stderr
        )
        min_code, max_code = max_code, min_code

    print(
        f"Configuration: min_code={min_code}, max_code={max_code}, "
        f"interval={interval}s, special_code={special_code} "
        f"({special_code_chance*100}% chance), dry_run={dry_run}"
    )

    while True:
        if random.random() < special_code_chance:
            exit_code = special_code
        else:
            exit_code = random.randint(min_code, max_code)

        print(f"Exiting with code: {exit_code}")
        sys.stdout.flush()
        time.sleep(interval)
        if not dry_run:
            sys.exit(exit_code)


if __name__ == "__main__":
    main()
