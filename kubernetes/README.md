# Running on Kubernetes

Using [minikube](https://minikube.sigs.k8s.io/docs/start/), you can simulate a kubernetes cluster locally by doing
```minikube start```

You can then add workloads and services for the cluster by using [kubectl](https://kubernetes.io/docs/tasks/tools/). 

Run the script at `kubernetes/kubectl-apply.sh`, to start all the containers.
You may have to wait a while for the mongo database to start.

Get the url for the protein structure storage service by using 
```minikube service pss --url```
If you get `SVC_UNREACHABLE` it might be that the containers haven't started yet.
You can check their progress in a web page by running
```minikube dashboard```

To clear the cluster and shut everything down you can use the script 
`kubernetes/kubectl-delete.sh`.
