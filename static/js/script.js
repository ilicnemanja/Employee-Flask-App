"use strict";

window.onload = function () {
  // Button logout
  const btnLogout = document.querySelector(".logout");
  const confirmLogout = function (e) {
    let question = confirm("Are you sure you want to logout?");
    if (!question) {
      e.preventDefault();
    }
  };
  btnLogout.addEventListener("click", confirmLogout);

  // Button delete
  const btnDelete = document.querySelectorAll(".btn-delete");
  if (btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        if (!confirm("Are you sure you want to delete employee?")) {
          e.preventDefault();
        }
      });
    });
  }
};
