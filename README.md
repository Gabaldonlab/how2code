How2Code - *"Better documentation and good practices in your codebase"*
========

# Material for the technical seminar of *"Better documentation and good practices in your codebase"*
(Find the corresponding materials in the ordered and enumerated directories, which should roughly follow the timeline of the presentation.)

---

# Necessary tools to install to follow along

## Docker

1. ### Add Docker's official GPG key:

```bash
sudo apt-get update
```

```bash
sudo apt-get install ca-certificates curl
```

```bash
sudo install -m 0755 -d /etc/apt/keyrings
```

```bash
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
```

```bash
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

---

2. ### Add the repository to Apt sources:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

```bash
sudo apt-get update
```

```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

```bash
sudo docker run hello-world
```

---

## Anaconda

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
```

```bash
chmod +x Anaconda3-2023.09-0-Linux-x86_64.sh
```

```bash
./Anaconda3-2023.09-0-Linux-x86_64.sh
```

*Following the instructions of the installer on the command line, you should give "yes" to all the questions.*

---

## Git

```bash
sudo apt-get install -y git
```

---

## VsCode

- 1. Download the ".deb" file from [Download VsCode](https://code.visualstudio.com/)
- 2. Run the downloaded ".deb" file.

---

