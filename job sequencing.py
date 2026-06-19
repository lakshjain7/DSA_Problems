def job_sequencing(jobs):
    """
    Jobs: list of tuples (job_id, deadline, profit)
    Returns: sequence of jobs and total profit
    """
    # Sort jobs by profit in descending order
    jobs.sort(key=lambda x: x[2], reverse=True)
    
    # Find maximum deadline
    max_deadline = max(job[1] for job in jobs)
    
    # Initialize result arrays
    result = [None] * max_deadline
    selected_jobs = []
    total_profit = 0
    
    for job in jobs:
        job_id, deadline, profit = job
        
        # Find a free slot for this job (from deadline-1 to 0)
        for slot in range(min(deadline - 1, max_deadline - 1), -1, -1):
            if result[slot] is None:
                result[slot] = job_id
                selected_jobs.append(job)
                total_profit += profit
                break
    
    return selected_jobs, total_profit

# Example
jobs = [('J1', 2, 100), ('J2', 1, 19), ('J3', 2, 27), ('J4', 1, 25), ('J5', 3, 15)]
selected, profit = job_sequencing(jobs)
print(f"Selected jobs: {selected}")
print(f"Total profit: {profit}")
