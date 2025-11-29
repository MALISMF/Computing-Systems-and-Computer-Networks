for n in range(1,4):
    myfile = open(f"telephones{n}.txt")

    N = int(myfile.readline())
    nums = {}

    for N in range(N):
        a, b = map(int, myfile.readline().split())
        for i in range(a,b):
            if i in nums.keys():
                nums[i] += 1
            else:
                nums[i] = 1
        
    myfile.close()

    maximum = max(nums.values())

    keys = [key for key, val in nums.items() if val == maximum]
    print(f"Момент времени для файла {n}: {min(keys)}")
