"use strict";

// Create employee
function PreviewImage() {
  let oFReader = new FileReader();
  oFReader.readAsDataURL(document.getElementById("photoUrl").files[0]);

  oFReader.onload = function (oFREvent) {
    document.getElementById("uploadPreview").src = oFREvent.target.result;
    document.querySelector(".photo-holder").classList.add("photo-x");
    document.querySelector("#uploadPreview").classList.remove("none");
  };
}

document
  .querySelector(".photo-holder-x")
  .addEventListener("click", function () {
    document.getElementById("photoUrl").value = "";
    document.querySelector("#uploadPreview").classList.add("none");
    document.querySelector(".photo-holder").classList.remove("photo-x");
  });
