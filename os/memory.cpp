#include <iostream>
#include <vector>
#include <algorithm>
#include <limits.h>

using namespace std;

struct Block
{
    int size;
    bool isAllocated;
    int allocatedSize; // Track allocated size within the block
};

class MemoryManager
{
private:
    vector<Block> blocks;
    vector<Block> initialBlocks; // Store initial state of blocks

    // Method to reset blocks to initial state
    void resetBlocks()
    {
        blocks = initialBlocks;
    }

public:
    MemoryManager(const vector<int> &sizes)
    {
        for (int size : sizes)
        {
            blocks.push_back({size, false, 0});
        }
        // Store initial state of blocks
        initialBlocks = blocks;
    }

    void displayMemory()
    {
        cout << "\nMemory Status:\n";
        for (int i = 0; i < blocks.size(); i++)
        {
            int freeSize = blocks[i].size - blocks[i].allocatedSize;
            cout << "Block " << i + 1 << ": Total Size = " << blocks[i].size
                 << ", Allocated Size = " << blocks[i].allocatedSize
                 << ", Free Size = " << freeSize
                 << ", Status = " << (blocks[i].isAllocated ? "Allocated" : "Free") << endl;
        }
        cout << endl;
    }

    void firstFit(int processSize)
    {
        cout << "First Fit Allocation:" << endl;
        for (int i = 0; i < blocks.size(); i++)
        {
            if (!blocks[i].isAllocated && blocks[i].size - blocks[i].allocatedSize >= processSize)
            {
                blocks[i].allocatedSize += processSize;
                if (blocks[i].allocatedSize == blocks[i].size)
                {
                    blocks[i].isAllocated = true;
                }
                cout << "Allocated to Block " << i + 1 << endl;
                return;
            }
        }
        cout << "No sufficient memory block found!" << endl;
    }

    void bestFit(int processSize)
    {
        cout << "Best Fit Allocation:" << endl;
        int bestIdx = -1;
        int minDiff = INT_MAX;
        for (int i = 0; i < blocks.size(); i++)
        {
            if (!blocks[i].isAllocated && blocks[i].size - blocks[i].allocatedSize >= processSize)
            {
                int diff = blocks[i].size - blocks[i].allocatedSize - processSize;
                if (diff < minDiff)
                {
                    minDiff = diff;
                    bestIdx = i;
                }
            }
        }
        if (bestIdx != -1)
        {
            blocks[bestIdx].allocatedSize += processSize;
            if (blocks[bestIdx].allocatedSize == blocks[bestIdx].size)
            {
                blocks[bestIdx].isAllocated = true;
            }
            cout << "Allocated to Block " << bestIdx + 1 << endl;
        }
        else
        {
            cout << "No sufficient memory block found!" << endl;
        }
    }

    void worstFit(int processSize)
    {
        cout << "Worst Fit Allocation:" << endl;
        int worstIdx = -1;
        int maxSize = -1;
        for (int i = 0; i < blocks.size(); i++)
        {
            if (!blocks[i].isAllocated && blocks[i].size - blocks[i].allocatedSize >= processSize)
            {
                if (blocks[i].size - blocks[i].allocatedSize > maxSize)
                {
                    maxSize = blocks[i].size - blocks[i].allocatedSize;
                    worstIdx = i;
                }
            }
        }
        if (worstIdx != -1)
        {
            blocks[worstIdx].allocatedSize += processSize;
            if (blocks[worstIdx].allocatedSize == blocks[worstIdx].size)
            {
                blocks[worstIdx].isAllocated = true;
            }
            cout << "Allocated to Block " << worstIdx + 1 << endl;
        }
        else
        {
            cout << "No sufficient memory block found!" << endl;
        }
    }

    void nextFit(int processSize, int &lastAllocatedIdx)
    {
        cout << "Next Fit Allocation:" << endl;
        int startIdx = (lastAllocatedIdx + 1) % blocks.size();
        for (int i = startIdx; i < blocks.size(); i++)
        {
            if (!blocks[i].isAllocated && blocks[i].size - blocks[i].allocatedSize >= processSize)
            {
                blocks[i].allocatedSize += processSize;
                if (blocks[i].allocatedSize == blocks[i].size)
                {
                    blocks[i].isAllocated = true;
                }
                lastAllocatedIdx = i;
                cout << "Allocated to Block " << i + 1 << endl;
                return;
            }
        }
        for (int i = 0; i < startIdx; i++)
        {
            if (!blocks[i].isAllocated && blocks[i].size - blocks[i].allocatedSize >= processSize)
            {
                blocks[i].allocatedSize += processSize;
                if (blocks[i].allocatedSize == blocks[i].size)
                {
                    blocks[i].isAllocated = true;
                }
                lastAllocatedIdx = i;
                cout << "Allocated to Block " << i + 1 << endl;
                return;
            }
        }
        cout << "No sufficient memory block found!" << endl;
    }

    void allocateProcesses(const vector<int> &processSizes, int choice)
    {
        int lastAllocatedIdx = -1;
        resetBlocks(); // Reset blocks before starting allocation
        for (int processSize : processSizes)
        {
            switch (choice)
            {
            case 1:
                firstFit(processSize);
                break;
            case 2:
                bestFit(processSize);
                break;
            case 3:
                worstFit(processSize);
                break;
            case 4:
                nextFit(processSize, lastAllocatedIdx);
                break;
            default:
                cout << "Invalid strategy choice!" << endl;
                return;
            }
            displayMemory();
        }
    }
};

int main()
{
    vector<int> blockSizes = {300,300,300,300,300}; 
    MemoryManager mm(blockSizes);

    vector<int> processSizes;
    int choice;
    bool exit = false;

    // Get process sizes from user
    cout << "Enter the number of processes: ";
    int numProcesses;
    cin >> numProcesses;

    cout << "Enter the sizes of the processes:" << endl;
    processSizes.resize(numProcesses);
    for (int i = 0; i < numProcesses; ++i)
    {
        cin >> processSizes[i];
    }

    while (!exit)
    {
        cout << "\nMemory Placement Strategies Menu:\n";
        cout << "1. First Fit\n";
        cout << "2. Best Fit\n";
        cout << "3. Worst Fit\n";
        cout << "4. Next Fit\n";
        cout << "5. Display Memory\n";
        cout << "6. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice)
        {
        case 1:
        case 2:
        case 3:
        case 4:
            mm.allocateProcesses(processSizes, choice);
            break;
        case 5:
            mm.displayMemory();
            break;
        case 6:
            cout << "Exiting...\n";
            exit = true;
            break;
        default:
            cout << "Invalid choice! Please try again.\n";
            break;
        }
    }

    return 0;
}
