# Define the available memory blocks (sizes in KB)
memory_blocks = [100, 500, 200, 300, 600]

# Define the list of processes as (Process Name, Size in KB)
processes = [("P1", 212), ("P2", 417), ("P3", 112), ("P4", 426)]

# First Fit Algorithm 
# Iterate through each process and find the first available memory block that can accommodate it.
# Allocate the process to the selected memory block.
# If no suitable memory block is found, mark the process as unallocated. 
# Repeat the process for each process in the list.
def first_fit(memory_blocks, processes):
    print("\n--- First Fit ---")
    
    # Create a copy of memory blocks to simulate allocation without affecting original
    mem = memory_blocks.copy()
    
    # Loop through each process
    for name, size in processes:
        allocated = False  # Flag to check if process is allocated

        # Loop through each memory block
        for j in range(len(mem)):
            if mem[j] >= size:  # If block size is enough for the process
                print(f"{name} ({size}KB) → Block {j+1} ({mem[j]}KB)")
                mem[j] -= size  # Allocate memory: reduce block size
                allocated = True
                break  # Stop after allocating to the first suitable block

        # If no suitable block was found
        if not allocated:
            print(f"{name} ({size}KB) → Not Allocated")

# Best Fit Algorithm 
# Iterate through each process and find the smallest available memory block that can accommodate it.
# Allocate the process to the selected memory block.
# If no suitable memory block is found, mark the process as unallocated. 
# Repeat the process for each process in the list.
def best_fit(memory_blocks, processes):
    print("\n--- Best Fit ---")
    
    # Copy memory blocks
    mem = memory_blocks.copy()
    
    # Loop through each process
    for name, size in processes:
        best_index = -1  # Store the index of the best-fit block

        # Loop through memory blocks
        for j in range(len(mem)):
            if mem[j] >= size:
                # Check if it's the smallest suitable block so far
                if best_index == -1 or mem[j] < mem[best_index]:
                    best_index = j

        # Allocate the process to best-fit block
        if best_index != -1:
            print(f"{name} ({size}KB) → Block {best_index+1} ({mem[best_index]}KB)")
            mem[best_index] -= size
        else:
            print(f"{name} ({size}KB) → Not Allocated")


# Worst Fit Algorithm   
# Iterate through each process and find the largest available memory block that can accommodate it.
# Allocate the process to the selected memory block.
# If no suitable memory block is found, mark the process as unallocated. 
# Repeat the process for each process in the list.   
def worst_fit(memory_blocks, processes):
    print("\n--- Worst Fit ---")
    
    # Copy memory blocks
    mem = memory_blocks.copy()
    
    # Loop through each process
    for name, size in processes:
        worst_index = -1  # Store the index of the worst-fit block

        # Loop through memory blocks
        for j in range(len(mem)):
            if mem[j] >= size:
                # Check if it's the largest suitable block so far
                if worst_index == -1 or mem[j] > mem[worst_index]:
                    worst_index = j

        # Allocate the process to worst-fit block
        if worst_index != -1:
            print(f"{name} ({size}KB) → Block {worst_index+1} ({mem[worst_index]}KB)")
            mem[worst_index] -= size
        else:
            print(f"{name} ({size}KB) → Not Allocated")

# ---------------------- Run All Strategies ----------------------

# Run First Fit strategy
first_fit(memory_blocks, processes)

# Run Best Fit strategy
best_fit(memory_blocks, processes)

# Run Worst Fit strategy
worst_fit(memory_blocks, processes)
