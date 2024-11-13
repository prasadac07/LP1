#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

class Job
{
public:
    string s;    // Job name
    int at, bt, wt, tat, pr, remBT; // Arrival Time, Burst Time, Waiting Time, Turnaround Time, Priority, Remaining Burst Time

    Job()
    {
        s = "";
        at = bt = wt = tat = pr = remBT = 0;
    }

    void getData()
    {
        cout << "Enter Job Name: ";
        cin >> s;
        cout << "Arrival Time: ";
        cin >> at;
        cout << "Burst Time: ";
        cin >> bt;
        remBT = bt;  // Initialize remaining burst time to the burst time
        cout << "Priority: ";
        cin >> pr;
    }
};

void displayTable(const vector<Job> &jobs)
{
    cout << "Job\tAT\tBT\tWT\tTAT\tPR" << endl;
    for (const auto &job : jobs)
    {
        cout << job.s << "\t" << job.at << "\t" << job.bt << "\t" << job.wt << "\t" << job.tat << "\t" << job.pr << endl;
    }
}
// FCFS
void FCFS(vector<Job> jobs)
{
    cout << "----FCFS Scheduling----" << endl;

    sort(jobs.begin(), jobs.end(), [](Job a, Job b) { return a.at < b.at; });
    int time = 0;
    int n = jobs.size();

    for (int i = 0; i < n; i++)
    {
        time = max(time, jobs[i].at);
        time += jobs[i].bt;
        jobs[i].tat = time - jobs[i].at;
        jobs[i].wt = jobs[i].tat - jobs[i].bt;
    }

    displayTable(jobs);
}

// SJF Preemptive
void SJF_Preemptive(vector<Job> jobs)
{
    cout << "----Shortest Job First (Preemptive) Scheduling----" << endl;

    int n = jobs.size(), completed = 0, time = 0;
    vector<int> rembt(n);
    for (int i = 0; i < n; i++) rembt[i] = jobs[i].bt;

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

// Priority Scheduling (Non-Preemptive)
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
            time += jobs[idx].bt;
            jobs[idx].tat = time - jobs[idx].at;
            jobs[idx].wt = jobs[idx].tat - jobs[idx].bt;
            completedJobs.push_back(jobs[idx]);
            jobs.erase(jobs.begin() + idx);
        }
    }

    displayTable(completedJobs);
}

// Round Robin
void RoundRobin(vector<Job>& jobs, int quantum) {
    cout << "----Round Robin (Preemptive) Scheduling----" << endl;

    int n = jobs.size();
    int time = 0;
    int completed = 0;
    queue<int> q;
    vector<int> rembt(n);
    vector<bool> addedToQueue(n, false);

    for (int i = 0; i < n; i++) {
        rembt[i] = jobs[i].bt;
        if (jobs[i].at <= time && !addedToQueue[i]) {
            q.push(i);
            addedToQueue[i] = true;
        }
    }

    while (completed < n) {
        if (!q.empty()) {
            int i = q.front();
            q.pop();

            int execTime = min(quantum, rembt[i]);
            rembt[i] -= execTime;
            time += execTime;

            if (rembt[i] == 0) {
                jobs[i].tat = time - jobs[i].at;
                jobs[i].wt = jobs[i].tat - jobs[i].bt;
                completed++;
            }

            for (int j = 0; j < n; j++) {
                if (jobs[j].at <= time && rembt[j] > 0 && !addedToQueue[j]) {
                    q.push(j);
                    addedToQueue[j] = true;
                }
            }

            if (rembt[i] > 0) {
                q.push(i);
            }
        } else {
            time++;
            for (int j = 0; j < n; j++) {
                if (jobs[j].at <= time && rembt[j] > 0 && !addedToQueue[j]) {
                    q.push(j);
                    addedToQueue[j] = true;
                }
            }
        }
    }

    displayTable(jobs);
}

int main()
{
    int n;
    cout << "Enter total number of jobs: ";
    cin >> n;

    vector<Job> jobs(n);
    for (int i = 0; i < n; i++)
    {
        cout << "Enter details for Job " << i + 1 << endl;
        jobs[i].getData();
    }

    FCFS(jobs);
    SJF_Preemptive(jobs);
    Priority(jobs);
    int quantum;
    cout << "Enter time quantum for Round Robin: ";
    cin >> quantum;
    RoundRobin(jobs, quantum);

    return 0;
}
