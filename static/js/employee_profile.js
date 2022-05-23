"use strict";

// Modal
const modal = document.querySelector(".custom-modal");
const overlay = document.querySelector(".overlay");
const btnCloseModal = document.querySelector(".close-modal");
const btnOpenModal = document.querySelector(".edit-profile");

const openModal = function () {
  modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
};

const closeModal = function () {
  modal.classList.add("hidden");
  overlay.classList.add("hidden");
};

btnOpenModal.addEventListener("click", openModal);
btnCloseModal.addEventListener("click", closeModal);
overlay.addEventListener("click", closeModal);

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && !modal.classList.contains("hidden")) {
    closeModal();
  }
});

// Update employee
document.getElementById("photoUrl").onchange = function () {
  let src = URL.createObjectURL(this.files[0]);
  document.getElementById("image").src = src;
  document.querySelector(".photo-holder").classList.add("photo-x");
  document.querySelector(".image").classList.remove("none");
};

let img = document.getElementById("image");
let src = img.getAttribute("src");

if (src !== "/static/") {
  document.querySelector(".photo-holder-x").classList.add("photo-x");
}

document
  .querySelector(".photo-holder-x")
  .addEventListener("click", function () {
    document.getElementById("deletePhoto").value = 1;
    document.getElementById("photoUrl").value = "";
    img.classList.add("none");
    document.querySelector(".photo-holder-x").classList.remove("photo-x");
  });
