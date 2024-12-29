//헤더 로드
fetch("/static/html/header.html")
  .then((response) => response.text())
  .then((data) => {
    document.getElementById("header-container").innerHTML = data;

    const menuItems = document.querySelectorAll(".menu-item");
    const currentPath = window.location.pathname;
    console.log(currentPath)

    menuItems.forEach(item => {
      let link = item.getAttribute("data-link");
      console.log(link)

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
  })
  .catch((err) => console.error("Error loading header: ", err));

document.querySelectorAll(".category-item").forEach((item) => {
  item.addEventListener("click", () => {
    document
      .querySelectorAll(".category-item")
      .forEach((el) => el.classList.remove("active"));
    item.classList.add("active");

    const link = item.getAttribute("data-link");
    if (link) {
      window.location.href = link;
    }
  });
});


