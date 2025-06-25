# kurbeScript.ps1

Write-Host "🔄 Starting Minikube cluster..."
minikube start

Start-Sleep -Seconds 10

Write-Host "`n✅ Kubernetes Cluster Info:"
kubectl cluster-info

Write-Host "`nCurrent Pods in All Namespaces:"
kubectl get pods --all-namespaces
