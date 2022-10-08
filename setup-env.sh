getConfigurationVariables () {
    aws ssm get-parameters-by-path --path "/churn-prediction-api/sa-east-1/"
}

vars_to_env () {
    vars=$1

    for obj in $(echo $vars | jq -c ".Parameters | .[] | {name: .Name, value: .Value}"); do
        name=$(basename $(echo $obj | jq '.name' | tr -d '"'))
        value=$(echo $obj | jq '.value' | tr -d '"')
        echo "Exporting $name=$value"
        export $name=$value
    done
}

variables=$(getConfigurationVariables)
vars_to_env "$variables"

export PIPENV_VERBOSITY=-1

pipenv run python download_model.py
pipenv run uvicorn churn_api:app --host 0.0.0.0 --port 8000