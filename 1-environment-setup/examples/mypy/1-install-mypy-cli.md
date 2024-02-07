# Install MyPy CLI

```bash
pip install mypy
```

```bash
conda install conda-forge::mypy
```

---

# Run MyPy on a file

```bash
mypy 2_faulty_script.py
```

```console
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/mypy$ 
ll
total 20
drwxrwxr-x 3 danielmajer danielmajer 4096 Feb  7 08:55 ./
drwxrwxr-x 4 danielmajer danielmajer 4096 Feb  7 08:55 ../
-rw-rw-r-- 1 danielmajer danielmajer  163 Feb  7 08:52 1-install-mypy-cli.md
-rw-rw-r-- 1 danielmajer danielmajer 1047 Feb  7 08:55 2-faulty-script.py
drwxrwxr-x 3 danielmajer danielmajer 4096 Feb  7 08:54 .mypy_cache/
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/mypy$ 
mypy 2-faulty-script.py 
2-faulty-script.py:8: error: Incompatible return value type (got "int", expected "str")  [return-value]
2-faulty-script.py:16: error: Argument 1 to "greet" has incompatible type "int"; expected "str"  [arg-type]
2-faulty-script.py:28: error: List item 0 has incompatible type "int"; expected "str"  [list-item]
2-faulty-script.py:28: error: List item 1 has incompatible type "int"; expected "str"  [list-item]
2-faulty-script.py:28: error: List item 2 has incompatible type "int"; expected "str"  [list-item]
2-faulty-script.py:41: error: Extra key "email" for TypedDict "Person"  [typeddict-unknown-key]
Found 6 errors in 1 file (checked 1 source file)
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/mypy$
```

---
