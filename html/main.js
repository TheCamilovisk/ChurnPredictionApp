const url = "/api/features/categorical";
fetch(url)
  .then((response) => response.json())
  .then((data) => {
    const categoricalValues = data["categorical_feature_values"];
    Object.entries(categoricalValues).forEach(([elementId, optionsList]) => {
      addOptions(elementId, optionsList);
    });

    checkFields();
  });

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
