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

**_Note:_** The Precision FDA Environment has a very short lived session. If you have a slow network connection, you may be logged out before the

## Importing Existing Models

There are a couple options for importing an pre-trained model. Most models come in the form of a `.tar.gz`. The first steps will be to create a workstation using the instruction above. Once this workstation is running, and open (Step 4), proceed as follows:

1. Upload trained models to pFDA using the Files interface. Click on the `Add Files` button and follow the dialog to upload to pFDA.

![Pre-trained model example](https://i.imgur.com/W7rfzaD.png)

2. In the Workstation tab, create a directory called `work/` and `cd` into it by running the following

```
mkdir work
```

![mkdir command](https://i.imgur.com/4Xq9WPc.png)

3. Download the model to the Workstation inside the `work/` directory, and return to the home directory

```
pfda download <name_of_model.tar.gz>
cd ..
```

![pfda download command](https://i.imgur.com/lvbYRRi.png)

4. Continue from Step 5 above to run your notebook
