
kospi_did = False
kosdaq_did = False
exch_did = False
second_bo_did = False

kospi_up = False
kosdaq_up = False
exch_up = False

n = 1
while not (kospi_did and kosdaq_did and exch_did and second_bo_did):
    kospi_did = True
    kosdaq_did = True
    exch_did = True
    second_bo_did = True
    n +=1
    print(n)
print("끝")

n = 2
print(n % 2 == 0)