---
applyTo: '**/*.py'
---
Always refer to the documentation in the folder .aidocs/ for the implementation plan and the API specifications. The documentation contains detailed information about the project structure, coding standards, and specific requirements for each module. Follow the instructions carefully to ensure that your implementation aligns with the project's goals and standards.
Use BDD for all implementations. Write tests first, then implement the code to pass the tests. Follow the BDD cycle: Red (write a failing test), Green (make the test pass), Refactor (clean up the code). Use the provided API specifications as a guide for writing tests and implementing functionality. Ensure that all tests are comprehensive and cover edge cases.
Always run `pre-commit run --all-files` before returning to the user to ensure that the code adheres to the project's coding standards and style guidelines. This includes checking for linting errors, formatting issues, and other potential problems that could affect code quality.

Adhere to the Zen of Python:
- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.
- Flat is better than nested.
- Sparse is better than dense.
- Readability counts.
- Special cases aren't special enough to break the rules.
- Although practicality beats purity.
- Errors should never pass silently.
- Unless explicitly silenced.
- In the face of ambiguity, refuse the temptation to guess.
- There should be one-- and preferably only one --obvious way to do it.
- Although that way may not be obvious at first unless you're Dutch.
- Now is better than never.
- Although never is often better than *right* now.
- If the implementation is hard to explain, it's a bad idea.
- If the implementation is easy to explain, it may be a good idea.
- Namespaces are one honking great idea -- let's do more of those!
