# Version control - Honing git true potential
Most of us already use git to download other tools and to update our own developed software to github to keep track of it and as an online storage of sorts. This however is just a tiny bit of what Github can offer for your projects. 

    *   Documentation - Readmes and wikis
    *   Continous development - commits and branches
    *   Version control - Releases
    *   Continous integration  - Github actions
## Documentation - Readmes and wikis
The github environment is great for basic tool documentation. From singular Markdown READMEs that may introduce the tool or provided a step by step usage to more complex wikis that provide information in a more organized and intuitive manner.

**README**
A simple text file with information. It can vary from fairly simplistic to quite complex. They use the Markdown format. You can import images, set up github badges, allow the inclusion of code blocks and much more.

**Wiki**
A feature within each repository. Allow the creation of wiki page-like structures in Markdown. A bit more clean and proper than just using a large README. May also help to convey a more step by step setup or even provide workshop-like examples for your tool. It is worth to consider if your tool is fairly complex to set up or to run. 

Overall github provides good features to use for documentation, although there are better alternatives such as [ReadtheDocs](https://docs.readthedocs.io/) which require a bit of a learning curve.

## Continous development - commits and branches
Git is a powerful tool. It allows developers to snapshot past versions of the code and incorporate changes through the commit features. A commit can be briefly defined as a snapshot of a change in the source during a given time, identified with an unique ID, a github hash. This commits can be associated to a commit message in which the devloper can provide additional information behind the rationale or the reason behind the commit. You can also cross-reference Github Issues to this commits.

Branches are copies of the complete repository at a given time. You can use branches to work on specific features without compromising your main production branch. It also allows to keep track of commits in a more ordered way, as you can branch master for an specific adaptation you are working on, ie: "minimap2_module_implementation"

Most of you already know how to commit. However, I would present some good practices on how to handle commits:

**Commit Frequently**: Make small, incremental commits that focus on a single logical change. Avoid "mega-commits" that address multiple issues or changes.

![Multiple commits](https://github.com/Gabaldonlab/how2code/blob/main/4-version-control/assets/multcommit.png?raw=true)

vs

![Single large commit](https://github.com/Gabaldonlab/how2code/blob/main/4-version-control/assets/singcommit.png?raw=true)

**Write Meaningful Commit Messages**: Provide clear and concise commit messages that describe the purpose of the change. ie: "Fix bug" vs "Correct unexepcted behavior with the map function for a single file"


**Separate Concerns**: Keep unrelated changes in separate commits. Also avoid mixing formatting, logic changes, and feature additions in a single commit.


**Review Changes Before Committing**: Use git diff or an interactive staging (git add -i or git add -p) to review changes before committing.


**Use Branches Wisely**: Create feature branches for new features or bug fixes. It is better to avoid committing directly to the main branch; prefer creating pull requests.


**Use Descriptive Branch Names**: Choose meaningful branch names that reflect the purpose of the changes. It is also a good a idea to prefix branch names with a category (e.g., feature/, bugfix/).


**Sign Your Commits**: Sign your commits with GPG to verify the authenticity of the author. This will become key in projects with multiple people.


**Use .gitignore**: I always include a .gitignore file to exclude unnecessary files (e.g., build artifacts, IDE-specific files) from version control. Keeps your repository at an acceptable size for pushing changes to your repo.


Please, note that keeping updated the README and documentation is a must while actively working on a tool. Keep in mind that if you are working with more people on a project, **all team members are aware and follow the agreed-upon commit practices.**


## Version control - Releases
Whenever you feel you've completed a milestone for your tool, it is a good practice to generate a proper release for it. A release is archived withing github, obeys versioning nomenclature and includes the source code as a tar ball or zipped. You can also auto-generate the release notes with all the relevant information from the latest commits and merges that you did, as well as any additional information you might want to share to the public.

Moreover, Zenodo uses it to generate a permanent DOI you can use to cite specific code versions if required. 

![Example of releases](https://github.com/Gabaldonlab/how2code/blob/main/4-version-control/assets/releases.png?raw=true)

I recommend to generate a release after a major milestone is achived, such as the correct implementation of a set of new modules, fixing a major bug or anything major.


## Continous integration  - Github actions
GitHub Actions is a powerful and flexible continuous integration and continuous delivery (CI/CD) platform provided by GitHub. It allows you to automate workflows, enabling you to build, test, and deploy your software directly from your GitHub repository. GitHub Actions is built directly into the GitHub platform, making it easy to set up and integrate with your projects.

![Example of a github action .yml](https://github.com/Gabaldonlab/how2code/blob/main/4-version-control/assets/actions.png?raw=true)

Key concepts of GitHub Actions:

    Workflow:
        A workflow is a set of configurable automated steps that run in response to specific triggers in your repository.
        Workflows can be defined using YAML files and are stored in the .github/workflows directory of your repository.

    Trigger Events:
        Workflows can be triggered by various events, such as pushes to the repository, pull request creation or updates, issue comments, and more.
        You can specify the events that should trigger your workflow in the workflow configuration file.

    Jobs:
        A workflow is made up of one or more jobs. Each job runs on a separate virtual machine or container.
        Jobs can be parallelized or depend on the completion of other jobs.

    Steps:
        Each job consists of a sequence of steps. A step is a single task or command, such as checking out code, running tests, or deploying an application.
        Steps are defined in the workflow configuration file.

    Actions:
        Actions are reusable, standalone units of work defined in a YAML file. They encapsulate one or more steps.
        GitHub provides a marketplace where you can find and share pre-built actions, but you can also create custom actions tailored to your specific needs.

    Matrix Builds:
        GitHub Actions supports matrix builds, allowing you to run the same set of steps across multiple configurations (e.g., different operating systems, language versions, etc.).

    Environment Variables:
        Actions can use environment variables, secrets, and other context information to customize their behavior.

    Artifacts:
        Workflows can produce artifacts, which are files or directories generated during the workflow execution. These artifacts can be used in subsequent jobs or workflow runs.

You can use the actions templates to set up your Actions workflows with minimal setup, although the most interesting results can be obtained through a bit of learning curve

![Actions templates](https://github.com/Gabaldonlab/how2code/blob/main/4-version-control/assets/templates.png?raw=true)

