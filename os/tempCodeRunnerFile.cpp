
// First-Come-First-Served (FCFS) Scheduling
void FCFS(vector<Job> jobs)
{
    cout << "----FCFS Scheduling----" << endl;

 
    sort(jobs.begin(), jobs.end(), [](Job a, Job b) { return a.at < b.at; });
    int time = 0;
    int n = jobs.size();

    for (int i = 0; i < n; i++)
    {
        time = max(time, jobs[i].at);
        jobs[i].wt = time - jobs[i].at;
        jobs[i].tat = jobs[i].wt + jobs[i].bt;
        time += jobs[i].bt;
    }

    displayTable(jobs);
}

// Shortest Job First (Preemptive SJF) Scheduling
void SJF_Preemptive(vector<Job> jobs)
{
    cout << "----Shortest Job First (Preemptive) Scheduling----" << endl;

    int n = jobs.size(), completed = 0, time = 0;
    vector<int> rembt(n); // Remaining burst time
    for (int i = 0; i < n; i++) {
    rembt[i] = jobs[i].bt;

    }


    while (completed < n)
    {
        int idx = -1, minBT = 999;

        for (int i = 0; i < n; i++)
        {
            if (jobs[i].at <= time && rembt[i] > 0 && rembt[i] < minBT)
            {
                idx = i;
                minBT = rembt[i];
            }
        }

        if (idx == -1)
            time++;
        else
        {
            rembt[idx]--;
            time++;
            if (rembt[idx] == 0)
            {
                completed++;
                jobs[idx].tat = time - jobs[idx].at;
                jobs[idx].wt = jobs[idx].tat - jobs[idx].bt;
            }
        }
    }

    displayTable(jobs);
}

// Priority (Non-Preemptive) Scheduling
void Priority(vector<Job> jobs)
{
    cout << "----Priority (Non-Preemptive) Scheduling----" << endl;

    int time = 0;
    vector<Job> completedJobs;

    while (!jobs.empty())
    {
        int idx = -1, minPR = 999;
        for (int i = 0; i < jobs.size(); i++)
        {
            if (jobs[i].at <= time && jobs[i].pr < minPR)
            {
                idx = i;
                minPR = jobs[i].pr;
            }
        }

        if (idx == -1)
            time++;
        else
        {
            jobs[idx].wt = time - jobs[idx].at;
            jobs[idx].tat = jobs[idx].wt + jobs[idx].bt;
            time += jobs[idx].bt;
            completedJobs.push_back(jobs[idx]);
            jobs.erase(jobs.begin() + idx);
        }
    }

    displayTable(completedJobs);
}


void RoundRobin(vector<Job>& jobs, int quantum) {
    cout << "----Round Robin (Preemptive) Scheduling----" << endl;

    int n = jobs.size();
    int time = 0;  // System clock
    int completed = 0;  // Number of jobs completed
    queue<int> q;  // Queue to hold the indexes of jobs ready to execute
    vector<int> rembt(n);  // Remaining burst times
    vector<bool> addedToQueue(n, false);  // Track jobs that have been added to the queue

    // Initialize remaining burst times and queue with jobs that have arrived at time 0
    for (int i = 0; i < n; i++) {
        rembt[i] = jobs[i].bt;
        if (jobs[i].at <= time && !addedToQueue[i]) {
            q.push(i);
            addedToQueue[i] = true;
        }
    }

    while (completed < n) {
        if (!q.empty()) {
            int i = q.front();  // Get the front job from the queue
            q.pop();

            int execTime = min(quantum, rembt[i]);  // Execute for the quantum or the remaining burst time
            rembt[i] -= execTime;
            time += execTime;

            // If the job finishes, calculate WT and TAT
            if (rembt[i] == 0) {
                jobs[i].tat = time - jobs[i].at;  // Turnaround Time
                jobs[i].wt = jobs[i].tat - jobs[i].bt;  // Waiting Time
                completed++;
            }

            // Check for new jobs that have arrived during this time slice and add them to the queue
            for (int j = 0; j < n; j++) {
                if (jobs[j].at <= time && rembt[j] > 0 && !addedToQueue[j]) {
                    q.push(j);
                    addedToQueue[j] = true;
                }
            }

            // If the job is not completed, re-add it to the queue
            if (rembt[i] > 0) {
                q.push(i);
            }
        } else {
            // If queue is empty, increment time until a job arrives
            time++;
            for (int j = 0; j < n; j++) {
                if (jobs[j].at <= time && rembt[j] > 0 && !addedToQueue[j]) {
                    q.push(j);
                    addedToQueue[j] = true;
                }
            }
        }
    }

    displayTable(jobs);  // Display the results
}

