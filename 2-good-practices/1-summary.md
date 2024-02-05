# Why is it important to pay attention and give some love when you write your code?

Well, it's not that obvious, because each of us have a different purpose to use code in our job.
There are codes that are once written, once ran and then out to the rubbish, and there's the other that started as the previously mentioned one,
but has the potential to be reused in other pipelines. So in my opinion it is easier to treat every code that you write with "love", so if the time
comes to re-use it somewhere, or send it to another person, you or the "another person" won't get a headache trying to dig through the ugly / spaghetti lines.

Following some principals you can avoid the cumbersome spaghetti code:
(I assume that everybody uses Python as a primary or secondary language.)

- Use a formatter that is following the standard language convention, PEP8. I recommend Black. Easy to install, configure (if needed) and use.
- Use PyLint as a static linter that will tell you how well written your code is. (Don't go crazy with it, but it's always nice to try to get a higher score.)
- Strive for your code is not over-indented. Maximum identation should be 3, or 4 in special cases.
- Functions should be short, but sometimes there are complicated functions that are inherently long so don't be sad if you have couple of long functions.
   BUT try not to overflow the height of your editor!!

- Long lines are confusing and ugly. Maximum column number should be 80 characters (or 100... some people say 100 and that's okay. They are bad programmers :-D)
- Don't use 2 spaces identation. It will let you to over-indent your code. Use 4 spaces (NOT TABS), that is the profession standard.

*Find examples in 2-well-and-poor-written-examples*

---

# Performance

Bad performance doesn't come from the single points in the codebase, but rather from "moldy breadcrumbs" spread all over your code.
That's why it is important to know your data types and structures of the given language, and to reduce the amount of copies made for each variables.
Copies equal more memory used and also more work for the garbage collector of the runtime, which can make your code slow and gready in spikes.

NOTE: Follow the middle road with the head on your shoulders. Premature optimization is a thing and millions of lines of code suffer from it! :-D

*Find examples in 3-fast-and-slow-examples*

---

