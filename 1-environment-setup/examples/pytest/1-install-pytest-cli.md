# Install pytest CLI

```bash
pip install pytest
```

```bash
 conda install anaconda::pytest 
```

---

# Run pytest

```bash
pytest .
```

*Or increasing the verbosity and allow pytest to show the prints from the stack calls*

```bash
pytest -vvvs .
```

```console
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/pytest$ 
ll
total 28
drwxrwxr-x 4 danielmajer danielmajer 4096 Feb  7 09:16 ./
drwxrwxr-x 5 danielmajer danielmajer 4096 Feb  7 09:11 ../
-rw-rw-r-- 1 danielmajer danielmajer  131 Feb  7 09:12 1-install-pytest-cli.md
-rw-rw-r-- 1 danielmajer danielmajer  526 Feb  7 09:16 my_module.py
drwxrwxr-x 2 danielmajer danielmajer 4096 Feb  7 09:18 __pycache__/
drwxrwxr-x 3 danielmajer danielmajer 4096 Feb  7 09:13 .pytest_cache/
-rw-rw-r-- 1 danielmajer danielmajer 1574 Feb  7 09:17 test_my_module.py
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/pytest$ 
pytest -vvvs .
============================================================================================================================= test session starts ==============================================================================================================================
platform linux -- Python 3.10.12, pytest-7.4.3, pluggy-1.2.0 -- /home/danielmajer/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/danielmajer/workspace/how2code/1-environment-setup/examples/pytest
plugins: anyio-3.7.1, mock-3.12.0
collected 10 items                                                                                                                                                                                                                                                             

test_my_module.py::test_add_numbers_parametrized[2-3-5] PASSED
test_my_module.py::test_add_numbers_parametrized[-2-3-1] PASSED
test_my_module.py::test_add_numbers PASSED
test_my_module.py::test_add_numbers_negative PASSED
test_my_module.py::test_divide_numbers PASSED
test_my_module.py::test_divide_numbers_by_zero PASSED
test_my_module.py::test_filter_even_numbers PASSED
test_my_module.py::test_filter_even_numbers_empty_list PASSED
test_my_module.py::test_invert_dictionary PASSED
test_my_module.py::test_invert_dictionary_empty_dict PASSED

============================================================================================================================== 10 passed in 0.01s ==============================================================================================================================
(venv) danielmajer@pop-os:~/workspace/how2code/1-environment-setup/examples/pytest$
```
