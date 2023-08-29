# Prometheus & Grafana

## Installation

You can use these instructions to install and configure Prometheus & Grafana using [`kube-prometheus-stack`](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack). The related GitHub repository can be found [here](https://github.com/prometheus-operator/kube-prometheus)

- Add repo:
    ```
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    ```
- Create namespace:
    ```sh
    kubectl create namespace monitor
    ```
- Update helm repo
    ```sh
    helm repo update
    ```
- Install Prometheus & Grafana
    ```sh
    helm install -n monitor monitor -f monitor/values.yaml prometheus-community/kube-prometheus-stack --debug
    ```

## Accessing the UI

The Grafana and Prometheus User Interfaces (UIs) can be exposed by exposing their respective ports

- Expose Grafana on port 3000 using the following command:
    ```sh
    kubectl port-forward deployment/monitor-grafana -n monitor 3000:3000
    ```
    Once exposed, visit Grafana by navigating to: http://localhost:3000

- Expose Prometheus on port 9090 using the following command:
    ```sh
    kubectl port-forward svc/monitor-kube-prometheus-st-prometheus -n monitor 9090:9090
    ```
    After exposing the port, access the Prometheus UI at: http://localhost:9090

## Upgrade

```
helm upgrade --install -n monitor monitor -f monitor/values.yaml prometheus-community/kube-prometheus-stack --debug
```
