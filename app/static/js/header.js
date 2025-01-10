document.addEventListener("DOMContentLoaded", () => {
  const menuItems = document.querySelectorAll(".menu-item");
  const logoutButton = document.querySelector("button.logout");

  const currentPath = window.location.pathname;

  menuItems.forEach(item => {
    const link = item.getAttribute("data-link");

    if (currentPath.startsWith(link)) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }

    item.addEventListener("click", () => {
      const link = item.getAttribute("data-link");
      if (link) {
        window.location.href = link;
      }
    });
  });

  logoutButton.addEventListener("click", () => {
    localStorage.removeItem("accessToken");
    window.location.href = "/admin/login";
  });
});