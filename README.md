# stay-classy-sd-v2
San Diego County history fun facts with weather integration

Steps to deploy to GCP Cloud Run:
docker build -t
gcloud artifacts repositories create stay-classy-sd --repository-format=docker --location=us-west2 --description="Docker repository for SD fun facts app"
gcloud auth configure-docker us-west2-docker.pkg.dev
docker tag stay-classy-sd us-west2-docker.pkg.dev/pytutoring-dev/stay-classy-sd/stay-classy-sd-0
docker push us-west2-docker.pkg.dev/pytutoring-dev/stay-classy-sd/stay-classy-sd-0
gcloud run deploy stay-classy-sd-0 --image us-west2-docker.pkg.dev/pytutoring-dev/stay-classy-sd/stay-classy-sd-0:latest --platform managed --region us-west2


To-Do:
- connect to open-source golf data source
- The text boxes that contain generated outputs should be fixed in size (no more than 50% the height of the vertical screen dimension
- re-deploy to CloudRun and Kubernetes with TF