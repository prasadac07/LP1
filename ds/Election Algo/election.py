def ring_election(processes, initiator):
    print("Process", initiator, "starts a Ring election.")
    
    # Initialize the election ring with the initiator
    election_ring = [initiator]
    current_index = processes.index(initiator)

    while True:
        # Find the next process in the ring
        next_index = (current_index + 1) % len(processes)
        next_process = processes[next_index]
        election_ring.append(next_process)
        print("Process", next_process, "passes the election message:", election_ring)
        
        # Move to the next process
        current_index = next_index

        # If we are back to the initiator, stop
        if next_process == initiator:
            break

    # Highest ID in the election_ring becomes the coordinator
    coordinator = max(election_ring)
    print("Ring Election complete. Process", coordinator, "is the new coordinator.\n")


def bully_election(processes, initiator):
    print("Process", initiator, "starts a Bully election.")
    
    higher_processes = []  # Create an empty list to store higher processes
    for process in processes:  # Iterate through all processes
        if process > initiator:  # Check if process ID is greater than initiator
            higher_processes.append(process)  # Append the process to the list if condition is met


    if not higher_processes:
        coordinator = initiator
        print("Process", initiator, "becomes the coordinator as no higher process responded.")
    else:
        for process in higher_processes:
            print("Process", initiator, "sends election message to Process", process)
            if process > initiator:
                print("Process", process, "responds to election from Process", initiator)
                # Recursive call to initiate the election from the responding process
                bully_election(processes, process)
                return

    print("Bully Election complete. Process", coordinator, "is the new coordinator.\n")


# Example usage
processes = [23, 11, 30, 15, 27]  # Processes with unique IDs in non-ascending order

# Start Ring election with initiator 11
ring_election(processes, initiator=11)

# Start Bully election with initiator 30
bully_election(processes, initiator=23)
