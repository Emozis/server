document.addEventListener("DOMContentLoaded", () => {
  const menuItems = document.querySelectorAll(".menu-item");

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
});
