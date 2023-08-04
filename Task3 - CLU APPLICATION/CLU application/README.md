Step 1: Create a conda environment
```
conda --version
```



Step2: Create  a conda environment
```
conda create -p venv python==3.8 -y
```



Step3:
```
conda activate venv/
```



Step4:
```
pip install -r requirements.txt
```

# Configuration
clu_endpoint = "https://application.cognitiveservices.azure.com/"
clu_key = "d75b520d38924220a568ed0866c7eeec"
project_name = "CLU_application"
deployment_name = "CLU_deployment"