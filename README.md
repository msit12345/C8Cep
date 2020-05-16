
# C8Automation

Repository for C8Cep

  

## Steps for executing workflows:

  

1. Clone the C8Cep

```

git clone https://github.com/msit12345/C8Cep.git

  
```
2. Create a new branch and checkout to it

```

git checkout -b <branch-name>
```
  

3. Edit the `functional_workflows.yaml` file

    * To provide the federation URL against     which the workflows are to be executed.

    * To set as `true` for the workflows you    want to excecute in the    functional_workflows.yaml file.

    * Test Suites : Use `test-suite` array  under `functional` attribute
    * `test-suite` if not provided, all test    cases will be executed. Otherwise only     those test cases will be executed which     belongs to tags provided in `test-suite`    array.
    * Available tags in `test-suite` : `db`     `spot` `rice` `pipeline` and `stream`
        ```
        For example:

        functional:
            enable: true
            # available markers
            # db, stream, spot, pipeline, rice
            test-suite:
              - db


        ```

  

4. Commit and push the updated tests_input.yaml file to the branch.

```

git add .

git commit -m "commit msg"

git push origin <branch-name>

  ```

5. Check the result of the workflows execution on circle web console - https://circleci.com/dashboard

  

6. Delete the branch on C8Automation gitub repository once you are done with testing.

  

## Steps for updating branch

  

```

git checkout master

git pull

git checkout <branch-name>

git merge master

git push

```
