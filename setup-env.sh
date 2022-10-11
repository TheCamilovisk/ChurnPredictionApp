getConfigurationVariables () {
    aws ssm get-parameters-by-path --region sa-east-1 --path "/churn-prediction-api/sa-east-1/"
}

vars_to_env () {
    vars=$1

    for obj in $(echo $vars | jq -c ".Parameters | .[] | {name: .Name, value: .Value}"); do
        name=$(basename $(echo $obj | jq '.name' | tr -d '"'))
        value=$(echo $obj | jq '.value' | tr -d '"')
        export $name=$value
    done
}

variables=$(getConfigurationVariables)
vars_to_env "$variables"

export PIPENV_VERBOSITY=-1

uvicorn churn_api:app --host 0.0.0.0 --port 8000