# Install Black formatter CLI

```bash
pip install black
```

```bash
conda install conda-forge::black
```

---

# Run MyPy on a file

```bash
black 2_unformatted_script_to_be_formatted.py
```

```console
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/black-formatter$ 
ll
total 20
drwxrwxr-x 2 danielmajer danielmajer 4096 Feb  7 09:06 ./
drwxrwxr-x 4 danielmajer danielmajer 4096 Feb  7 08:55 ../
-rw-rw-r-- 1 danielmajer danielmajer  198 Feb  7 09:06 1-install-black-formatter-cli.md
-rw-r--r-- 1 danielmajer danielmajer  530 Feb  7 09:04 2_unformatted_script_to_be_formatted.py
-rw-r--r-- 1 danielmajer danielmajer  530 Feb  7 09:05 unformatted_script_original.py
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/black-formatter$ 
black 2_unformatted_script_to_be_formatted.py
reformatted 2_unformatted_script_to_be_formatted.py

All done! ✨ 🍰 ✨
1 file reformatted.
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/black-formatter$ 
diff unformatted_script_original.py 2_unformatted_script_to_be_formatted.py 
1,3c1,5
< 
< def poorly_formatted_function(a:int,b:  float,c :str,d:   list[int])->   tuple[int, int]:
<     if a>0: print("Positive")
---
> def poorly_formatted_function(
>     a: int, b: float, c: str, d: list[int]
> ) -> tuple[int, int]:
>     if a > 0:
>         print("Positive")
5c7
<             print("Non-positive")
---
>         print("Non-positive")
11,13d12
<         
< if __name__ =="__main__":
<     input_list = [1,2,3,4]
15c14,20
<     long_nested_comprehension: list[list[int]] = [[i * j for j in range(1, 6) if j % 2 == 0] for i in range(1, 11) if i % 2 != 0]
---
> 
> if __name__ == "__main__":
>     input_list = [1, 2, 3, 4]
> 
>     long_nested_comprehension: list[list[int]] = [
>         [i * j for j in range(1, 6) if j % 2 == 0] for i in range(1, 11) if i % 2 != 0
>     ]
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/black-formatter$
```

---
