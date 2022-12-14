const onPageLoad = () => {
  const url = "/api/features";
  fetch(url)
    .then((response) => handleAPICallErrors(response).json())
    .then((data) => {
      const categoricalValues = data["categorical_feature_values"];
      Object.entries(categoricalValues).forEach(([elementId, optionsList]) => {
        addOptions(elementId, optionsList);
      });

      checkFields();
    })
    .catch((error) => {
      showError(
        "An error occurred in connecting to server while trying to call the features endpoint."
      );
    });
  console.log("Paged loaded!");

  const form = document.getElementById("churnForm");
  console.log("AKI");
  form.addEventListener("submit", (event) => {
    console.log("Submitted!");
    cleanRequireds();
    cleanErrors();
    const gender = document.querySelector('input[name="gender"]:checked');
    if (!gender) {
      showRequired();
      showError("Check the required features");
    } else callPredictionApi();

    event.preventDefault();
  });
};

const addOptions = (elementId, optionsList) => {
  const selectElement = document.getElementById(elementId);
  optionsList.forEach((optionString, index) => {
    const option = document.createElement("option");
    option.setAttribute("value", optionString);
    option.innerHTML = optionString;
    selectElement.appendChild(option);
    if (index == 0) {
      selectElement.value = optionString;
      option.selected = true;
      if (selectElement.hasAttribute("dependency")) option.disabled = true;
    }
  });
};

const checkFields = () => {
  checkInternetServices();
  checkPhoneServices();
};

const checkInternetServices = () => {
  const isInternetEnabled = !document
    .getElementById("InternetService")
    .value.startsWith("No");
  handleServiceStateChange("InternetService", isInternetEnabled);
};

const checkPhoneServices = () => {
  const isPhoneEnabled = document.getElementById("PhoneService").checked;
  handleServiceStateChange("PhoneService", isPhoneEnabled);
};

const handleServiceStateChange = (serviceType, isServiceEnabled) => {
  Array.prototype.slice
    .call(document.getElementsByTagName("select"))
    .filter(
      (element) =>
        element.hasAttribute("dependency") &&
        element.getAttribute("dependency") == serviceType
    )
    .forEach((element) => {
      if (!isServiceEnabled) {
        element.value = element.options[0].value;
        element.options[0].selected = true;
        element.disabled = true;
      } else {
        if (element.options[0].selected) {
          element.disabled = false;
          element.value = element.options[1].value;
          element.options[1].selected = true;
        }
      }
    });
};

const getGender = () => {
  document.querySelector('input[name="gender"]:checked').value;
};

const getFeatureValue = (featureName) => {
  const featureTag = document.getElementsByName(featureName)[0];
  let value = null;
  if (featureTag.tagName.toLowerCase() == "input") {
    switch (featureTag.type.toLowerCase()) {
      case "checkbox":
        value = featureTag.value == "on" ? "Yes" : "No";
        break;
      case "text":
        value = parseInt(featureTag.value);
        break;
      default:
        value = featureTag.value;
        break;
    }
  } else value = featureTag.value;
  return value;
};

const getFeatures = () => {
  const gender = document.querySelector('input[name="gender"]:checked');

  const data = {
    gender: gender.value,
    SeniorCitizen: getFeatureValue("SeniorCitizen"),
    Partner: getFeatureValue("Partner"),
    Dependents: getFeatureValue("Dependents"),
    PhoneService: getFeatureValue("PhoneService"),
    MultipleLines: getFeatureValue("MultipleLines"),
    InternetService: getFeatureValue("InternetService"),
    OnlineSecurity: getFeatureValue("OnlineSecurity"),
    OnlineBackup: getFeatureValue("OnlineBackup"),
    DeviceProtection: getFeatureValue("DeviceProtection"),
    TechSupport: getFeatureValue("TechSupport"),
    StreamingTV: getFeatureValue("StreamingTV"),
    StreamingMovies: getFeatureValue("StreamingMovies"),
    Contract: getFeatureValue("Contract"),
    PaperlessBilling: getFeatureValue("PaperlessBilling"),
    PaymentMethod: getFeatureValue("PaymentMethod"),
    tenure: getFeatureValue("tenure"),
    MonthlyCharges: getFeatureValue("MonthlyCharges"),
    TotalCharges: getFeatureValue("TotalCharges"),
  };
  return JSON.stringify([data]);
};

const cleanRequireds = () => {
  const genderRequiredTag = document.getElementById("required");
  genderRequiredTag.innerText = "";
};

const cleanErrors = () => {
  showError("");
};

const showRequired = () => {
  const genderRequiredTag = document.getElementById("required");
  genderRequiredTag.innerText = "Required";
};

const showError = (msg) => {
  const errorsTag = document.getElementById("errors");
  errorsTag.innerText = msg;
};

const handleAPICallErrors = (response) => {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
};

const callPredictionApi = async () => {
  const url = "/api/predict";
  const data = getFeatures();
  const prediction = fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: data,
  })
    .then((response) => handleAPICallErrors(response).json())
    .then((data) => showPrediction(data["predictions"]))
    .catch((error) => {
      showError(
        "An error occurred in connecting to server while trying to call the predict endpoint."
      );
    });
  return prediction;
};

const showPrediction = (predictions) => {
  const predictionTag = document.getElementById("prediction");
  predictionTag.classList.remove("yes");
  predictionTag.classList.remove("no");
  const prediction = predictions[0][null];
  predictionTag.innerText = prediction.toUpperCase();
  predictionTag.classList.add(prediction.toLowerCase());
};

window.onload = onPageLoad;
