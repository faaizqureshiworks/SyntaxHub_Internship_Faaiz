def perform_calculation():
    # Simple interactive script to demonstrate basic Python operations
    print("--- SyntaxHub Project 1: Basic Operations ---")
    
    try:
        val1 = float(input("Enter first number: "))
        val2 = float(input("Enter second number: "))
        
        # Calculate results
        addition = val1 + val2
        product = val1 * val2
        
        print(f"\nResults:")
        print(f"Addition: {addition}")
        print(f"Multiplication: {product}")
        
    except ValueError:
        print("Error: Please enter valid numerical values.")

if __name__ == "__main__":
    perform_calculation()