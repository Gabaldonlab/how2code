# Reproducibility for your code

Most of you already know how important it is make your code as clean and reproducible as it can be. Not only is it relevant in order to publish. It will help you spread your tool's userbase and enchance it with feedaback that can point out bugs or logic flaws.

As members of the scientific community we should strive to achive the golden standard of reproducibility which includes **documentation** as well as providing all the necesary information to run your software in any other platform with the minimal interjection from your users. In this regard, we are going to briefly touch the following:

    *   Compiler scripts
    *   Conda environemnts
    *   Docker / Singularity
    *   Workflows (Nextflow, Snakemake, Lugi)
    *   Bioconda-recipes / Pypi

## 0.5 Usage of wrapper scripts (amost the bare minimum)

Sometimes it is necessary to include wrapper scripts to facilitate the usage or the instalation of your tools. While useful, they are not the best for tools with multiple versioning. Have a look at the specific example provided and install the dependencies

```bash
bash compile.sh
```
See the potential issues?

## 1. Conda environments or the bronze standard (bare minimum to be accepted)

Conda is an open-source package management and environment management system that helps users create and manage environments for various programming languages, with a primary focus on **Python**. It is widely used for ensuring reproducibility in software development projects by allowing users to specify and control the dependencies and versions of software packages.

**Advantages**

.   **Package Management:** Conda simplifies the installation, update, and removal of software packages, handling dependencies automatically.

.   **Environment Management:** Users can create isolated environments in a .yml file extension with specific package versions, enabling reproducibility across different systems.

.   **Cross-Platform:** Conda works on multiple operating systems, making it easier to share and reproduce environments across different platforms.


**Limitations**

.   **Package Availability:** Not all packages are available through Conda, and users may need to resort to other package managers or installation methods for certain software.

.   **Limited Version Control:** Conda's version control is primarily focused on package versions, and it may not handle all aspects of versioning for every software component within an environment. It is also quite prone to broken dependencies.

.   **Build System Complexity:** Creating custom packages or dealing with packages that require compilation can be complex, and users may need additional tools or knowledge to manage such scenarios.

.   **Size of Environments:** Conda environments can be relatively large, especially when dealing with data science or scientific computing packages, which may lead to increased storage and bandwidth requirements.

Despite these limitations, Conda remains a powerful tool for creating and managing reproducible environments, and its ease of use makes it a popular choice among developers and data scientists.

Whenever you want to export an environment, you can use the following command to generate a .yml file with all the precise information to recreate it in another instance:

```bash
conda env export > my_environment.yml
```

Installing an environment from a YAML file is trivial, however conda dependencies may break without being it your fault due to botched updates to some of the dependencies.

```bash
conda env create -f my_environment.yml
```

I've provided two examples: **pilon_env and busco_env**. Try to install them.


What was the difference?


---

## 2. Docker / Singularity - The silver standard

Docker and Singularity are containerization tools designed to create and manage reproducible images, encapsulating an entire environment and its dependencies. They are particularly useful for ensuring consistency across different computing environments. It is just as if we were running a portable virtual machine with our desired OS and all the dependencies we require for our tool to properly function. I'll only focus on single images not in networks of images (docker networks and docker-compose)

**Advantages:**

.   **Portability:** Docker and Singularity images are highly portable and can run consistently on any system that supports Docker/Singularity, regardless of the underlying infrastructure.

.   **Isolation:** Both of them provide strong isolation by encapsulating the application and its dependencies, reducing conflicts and ensuring that the containerized application runs consistently across various environments. This encapsulation is better described as if you were to take a snapshot of the environment with all the dependencies you required in order to run your tool.

.   **Versioning:** Docker and singularity images support versioning, enabling users to precisely specify the environment and dependencies required for a particular application or service, ie: 

.   **Large ecosystem:** Docker (although to similar extent Singularity) has a vast and active ecosystem with a wide range of pre-built images available on Docker Hub, making it easy to share and distribute containerized applications.

.   **HPC-friendly:** Singularity is specifically designed for high-performance computing (HPC) environments, allowing users to run containers without requiring elevated privileges. This is the case for the MN4 and most likely MN5 too.

.   **Single file format:** Singularity uses a single container image file, making it easier to manage and share compared to Docker's multi-layered image structure that is shared to Dockerfile recipes. Care however with the image size, as it tends to grow quite fast and get to the Gb range.

.   **Interoperability:** Singularity can run Docker images directly and even convert them to a Singularity image, enhancing interoperability and enabling users to leverage the vast ![Docker hub environment](https://hub.docker.com/repositories/cgenomics). Keep in mind that although Singularity has its own ecosystem, it is not as extensive as Docker's.

**Limitations:**

.   **Compatibility:** Docker containers are designed to run on Linux, and while Docker Desktop provides support for Windows and macOS, it introduces some performance differences and may not offer a completely seamless experience. It is highly recommended to run it in Linux distros.

.   **Security concerns:** Running containers or singularity images as root can pose security risks, and users need to be cautious about container security practices to prevent potential vulnerabilities, specially if you mount volumes of your data directories.

.   **Limited daemonless mode:** Singularity's daemonless mode can limit certain functionalities compared to Docker's continuous background process. But it is an advantage for HPC execution.

.   **Learning curve:** As with any new tool, it has a learning curve. You will need to invest some time to get a hang of its basics, but that should be good enough to generate reproducible docker images

Check the following examples. For docker you can run the following to build it and then to run the image:

```bash
#First build from the docker/ directory allocated within this workshop
cd docker/
docker build -t test .
#Run image
docker run -dit --name=testy --rm test
#If you want to execute it interactively
docker exec -it testy bash
```

While it is installing we can have a look at the proper code:
![Dockerfile](https://github.com/Gabaldonlab/how2code/blob/main/3-reproducibility/assets/dockerfile.png?raw=true)

For singularity, you can build it using the description file (which is a bit less intuitive than a Dockerfile) or you can take advantage of singularity commands and actually build a .sif image out of a docker hub repository. Ie: 

```bash
#Build from the dockerhub
sudo singularity build myimage.sif docker://cgenomics/myimage.v1.0.0
```


### Note that in order to use images at an HPC enviornment you are forced to use singularity images, you cannot use docker images. However it is a good idea to build a docker image, export it to dockerhub and build a singularity image from that dockerhub repo.

---

## 3. Workflows (Nextflow, Snakemake) - Gold standard in conjunction with any of the previous in specific cases

A workflow language is a great idea for pipelines that are meant to be reused often and to automatize and streamline most of your work. It is intuitive, more reproducible and easier to update/control than bash or python wrappers. 

For this testing we are going to use the followign command to create the conda env to run the snakefile.

```bash
conda create -y -n workflow_test_env -c bioconda -c conda-forge bwa samtools snakemake
conda activate workflow_test_env
#Now we can run the snakemake commandline to execute the pipeline from the workflow/ directory:
snakemake -s main.smk --cores 4 -f all

```

We are not to get into detail on how to write in Snakemake or Nextflow, however we had in the past a couple workshops that might prove valuable for you to check out if you want to. Either that or refer to proper courses and seminars from their original developers (or youtube!!).

Both are an excellent suggestion for your pipelines and one you are proficient at it, it will become an indespensable skill for future projects.

---

## 4. Bioconda-recipes / PyPI - True Gold standard.

In my personal opinion, the true gold standard for a specific package, pipeline or software tool is to have it available through the manually curated and format enforced environments of PyPI(Python Package Index)  or Bioconda. I do not include R-cran or Bioconductor as in my personal experience they lack the levels of curation of the previous two. Both of them are community driven and work well with virtual environments

### PyPI (Python Package Index):Purpose
PyPI is the official package repository for Python. It hosts a vast collection of Python libraries and tools that developers can easily install and use in their Python projects through PIP.

**Advantages**

-   **Extensive Library Collection**: PyPI contains a vast and diverse collection of Python packages, covering a wide range of domains and many different user communities.
-   **Ease of Use**: Pip makes it easy to install Python packages and manage dependencies; or to set up the recipe.

**Disadvantages**

-   **Non-Python Dependencies**: PyPI primarily focuses on Python packages, so installing non-Python dependencies require additional steps and it is a pain.

### Bioconda
Bioconda is a specialized package manager for bioinformatics software. It focuses on providing a centralized repository for bioinformatics tools and libraries.

**Advantages**

-   **Bioinformatics Focus**: Tailored for the bioinformatics community, Bioconda simplifies the installation of bioinformatics tools and their dependencies.
-   **Cross-Language Support**: Conda can manage packages for multiple programming languages, facilitating the integration of bioinformatics tools with different language requirements.


**Disadvantages**

-   **Bioconda recipes learning Curve**: bioconda recipes require additional bugfixing and the documentation is sparse. Might prove a challenge but is worth it.

In summary, PyPI and Bioconda serve different purposes. PyPI is a general-purpose package manager for Python, while Bioconda specializes in bioinformatics tools and integrates with a broader set of programming languages through Conda. The choice between them depends on the specific requirements of your project and the tools you need, but both are excellent choices for a more reproducible and well used code to share with the community.

Take as an example the bioconda-recipe for redundans:

![meta.yml](https://github.com/Gabaldonlab/how2code/blob/main/3-reproducibility/assets/meta.png?raw=true)


![build.sh](https://github.com/Gabaldonlab/how2code/blob/main/3-reproducibility/assets/build.png?raw=true)
