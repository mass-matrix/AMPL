# Running AMPL on Precision FDA

## Requirements

- Account on pFDA / DNANexus
- Access to Workstations
- Access to `AMPL on pFDA` shared Space

## Running Jupyter Notebook

1. Create .env file with the following configuration:

```shell
export ENV=1.6.1                        # Any published version tag
export IMAGE_REPO=atomsci/atomsci-ampl  # Name of the dockerhub repository
export JUPYTER_PORT=8080                # Port 8080 is open by default on pFDA
export PLATFORM=cpu                     # Can be cpu / gpu
export WORK_DIR=work/                   # Working directory to use
```

2. Upload this to your Files section:

![.env](https://i.imgur.com/Jw8BLVp.png)

3. Launch the `pfda-ttyd` Workstation (located in Featured) with the latest `pfda-ttyd-ampl` snapshot

![Select pfda-ttyd Workstation](https://i.imgur.com/AOKH9dZ.png)
![Load Snapshot](https://i.imgur.com/xoveFH2.png)

4. Wait for the Workstation to start. It takes a few minutes for it to reach the `Running` state. Click on `Open Workstation`.

5. Run the `./start_pfda` command

![Run start_pfda](https://i.imgur.com/bJGEjEx.png)

6. Copy the Jupyter Notebook URL

![Jupyter Notebook](https://i.imgur.com/PuXkrmx.png)

7. Replace `127.0.0.1` with the workstation host and add `:8080` to the end. Enter this into the browser URL.
