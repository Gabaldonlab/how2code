
def poorly_formatted_function(a:int,b:  float,c :str,d:   list[int])->   tuple[int, int]:
    if a>0: print("Positive")
    else:
            print("Non-positive")
    result = b + sum(d)
    if c == "foo":
        return (result, 0)
    else:
        return (0, result)
        
if __name__ =="__main__":
    input_list = [1,2,3,4]

    long_nested_comprehension: list[list[int]] = [[i * j for j in range(1, 6) if j % 2 == 0] for i in range(1, 11) if i % 2 != 0]
    print(poorly_formatted_function(5, 3.14, "bar", input_list))
