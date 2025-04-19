
allocated_blocks = []  # Each item is (start_address, size, process_name)
free_blocks = []       # Each item is (start_address, size)
total_memory_size = 0  # Total size of the memory

def create_memory(size):
    
    #Initialize the memory with a given size.
   
    global allocated_blocks, free_blocks, total_memory_size
    if size <= 0:
        print("Error: Memory size must be greater than zero!")
        return False

    total_memory_size = size
    allocated_blocks = []  # No processes allocated at the start
    free_blocks = [(0, size)]  # Entire memory is free at the beginning
    print(f"Memory initialized with {size} units.")
    return True

def display_memory():

    #Display the current state of memory showing used and free blocks.
    
    print("\n--- Current Memory Layout ---")
    combined = []

    # Add allocated blocks to the combined list
    for start, size, pname in allocated_blocks:
        combined.append((start, size, f"Process {pname}"))

    # Add free blocks to the combined list
    for start, size in free_blocks:
        combined.append((start, size, "Free"))

    combined.sort()  # Sort all blocks by their start address

    # Display all blocks
    for start, size, label in combined:
        print(f"[{start}-{start + size - 1}] {label} ({size} units)")

    print("=" * 50)

def allocate(process_name, size, strategy='F'):
    """
    Allocate a block of memory for a process using the selected strategy.
    Strategies:
    'F' - First Fit
    'B' - Best Fit
    'W' - Worst Fit
    """
    global allocated_blocks, free_blocks

    if size <= 0:
        print("Error: Allocation size must be greater than zero!")
        return False

    index = -1  # Will store the index of the selected free block

    # Strategy: First Fit
    if strategy == 'F':
        for i, (start, block_size) in enumerate(free_blocks):
            if block_size >= size:
                index = i
                break

    # Strategy: Best Fit
    elif strategy == 'B':
        best = float('inf')
        for i, (start, block_size) in enumerate(free_blocks):
            if block_size >= size and block_size - size < best:
                best = block_size - size
                index = i

    # Strategy: Worst Fit
    elif strategy == 'W':
        worst = -1
        for i, (start, block_size) in enumerate(free_blocks):
            if block_size >= size and block_size - size > worst:
                worst = block_size - size
                index = i

    # Invalid Strategy
    else:
        print("Error: Unknown strategy. Use 'F' (First Fit), 'B' (Best Fit), or 'W' (Worst Fit).")
        return False

    # If no suitable block is found
    if index == -1:
        total_free = sum(size for _, size in free_blocks)
        if total_free >= size:
            print(f"Allocation failed for {process_name}: External Fragmentation Detected!")
        else:
            print(f"Allocation failed for {process_name}: Not enough total memory!")
        return False

    # Allocation Success: Split block if necessary
    start, block_size = free_blocks.pop(index)  # Take the selected block
    allocated_blocks.append((start, size, process_name))
    allocated_blocks.sort()  # Keep the allocated list sorted

    # If leftover space exists, add it back to the free list
    if block_size > size:
        free_blocks.append((start + size, block_size - size))
        free_blocks.sort()

    print(f"Allocated {size} units to Process {process_name} at address {start}.")
    return True

def deallocate(process_name):
    
    #Free memory occupied by a specific process.
    
    global allocated_blocks, free_blocks

    for i, (start, size, pname) in enumerate(allocated_blocks):
        if pname == process_name:
            # Remove the process from allocated list
            allocated_blocks.pop(i)
            # Add the freed space back to free blocks
            free_blocks.append((start, size))
            free_blocks.sort()
            # Merge neighboring free blocks
            _merge_free_blocks()
            print(f"Deallocated Process {process_name}.")
            return True

    print(f"Process {process_name} not found.")
    return False

def _merge_free_blocks():
    
    #Combine neighboring free blocks into one larger block.
    
    global free_blocks
    i = 0
    while i < len(free_blocks) - 1:
        current_start, current_size = free_blocks[i]
        next_start, next_size = free_blocks[i + 1]

        # If two blocks are adjacent, merge them
        if current_start + current_size == next_start:
            free_blocks[i] = (current_start, current_size + next_size)
            free_blocks.pop(i + 1)  # Remove merged block
        else:
            i += 1  # Move to the next block

def compact():
   
    #Move all processes to the start of memory to eliminate fragmentation.
    
    global allocated_blocks, free_blocks
    print("Compacting memory...")

    allocated_blocks.sort()  # Make sure the list is sorted by address
    offset = 0  # The next available memory address

    for i in range(len(allocated_blocks)):
        start, size, pname = allocated_blocks[i]
        if start != offset:
            print(f"Moved Process {pname} from {start} to {offset}.")
            allocated_blocks[i] = (offset, size, pname)
        offset += size

    remaining = total_memory_size - offset

    if remaining > 0:
        free_blocks[:] = [(offset, remaining)]  # One big free block at the end
    else:
        free_blocks[:] = []  # No free space left

    print("Compaction complete.")


## TEST ## 

create_memory(100)
display_memory()

#step 1 : allocate processes 

allocate("P1", 20, 'F')
allocate("P2", 30, 'F')
allocate("P3", 10, 'F')
display_memory()

#step 2: deallocate p2 for an example 

deallocate("P2")
display_memory()

#step 3 : allocate p4 
allocate("P4", 50, 'F')
display_memory()

compact() 
display_memory()

allocate("P4", 50, 'F')
display_memory()

