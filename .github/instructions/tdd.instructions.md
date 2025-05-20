---
applyTo: '**'
---
Always refer to the documentation in the folder .aidocs/ for the implementation plan and the API specifications. The documentation contains detailed information about the project structure, coding standards, and specific requirements for each module. Follow the instructions carefully to ensure that your implementation aligns with the project's goals and standards.

Use BDD for all implementations. Write tests first, then implement the code to pass the tests. Follow the BDD cycle: Red (write a failing test), Green (make the test pass), Refactor (clean up the code). Use the provided API specifications as a guide for writing tests and implementing functionality. Ensure that all tests are comprehensive and cover edge cases.

Code Style and Quality Requirements:
1. Format all Python code using Black formatter
2. Sort imports using isort
3. Follow flake8 guidelines:
   - Maximum line length: 79 characters
   - No unused imports
   - No undefined names
   - No syntax errors
4. Use mypy for type checking with strict settings
5. Remove all debug statements before committing
6. Ensure no trailing whitespace in any files
7. All files must end with a newline
8. YAML and TOML files must be valid
9. Avoid adding large files to the repository

Always run `pre-commit run --all-files` before returning to the user to ensure that the code adheres to these coding standards and style guidelines. Fix any issues reported by the pre-commit hooks before proceeding.
Alway run all tests as the last step before returning to the user. Ensure that all tests pass and that there are no errors or warnings. If any tests fail, investigate the cause and fix the issues before returning the code.

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
