import functools
import time
import inspect

def debug_trace(func):
    """
    Decorator to log function execution details (Inputs, Outputs, Execution Time).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get function name and docstring (first line)
        func_name = func.__name__
        doc = inspect.getdoc(func)
        summary = doc.split('\n')[0] if doc else "No description"
        
        print(f"\n[DEBUG] ➤ Executing '{func_name}'")
        print(f"        ℹ️  Description: {summary}")
        
        # Log Inputs (safely)
        try:
            # Avoid printing self or massive objects if possible, but for now simple repr
            # We filter out 'self' from args if it's a method, but tricky to know context easily without inspection
            # Just printing args is usually fine for simple types
            arg_str = str(args)
            if len(arg_str) > 500: arg_str = arg_str[:500] + "..."
            
            kwarg_str = str(kwargs)
            if len(kwarg_str) > 500: kwarg_str = kwarg_str[:500] + "..."
            
            print(f"        📥 Inputs: Args={arg_str}, Kwargs={kwarg_str}")
        except Exception:
            print("        📥 Inputs: (Error displaying inputs)")

        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            
            # Log Output
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            
            res_str = str(result)
            if len(res_str) > 500: res_str = res_str[:500] + "..."
            
            print(f"        out Output: {res_str}")
            print(f"        ⏱️  Time: {duration:.2f}ms")
            print(f"[DEBUG] ✓ Finished '{func_name}'\n")
            return result
            
        except Exception as e:
            print(f"        ❌ Error: {e}")
            print(f"[DEBUG] ⚠ Failed '{func_name}'\n")
            raise e

    return wrapper
