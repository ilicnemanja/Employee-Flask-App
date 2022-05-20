const btnLogout = document.querySelector(".logout");
const btnDelete = document.querySelectorAll(".btn-delete");

const confirmLogout = function (e) {
  let question = confirm("Are you sure you want to logout?");
  if (!question) {
    e.preventDefault();
  }
};

btnLogout.addEventListener("click", confirmLogout);

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
