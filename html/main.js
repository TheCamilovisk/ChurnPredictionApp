const onPageLoad = () => {
  const url = "/api/features";
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const categoricalValues = data["categorical_feature_values"];
      Object.entries(categoricalValues).forEach(([elementId, optionsList]) => {
        addOptions(elementId, optionsList);
      });

      checkFields();
    });
  console.log("Paged loaded!");

  const form = document.getElementById("form");
  form.addEventListener("submit", (event) => {
    console.log("Submitted!");
    cleanErrors();
    const gender = document.querySelector('input[name="gender"]:checked');
    if (!gender) showError();
    else callPredictionApi();

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

const cleanErrors = () => {
  const genderErrorTag = document.getElementById("error");
  genderErrorTag.innerText = "";
};

const showError = () => {
  const genderErrorTag = document.getElementById("error");
  genderErrorTag.innerText = "Required";
};

const callPredictionApi = async () => {
  const url = "/api/predict";
  const data = getFeatures();
  const prediction = fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: data,
  })
    .then((response) => response.json())
    .then((data) => showPrediction(data["predictions"]));
  return prediction;
};

const showPrediction = (predictions) => {
  const predictionTag = document.getElementById("prediction");
  predictionTag.innerText = predictions[0][null];
};

window.onload = onPageLoad;
